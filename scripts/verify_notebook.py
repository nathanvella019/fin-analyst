"""Execute trusted project client cells in Python, without requiring Jupyter UI."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys

path=Path('notebooks/analyst_client.ipynb')
book=json.loads(path.read_text());scope={'__name__':'__main__'};records=[]
for i,cell in enumerate(book['cells']):
    if cell['cell_type']=='code':
        with contextlib.redirect_stdout(io.StringIO()) as capture:
            exec(compile(''.join(cell['source']),f'{path}:cell-{i}','exec'),scope)
        records.append({'cell':i,'passed':True,'stdout':capture.getvalue()})
assert scope['candidate']['value']==63843837
output=Path('data/evaluation/notebook_client_check.json')
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(json.dumps({
    'notebook_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
    'python':sys.version,'execution':'Sequential Python code-cell execution, not a Jupyter UI test',
    'results':records,
},indent=2)+'\n')
print(f'{len(records)} code cells passed; evidence: {output}')
