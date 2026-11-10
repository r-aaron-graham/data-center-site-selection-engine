import unittest
from click.testing import CliRunner
from model import main, normalize

class SiteInputTests(unittest.TestCase):
    def test_empty_csv_reports_error_without_output(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            from pathlib import Path
            Path("sites.csv").write_text("site_name,power_mw\n")
            result = runner.invoke(main, ["--input", "sites.csv", "--output", "scores.csv"])
            self.assertNotEqual(result.exit_code, 0)
            self.assertIn("at least one site", result.output)
            self.assertFalse(Path("scores.csv").exists())

    def test_nonfinite_metrics(self):
        for values in ([], [float("nan")], [float("inf")]):
            with self.assertRaises(ValueError):
                normalize(values)
