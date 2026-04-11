import re

triggers = {
    # https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Overuse_of_boldface
    "**...**": r"\1",
    # https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Overuse_of_em_dashes
    r" ?— ?": r", ",
    "meticulous": "",
    "meticulously": "",
    # https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Emoji
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
}

initial_transitions = [
    "Additionally",
    "Furthermore",
    "Moreover",
    "In addition",
    "Notably",
    "Importantly",
    "Equally important",
    "Nevertheless",
    "Nonetheless",
    "In contrast",
    "Consequently",
    "Accordingly",
    "Subsequently",
    "Hence",
    "Thus",
    "In summary",
    "Overall",
    "Ultimately",
    "In conclusion",
    "To conclude",
    "Essentially",
    "In essence",
    "Specifically",
    "In particular",
    "Indeed",
    "In fact",
    "Significantly",
    "It is important to note",
    "No discussion would be complete without",
    "Furthermore",
    "Moreover",
    "In summary",
]

for transition in initial_transitions:
    triggers[transition + ","] = ""

for trigger in triggers:
    if not isinstance(triggers[trigger], tuple):
        triggers[trigger] = (trigger, triggers[trigger])

    rule, replacement = triggers[trigger]

    if not "\\" in rule and not "?" in rule:
        rule = re.escape(rule)
        rule = rule.replace("\\.\\.\\.", "(.*?)")
        if rule[0].isalnum():
            rule = r"\b" + rule
        if not replacement:
            rule = rule + r" ?"

        triggers[trigger] = (rule, replacement)


def fix(content: str) -> str:
    """Return content with detectable markdown issues fixed.

    >>> fix('This **bold** text\\n')
    'This bold text\\n'

    >>> fix('This **bold** text in **bold**\\n')
    'This bold text in bold\\n'

    >>> fix('Pause — here\\n')
    'Pause, here\\n'

    >>> fix('Smile 😊\\n')
    'Smile \\n'

    >>> fix('Additionally, note this.\\n')
    'Note this.\\n'

    >>> fix('It is meticulous work.\\n')
    'It is work.\\n'
    """
    for pattern, replacement in triggers.values():
        if replacement != "":
            content = re.sub(pattern, replacement, content)
        else:
            while True:
                match = re.search(pattern, content)
                if not match or match.start() == match.end():
                    break
                start = match.start()
                end = match.end()
                match_text = match.group(0)
                if match_text and match_text[0].isupper() and end < len(content):
                    content = content[:end] + content[end].upper() + content[end + 1 :]
                content = content[:start] + content[end:]
    return content


def lint(content: str) -> list[str]:
    """Return a list of markdown issues detected in the content.

    >>> lint('This **bold** text\\n')
    ['1: **...**']

    >>> len(lint('This **bold** text in **bold**\\n'))
    2

    >>> lint('Pause — here\\n')
    ['1:  ?— ?']

    >>> lint('Smile 😊\\n')
    ['1: char:emoji']

    >>> lint('Additionally, note this.\\n')
    ['1: Additionally,']

    >>> lint('It is meticulous work.\\n')
    ['1: meticulous']
    """
    issues: list[str] = []

    for line_number, line in enumerate(content.splitlines(), start=1):
        for name, trigger in triggers.items():
            for match in re.findall(trigger[0], line):
                issues.append(f"{line_number}: {name}")

    return issues
