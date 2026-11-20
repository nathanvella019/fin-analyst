import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from fastapi.testclient import TestClient
from sec_analyst.api import create_app


class FakeRuntime:
    identity={"package_version":"test", "code_revision":"test-commit", "source_sha256":"test-source"}
    def __init__(self):
        self.closed=False
    def ask(self,question):
        return {'candidate':{'status':'answered','value':100,'provenance':['filing-1','Assets','2016-12-31',0,'10-K','2017-02-01']},'decision':'refer','version':'test'}
    def close(self):
        self.closed=True


class APITests(unittest.TestCase):
    def test_request_validation_and_lifecycle(self):
        runtime=FakeRuntime()
        with TemporaryDirectory() as folder, TestClient(create_app(lambda:runtime, folder)) as client:
            self.assertEqual(client.get('/health').status_code,200)
            for body in [{},{'question':' '},{'question':42},{'question':'x'*2001},{'question':'x','sql':'DROP TABLE num'}]:
                with self.subTest(body=str(body)[:60]):
                    self.assertEqual(client.post('/ask',json=body).status_code,422)
            response=client.post('/ask',json={'question':'Example question'})
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.json()['decision'],'refer')
            metrics=client.get('/metrics').json()
            self.assertEqual(metrics['requests'],6)
            self.assertEqual(metrics['http_status_counts'],{'422':5,'200':1})
            self.assertEqual(metrics['referrals'],1)
            self.assertEqual(metrics['question_length_samples'],1)
            exposition = client.get('/metrics/prometheus')
            self.assertEqual(exposition.status_code, 200)
            self.assertIn('version=0.0.4', exposition.headers['content-type'])
            self.assertIn('fin_analyst_requests_total 6\n', exposition.text)
            self.assertIn('fin_analyst_question_mean_chars 16.0\n', exposition.text)
            self.assertIn('Financial Analyst monitoring',client.get('/monitor').text)
            records=[json.loads(line) for line in (Path(folder)/'requests.jsonl').read_text().splitlines()]
            self.assertEqual(len(records),6)
            self.assertEqual(records[-1]['request_id'],response.headers['X-Request-ID'])
            self.assertEqual(records[-1]['candidate_value'],100)
            self.assertEqual(records[-1]['candidate_provenance'][0],'filing-1')
            self.assertEqual(records[-1]['model_identity']['code_revision'],'test-commit')
            self.assertIsNone(records[-1]['released_answer'])
            self.assertNotIn('Example question',json.dumps(records))
        self.assertTrue(runtime.closed)

    def test_server_failure_is_recorded(self):
        class FailingRuntime(FakeRuntime):
            def ask(self, question):
                raise RuntimeError("Simulated database failure")
        with TemporaryDirectory() as folder:
            with TestClient(create_app(FailingRuntime, folder), raise_server_exceptions=False) as client:
                self.assertEqual(client.post('/ask',json={'question':'Example'}).status_code,500)
                self.assertEqual(client.get('/metrics').json()['server_errors'],1)

    def test_metadata_survives_restart_but_counters_reset(self):
        with TemporaryDirectory() as folder:
            for run in range(2):
                with TestClient(create_app(FakeRuntime, folder)) as client:
                    self.assertEqual(client.get('/metrics').json()['requests'],0)
                    client.post('/ask',json={'question':'Example'})
            self.assertEqual(len((Path(folder)/'requests.jsonl').read_text().splitlines()),2)
