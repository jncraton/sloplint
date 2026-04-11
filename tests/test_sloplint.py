from sloplint.cli import main
from sloplint.lint import fix, lint


def test_lint():
    content = (
        "First line — with em dash\n"
        "Second line **bold**\n"
        "Third line 😊\n"
        "Additionally, this is true.\n"
        "It is meticulous work.\n"
    )
    issues = lint(content)

    assert "1: char:em-dash" in issues
    assert "2: style:bold" in issues
    assert "3: char:emoji" in issues
    assert "4: word:additionally" in issues
    assert "5: word:meticulous" in issues


def test_fix():
    content = (
        "First line — with em dash\n"
        "Second line **bold**\n"
        "Third line 😊\n"
        "Additionally, this is true.\n"
        "It is meticulous work.\n"
    )
    fixed = fix(content)

    assert fixed == (
        "First line, with em dash\n"
        "Second line bold\n"
        "Third line \n"
        "This is true.\n"
        "It is work.\n"
    )


def test_main_returns_non_zero_for_issues(tmp_path, capsys):
    path = tmp_path / "sample.md"
    path.write_text("This is **bold**\n", encoding="utf-8")

    exit_code = main([str(path)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert f"{path}:1: style:bold" in captured.out


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
