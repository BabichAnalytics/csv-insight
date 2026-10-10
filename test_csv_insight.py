import tempfile
import unittest
from pathlib import Path
from csv_insight import analyze

class ReportTests(unittest.TestCase):
    def inspect(self, text):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"input.csv"
            path.write_text(text, encoding="utf-8")
            return analyze(path)
    def test_report(self):
        r = self.inspect('name,value\n"a,b",2\nc,\n"a,b",2\nd,4\n')
        self.assertEqual(r["rows"], 4)
        self.assertEqual(r["duplicate_rows"], 1)
        self.assertEqual(r["columns"]["value"]["missing"], 1)
        self.assertAlmostEqual(r["columns"]["value"]["numeric"]["mean"], 8/3)
    def test_invalid_shape(self):
        with self.assertRaises(ValueError):
            self.inspect("a,b\n1\n")
    def test_nonfinite(self):
        self.assertNotIn("numeric", self.inspect("a\nNaN\n")["columns"]["a"])
    def test_empty_data(self):
        self.assertEqual(self.inspect("a,b\n")["rows"], 0)

if __name__ == "__main__":
    unittest.main()

