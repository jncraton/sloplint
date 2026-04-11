from sloplint.cli import main
from sloplint.lint import fix, lint


def test_main_returns_non_zero_for_issues(tmp_path, capsys):
    path = tmp_path / "sample.md"
    path.write_text("This is **bold**\n", encoding="utf-8")

    exit_code = main([str(path)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert f"{path}:1: " in captured.out


def test_issue_count(tmp_path, capsys):
    exit_code = main(["samples/chatgpt-20260411-black-holes.md"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert f"samples/chatgpt-20260411-black-holes.md:1: " in captured.out
    assert len(captured.out.splitlines()) == 25


def test_main_fix_rewrites_file(tmp_path, capsys):
    path = tmp_path / "sample.md"
    path.write_text("This — is **bold** 😊\n", encoding="utf-8")

    exit_code = main(["--fix", str(path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == ""
    assert path.read_text(encoding="utf-8") == "This, is bold \n"


def test_main_returns_zero_for_clean_file(tmp_path):
    path = tmp_path / "clean.md"
    path.write_text("This is plain markdown\n", encoding="utf-8")

    exit_code = main([str(path)])

    assert exit_code == 0


def test_main_reports_missing_file(tmp_path, capsys):
    path = tmp_path / "missing.md"

    exit_code = main([str(path)])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "file not found" in captured.out
