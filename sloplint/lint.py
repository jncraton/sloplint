import re

triggers = {
    # https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Curly_quotation_marks_and_apostrophes
    "“": '"',
    "”": '"',
    "‘": "'",
    "’": "'",
    # https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#High_density_of_%22AI_vocabulary%22_words
    "Additionally,": "",
    "aligns? with": None,
    "bolstered": None,
    "crucial": None,
    "delve": None,
    "emphasizing": None,
    "enduring": None,
    "enhance": None,
    "fostering": None,
    "garner": None,
    "highlight": None,
    "interplay": None,
    "intricate": None,
    "intricacies": None,
    "landscape": None,
    "meticulous": None,
    "meticulously": None,
    "pivotal": None,
    "showcase": None,
    "tapestry": None,
    "testament": None,
    "underscore": None,
    "valuable": None,
    "vibrant": None,
    # https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Avoidance_of_basic_copulatives_(%22is%22/%22are%22_phrases)
    "serves as": "is",
    "serve as": "are",
    "stands as": "is",
    "stand as": "are",
    "represents": "is",
    "represent": "are",
    "boasts": "has",
    "features": "has",
    "offers": "has",
    # https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Not_just_X,_but_also_Y
    "not just": None,
    "isn't just": None,
    "not only": None,
    "isn't only": None,
    # https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Overuse_of_boldface
    "**...**": r"\1",
    # https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing#Overuse_of_em_dashes
    r" ?— ?": r", ",
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

    >>> fix('This **bold** text')
    'This bold text'

    >>> fix('This **bold** text in **bold**')
    'This bold text in bold'

    >>> fix('Pause — here')
    'Pause, here'

    >>> fix('Smile 😊')
    'Smile '

    >>> fix('Additionally, note this.')
    'Note this.'

    >>> fix('This aligns with that')
    'This aligns with that'

    >>> fix('The city boasts two hotels')
    'The city has two hotels'

    >>> fix('The book represents a key moment and stands as a work')
    'The book is a key moment and is a work'

    >>> fix('The books represent a key moment and stand as the')
    'The books are a key moment and are the'

    >>> fix('It is meticulous work.')
    'It is meticulous work.'

    >>> fix("It isn't only good, but great")
    "It isn't only good, but great"

    >>> fix('“Hello, world”')
    '"Hello, world"'

    >>> fix('‘Hello, world’')
    "'Hello, world'"
    """
    for pattern, replacement in triggers.values():
        if replacement != "":
            if replacement != None:
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

    >>> lint('This **bold** text')
    ['1: **...**']

    >>> len(lint('This **bold** text in **bold**'))
    2

    >>> lint('Pause — here')
    ['1:  ?— ?']

    >>> lint('Smile 😊')
    ['1: char:emoji']

    >>> lint('Additionally, note this.')
    ['1: Additionally,']

    >>> lint('This aligns with that')
    ['1: aligns? with']

    >>> lint('It is meticulous work.')
    ['1: meticulous']

    >>> lint("It isn't only good, but great")
    ["1: isn't only"]

    >>> lint("It isn’t only good, but great")
    ["1: isn't only"]

    >>> lint('“Hello, world”')
    ['1: “', '1: ”']

    >>> lint('‘Hello, world’')
    ['1: ‘', '1: ’']
    """
    issues: list[str] = []

    for line_number, line in enumerate(content.splitlines(), start=1):
        for name, trigger in triggers.items():
            for match in re.findall(trigger[0], line):
                issues.append(f"{line_number}: {name}")

    return issues
