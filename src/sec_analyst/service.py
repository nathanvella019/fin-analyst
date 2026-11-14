"""The notebook's SQL templates, answer execution and verification."""

from functools import lru_cache

import duckdb

from sec_analyst.parser import QuestionParser



RUNGS = ['R0 raw schema', 'R1 + taxonomy concepts', 'R2 + as-filed rule', 'R3 + fiscal-year convention', 'R4 + custom-tag mapper']


def correct(a, g):
    if a is None:
        return False
    return abs(float(a) - float(g)) <= max(0.5, 1e-06 * abs(float(g)))


class QuestionService:
    """Answer questions through one warehouse connection."""

    def __init__(self, connection: duckdb.DuckDBPyConnection):
        self.connection = connection
        self.parser = QuestionParser(connection)

    def build_sql(self, p, rung, original_only=False):
        kb, asfiled, fiscal, mapper = (rung >= 1, rung >= 2, rung >= 3, rung >= 4)
        original = asfiled or original_only
        tags = p['tags']
        tag_in = ', '.join((f"'{t}'" for t in tags))
        prio = 'CASE n.tag ' + ' '.join((f"WHEN '{t}' THEN {i}" for i, t in enumerate(tags))) + ' ELSE 99 END'
        tag_filter = f'n.tag IN ({tag_in})'
        if mapper and p['intent'] in ('point', 'fiscal', 'quarter'):
            mapped = self.connection.execute(f"SELECT DISTINCT m.adsh, m.ctag FROM custom_map m JOIN sub s USING (adsh)\n                                 WHERE s.cik = {p['ciks'][0]} AND m.stag IN ({tag_in})").fetchall()
            if mapped:
                names_in = ', '.join(sorted({f"'{t}'" for _, t in mapped}))
                pairs_in = ', '.join((f"('{a}', '{t}')" for a, t in mapped))
                tag_filter = f'n.tag IN ({tag_in}, {names_in}) AND (n.tag IN ({tag_in}) OR (n.custom AND (n.adsh, n.tag) IN ({pairs_in})))'
                prio = prio.replace('ELSE 99', 'ELSE 50')
        filt = (" AND s.form IN ('10-K', '10-Q') AND n.ddate = s.period" if original else '') + (" AND n.coreg IS NULL AND n.uom = 'USD' AND n.value IS NOT NULL" if asfiled else '')
        q_inst = ' AND n.qtrs = 0' if asfiled else ''
        if p['intent'] == 'fiscal':
            period = (f"s.fy = {p['fy']} AND s.fp = 'FY' AND s.form = '10-K'" if fiscal else f"year(n.ddate) = {p['fy']}") + ' AND n.qtrs = 4'
        elif p['intent'] == 'quarter':
            period = f"n.ddate = DATE '{p['date']:%Y-%m-%d}'" + (" AND n.qtrs = 1 AND s.form = '10-Q'" if asfiled else '')
        elif p['intent'] in ('point', 'sum', 'rank'):
            period = f"n.ddate = DATE '{p['date']:%Y-%m-%d}'" + q_inst
        else:
            period = (f"s.fy = {p['fy']} AND s.fp = 'FY' AND s.form = '10-K'" if fiscal else f"year(n.ddate) = {p['fy']}") + ' AND n.qtrs = 4'
        base = f'FROM num n JOIN sub s USING (adsh) WHERE {tag_filter} AND {period}{filt}'
        order = f'ORDER BY {prio}, s.filed, n.adsh' if kb else 'ORDER BY n.adsh'
        if p['intent'] in ('point', 'fiscal', 'quarter'):
            return f"SELECT n.value, n.adsh, n.tag, n.ddate, n.qtrs, s.form, s.filed {base} AND s.cik = {p['ciks'][0]} {order} LIMIT 1"
        if not original:
            if p['intent'] == 'rank':
                return f"SELECT s.cik {base} AND s.sic = {p['sic']} AND n.value IS NOT NULL ORDER BY n.value DESC, s.cik LIMIT 1"
            agg = {'count': 'count(*) FILTER (WHERE n.value < 0)', 'sum': 'sum(n.value)'}[p['intent']]
            return f"SELECT {agg} {base} AND s.sic = {p['sic']}"
        one = f"SELECT s.cik, arg_min(n.value, {prio} * 1e10 + epoch(s.filed)) AS value {base} AND s.sic = {p['sic']} GROUP BY s.cik"
        if p['intent'] == 'rank':
            return f'SELECT cik FROM ({one}) ORDER BY value DESC, cik LIMIT 1'
        agg = {'count': 'count(*) FILTER (WHERE value < 0)', 'sum': 'sum(value)'}[p['intent']]
        return f'SELECT {agg} FROM ({one})'

    @lru_cache(maxsize=None)
    def run_sql(self, sql):
        return self.connection.execute(sql).fetchall()

    def answer(self, q, rung, original_only=False):
        p = self.parser.parse(q, kb_context=rung >= 1)
        if p['status'] != 'ok':
            return {'status': p['status'], 'value': None, 'sql': None}
        sql = self.build_sql(p, rung, original_only)
        rows = self.run_sql(sql)
        row = rows[0] if rows else None
        if row is None or row[0] is None:
            return {'status': 'no rows', 'value': None, 'sql': sql}
        return {'status': 'answered', 'value': row[0], 'sql': sql, 'provenance': row[1:] if len(row) > 1 else None}

    def verify(self, sql: str, claimed: float) -> dict:
        """Re-run the query, recompute the number from the returned rows, and only then show it (S1 keeps this for LLM-written SQL)."""
        rows = self.connection.execute(sql).fetchall()
        recomputed = rows[0][0] if rows else None
        return {'rows': len(rows), 'recomputed': recomputed, 'shown': recomputed if recomputed is not None and correct(claimed, recomputed) else None}
