import re

triggers = {
    "style:bold": (r"\*\*([^*\n]+)\*\*", r"\1"),
    "char:em-dash": (r" \u2014 ", r", "),
    "char:emoji": (
        r"["
        r"\U0001F300-\U0001F5FF"
        r"\U0001F600-\U0001F64F"
        r"\U0001F680-\U0001F6FF"
        r"\U0001F700-\U0001F77F"
        r"\U0001F780-\U0001F7FF"
        r"\U0001F800-\U0001F8FF"
        r"\U0001F900-\U0001F9FF"
        r"\U0001FA00-\U0001FA6F"
        r"\U0001FA70-\U0001FAFF"
        r"\u2600-\u26FF"
        r"\u2700-\u27BF"
        r"]",
        "",
    ),
    "word:additionally": (
        r"Additionally, ",
        r"",
    ),
    "word:meticulous": (r"\bmeticulous(?:ly)? ", r""),
}


def fix_markdown_content(content: str) -> str:
    """Return content with detectable markdown issues fixed.

    >>> fix_markdown_content('This **bold** text\\n')
    'This bold text\\n'

    >>> fix_markdown_content('Pause — here\\n')
    'Pause, here\\n'

    >>> fix_markdown_content('Smile 😊\\n')
    'Smile \\n'

    >>> fix_markdown_content('Additionally, note this.\\n')
    'note this.\\n'

    >>> fix_markdown_content('It is meticulous work.\\n')
    'It is work.\\n'
    """
    for trigger in triggers.values():
        content = re.sub(trigger[0], trigger[1], content)
    return content


def find_markdown_issues(content: str) -> list[str]:
    """Return a list of markdown issues detected in the content.

    >>> find_markdown_issues('This **bold** text\\n')
    ['1: style:bold']

    >>> find_markdown_issues('Pause — here\\n')
    ['1: char:em-dash']

    >>> find_markdown_issues('Smile 😊\\n')
    ['1: char:emoji']

    >>> find_markdown_issues('Additionally, note this.\\n')
    ['1: word:additionally']

    >>> find_markdown_issues('It is meticulous work.\\n')
    ['1: word:meticulous']
    """
    issues: list[str] = []

    for line_number, line in enumerate(content.splitlines(), start=1):
        for name, trigger in triggers.items():
            if re.search(trigger[0], line):
                issues.append(f"{line_number}: {name}")

    return issues

