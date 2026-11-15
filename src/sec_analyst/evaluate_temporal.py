"""Notebook quarterly mapper diagnostic plus an input-restricted time check."""
import gc
import json
from pathlib import Path
import time
import numpy as np
import pandas as pd
import yaml
from sec_analyst.mapper import TagMapper, evaluate, ci95
from sec_analyst.mapper_data import prepare_line_items, prepare_silver_labels
from sec_analyst.provenance import model_identity
from sec_analyst.warehouse import connect_warehouse


def score(mapper, test):
    value=float(evaluate(mapper,test,{'both':('taxonomy','labels')}).loc['both','top-5'])
    lo,hi=ci95(round(value*len(test)),len(test))
    return value,float(lo),float(hi)


def main():
    config=Path('config/config.yaml');settings=yaml.safe_load(config.read_text())
    processed=Path(settings['processed_dir']);quarters=settings['quarters']
    output=processed.parent/'evaluation';output.mkdir(parents=True,exist_ok=True)
    records=[];started=time.perf_counter()
    with connect_warehouse(processed,quarters) as con:
        prepare_line_items(con,processed)
        silver=prepare_silver_labels(con,processed,settings['min_abs_usd'])
        companies=np.array(sorted(silver.cik.unique()))
        held=set(np.random.default_rng(settings['seed']).choice(companies,len(companies)//2,replace=False))
        test=silver[silver.cik.isin(held)].reset_index(drop=True)
        exclude='cik NOT IN ('+','.join(map(str,sorted(held)))+')'
        frozen=TagMapper(con,where=f"fsq = '{quarters[0]}' AND {exclude}")
        leaky=TagMapper(con,where=f"fsq = '{quarters[0]}'")
        for q in quarters:
            tq=test[test.fsq==q].reset_index(drop=True)
            refreshed=frozen if q==quarters[0] else TagMapper(con,where=f"fsq <= '{q}' AND {exclude}")
            for label,mapper in [('notebook frozen',frozen),('notebook refreshed',refreshed),('notebook leaky',leaky)]:
                value,lo,hi=score(mapper,tq)
                records.append(dict(quarter=q,method=label,test_tags=len(tq),top5=value,lo=lo,hi=hi))
            if refreshed is not frozen: del refreshed
        del frozen,leaky;gc.collect()
        # Refit the same algorithm with line items and taxonomy metadata visible by cutoff.
        # Silver labels are retrospective evaluation references, not training examples.
        strict_frozen=None
        for q in quarters:
            with connect_warehouse(processed,[x for x in quarters if x<=q]) as strict:
                strict.execute(f"CREATE VIEW li AS SELECT * FROM read_parquet('{str(processed / '08_line_items.parquet').replace(chr(39),chr(39)*2)}') WHERE fsq <= '{q}'")
                mapper=TagMapper(strict,where=exclude)
                if q==quarters[0]: strict_frozen=mapper
                tq=test[test.fsq==q].reset_index(drop=True)
                for label,current in [('time-restricted frozen',strict_frozen),('time-restricted refreshed',mapper)]:
                    value,lo,hi=score(current,tq)
                    records.append(dict(quarter=q,method=label,test_tags=len(tq),top5=value,lo=lo,hi=hi))
                if mapper is not strict_frozen: del mapper
            gc.collect()
    table=pd.DataFrame(records);table.to_csv(output/'temporal_mapper.csv',index=False)
    (output/'temporal_metrics.json').write_text(json.dumps({
        'model_identity':model_identity(config),'seed':settings['seed'],
        'held_out_companies':len(held),'test_tags':len(test),
        'seconds':time.perf_counter()-started,
        'scope':'Quarterly reference-index diagnostic from notebook; separate same-algorithm refits restrict line-item vocabulary and taxonomy metadata by quarter. Retrospective silver labels; hand concept table and this cohort were not a prospectively frozen 2016 deployment.',
    },indent=2)+'\n')
    print(table.to_string(index=False,float_format='{:.4f}'.format))

if __name__=='__main__':main()
