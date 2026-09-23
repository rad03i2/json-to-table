"""Core conversion functions for json-to-table."""
from __future__ import annotations

import csv
import html
import io
import json
from collections.abc import Iterable, Mapping
from typing import Any

SCALAR = (str, int, float, bool, type(None))

class TableError(ValueError):
    """Raised when input cannot be represented as a record table."""

def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)

def flatten(record: Mapping[str, Any], *, separator: str = ".") -> dict[str, Any]:
    """Flatten nested mappings while keeping lists as JSON values."""
    if not separator:
        raise TableError("separator must not be empty")
    out: dict[str, Any] = {}
    def walk(obj: Mapping[str, Any], prefix: str = "") -> None:
        for key, value in obj.items():
            key = str(key)
            name = f"{prefix}{separator}{key}" if prefix else key
            if isinstance(value, Mapping):
                walk(value, name)
            else:
                out[name] = value
    walk(record)
    return out

def normalize(data: Any, *, flatten_nested: bool = False, separator: str = ".") -> tuple[list[str], list[dict[str, Any]]]:
    """Normalize a JSON object/list into ordered columns and records."""
    if isinstance(data, Mapping):
        records = [dict(data)]
    elif isinstance(data, list):
        if not data:
            return [], []
        if not all(isinstance(item, Mapping) for item in data):
            raise TableError("top-level arrays must contain JSON objects")
        records = [dict(item) for item in data]
    else:
        raise TableError("top-level JSON must be an object or an array of objects")
    if flatten_nested:
        records = [flatten(r, separator=separator) for r in records]
    columns: list[str] = []
    seen: set[str] = set()
    for record in records:
        for key in record:
            key = str(key)
            if key not in seen:
                seen.add(key); columns.append(key)
    return columns, records

def select(columns: list[str], records: list[dict[str, Any]], wanted: Iterable[str] | None) -> tuple[list[str], list[dict[str, Any]]]:
    if wanted is None:
        return columns, records
    requested = list(wanted)
    missing = [c for c in requested if c not in columns]
    if missing:
        raise TableError("unknown column(s): " + ", ".join(missing))
    return requested, records

def to_csv(columns: list[str], records: list[dict[str, Any]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(columns)
    for row in records:
        writer.writerow([_stringify(row.get(c)) for c in columns])
    return stream.getvalue()

def _md(value: Any) -> str:
    return _stringify(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")

def to_markdown(columns: list[str], records: list[dict[str, Any]]) -> str:
    if not columns:
        return "(empty table)\n"
    lines = ["| " + " | ".join(_md(c) for c in columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    lines += ["| " + " | ".join(_md(r.get(c)) for c in columns) + " |" for r in records]
    return "\n".join(lines) + "\n"

def to_html(columns: list[str], records: list[dict[str, Any]]) -> str:
    head = "".join(f"<th>{html.escape(c)}</th>" for c in columns)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(_stringify(r.get(c)))}</td>" for c in columns) + "</tr>" for r in records)
    return f'<table>\n<thead><tr>{head}</tr></thead>\n<tbody>{body}</tbody>\n</table>\n'

def to_text(columns: list[str], records: list[dict[str, Any]]) -> str:
    if not columns:
        return "(empty table)\n"
    rows = [[_stringify(r.get(c)).replace("\n", "\\n") for c in columns] for r in records]
    widths = [max(len(c), *(len(row[i]) for row in rows)) for i, c in enumerate(columns)]
    line = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    render = lambda row: "| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(columns))) + " |"
    return "\n".join([line, render(columns), line, *(render(r) for r in rows), line]) + "\n"

def convert(data: Any, fmt: str = "markdown", *, flatten_nested: bool = False, columns: Iterable[str] | None = None, separator: str = ".") -> str:
    cols, rows = normalize(data, flatten_nested=flatten_nested, separator=separator)
    cols, rows = select(cols, rows, columns)
    renderers = {"markdown": to_markdown, "csv": to_csv, "html": to_html, "text": to_text}
    try:
        return renderers[fmt](cols, rows)
    except KeyError as exc:
        raise TableError(f"unsupported format: {fmt}") from exc
