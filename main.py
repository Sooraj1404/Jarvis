from brain.llm import Brain
from memory.memory import Memory
from memory.intent import MemoryIntentDetector
from tools.permissions import (
    ToolPermission,
    get_tool_permission,
)

# Memories that should not be silently overwritten.
PROTECTED_MEMORY_KEYS = {
    "name",
    "age",
    "birthday",
    "location",
    "origin",
    "phone",
    "laptop",
    "computer",
}


def format_memory_name(key):
    """
    Convert an internal memory key into natural language.

    Example:
        favorite_programming_language
        -> favorite programming language
    """
    return key.replace("_", " ")


def main():
    brain = Brain()
    memory = Memory()
    intent_detector = MemoryIntentDetector()

    # Pending protected-memory update waiting for confirmation.
    pending_memory_update = None
    pending_tool_command = None

    print("=" * 45)
    print("        JARVIS V0.2 - NATURAL MEMORY")
    print("=" * 45)
    print()
    print("Jarvis: Online, Sergeant.")
    print("Jarvis: Local brain initialized.")
    print("Jarvis: Persistent memory initialized.")
    print()
    print("Commands:")
    print("  /remember <key> <value>")
    print("  /recall <key>")
    print("  /memories")
    print("  /forget <key>")
    print("  /exit")
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # =================================================
            # EXIT
            # =================================================

            if user_input.lower() in {
                "/exit",
                "exit",
                "quit",
                "shutdown",
            }:
                print(
                    "\nJarvis: Shutting down. "
                    "Goodbye, Sergeant."
                )
                break

            # =================================================
            # PENDING MEMORY CONFIRMATION
            # =================================================

            if pending_memory_update is not None:
                answer = user_input.lower().strip()

                if answer in {
                    "yes",
                    "y",
                    "yes please",
                    "do it",
                    "update it",
                    "update",
                }:
                    key = pending_memory_update["key"]
                    value = pending_memory_update["value"]

                    memory.remember(key, value)

                    memory_name = format_memory_name(key)

                    print(
                        f"\nJarvis: Certainly, Sergeant. "
                        f"I've updated your {memory_name} "
                        f"to '{value}'.\n"
                    )

                    pending_memory_update = None
                    continue

                if answer in {
                    "no",
                    "n",
                    "no thanks",
                    "don't",
                    "do not",
                    "leave it",
                }:
                    print(
                        "\nJarvis: Very well, Sergeant. "
                        "I'll leave that memory unchanged.\n"
                    )

                    pending_memory_update = None
                    continue

                print(
                    "\nJarvis: A simple yes or no will suffice, "
                    "Sergeant.\n"
                )
                continue

            # =================================================
            # PENDING TOOL CONFIRMATION
            # =================================================

            if pending_tool_command is not None:
                answer = user_input.lower().strip()

                if answer in {
                    "yes",
                    "y",
                    "yes please",
                    "do it",
                    "proceed",
                    "confirm",
                }:
                    command = pending_tool_command

                    result = brain.tool_executor.execute(
                        command
                    )

                    pending_tool_command = None

                    print(
                        f"\nJarvis: {result.message}\n"
                    )

                    continue

                if answer in {
                    "no",
                    "n",
                    "no thanks",
                    "cancel",
                    "don't",
                    "do not",
                }:
                    pending_tool_command = None

                    print(
                        "\nJarvis: Very well, Sergeant. "
                        "The operation has been cancelled.\n"
                    )

                    continue

                print(
                    "\nJarvis: A simple yes or no will suffice, "
                    "Sergeant.\n"
                )

                continue

            # =================================================
            # REMEMBER COMMAND
            # =================================================

            if user_input.startswith("/remember "):
                parts = user_input.split(maxsplit=2)

                if len(parts) < 3:
                    print(
                        "\nJarvis: Usage: "
                        "/remember <key> <value>\n"
                    )
                    continue

                key = parts[1]
                value = parts[2]

                result = memory.remember(key, value)

                if result == "created":
                    print(
                        f"\nJarvis: Remembered '{key}' "
                        f"as '{value}'.\n"
                    )

                elif result == "updated":
                    print(
                        f"\nJarvis: Updated '{key}' "
                        f"to '{value}'.\n"
                    )

                else:
                    print(
                        f"\nJarvis: I already have "
                        f"'{key}' noted as '{value}'.\n"
                    )

                continue

            # =================================================
            # RECALL COMMAND
            # =================================================

            if user_input.startswith("/recall "):
                parts = user_input.split(maxsplit=1)

                if len(parts) < 2:
                    print(
                        "\nJarvis: Usage: /recall <key>\n"
                    )
                    continue

                key = parts[1]

                value = memory.recall(key)

                if value:
                    print(
                        f"\nJarvis: {key} = {value}\n"
                    )
                else:
                    print(
                        f"\nJarvis: I don't have a memory "
                        f"for '{key}'.\n"
                    )

                continue

            # =================================================
            # LIST MEMORIES
            # =================================================

            if user_input == "/memories":
                memories = memory.get_all()

                if not memories:
                    print(
                        "\nJarvis: I don't remember "
                        "anything yet.\n"
                    )
                    continue

                print("\nJarvis: Stored memories:")

                for key, value in memories:
                    print(f"  {key}: {value}")

                print()

                continue

            # =================================================
            # FORGET COMMAND
            # =================================================

            if user_input.startswith("/forget "):
                parts = user_input.split(maxsplit=1)

                if len(parts) < 2:
                    print(
                        "\nJarvis: Usage: /forget <key>\n"
                    )
                    continue

                key = parts[1]

                if memory.forget(key):
                    brain.reset_context()

                    print(
                        f"\nJarvis: I've forgotten "
                        f"'{key}', Sergeant.\n"
                    )
                else:
                    print(
                        f"\nJarvis: I don't have a memory "
                        f"for '{key}', Sergeant.\n"
                    )

                continue

            # =================================================
            # NATURAL MEMORY DETECTION
            # =================================================

            intent = intent_detector.detect(user_input)

            if intent.get("intent") == "remember":
                key = intent.get("key")
                value = intent.get("value")

                if key and value:

                    existing_value = memory.recall(key)

                    # -----------------------------------------
                    # NEW MEMORY
                    # -----------------------------------------

                    if existing_value is None:
                        memory.remember(key, value)

                        print(
                            "\nJarvis: Understood, Sergeant. "
                            "I'll remember that.\n"
                        )

                        continue

                    # -----------------------------------------
                    # SAME MEMORY
                    # -----------------------------------------

                    if existing_value == value:
                        print(
                            "\nJarvis: I already have that "
                            "noted, Sergeant.\n"
                        )

                        continue

                    # -----------------------------------------
                    # PROTECTED MEMORY CONFLICT
                    # -----------------------------------------

                    if key in PROTECTED_MEMORY_KEYS:
                        pending_memory_update = {
                            "key": key,
                            "value": value,
                        }

                        memory_name = format_memory_name(key)

                        print(
                            f"\nJarvis: Sergeant, I currently "
                            f"have your {memory_name} recorded "
                            f"as '{existing_value}'."
                        )

                        print(
                            f"Would you like me to change it "
                            f"to '{value}'? (yes/no)\n"
                        )

                        continue

                    # -----------------------------------------
                    # SAFE MEMORY UPDATE
                    # -----------------------------------------

                    memory.remember(key, value)

                    print(
                        "\nJarvis: Of course, Sergeant. "
                        "I've updated that memory.\n"
                    )

                    continue

            # =================================================
            # NATURAL FORGET
            # =================================================

            if intent.get("intent") == "forget":
                key = intent.get("key")

                if key and memory.forget(key):
                    brain.reset_context()

                    print(
                        "\nJarvis: Consider it forgotten, "
                        "Sergeant.\n"
                    )
                else:
                    print(
                        "\nJarvis: I don't appear to have that "
                        "in my memory, Sergeant.\n"
                    )

                continue

            # =================================================
            # TOOL REQUEST
            # =================================================

            tool_command = brain.detect_tool_request(
                user_input
            )

            if tool_command is not None:
                permission = get_tool_permission(
                    tool_command.tool
                )

                if permission == ToolPermission.DESTRUCTIVE:
                    pending_tool_command = tool_command

                    print(
                        f"\nJarvis: Sergeant, "
                        f"'{tool_command.tool}' is a "
                        f"destructive operation."
                    )

                    print(
                        "Would you like me to proceed? "
                        "(yes/no)\n"
                    )

                    continue

                tool_result = brain.tool_executor.execute(
                    tool_command
                )

                print(
                    f"\nJarvis: {tool_result.message}\n"
                )

                continue

            # =================================================
            # NORMAL AI CONVERSATION
            # =================================================

            memories = memory.get_all()

            reply = brain.chat(
                user_input,
                memories=memories,
            )

            print(f"\nJarvis: {reply}\n")

        except KeyboardInterrupt:
            print(
                "\n\nJarvis: Shutting down. "
                "Goodbye, Sergeant."
            )
            break

        except Exception as error:
            print(
                f"\nJarvis: I encountered an error: "
                f"{error}\n"
            )

    memory.close()


if __name__ == "__main__":
    main()