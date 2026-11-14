import unittest
from fastapi.testclient import TestClient
from sec_analyst.api import create_app


class FakeRuntime:
    def __init__(self):
        self.closed=False
    def ask(self,question):
        return {'candidate':{'status':'answered','value':100},'decision':'refer','version':'test'}
    def close(self):
        self.closed=True


class APITests(unittest.TestCase):
    def test_request_validation_and_lifecycle(self):
        runtime=FakeRuntime()
        with TestClient(create_app(lambda:runtime)) as client:
            self.assertEqual(client.get('/health').status_code,200)
            for body in [{},{'question':' '},{'question':42},{'question':'x'*2001},{'question':'x','sql':'DROP TABLE num'}]:
                with self.subTest(body=str(body)[:60]):
                    self.assertEqual(client.post('/ask',json=body).status_code,422)
            response=client.post('/ask',json={'question':'Example question'})
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.json()['decision'],'refer')
        self.assertTrue(runtime.closed)
