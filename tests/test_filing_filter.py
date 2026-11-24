import unittest

import duckdb

from sec_analyst.policy import passes_filing_filter


class FilingFilterTests(unittest.TestCase):
    def setUp(self):
        self.con = duckdb.connect()
        self.addCleanup(self.con.close)
        self.con.execute("""
            CREATE TABLE pre AS SELECT * FROM (VALUES
                ('F', 'TotalTag', 'v', 'IS', 0, 'Net sales'),
                ('F', 'GoodsTag', 'v', 'IS', 0, 'Product sales')
            ) p(adsh, tag, version, stmt, inpth, plabel)
        """)
        self.con.execute("""
            CREATE TABLE num AS SELECT * FROM (VALUES
                ('F', 'TotalTag', 'v', DATE '2020-12-31', 4, NULL::VARCHAR, 'USD', 120),
                ('F', 'GoodsTag', 'v', DATE '2020-12-31', 4, NULL, 'USD', 80)
            ) n(adsh, tag, version, ddate, qtrs, coreg, uom, value)
        """)

    def passes(self, tag, value, **overrides):
        flags = {"answered": True, "via_mapper": False, "single_candidate": True, **overrides}
        candidate = {"provenance": ["F", tag, "2020-12-31", 4], "value": value}
        return passes_filing_filter(self.con, {"concept": "Revenue"}, candidate, flags)

    def test_total_supported_but_component_and_wrong_value_referred(self):
        self.assertTrue(self.passes("TotalTag", 120))
        self.assertFalse(self.passes("GoodsTag", 80))
        self.assertFalse(self.passes("TotalTag", 80))
        self.assertFalse(self.passes("TotalTag", 120, via_mapper=True))

    def test_ambiguous_or_missing_statement_evidence_referred(self):
        self.con.execute("UPDATE pre SET plabel = 'Revenue' WHERE tag = 'GoodsTag'")
        self.assertFalse(self.passes("TotalTag", 120))
        self.con.execute("UPDATE pre SET stmt = 'BS'")
        self.assertFalse(self.passes("TotalTag", 120))
