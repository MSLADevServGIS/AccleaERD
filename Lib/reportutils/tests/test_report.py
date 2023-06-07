"""Tests for report.py."""
import unittest

from dbconnections import SQLiteConnector
from reportutils import Report


class ProcReport(Report):
    def process(self):
        df = self.result
        df.iloc[0, 0] = "Okay"
        self.result = df
        return


class TestSimple(unittest.TestCase):
    def setUp(self):
        # Initialize the Test Report
        self.test_rpt = Report(
            __file__,
            "ok.sql"
        )
        
        # Run the report
        self.test_rpt.connect(SQLiteConnector)
        self.test_rpt.execute()

    def test_simplereport(self):
        # Test for correct results
        self.assertEqual(self.test_rpt.result.iloc[0, 0], "OK")


class TestAdv(unittest.TestCase):
    def setUp(self):
        self.test_rpt = ProcReport(
            __file__,
            "ok.sql"
        )
        self.test_rpt.connect(SQLiteConnector)
        self.test_rpt.execute()

    def test_processing_method(self):
        self.assertEqual(self.test_rpt.result.iloc[0, 0], "OK")
        self.test_rpt.process()
        self.assertEqual(self.test_rpt.result.iloc[0, 0], "Okay")