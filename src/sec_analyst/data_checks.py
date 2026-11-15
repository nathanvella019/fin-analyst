"""Remeasure notebook data traps on the configured prepared files."""
import json
from pathlib import Path
import yaml
from sec_analyst.provenance import model_identity
from sec_analyst.warehouse import connect_warehouse

QUERIES = {
    'durations': """SELECT count(*) filings FROM (
        SELECT n.adsh FROM num n JOIN sub s USING(adsh)
        WHERE s.form='10-Q' AND n.tag='NetIncomeLoss' AND n.ddate=s.period
          AND n.coreg IS NULL GROUP BY n.adsh HAVING count(DISTINCT n.qtrs)>1)""",
    'entities': """SELECT count(*) assets_facts,
        count(*) FILTER(WHERE coreg IS NOT NULL) coreg_assets,
        avg((coreg IS NOT NULL)::INT) coreg_share FROM num WHERE tag='Assets'""",
    'units': """SELECT uom,count(*) facts,count(DISTINCT adsh) filings FROM num
        WHERE tag IN ('Revenues','SalesRevenueNet') AND qtrs=4 GROUP BY uom ORDER BY facts DESC""",
    'currency_sum': """SELECT sum(value) all_units,
        sum(value) FILTER(WHERE uom='USD') usd_only FROM num n JOIN sub s USING(adsh)
        WHERE n.tag='Revenues' AND n.qtrs=4 AND n.coreg IS NULL
          AND s.form IN ('10-K','20-F','40-F') AND n.ddate=s.period""",
    'fiscal_year': """SELECT count(*) annual_reports,
        count(*) FILTER(WHERE fy<>year(period)) year_mismatches,
        count(*) FILTER(WHERE month(period)<=3) jan_mar_ends,
        count(*) FILTER(WHERE month(period)<=3 AND fy=year(period)-1) jan_mar_prior_fy
        FROM sub WHERE form='10-K'""",
    'amendments': """SELECT count(*) filings,
        count(*) FILTER(WHERE form IN ('10-K/A','10-Q/A')) amendments,
        sum(prevrpt::INT) originals_later_amended FROM sub""",
    'apple_comparatives': """SELECT s.name,s.form,s.filed,s.period,n.tag,n.ddate,n.qtrs,n.uom,n.value
        FROM num n JOIN sub s USING(adsh) WHERE s.cik=320193 AND n.tag='Assets'
        AND n.ddate=DATE '2015-09-30' AND n.qtrs=0 AND n.uom='USD' AND n.coreg IS NULL
        AND s.form IN ('10-K','10-Q') ORDER BY s.filed""",
}


def run_checks(connection):
    return {name: connection.execute(sql).df().to_dict('records') for name,sql in QUERIES.items()}


def main():
    config=Path('config/config.yaml')
    settings=yaml.safe_load(config.read_text())
    with connect_warehouse(Path(settings['processed_dir']),settings['quarters']) as connection:
        results=run_checks(connection)
    results['model_identity']=model_identity(config)
    destination=Path(settings['processed_dir']).parent/'evaluation/data_checks.json'
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(results,indent=2,default=str)+'\n')
    print(json.dumps(results,indent=2,default=str))

if __name__=='__main__':
    main()
