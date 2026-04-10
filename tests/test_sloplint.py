from sloplint.cli import main
from sloplint.lint import fix_markdown_content, find_markdown_issues


def test_find_markdown_issues():
    content = "First line — with em dash\nSecond line **bold**\nThird line 😊\n"
    issues = find_markdown_issues(content)

    assert "1: em-dash detected" in issues
    assert "2: bold markdown detected" in issues
    assert "3: emoji detected" in issues


def test_fix_markdown_content():
    content = "First line — with em dash\nSecond line **bold**\nThird line 😊\n"
    fixed = fix_markdown_content(content)

    assert fixed == "First line, with em dash\nSecond line bold\nThird line \n"


def test_main_returns_non_zero_for_issues(tmp_path, capsys):
    path = tmp_path / "sample.md"
    path.write_text("This is **bold**\n", encoding="utf-8")

    exit_code = main([str(path)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert f"{path}:1: bold markdown detected" in captured.out


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
