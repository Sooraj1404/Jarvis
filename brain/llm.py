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

    def chat(self, user_input, memories=None):
        memory_context = self._build_memory_context(memories)

        prompt = user_input

        if memory_context:
            prompt = f"""
Relevant information remembered about the user:

{memory_context}

User's current message:
{user_input}
"""

        self.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        try:
            response = ollama.chat(
                model=MODEL,
                messages=self.messages,
                think=False,
            )

            reply = response["message"]["content"]

            self.messages.append(
                {
                    "role": "assistant",
                    "content": reply,
                }
            )

            return reply

        except Exception:
            self.messages.pop()
            raise

    @staticmethod
    def _build_memory_context(memories):
        if not memories:
            return ""

        return "\n".join(
            f"- {key}: {value}"
            for key, value in memories
        )