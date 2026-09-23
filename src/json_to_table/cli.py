from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from .core import TableError, convert

VERSION = "1.0.0"

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="json-to-table", description="Convert JSON records into Markdown, CSV, HTML, or terminal tables.")
    p.add_argument("input", nargs="?", default="-", help="JSON file path, or - for stdin")
    p.add_argument("-f", "--format", choices=["markdown","csv","html","text"], default="markdown")
    p.add_argument("-o", "--output", help="write output to a file instead of stdout")
    p.add_argument("--flatten", action="store_true", help="flatten nested objects")
    p.add_argument("--separator", default=".", help="flattened-key separator (default: .)")
    p.add_argument("--columns", help="comma-separated columns and order")
    p.add_argument("--version", action="version", version=f"json-to-table {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    return p

def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
        data = json.loads(raw)
        wanted = [x.strip() for x in args.columns.split(",") if x.strip()] if args.columns else None
        result = convert(data, args.format, flatten_nested=args.flatten, columns=wanted, separator=args.separator)
        if args.output:
            Path(args.output).write_text(result, encoding="utf-8", newline="")
        else:
            sys.stdout.write(result)
        return 0
    except (OSError, json.JSONDecodeError, TableError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
