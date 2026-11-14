"""Build the notebook's reference questions and independently computed answers."""

import hashlib
from pathlib import Path

import duckdb
import pandas as pd

from sec_analyst.concepts import CONCEPTS
from sec_analyst.parser import MONTHS, QuestionParser



PHRASE = {'Revenue': ['revenue', 'net sales', 'sales', 'turnover'], 'NetIncome': ['net income', 'net profit', 'earnings'], 'OperatingCashFlow': ['operating cash flow', 'cash from operations'], 'Assets': ['total assets'], 'Liabilities': ['total liabilities'], 'Equity': ["shareholders' equity", "stockholders' equity", 'book value'], 'Cash': ['cash and cash equivalents', 'cash']}


DEV = {'point': ["What were {co}'s {c} at {d}?", '{co} {c} as of {d}?'], 'fiscal': ["What was {co}'s {c} in fiscal {fy}?", '{co} {c} for fiscal year {fy}?'], 'quarter': ["What was {co}'s {c} for the quarter ended {d}?", '{co} {c} in the three months to {d}?'], 'count': ['How many SIC {sic} companies reported a net loss for fiscal {fy}?'], 'sum': ['What were the combined total assets of SIC {sic} companies at {d}?'], 'rank': ['Which SIC {sic} company had the largest total assets at {d}?']}


HELD_OUT = {'point': ["Can you pull {co}'s {c} on the {d} balance sheet?", "As at {d}, how much were {co}'s {c}?"], 'fiscal': ['Give me {c} for {co}, FY{fy}.', 'How much {c} did {co} book in its {fy} fiscal year?'], 'quarter': ['{co}: {c}, quarter ending {d}?', 'What {c} did {co} post in the quarter to {d}?'], 'count': ['Number of loss-making SIC {sic} firms in fiscal {fy}?'], 'sum': ['Sum of total assets across SIC {sic} filers as of {d}?'], 'rank': ['Biggest SIC {sic} company by total assets at {d}?']}


fmt_date = lambda d, style: f'{d.day} {MONTHS[d.month - 1].title()} {d.year}' if style == 0 else f'{d:%Y-%m-%d}'


def as_filed(tags, number_files, reports):
    """Independent path: read the sorted Parquet with a pyarrow filter, keep original 10-K/10-Q filings and the filing's own period."""
    df = pd.concat([pd.read_parquet(f, columns=['adsh', 'tag', 'coreg', 'ddate', 'qtrs', 'uom', 'value'], filters=[('tag', 'in', tags)]) for f in number_files])
    df = df[df.coreg.isna() & (df.uom == 'USD') & df.value.notna()].merge(reports[['adsh', 'cik', 'name', 'sic', 'form', 'fy', 'fp', 'period', 'filed', 'fye']], on='adsh')
    df = df[df.form.isin(['10-K', '10-Q']) & (df.ddate == df.period)]
    return df.sort_values('filed').drop_duplicates(['cik', 'tag', 'form', 'period', 'qtrs'])


def golden_fingerprint(gold: pd.DataFrame) -> str:
    """Fingerprint the same five reference columns as the notebook."""
    columns = ["family", "concept", "question", "held_out", "answer"]
    return hashlib.sha256(gold[columns].to_csv(index=False).encode()).hexdigest()


def build_golden_set(
    connection: duckdb.DuckDBPyConnection,
    processed_dir: Path,
    quarters: list[str],
    seed: int,
    n_per_cell: int,
) -> tuple[pd.DataFrame, str]:
    """Preserve the notebook's sampling, expected answers and question wording."""
    reports = connection.execute("SELECT * FROM sub").df()
    parser = QuestionParser(connection)
    number_files = [
        str(processed_dir / f"08_num_{quarter}.parquet")
        for quarter in quarters
    ]

    def unique_key(cik):
        return cik in parser.unique

    def display_name(cik):
        return parser.key_of[cik].title()

    REV_LABEL = '^(total )?(net )?(operating )?(revenues?|sales)( net)?$|^(total )?(net )?(revenues?|sales),? net$|^total (net )?(operating )?(revenues?|sales)$|^net sales and (operating )?revenues?$|^sales and (other )?revenues?$'

    connection.execute("CREATE OR REPLACE MACRO norm_label(s) AS trim(regexp_replace(regexp_replace(lower(coalesce(s, '')), '[^a-z, ]', ' ', 'g'), '\\s+', ' ', 'g'))")

    connection.execute(f"CREATE OR REPLACE TEMP TABLE rev_lines AS\n   SELECT s.adsh, s.cik, s.form, s.fy, s.fp, s.period, s.fsq, p.tag, p.custom, p.plabel, n.qtrs, n.value\n   FROM pre p JOIN sub s USING (adsh)\n   JOIN num n ON n.adsh = p.adsh AND n.tag = p.tag AND n.version = p.version AND n.ddate = s.period AND n.coreg IS NULL AND n.uom = 'USD'\n   WHERE p.stmt = 'IS' AND p.inpth = 0 AND s.form IN ('10-K', '10-Q') AND regexp_matches(norm_label(p.plabel), '{REV_LABEL}')\n     AND ((s.form = '10-K' AND n.qtrs = 4) OR (s.form = '10-Q' AND n.qtrs = 1))")

    rev_one = connection.execute('SELECT * FROM rev_lines WHERE adsh IN (SELECT adsh FROM rev_lines GROUP BY adsh HAVING count(DISTINCT value) = 1)\n                         QUALIFY row_number() OVER (PARTITION BY adsh ORDER BY tag) = 1').df()

    gold_rows = []

    pick = lambda df, n: df.sample(min(n, len(df)), random_state=seed)

    def add(family, concept, row, answer, **slots):
        gold_rows.append({'family': family, 'concept': concept, 'answer': answer, **slots, 'cik': row.get('cik'), 'fye': row.get('fye')})

    facts_bs = as_filed(['Assets', 'Liabilities', 'StockholdersEquity', 'CashAndCashEquivalentsAtCarryingValue'], number_files, reports)

    for concept, tag in [('Assets', 'Assets'), ('Liabilities', 'Liabilities'), ('Equity', 'StockholdersEquity'), ('Cash', 'CashAndCashEquivalentsAtCarryingValue')]:
        f = facts_bs[(facts_bs.tag == tag) & (facts_bs.qtrs == 0)]
        f = f[f.cik.map(unique_key)].drop_duplicates(['cik', 'period'])
        for r in pick(f, n_per_cell).to_dict('records'):
            add('point', concept, r, r['value'], d=r['period'], answer_tag=tag)

    facts_fl = as_filed(['NetIncomeLoss', 'NetCashProvidedByUsedInOperatingActivities'], number_files, reports)

    rev = rev_one[~rev_one.custom].merge(reports[['adsh', 'name', 'sic', 'filed', 'fye']], on='adsh')

    for concept, f in [('Revenue', rev.rename(columns={})), ('NetIncome', facts_fl[facts_fl.tag == 'NetIncomeLoss']), ('OperatingCashFlow', facts_fl[facts_fl.tag == 'NetCashProvidedByUsedInOperatingActivities'])]:
        f = f[f.cik.map(unique_key)]
        k = f[(f.form == '10-K') & (f.fp == 'FY') & (f.qtrs == 4)].drop_duplicates(['cik', 'fy'])
        k = k[k.fy.isin([2015, 2016])]
        k = pd.concat([pick(k[k.fye == '1231'], n_per_cell // 2), pick(k[k.fye != '1231'], n_per_cell - n_per_cell // 2)])
        for r in k.to_dict('records'):
            add('fiscal', concept, r, r['value'], fy=r['fy'], answer_tag=r['tag'])
        if concept in ('Revenue', 'NetIncome'):
            qq = f[(f.form == '10-Q') & (f.qtrs == 1)].drop_duplicates(['cik', 'period'])
            for r in pick(qq, n_per_cell).to_dict('records'):
                add('quarter', concept, r, r['value'], d=r['period'], answer_tag=r['tag'])

    rev_custom = rev_one[rev_one.custom].merge(reports[['adsh', 'name', 'sic', 'filed', 'fye']], on='adsh')

    rev_custom = rev_custom[rev_custom.cik.map(unique_key)].drop_duplicates('cik')

    for r in rev_custom.to_dict('records'):
        if r['form'] == '10-K':
            add('fiscal', 'Revenue (custom tag)', r, r['value'], fy=r['fy'], answer_tag=r['tag'])
        else:
            add('quarter', 'Revenue (custom tag)', r, r['value'], d=r['period'], answer_tag=r['tag'])

    ni_tags = CONCEPTS['NetIncome'][1]

    loss = as_filed(ni_tags, number_files, reports).query("form == '10-K' and fp == 'FY' and qtrs == 4")

    loss = loss.assign(rank=loss.tag.map(ni_tags.index)).sort_values(['rank', 'filed']).drop_duplicates(['cik', 'fy'])

    sics = loss[loss.fy == 2015].groupby('sic').cik.nunique()

    for sic in pick(sics[sics >= 15].reset_index(), n_per_cell).sic:
        g = loss[(loss.sic == sic) & (loss.fy == 2015)]
        add('count', 'NetIncome', {}, int((g.value < 0).sum()), sic=int(sic), fy=2015)

    assets = facts_bs[(facts_bs.tag == 'Assets') & (facts_bs.qtrs == 0)].drop_duplicates(['cik', 'period'])

    cells = assets.groupby(['sic', 'period']).cik.nunique()

    cells = cells[cells >= 8].reset_index()

    for r in pick(cells, n_per_cell).to_dict('records'):
        g = assets[(assets.sic == r['sic']) & (assets.period == r['period'])]
        add('sum', 'Assets', {}, float(g.value.sum()), sic=int(r['sic']), d=r['period'])

    for r in pick(cells.sample(frac=1, random_state=1), n_per_cell).to_dict('records'):
        g = assets[(assets.sic == r['sic']) & (assets.period == r['period'])]
        add('rank', 'Assets', {}, int(g.sort_values(['value', 'cik'], ascending=[False, True]).cik.iloc[0]), sic=int(r['sic']), d=r['period'])

    gold = pd.DataFrame(gold_rows)

    def phrase(row, templates, i):
        c = PHRASE[row.concept.split(' (')[0]][i % len(PHRASE[row.concept.split(' (')[0]])] if row.family in ('point', 'fiscal', 'quarter') else ''
        co = display_name(row.cik) if row.family in ('point', 'fiscal', 'quarter') else ''
        t = templates[row.family][i % len(templates[row.family])]
        d, fy, sic = (getattr(row, 'd', None), getattr(row, 'fy', None), getattr(row, 'sic', None))
        return t.format(co=co, c=c, d=fmt_date(pd.Timestamp(d), i % 2) if pd.notna(d) else '', fy=int(fy) if pd.notna(fy) else '', sic=int(sic) if pd.notna(sic) else '')

    gold['question'] = [phrase(r, DEV, i) for i, r in enumerate(gold.itertuples())]

    gold['held_out'] = [phrase(r, HELD_OUT, i) for i, r in enumerate(gold.itertuples())]

    return gold, golden_fingerprint(gold)
