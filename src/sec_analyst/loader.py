"""Find and prepare SEC financial statement data."""

from tempfile import TemporaryDirectory
import duckdb
import json
import re
from pathlib import Path

def get_raw(
    filename: str,
    raw_dir: Path,
    kaggle_handle: str,
) -> Path:
    """Use a local file when available, otherwise download it."""
    local = raw_dir / filename

    if local.exists():
        return local

    import kagglehub

    return Path(
        kagglehub.dataset_download(kaggle_handle, path=filename)
    )


END_QUOTE = re.compile(rb'(?<!\\)(?:\\\\)*"')   # a quote preceded by an even number of backslashes ends a JSON string
KEY = re.compile(rb'"([^"]+)"\s*:\s*"')

def unpack_members(src: Path, out_dir: Path, chunk: int = 1 << 22) -> dict:
    '''Stream {"num.txt": "<tsv>", "sub.txt": ...} into one TSV per member, 4 MB at a time: a 400 MB member is never held whole.'''
    out_dir.mkdir(parents=True, exist_ok=True)
    sizes, buf, fh, name, eof = {}, b"", None, None, False
    with open(src, "rb") as f:
        while True:
            if not eof:
                data = f.read(chunk); eof = not data; buf += data
            if fh is None:
                m = KEY.search(buf)
                if not m:
                    if eof: break
                    continue
                name = m.group(1).decode(); sizes[name] = 0
                fh = open(out_dir / name, "w", encoding="utf-8", errors="replace", newline="")
                buf = buf[m.end():]
            m = END_QUOTE.search(buf)
            if m:                                                       # the member ends inside this buffer
                s = json.loads(b'"' + buf[:m.end() - 1] + b'"'); fh.write(s); sizes[name] += len(s)
                fh.close(); fh = None; buf = buf[m.end():]
                continue
            for cut in range(len(buf), max(len(buf) - 8, -1), -1):      # decode up to the last complete escape
                try:
                    s = json.loads(b'"' + buf[:cut] + b'"'); break
                except json.JSONDecodeError:
                    continue
            fh.write(s); sizes[name] += len(s); buf = buf[cut:]
            if eof and not buf: break
    return sizes


TSV = "delim='\t', header=true, quote='', escape='', all_varchar=true"
EXTRACT = {   # governance on load: street addresses, phone numbers, EIN and former names never reach the cache
    "sub": """SELECT adsh, cik::INTEGER AS cik, name, sic::INTEGER AS sic, countryba, stprba, countryinc, fye, form,
                     strptime(period, '%Y%m%d')::DATE AS period, fy::INTEGER AS fy, fp, strptime(filed, '%Y%m%d')::DATE AS filed,
                     prevrpt::INTEGER AS prevrpt, afs, nciks::INTEGER AS nciks, '{q}' AS fsq FROM read_csv('{d}/sub.txt', {TSV})""",
    "num": """SELECT adsh, tag, version, version = adsh AS custom, coreg, strptime(ddate, '%Y%m%d')::DATE AS ddate,
                     qtrs::SMALLINT AS qtrs, uom, value::DOUBLE AS value, '{q}' AS fsq FROM read_csv('{d}/num.txt', {TSV})
              ORDER BY tag, adsh, ddate""",                              # sorted by tag: a filter on tag reads a few row groups
    "pre": """SELECT adsh, report::SMALLINT AS report, line::SMALLINT AS line, stmt, inpth::SMALLINT AS inpth, tag, version,
                     version = adsh AS custom, plabel, negating::SMALLINT AS negating, '{q}' AS fsq FROM read_csv('{d}/pre.txt', {TSV})
              ORDER BY adsh, report, line""",
    "tag": """SELECT tag, version, custom::SMALLINT AS custom, abstract::SMALLINT AS abstract, datatype, iord, crdr, tlabel, doc,
                     '{q}' AS fsq FROM read_csv('{d}/tag.txt', {TSV})""",
}


def load_quarter(
    quarter: str,
    raw_dir: Path,
    processed_dir: Path,
    kaggle_handle: str,
) -> None:
    """Convert one quarter into the notebook's four Parquet tables."""
    processed_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        table: processed_dir / f"08_{table}_{quarter}.parquet"
        for table in EXTRACT
    }

    if all(path.exists() for path in outputs.values()):
        print(f"{quarter}: prepared files already exist")
        return

    source = get_raw(f"{quarter}.json", raw_dir, kaggle_handle)

    with TemporaryDirectory(dir=processed_dir) as folder:
        temporary = Path(folder)
        unpack_members(source, temporary)

        with duckdb.connect() as connection:
            connection.execute("SET memory_limit='1GB'")
            connection.execute("SET threads=2")
            connection.execute("SET preserve_insertion_order=false")
            temporary_sql = str(temporary).replace("'", "''")
            connection.execute(
                f"SET temp_directory='{temporary_sql}'"
            )

            for table, template in EXTRACT.items():
                query = template.format(
                    q=quarter,
                    d=temporary_sql,
                    TSV=TSV,
                )
                destination = temporary / outputs[table].name
                destination_sql = str(destination).replace("'", "''")

                connection.execute(
                    f"COPY ({query}) TO '{destination_sql}' "
                    "(FORMAT parquet, COMPRESSION zstd, "
                    "ROW_GROUP_SIZE 100000)"
                )

        for destination in outputs.values():
            (temporary / destination.name).replace(destination)

    print(f"{quarter}: prepared {len(outputs)} Parquet files")
