"""Workspace paths for data, reports and the editable knowledge bundle."""
import os
from pathlib import Path

# Editable uv installation resolves back to this checkout, independent of cwd.
# A wheel installation can point at a separate workspace with the environment variable.
PROJECT_ROOT = Path(os.environ.get("SITUATIONAL_AWARENESS_HOME", Path(__file__).resolve().parents[2])).expanduser().resolve()
