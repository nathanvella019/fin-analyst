"""Small adversarial data: each omitted filter admits a wrong financial fact."""
import datetime
import unittest
import duckdb
from sec_analyst.service import QuestionService


class SQLTrapTests(unittest.TestCase):
    def setUp(self):
        self.con = duckdb.connect()
        self.con.execute("CREATE TABLE sub(adsh VARCHAR, cik BIGINT, period DATE, form VARCHAR, filed DATE, fy INTEGER, fp VARCHAR)")
        self.con.execute("CREATE TABLE num(adsh VARCHAR, tag VARCHAR, ddate DATE, qtrs INTEGER, coreg VARCHAR, uom VARCHAR, value DOUBLE)")
        self.con.execute("INSERT INTO sub VALUES ('good',1,'2016-06-30','10-Q','2016-08-01',2016,'Q2')")
        self.con.execute("INSERT INTO num VALUES ('good','Revenues','2016-06-30',1,NULL,'USD',100)")
        self.service = object.__new__(QuestionService)
        self.service.connection = self.con
        self.parsed = dict(intent='quarter',concept='Revenue', tags=['Revenues'],ciks=[1],date=datetime.date(2016,6,30))

    def tearDown(self):
        self.con.close()

    def test_filters_reject_wrong_contexts(self):
        cases = [
            (" AND n.qtrs = 1", "good", 2, None, 'USD'),
            (" AND n.coreg IS NULL", "good", 1, 'subsidiary', 'USD'),
            (" AND n.uom = 'USD'", "good", 1, None, 'JPY'),
        ]
        for clause, adsh, qtrs, coreg, uom in cases:
            with self.subTest(clause=clause):
                self.con.execute("DELETE FROM num WHERE value=999")
                self.con.execute("INSERT INTO num VALUES (?, 'Revenues','2016-06-30',?,?,?,999)",[adsh,qtrs,coreg,uom])
                sql=self.service.build_sql(self.parsed,3).replace(' LIMIT 1','')
                self.assertEqual([r[0] for r in self.con.execute(sql).fetchall()],[100])
                self.assertIn(999,[r[0] for r in self.con.execute(sql.replace(clause,'')).fetchall()])

    def test_original_period_end_excludes_later_comparative(self):
        self.con.execute("INSERT INTO sub VALUES ('later',1,'2016-09-30','10-Q','2016-11-01',2016,'Q3')")
        self.con.execute("INSERT INTO num VALUES ('later','Revenues','2016-06-30',1,NULL,'USD',999)")
        sql=self.service.build_sql(self.parsed,3).replace(' LIMIT 1','')
        self.assertEqual([r[0] for r in self.con.execute(sql).fetchall()],[100])
        self.assertEqual(len(self.con.execute(sql.replace(' AND n.ddate = s.period','')).fetchall()),2)

    def test_amendment_is_not_original_annual_report(self):
        self.con.execute("DELETE FROM sub")
        self.con.execute("DELETE FROM num")
        self.con.execute("INSERT INTO sub VALUES ('good',1,'2016-03-31','10-K','2016-05-01',2015,'FY'),('amended',1,'2016-03-31','10-K/A','2016-06-01',2015,'FY')")
        self.con.execute("INSERT INTO num VALUES ('good','Revenues','2016-03-31',4,NULL,'USD',100),('amended','Revenues','2016-03-31',4,NULL,'USD',999)")
        parsed=dict(intent='fiscal',concept='Revenue',tags=['Revenues'],ciks=[1],fy=2015)
        self.assertEqual(self.con.execute(self.service.build_sql(parsed,3)).fetchone()[0],100)
        # R2 uses the calendar year: it misses this fiscal-2015 report entirely.
        self.assertIsNone(self.con.execute(self.service.build_sql(parsed,2)).fetchone())
