"""Load the OKF knowledge bundle and retrieve the concepts relevant to a report section."""

from __future__ import annotations

from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parent / "knowledge"
RESERVED = {"index.md", "log.md"}
BODY_LINK = re.compile(r"\]\((/[^)\s]+\.md)\)")


def load_concepts(root: Path = ROOT) -> dict[str, dict]:
    """Return concepts keyed by bundle path (e.g. "/breadth/mmof.md")."""
    concepts = {}
    for path in sorted(root.rglob("*.md")):
        if path.name in RESERVED:
            continue
        text = path.read_text(encoding="utf-8")
        parts = text.split("---\n", 2)
        if not text.startswith("---\n") or len(parts) < 3:
            raise ValueError(f"{path}: concept has no YAML frontmatter")
        meta = yaml.safe_load(parts[1]) or {}
        if not meta.get("type"):
            raise ValueError(f"{path}: frontmatter needs a non-empty type")
        key = "/" + path.relative_to(root).as_posix()
        concepts[key] = {"path": key, "meta": meta, "body": parts[2].strip(), "text": text}
    return concepts


def _extension(concept: dict) -> dict:
    return concept["meta"].get("market_report") or {}


def _mentions(concept: dict, needles: set[str]) -> bool:
    haystack = concept["text"]
    return any(needle in haystack for needle in needles)


def retrieve(concepts: dict[str, dict], section: str, symbols: tuple[str, ...]) -> list[dict]:
    """Find concepts for a section: its metrics, concepts mentioning them, and one hop of links."""
    found = {p: "metric" for p, c in concepts.items() if _extension(c).get("symbol") in symbols}
    needles = set(symbols) | set(found)
    for path, concept in concepts.items():
        if path not in found and (_extension(concept).get("section") == section or _mentions(concept, needles)):
            found[path] = "related"
    for path in list(found):
        concept = concepts[path]
        links = [_extension(concept).get("insight_source")]
        links += [s.get("resource") for s in concept["meta"].get("sources") or []]
        links += BODY_LINK.findall(concept["body"])
        for link in links:
            if link in concepts and link not in found:
                found[link] = "linked"
    results = []
    for path, relation in found.items():
        meta, extension = concepts[path]["meta"], _extension(concepts[path])
        results.append({"path": path, "relation": relation, "type": meta["type"], "title": meta.get("title"),
                        "status": meta.get("status", "stable"),
                        "evidence_status": extension.get("evidence_status"), "enabled": extension.get("enabled")})
    order = {"metric": 0, "related": 1, "linked": 2}
    return sorted(results, key=lambda r: (order[r["relation"]], r["path"]))
