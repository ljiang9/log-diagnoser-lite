"""log-diagnoser-lite 单元测试。运行：python3 -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from diagnoser import parse_levels, diagnose, report, SAMPLE_LOG  # noqa: E402


class TestParse(unittest.TestCase):
    def test_levels(self):
        lv = parse_levels(SAMPLE_LOG)
        self.assertGreaterEqual(lv["ERROR"], 5)
        self.assertIn("INFO", lv)

    def test_clusters(self):
        d = diagnose(SAMPLE_LOG)
        patterns = {x["pattern"] for x in d}
        self.assertTrue(any("Connection" in p for p in patterns))

    def test_cause(self):
        d = diagnose(SAMPLE_LOG)
        oom = [x for x in d if "OutOfMemory" in x["pattern"]]
        self.assertTrue(oom)
        self.assertIn("内存", oom[0]["cause"])

    def test_no_errors(self):
        self.assertEqual(diagnose("2026 INFO everything ok"), [])

    def test_report(self):
        r = report(SAMPLE_LOG)
        self.assertIn("诊断报告", r)


if __name__ == "__main__":
    unittest.main()
