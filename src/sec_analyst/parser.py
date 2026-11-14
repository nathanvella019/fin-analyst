"""The notebook's company lookup and rule-based question parser."""

import re

import duckdb
import pandas as pd

from sec_analyst.concepts import CONCEPTS
from sec_analyst.mapper import split_camel


SUFFIX = (
    r"\b(inc|incorporated|corp|corporation|co|company|ltd|limited|llc|"
    r"l l c|lp|l p|plc|n v|s a|the)\b"
)


MONTHS = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
]


STOP = set(
    "what were was is are the of at as on in for to did does how much many "
    "which company companies had have has report reported a an its their "
    "fiscal year quarter ended ending three months sic combined largest "
    "highest biggest can you pull give me book post balance sheet number "
    "sum across filers firms and by".split()
)


def norm_name(name: str) -> str:
    """Apply the notebook's company-name cleaning rules."""
    name = re.sub(r"/[a-z]{2,3}/?$|\\[a-z]{2,3}\\?$", "", name.lower().strip())
    name = re.sub(r"[^a-z0-9 ]", " ", name)
    name = re.sub(SUFFIX, " ", name)
    return re.sub(r"\s+", " ", name).strip()


def qnorm(question):
    """Apply the notebook's question cleaning rules."""
    text = question.lower().replace("'s ", " ").replace("’s ", " ")
    text = re.sub(r"[^a-z0-9\- ]", " ", text)
    return " " + re.sub(r"\s+", " ", text) + " "


def parse_period(ql):
    if (m := re.search('\\b(20\\d\\d)-(\\d\\d)-(\\d\\d)\\b', ql)):
        return ('date', pd.Timestamp(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    if (m := re.search('\\b(\\d{1,2}) (' + '|'.join(MONTHS) + ') (20\\d\\d)\\b', ql)):
        return ('date', pd.Timestamp(int(m.group(3)), MONTHS.index(m.group(2)) + 1, int(m.group(1))))
    if (m := re.search('\\b(?:fiscal(?: year)?|fy) ?(20\\d\\d)\\b', ql)):
        return ('fy', int(m.group(1)))
    return (None, None)


class QuestionParser:
    """Interpret questions using the notebook's existing rules."""

    def __init__(self, connection: duckdb.DuckDBPyConnection):
        reports = connection.execute("SELECT * FROM sub").df()
        self.names = reports.drop_duplicates("cik")[["cik", "name"]].assign(
            key=lambda data: data.name.map(norm_name)
        )
        key_ciks = self.names.groupby("key").cik.apply(
            lambda values: sorted(set(values))
        )
        self.gaz = {
            key: values for key, values in key_ciks.items() if len(key) >= 4
        }
        self.key_of = dict(zip(self.names.cik, self.names.key))
        self.unique = {
            cik for cik, key in self.key_of.items()
            if len(self.gaz.get(key, [])) == 1
        }
        self.normalised_name_count = len(key_ciks)
        self.shared_name_count = int((key_ciks.map(len) > 1).sum())

        top_tags = connection.execute("""
            SELECT tag, count(*) AS n
            FROM num
            WHERE NOT custom
            GROUP BY tag
            ORDER BY n DESC
            LIMIT 500
        """).df()
        self.schema_tags = [
            (tag, set(split_camel(tag).split())) for tag in top_tags.tag
        ]
        self.phrase_to_concept = sorted(
            (
                (phrase, concept)
                for concept, (phrases, _, _) in CONCEPTS.items()
                for phrase in phrases
            ),
            key=lambda item: -len(item[0]),
        )

    def raw_schema_tag(self, words):
        """Raw schema only: pick the schema tag whose CamelCase words best overlap the question's content words."""
        stem = lambda w: w[:-1] if w.endswith('s') and len(w) > 3 else w
        ws = {stem(w) for w in words}
        best = max(self.schema_tags, key=lambda t: (len(ws & {stem(x) for x in t[1]}), -len(t[1])))
        return [best[0]] if ws & {stem(x) for x in best[1]} else []

    def parse(self, q: str, kb_context=True) -> dict:
        ql = qnorm(q)
        out = {'status': 'ok'}
        if (m := re.search('\\bsic (\\d{4})\\b', ql)):
            out['sic'] = int(m.group(1))
        ptype, pval = parse_period(ql)
        if ptype:
            out[ptype] = pval
        hits = [k for k in self.gaz if f' {k} ' in ql]
        if hits:
            k = max(hits, key=len)
            out['ciks'] = self.gaz[k]
            ql_rest = ql.replace(f' {k} ', ' ')
        else:
            ql_rest = ql
        if kb_context:
            c = next((c for p, c in self.phrase_to_concept if f' {p} ' in ql_rest), None)
            if 'loss' in ql_rest and 'sic' in out:
                c = 'NetIncome'
            out['concept'], out['tags'] = (c, CONCEPTS[c][1] if c else [])
        else:
            words = [w for w in re.sub('\\d', ' ', ql_rest).split() if w not in STOP and len(w) > 2]
            out['concept'], out['tags'] = ('raw', self.raw_schema_tag(words))
        if 'how many' in ql or 'number of' in ql:
            out['intent'] = 'count'
        elif any((w in ql for w in (' combined ', ' sum of ', ' total across '))):
            out['intent'] = 'sum'
        elif any((w in ql for w in (' which ', ' biggest ', ' largest '))) and 'sic' in out:
            out['intent'] = 'rank'
        elif any((w in ql for w in (' quarter ', ' three months '))) and 'date' in out:
            out['intent'] = 'quarter'
        elif 'fy' in out:
            out['intent'] = 'fiscal'
        elif 'date' in out:
            out['intent'] = 'point'
        else:
            return {'status': 'not understood'}
        if out['intent'] in ('point', 'fiscal', 'quarter'):
            if 'ciks' not in out:
                return {'status': 'unknown company'}
            if len(out['ciks']) > 1:
                return {'status': 'ambiguous company', 'candidates': out['ciks']}
        elif 'sic' not in out:
            return {'status': 'not understood'}
        if not out['tags']:
            return {'status': 'unknown concept'}
        return out
