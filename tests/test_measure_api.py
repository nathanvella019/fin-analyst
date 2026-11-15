"""Check that the client experiment distinguishes HTTP success from accuracy."""
import io
import json
import time
import unittest
from unittest.mock import patch
from urllib.error import URLError

import pandas as pd
from scripts.measure_api import send


class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.row = pd.Series({'family': 'point', 'answer': 100, 'question': 'Example'}, name=7)

    def test_wrong_candidate_is_not_a_network_failure(self):
        response = io.BytesIO(json.dumps({
            'candidate': {'value': 999, 'status': 'answered'}, 'decision': 'refer',
        }).encode())
        response.status = 200
        response.headers = {"X-Request-ID":"test-request"}
        with patch('urllib.request.urlopen', return_value=response):
            record = send('http://localhost', self.row, 'question', 0, time.perf_counter())
        self.assertEqual(record['http_status'], 200)
        self.assertFalse(record['correct'])
        self.assertIsNone(record['error'])
        self.assertEqual(record['decision'], 'refer')

    def test_failed_connection_is_saved_as_a_client_error(self):
        with patch('urllib.request.urlopen', side_effect=URLError('connection refused')):
            record = send('http://localhost', self.row, 'question', 0, time.perf_counter())
        self.assertIsNone(record['http_status'])
        self.assertIn('connection refused', record['error'])
        self.assertFalse(record['correct'])
