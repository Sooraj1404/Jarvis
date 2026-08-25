import re


class MemoryIntentDetector:
    """
    Fast, local memory intent detector.

    Uses deterministic patterns instead of an LLM so that
    ordinary conversations do not incur another model call.
    """

    def detect(self, user_input):
        text = user_input.strip()

        if not text:
            return {"intent": "none"}

        # ---------------------------
        # FORGET
        # ---------------------------

        forget_patterns = [
            r"^forget (?:that )?my (.+)$",
            r"^forget (?:my )?(.+)$",
            r"^don't remember (?:my )?(.+)$",
            r"^do not remember (?:my )?(.+)$",
        ]

        for pattern in forget_patterns:
            match = re.match(pattern, text, re.IGNORECASE)

            if match:
                key_text = match.group(1).strip()
                key = self._normalize_key(key_text)

                return {
                    "intent": "forget",
                    "key": key,
                }

        # ---------------------------
        # REMEMBER: "my X is Y"
        # ---------------------------

        match = re.match(
            r"^my (.+?) is (.+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            key_text = match.group(1).strip()
            value = match.group(2).strip()

            return {
                "intent": "remember",
                "key": self._normalize_key(key_text),
                "value": value,
            }

        # ---------------------------
        # REMEMBER: "I prefer X"
        # ---------------------------

        match = re.match(
            r"^i prefer (.+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            value = match.group(1).strip()

            return {
                "intent": "remember",
                "key": "preference",
                "value": value,
            }

        # ---------------------------
        # REMEMBER: "I like X"
        # ---------------------------

        match = re.match(
            r"^i like (.+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            value = match.group(1).strip()

            return {
                "intent": "remember",
                "key": "likes",
                "value": value,
            }

        # ---------------------------
        # REMEMBER: "remember that..."
        # ---------------------------

        match = re.match(
            r"^(?:remember|remember that) (.+)$",
            text,
            re.IGNORECASE,
        )

        if match:
            statement = match.group(1).strip()

            return {
                "intent": "remember",
                "key": "user_fact",
                "value": statement,
            }

        return {"intent": "none"}

    @staticmethod
    def _normalize_key(text):
        text = text.lower().strip()

        text = re.sub(r"^(my|the)\s+", "", text)

        text = re.sub(r"[^a-z0-9]+", "_", text)

        text = text.strip("_")

        return text