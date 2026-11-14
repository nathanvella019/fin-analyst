"""Accounting identity checks from the given notebook."""

import numpy as np


IDENTITIES = {
    "Assets = LiabilitiesAndStockholdersEquity":            ("Assets", ["LiabilitiesAndStockholdersEquity"], [], 0),
    "SalesRevenueNet = Goods + Services":                   ("SalesRevenueNet", ["SalesRevenueGoodsNet", "SalesRevenueServicesNet"], [], None),
    "GrossProfit = Revenues − CostOfRevenue":               ("GrossProfit", ["Revenues"], ["CostOfRevenue"], None),
    "ProfitLoss = NetIncomeLoss + NCI share":               ("ProfitLoss", ["NetIncomeLoss", "NetIncomeLossAttributableToNoncontrollingInterest"], [], None),
    "L&SE = Liabilities + StockholdersEquity (ignores NCI, temporary equity)": ("LiabilitiesAndStockholdersEquity", ["Liabilities", "StockholdersEquity"], [], 0),
}
def identity_check(connection, total, plus, minus, qtrs):
    tags = [total] + plus + minus
    w = connection.execute(f"""
        SELECT n.adsh, n.ddate, n.qtrs, {', '.join(f"max(CASE WHEN n.tag = '{t}' THEN n.value END) AS \"{t}\"" for t in tags)}
        FROM num n JOIN sub s USING (adsh)
        WHERE n.tag IN ({', '.join(f"'{t}'" for t in tags)}) AND n.coreg IS NULL AND n.uom = 'USD' AND s.form IN ('10-K', '10-Q')
          AND n.ddate = s.period {'' if qtrs is None else f'AND n.qtrs = {qtrs}'}
        GROUP BY ALL""").df().dropna()
    rhs = w[plus].sum(axis=1) - (w[minus].sum(axis=1) if minus else 0)
    ok = (w[total] - rhs).abs() <= np.maximum(1000, 0.005 * w[total].abs())
    return len(w), ok.mean()
