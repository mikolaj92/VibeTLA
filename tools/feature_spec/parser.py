from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


SECTION_MAP = {
    "summary": "summary",
    "entities": "entities",
    "states": "states",
    "transitions": "transitions",
    "invariants": "invariants",
    "forbidden states": "forbidden_states",
    "assumptions": "assumptions",
    "non-goals": "non_goals",
    "non goals": "non_goals",
}


@dataclass(slots=True)
class ParsedTask:
    source: str
    title: str | None
    sections: dict[str, list[str]]


def read_task_file(path: Path) -> ParsedTask:
    return parse_task_text(path.read_text(encoding="utf-8"), source=str(path), title_hint=path.stem)


def parse_task_text(text: str, source: str = "<text>", title_hint: str | None = None) -> ParsedTask:
    sections: dict[str, list[str]] = {value: [] for value in SECTION_MAP.values()}
    current_section: str | None = None
    title = title_hint

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        heading = re.match(r"^#{1,6}\s+(.*)$", line)
        if heading:
            heading_text = heading.group(1).strip()
            normalized = SECTION_MAP.get(heading_text.lower())
            if normalized:
                current_section = normalized
                continue
            if title is None:
                title = heading_text
            continue

        item = re.sub(r"^[-*]\s+", "", line).strip()
        if current_section is None:
            sections["summary"].append(item)
            continue
        sections[current_section].append(item)

    return ParsedTask(source=source, title=title, sections=sections)
