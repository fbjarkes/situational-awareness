"""Report settings: explicit arguments > process environment > project .env > defaults."""
import os
from pathlib import Path
from dotenv import dotenv_values
from situational_awareness.paths import PROJECT_ROOT


def ratio_lookback_months(value=None, *, env_file: Path | None = None):
    """Resolve the ratio window independently of other report chart windows."""
    if value is None:
        value = os.environ.get("RATIO_LOOKBACK_MONTHS")
    if value is None:
        value = dotenv_values(env_file or PROJECT_ROOT / ".env").get("RATIO_LOOKBACK_MONTHS", "36")
    try:
        months = int(value)
    except (TypeError, ValueError):
        raise ValueError("RATIO_LOOKBACK_MONTHS must be an integer between 1 and 120") from None
    if not 1 <= months <= 120:
        raise ValueError("RATIO_LOOKBACK_MONTHS must be an integer between 1 and 120")
    return months
