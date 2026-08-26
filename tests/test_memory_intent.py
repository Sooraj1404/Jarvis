from memory.intent import MemoryIntentDetector


detector = MemoryIntentDetector()


def test(description, text, expected):
    result = detector.detect(text)

    if result == expected:
        print(f"[PASS] {description}")
    else:
        print(f"[FAIL] {description}")
        print(f"       Input:    {text}")
        print(f"       Expected: {expected}")
        print(f"       Received: {result}")


# ---------------------------------------------------------
# BASIC MEMORY CREATION
# ---------------------------------------------------------

test(
    "favorite programming language",
    "My favorite programming language is Python.",
    {
        "intent": "remember",
        "key": "favorite_programming_language",
        "value": "Python",
    },
)

test(
    "name",
    "My name is Alex.",
    {
        "intent": "remember",
        "key": "name",
        "value": "Alex",
    },
)

test(
    "operating system",
    "My operating system is Windows 11.",
    {
        "intent": "remember",
        "key": "operating_system",
        "value": "Windows 11",
    },
)


# ---------------------------------------------------------
# PREFERENCES
# ---------------------------------------------------------

test(
    "preferred editor",
    "I prefer VS Code.",
    {
        "intent": "remember",
        "key": "preferred_editor",
        "value": "VS Code",
    },
)

test(
    "preferred programming language",
    "I prefer Python.",
    {
        "intent": "remember",
        "key": "preferred_programming_language",
        "value": "Python",
    },
)


# ---------------------------------------------------------
# VALUE CLEANING
# ---------------------------------------------------------

test(
    "remove punctuation",
    "My favorite language is Python!",
    {
        "intent": "remember",
        "key": "favorite_language",
        "value": "Python",
    },
)

test(
    "remove extra whitespace",
    "My favorite food is   Pizza.",
    {
        "intent": "remember",
        "key": "favorite_food",
        "value": "Pizza",
    },
)


# ---------------------------------------------------------
# OTHER NATURAL PATTERNS
# ---------------------------------------------------------

test(
    "software",
    "I use VS Code.",
    {
        "intent": "remember",
        "key": "software_or_tool",
        "value": "VS Code",
    },
)

test(
    "field of study",
    "I study Computer Engineering.",
    {
        "intent": "remember",
        "key": "field_of_study",
        "value": "Computer Engineering",
    },
)

test(
    "occupation",
    "I work as a software developer.",
    {
        "intent": "remember",
        "key": "occupation",
        "value": "a software developer",
    },
)


# ---------------------------------------------------------
# FORGET
# ---------------------------------------------------------

test(
    "forget favorite language",
    "Forget my favorite programming language.",
    {
        "intent": "forget",
        "key": "favorite_programming_language",
    },
)


# ---------------------------------------------------------
# SHOULD NOT CREATE MEMORY
# ---------------------------------------------------------

test(
    "question",
    "What is my favorite programming language?",
    {
        "intent": "none",
    },
)

test(
    "question",
    "Do I prefer Python?",
    {
        "intent": "none",
    },
)

test(
    "normal statement",
    "Python is a programming language.",
    {
        "intent": "none",
    },
)

test(
    "normal conversation",
    "That sounds interesting.",
    {
        "intent": "none",
    },
)

