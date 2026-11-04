"""Collect open research tasks from the OKF bundle for report status."""
from pathlib import Path
import re

import yaml


def collect_research_todos(root: Path) -> list[dict]:
    tasks = []
    for path in sorted(root.rglob("*.md")):
        if path.name in ("index.md", "log.md"):
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "---":
            continue
        end = lines.index("---", 1)
        metadata = yaml.safe_load("\n".join(lines[1:end]))
        if metadata.get("status") == "deprecated":
            continue
        research_level = None
        fence = None
        current = None
        for number, line in enumerate(lines[end + 1:], end + 2):
            stripped = line.strip()
            fenced = re.match(r"^(`{3,}|~{3,})", stripped)
            if fenced:
                marker = fenced[1][0]
                if fence is None:
                    fence = marker
                elif fence == marker:
                    fence = None
                current = None
                continue
            if fence:
                continue
            heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
            if heading:
                level, title = len(heading[1]), heading[2].casefold()
                if research_level is not None and level <= research_level:
                    research_level = None
                if title == "research todos":
                    research_level = level
                current = None
                continue
            if research_level is None:
                continue
            checkbox = re.match(r"^\s*[-*+]\s+\[([ xX])\]\s+(.+)", line)
            if checkbox:
                current = None
                if checkbox[1] == " ":
                    current = {"title": str(metadata.get("title", path.stem)),
                               "description": checkbox[2],
                               "source": "/" + path.relative_to(root).as_posix(), "line": number}
                    tasks.append(current)
            elif not stripped or re.match(r"^\s*(?:[-*+]|\d+[.)])\s", line):
                current = None
            elif current and line[:1].isspace():
                current["description"] += " " + stripped
            else:
                current = None
    for task in tasks:
        text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", task["description"])
        text = re.sub(r"[`*_]", "", text)
        text = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0].strip()
        task["description"] = text if text.endswith((".", "!", "?")) else text + "."
    return tasks
