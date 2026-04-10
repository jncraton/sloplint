import re

triggers = {
    "em-dash": {
        "find": re.compile(r" \u2014 "),
        "replace": lambda match: ", ",
    },
    "bold markdown": {
        "find": re.compile(r"(?:\*\*[^*\n]+\*\*)"),
        "replace": lambda match: match.group(0).replace("**", "").replace("__", ""),
    },
    "emoji": {
        "find": re.compile(
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
            r"]"
        ),
        "replace": lambda match: "",
    },
    "additionally": {
        "find": re.compile(r"Additionally, "),
        "replace": lambda match: "",
    },
    "meticulous wording": {
        "find": re.compile(r"\bmeticulous(?:ly)? "),
        "replace": lambda match: "",
    },
}


def fix_markdown_content(content: str) -> str:
    """Return content with detectable markdown issues fixed."""
    for trigger in triggers.values():
        content = trigger["find"].sub(trigger["replace"], content)
    return content


def find_markdown_issues(content: str) -> list[str]:
    """Return a list of markdown issues detected in the content."""
    issues: list[str] = []

    for line_number, line in enumerate(content.splitlines(), start=1):
        for name, trigger in triggers.items():
            if trigger["find"].search(line):
                issues.append(f"{line_number}: {name} detected")

    return issues
