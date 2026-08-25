import re


class MemoryIntentDetector:
    """
    Fast, local memory intent detector.

    Uses deterministic patterns instead of an LLM so that
    ordinary conversations do not incur another model call.

    V0.2.1:
    - Better semantic memory keys
    - Cleaner memory values
    - Natural memory updates
    - Safer generic memory detection
    """

    def detect(self, user_input):
        text = self._clean_text(user_input)

        if not text:
            return {"intent": "none"}

        # =====================================================
        # FORGET
        # =====================================================

        forget_patterns = [
            r"^forget (?:that )?my (.+)$",
            r"^forget (?:my )?(.+)$",
            r"^don't remember (?:my )?(.+)$",
            r"^do not remember (?:my )?(.+)$",
        ]

        for pattern in forget_patterns:
            match = re.match(pattern, text, re.IGNORECASE)

            if match:
                key_text = self._clean_text(match.group(1))

                return {
                    "intent": "forget",
                    "key": self._semantic_key(key_text),
                }

        # =====================================================
        # "MY X IS Y"
        # =====================================================

        match = re.match(
            r"^my (.+?) is (.+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            key_text = match.group(1).strip()
            value = self._clean_value(match.group(2))

            key = self._semantic_key(key_text)

            if key and value:
                return {
                    "intent": "remember",
                    "key": key,
                    "value": value,
                }

        # =====================================================
        # "I USE X"
        # =====================================================

        match = re.match(
            r"^i use (.+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            value = self._clean_value(match.group(1))

            if value:
                key = self._usage_key(value)

                return {
                    "intent": "remember",
                    "key": key,
                    "value": value,
                }

        # =====================================================
        # "I PREFER X"
        # =====================================================

        match = re.match(
            r"^i prefer (.+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            value = self._clean_value(match.group(1))

            if value:
                key = self._preference_key(value)

                return {
                    "intent": "remember",
                    "key": key,
                    "value": value,
                }

        # =====================================================
        # "I LIKE X"
        # =====================================================

        match = re.match(
            r"^i like (.+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            value = self._clean_value(match.group(1))

            if value:
                return {
                    "intent": "remember",
                    "key": "likes",
                    "value": value,
                }

        # =====================================================
        # "I AM X"
        # =====================================================

        match = re.match(
            r"^i am (.+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            value = self._clean_value(match.group(1))

            if value:
                return {
                    "intent": "remember",
                    "key": "user_description",
                    "value": value,
                }

        # =====================================================
        # "I STUDY X"
        # =====================================================

        match = re.match(
            r"^i study (.+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            value = self._clean_value(match.group(1))

            if value:
                return {
                    "intent": "remember",
                    "key": "field_of_study",
                    "value": value,
                }

        # =====================================================
        # "I WORK AS X"
        # =====================================================

        match = re.match(
            r"^i work as (.+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            value = self._clean_value(match.group(1))

            if value:
                return {
                    "intent": "remember",
                    "key": "occupation",
                    "value": value,
                }

        # =====================================================
        # "REMEMBER THAT..."
        # =====================================================

        match = re.match(
            r"^(?:remember|remember that) (.+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            statement = self._clean_value(match.group(1))

            if statement and self._looks_like_fact(statement):
                return {
                    "intent": "remember",
                    "key": self._generic_fact_key(statement),
                    "value": statement,
                }

        return {"intent": "none"}

    # =========================================================
    # TEXT CLEANING
    # =========================================================

    @staticmethod
    def _clean_text(text):
        return text.strip()

    @classmethod
    def _clean_value(cls, value):
        """
        Normalize a memory value without changing its meaning.

        Examples:

            "Python."       -> "Python"
            "'Python'"      -> "Python"
            "Python!!!"     -> "Python"
            "  Python  "    -> "Python"
            "a developer"   -> "developer"
        """

        value = value.strip()

        # Remove surrounding quotation marks.
        value = value.strip("\"'")

        # Normalize repeated whitespace.
        value = re.sub(r"\s+", " ", value)

        # Remove common trailing punctuation.
        value = re.sub(r"[.!?,;:]+$", "", value)

        # Remove surrounding quotation marks again in case
        # punctuation was positioned outside the quotes.
        value = value.strip("\"'")

        # Remove unnecessary leading articles for certain
        # descriptive values.
        value = cls._remove_unnecessary_article(value)

        return value.strip()

    @staticmethod
    def _remove_unnecessary_article(value):
        """
        Remove 'a' or 'an' when the value is clearly a
        descriptive role/category.

        Examples:

            a software developer -> software developer
            an engineer           -> engineer

        This is intentionally conservative.
        """

        value = re.sub(
            r"^(a|an)\s+",
            "",
            value,
            flags=re.IGNORECASE,
        )

        return value

    # =========================================================
    # KEY GENERATION
    # =========================================================

    @classmethod
    def _semantic_key(cls, text):
        """
        Convert common natural-language memory descriptions
        into useful semantic keys.
        """

        normalized = re.sub(
            r"\s+",
            " ",
            text.lower().strip(),
        )

        semantic_keys = {
            # Identity
            "name": "name",
            "full name": "name",

            # Programming
            "favorite programming language":
                "favorite_programming_language",
            "favourite programming language":
                "favorite_programming_language",
            "favorite language":
                "favorite_programming_language",
            "favourite language":
                "favorite_programming_language",
            "preferred programming language":
                "preferred_programming_language",
            "programming language":
                "programming_language",

            # Editors
            "preferred editor":
                "preferred_editor",
            "favorite editor":
                "favorite_editor",
            "favourite editor":
                "favorite_editor",
            "code editor":
                "preferred_editor",
            "editor":
                "preferred_editor",

            # Operating systems
            "operating system":
                "operating_system",
            "os":
                "operating_system",
            "preferred operating system":
                "preferred_operating_system",

            # Devices
            "phone":
                "phone",
            "mobile phone":
                "phone",
            "smartphone":
                "phone",
            "laptop":
                "laptop",
            "computer":
                "computer",

            # Favorites
            "favorite color":
                "favorite_color",
            "favourite colour":
                "favorite_color",
            "favorite food":
                "favorite_food",
            "favourite food":
                "favorite_food",
            "favorite game":
                "favorite_game",
            "favourite game":
                "favorite_game",
            "favorite movie":
                "favorite_movie",
            "favourite movie":
                "favorite_movie",
            "favorite book":
                "favorite_book",
            "favourite book":
                "favorite_book",
        }

        if normalized in semantic_keys:
            return semantic_keys[normalized]

        return cls._normalize_key(normalized)

    @classmethod
    def _preference_key(cls, value):
        """
        Infer a useful semantic key for common preference statements.
        """

        normalized = value.lower().strip()

        if cls._contains_any(
            normalized,
            [
                "vs code",
                "visual studio code",
                "pycharm",
                "visual studio",
            ],
        ):
            return "preferred_editor"

        if cls._contains_any(
            normalized,
            [
                "python",
                "javascript",
                "typescript",
                "java",
                "c++",
                "c#",
                "rust",
                "go",
            ],
        ):
            return "preferred_programming_language"

        if cls._contains_any(
            normalized,
            [
                "windows",
                "linux",
                "ubuntu",
                "fedora",
                "debian",
                "macos",
            ],
        ):
            return "preferred_operating_system"

        return "preference"

    @classmethod
    def _usage_key(cls, value):
        """
        Infer a semantic key for 'I use X' statements.
        """

        normalized = value.lower().strip()

        if cls._contains_any(
            normalized,
            [
                "vs code",
                "visual studio code",
                "pycharm",
                "visual studio",
            ],
        ):
            return "preferred_editor"

        if cls._contains_any(
            normalized,
            [
                "windows",
                "linux",
                "ubuntu",
                "fedora",
                "debian",
                "macos",
            ],
        ):
            return "preferred_operating_system"

        if cls._contains_any(
            normalized,
            [
                "python",
                "javascript",
                "typescript",
                "java",
                "c++",
                "c#",
                "rust",
                "go",
            ],
        ):
            return "programming_language"

        return "software_or_tool"

    @staticmethod
    def _contains_any(text, values):
        return any(value in text for value in values)

    @staticmethod
    def _normalize_key(text):
        """
        Convert arbitrary memory descriptions into
        safe SQLite-friendly keys.
        """

        text = text.lower().strip()

        text = re.sub(
            r"^(my|the)\s+",
            "",
            text,
        )

        text = re.sub(
            r"[^a-z0-9]+",
            "_",
            text,
        )

        return text.strip("_")

    # =========================================================
    # GENERIC FACT KEY
    # =========================================================

    @staticmethod
    def _generic_fact_key(statement):
        """
        Generate a conservative key for generic facts.

        We intentionally do not attempt full semantic extraction
        here. Ambiguous statements should remain safe rather than
        being incorrectly categorized.
        """

        normalized = statement.lower()

        if "i have " in normalized:
            return "user_has"

        if "i live in " in normalized:
            return "location"

        if "i am from " in normalized:
            return "origin"

        if "my birthday is " in normalized:
            return "birthday"

        if "my age is " in normalized:
            return "age"

        return "user_fact"

    # =========================================================
    # SAFETY
    # =========================================================

    @staticmethod
    def _looks_like_fact(statement):
        """
        Prevent obvious questions from being stored through
        the generic 'remember that...' pattern.
        """

        if statement.endswith("?"):
            return False

        question_patterns = [
            r"^what ",
            r"^who ",
            r"^where ",
            r"^when ",
            r"^why ",
            r"^how ",
            r"^do i ",
            r"^am i ",
            r"^is my ",
            r"^can i ",
        ]

        for pattern in question_patterns:
            if re.match(pattern, statement, re.IGNORECASE):
                return False

        return True