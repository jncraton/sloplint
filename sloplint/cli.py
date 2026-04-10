import argparse
from pathlib import Path
from typing import Sequence

from .lint import find_markdown_issues


def _parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sloplint",
        description="A linter to detect AI-generated markdown prose",
    )
    parser.add_argument("paths", nargs="+", help="Markdown file paths to lint")
    return parser.parse_args(args)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    messages: list[str] = []

    for path_text in args.paths:
        path = Path(path_text)
        if not path.exists():
            print(f"{path}: file not found")
            return 2
        if not path.is_file():
            print(f"{path}: not a file")
            return 2

        content = path.read_text(encoding="utf-8")
        issues = find_markdown_issues(content)
        for issue in issues:
            messages.append(f"{path}:{issue}")

    if messages:
        print("\n".join(messages))
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
