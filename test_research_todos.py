from pathlib import Path
import tempfile
import unittest

from research_todos import collect_research_todos


class ResearchTodoTests(unittest.TestCase):
    def test_only_open_research_tasks_with_one_sentence(self):
        Path("reports").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir="reports") as folder:
            root = Path(folder)
            (root / "example.md").write_text('''---
type: Metric
title: GDX
status: draft
---
# TODOs
- [ ] Not a research task.
# Research TODOs
- [ ] Conduct a [breadth study](/method.md)
  using daily data. Then test robustness.
  - Test three thresholds.
- [x] Completed study.
```
- [ ] Example only.
```
## Follow-up
- [ ] Measure drawdowns.
# Other
- [ ] Outside research.
''', encoding="utf-8")
            tasks = collect_research_todos(root)
            self.assertEqual([t["description"] for t in tasks], ["Conduct a breadth study using daily data.", "Measure drawdowns."])
            self.assertEqual(tasks[0]["source"], "/example.md")
            self.assertEqual(tasks[0]["title"], "GDX")

    def test_no_tasks_is_empty(self):
        Path("reports").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir="reports") as folder:
            self.assertEqual(collect_research_todos(Path(folder)), [])


if __name__ == "__main__":
    unittest.main()
