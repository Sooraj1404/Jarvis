import pytest

from memory.intent import MemoryIntentDetector


detector = MemoryIntentDetector()


@pytest.mark.parametrize(
    "description,text,expected",
    [
        # -------------------------------------------------
        # BASIC MEMORY CREATION
        # -------------------------------------------------

        (
            "favorite programming language",
            "My favorite programming language is Python.",
            {
                "intent": "remember",
                "key": "favorite_programming_language",
                "value": "Python",
            },
        ),
        (
            "name",
            "My name is Alex.",
            {
                "intent": "remember",
                "key": "name",
                "value": "Alex",
            },
        ),
        (
            "operating system",
            "My operating system is Windows 11.",
            {
                "intent": "remember",
                "key": "operating_system",
                "value": "Windows 11",
            },
        ),

        # -------------------------------------------------
        # PREFERENCES
        # -------------------------------------------------

        (
            "preferred editor",
            "I prefer VS Code.",
            {
                "intent": "remember",
                "key": "preferred_editor",
                "value": "VS Code",
            },
        ),
        (
            "preferred programming language",
            "I prefer Python.",
            {
                "intent": "remember",
                "key": "preferred_programming_language",
                "value": "Python",
            },
        ),

        # -------------------------------------------------
        # VALUE CLEANING
        # -------------------------------------------------

        (
            "remove punctuation",
            "My favorite language is Python!",
            {
                "intent": "remember",
                "key": "favorite_programming_language",
                "value": "Python",
            },
        ),
        (
            "remove extra whitespace",
            "My favorite food is   Pizza.",
            {
                "intent": "remember",
                "key": "favorite_food",
                "value": "Pizza",
            },
        ),

        # -------------------------------------------------
        # OTHER NATURAL PATTERNS
        # -------------------------------------------------

        (
            "software",
            "I use VS Code.",
            {
                "intent": "remember",
                "key": "preferred_editor",
                "value": "VS Code",
            },
        ),
        (
            "field of study",
            "I study Computer Engineering.",
            {
                "intent": "remember",
                "key": "field_of_study",
                "value": "Computer Engineering",
            },
        ),
        (
            "occupation",
            "I work as a software developer.",
            {
                "intent": "remember",
                "key": "occupation",
                "value": "software developer",
            },
        ),

        # -------------------------------------------------
        # FORGET
        # -------------------------------------------------

        (
            "forget favorite language",
            "Forget my favorite programming language.",
            {
                "intent": "forget",
                "key": "favorite_programming_language",
            },
        ),

        # -------------------------------------------------
        # SHOULD NOT CREATE MEMORY
        # -------------------------------------------------

        (
            "question",
            "What is my favorite programming language?",
            {
                "intent": "none",
            },
        ),
        (
            "question",
            "Do I prefer Python?",
            {
                "intent": "none",
            },
        ),
        (
            "normal statement",
            "Python is a programming language.",
            {
                "intent": "none",
            },
        ),
        (
            "normal conversation",
            "That sounds interesting.",
            {
                "intent": "none",
            },
        ),
    ],
)
def test_memory_intent(description, text, expected):
    result = detector.detect(text)

    assert result == expected, (
        f"\nTest: {description}"
        f"\nInput: {text}"
        f"\nExpected: {expected}"
        f"\nReceived: {result}"
    )