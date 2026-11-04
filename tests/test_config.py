from pathlib import Path
import os
import tempfile
import unittest
from unittest.mock import patch
from situational_awareness.config import ratio_lookback_months


class RatioConfigTests(unittest.TestCase):
    def test_default_file_environment_and_explicit_precedence(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {}, clear=True):
            path = Path(folder) / ".env"
            self.assertEqual(ratio_lookback_months(env_file=path), 36)
            path.write_text("RATIO_LOOKBACK_MONTHS=48\n", encoding="utf-8")
            self.assertEqual(ratio_lookback_months(env_file=path), 48)
            os.environ["RATIO_LOOKBACK_MONTHS"] = "24"
            self.assertEqual(ratio_lookback_months(env_file=path), 24)
            self.assertEqual(ratio_lookback_months(12, env_file=path), 12)

    def test_invalid_settings_are_rejected(self):
        for value in ("bad", "", "3.5", "0", "121"):
            with self.subTest(value=value), patch.dict(os.environ, {"RATIO_LOOKBACK_MONTHS": value}):
                with self.assertRaisesRegex(ValueError, "between 1 and 120"):
                    ratio_lookback_months()
