import unittest

import pandas as pd

from sec_analyst.rd2_monitoring import decisions, mix_distance


class QuarterlyMonitoringTests(unittest.TestCase):
    def test_category_shift_and_reference(self):
        counts = pd.DataFrame([[100, 0], [200, 0], [90, 10]], index=["ref", "same", "new"])
        result = mix_distance(counts, "ref")
        self.assertEqual(result["ref"], 0)
        self.assertEqual(result["same"], 0)
        self.assertEqual(result["new"], 0.10)
        with self.assertRaises(ValueError):
            mix_distance(counts * 0, "ref")

    def test_alerts_and_retraining_use_separate_rules(self):
        rows = pd.DataFrame({"top5": [0.4, 0.49, None, 0.49, 0.49, 0.5],
                             "mix_distance": [0, 0.10, 0, 0, 0, 0.11]},
                            index=["q1", "q2", "q3", "q4", "q5", "q6"])
        flags = decisions(rows, "q1", 0.10, 0.5, 2)
        self.assertEqual(flags.index[flags.mix_alert].tolist(), ["q2", "q6"])
        self.assertEqual(flags.index[flags.accuracy_alert].tolist(), ["q2", "q4", "q5"])
        self.assertEqual(flags.index[flags.labels_missing].tolist(), ["q3"])
        self.assertEqual(flags.index[flags.train_candidate].tolist(), ["q5"])
