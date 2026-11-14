import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from sec_analyst.loader import get_raw, unpack_members


class LoaderTests(unittest.TestCase):
    def test_existing_file_is_used(self):
        with TemporaryDirectory() as folder:
            raw_dir = Path(folder)
            source = raw_dir / "example.json"
            source.write_text("{}", encoding="utf-8")

            result = get_raw("example.json", raw_dir, "unused/dataset")

            self.assertEqual(result, source)

    def test_tables_survive_small_reads(self):
        expected = {
            "num.txt": "tag\tvalue\nAssets\t100\nRevenue\t200\n",
            "sub.txt": 'name\tform\nExample "Company"\t10-K\n',
        }

        with TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "quarter.json"
            source.write_text(json.dumps(expected), encoding="utf-8")
            output = root / "tables"

            sizes = unpack_members(source, output, chunk=32)

            for name, content in expected.items():
                with self.subTest(filename=name):
                    actual = (output / name).read_text(encoding="utf-8")
                    self.assertEqual(actual, content)
                    self.assertEqual(sizes[name], len(content))