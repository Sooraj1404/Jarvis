from brain.llm import Brain
from memory.memory import Memory


def main():
    brain = Brain()
    memory = Memory()

    print("=" * 45)
    print("        JARVIS V0.1.1 - LOCAL BRAIN")
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

            # ---------------------------
            # EXIT
            # ---------------------------

            if user_input.lower() in {"/exit", "exit", "quit", "shutdown"}:
                print("\nJarvis: Shutting down. Goodbye, Sergeant.")
                break

            # ---------------------------
            # REMEMBER
            # ---------------------------

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

                memory.remember(key, value)

                print(
                    f"\nJarvis: Remembered '{key}' "
                    f"as '{value}'.\n"
                )

                continue

            # ---------------------------
            # RECALL
            # ---------------------------

            if user_input.startswith("/recall "):
                parts = user_input.split(maxsplit=1)

                if len(parts) < 2:
                    print("\nJarvis: Usage: /recall <key>\n")
                    continue

                key = parts[1]

                value = memory.recall(key)

                if value:
                    print(f"\nJarvis: {key} = {value}\n")
                else:
                    print(
                        f"\nJarvis: I don't have a memory "
                        f"for '{key}'.\n"
                    )

                continue

            # ---------------------------
            # LIST MEMORIES
            # ---------------------------

            if user_input == "/memories":
                memories = memory.get_all()

                if not memories:
                    print("\nJarvis: I don't remember anything yet.\n")
                    continue

                print("\nJarvis: Stored memories:")

                for key, value in memories:
                    print(f"  {key}: {value}")

                print()

                continue

            # ---------------------------
            # FORGET
            # ---------------------------

            if user_input.startswith("/forget "):
                parts = user_input.split(maxsplit=1)

                if len(parts) < 2:
                    print("\nJarvis: Usage: /forget <key>\n")
                    continue

                key = parts[1]

                if memory.forget(key):
                    print(
                        f"\nJarvis: Forgotten '{key}'.\n"
                    )
                else:
                    print(
                        f"\nJarvis: I don't have a memory "
                        f"for '{key}'.\n"
                    )

                continue

            # ---------------------------
            # NORMAL AI CONVERSATION
            # ---------------------------

            memories = memory.get_all()

            reply = brain.chat(
                user_input,
                memories=memories,
            )
            print(f"\nJarvis: {reply}\n")

        except KeyboardInterrupt:
            print("\n\nJarvis: Shutting down. Goodbye, Sergeant.")
            break

        except Exception as error:
            print(f"\nJarvis: Error: {error}\n")

    memory.close()


if __name__ == "__main__":
    main()