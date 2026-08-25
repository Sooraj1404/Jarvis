import ollama

from config.settings import MODEL, SYSTEM_PROMPT


class Brain:
    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]
    def reset_context(self):
        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]
    def chat(self, user_input, memories=None):
        messages = list(self.messages)

        memory_context = self._build_memory_context(memories)

        if memory_context:
            messages.append(
                {
                    "role": "system",
                    "content": (
                        "CURRENT USER MEMORY:\n"
                        f"{memory_context}\n\n"
                        "Use these memories when relevant. "
                        "Do not invent additional memories."
                    ),
                }
            )

        messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        response = ollama.chat(
            model=MODEL,
            messages=messages,
            think=False,
        )

        reply = response["message"]["content"]

        self.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        self.messages.append(
            {
                "role": "assistant",
                "content": reply,
            }
        )

        return reply

    @staticmethod
    def _build_memory_context(memories):
        if not memories:
            return ""

        return "\n".join(
            f"- {key}: {value}"
            for key, value in memories
        )