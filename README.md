**# JARVIS**

\> A local-first, open-source personal AI assistant inspired by JARVIS from Iron Man.

JARVIS is an experimental personal AI assistant being built from the ground up with a focus on \*\*local execution, privacy, modularity, reliability, natural interaction, and zero paid APIs\*\*.

The goal is not to create another chatbot. The goal is to gradually build an assistant that can understand natural language, remember its user, perform computer tasks, and eventually provide a natural voice interface.

\---

**## Current Status**

\*\*Version: V0.3 — Tool / Action System\*\*

JARVIS currently runs locally on a Windows laptop using Ollama and a local Qwen3 1.7B model.

**### Working**

- [x] Local LLM inference
- [x] Ollama integration
- [x] Qwen3 1.7B
- [x] Thinking disabled for faster responses
- [x] Terminal-based conversation
- [x] Conversation context
- [x] JARVIS personality
- [x] SQLite persistent memory
- [x] Store memories
- [x] Recall memories
- [x] Delete memories
- [x] Natural-language memory creation
- [x] Natural-language memory deletion
- [x] Memory persistence across restarts
- [x] Deterministic local memory routing
- [x] Prevention of obvious false memories
- [x] Memory-aware responses
- [x] Semantic memory key refinement
- [x] Memory value normalization
- [x] Natural memory updates
- [x] Duplicate memory detection
- [x] Protected-memory conflict handling
- [x] Confirmation before protected memory updates
- [x] Natural memory confirmations
- [x] Expanded memory reliability testing
- [x] Tool architecture
- [x] Tool registry and manager
- [x] Tool intent routing
- [x] Tool executor
- [x] Application control
- [x] System information
- [x] File and directory operations
- [x] File search and metadata
- [x] Tool permission system
- [x] Destructive-operation confirmation
- [x] Restricted command execution
- [x] Command allowlist
- [x] Tool verification tests
- [x] Permission verification tests
- [x] Command execution verification
- [x] No paid APIs

**### Not Implemented Yet**

- [ ] Web search
- [ ] Web summarization
- [ ] Browser interaction
- [ ] Advanced semantic memory
- [ ] Voice input
- [ ] Voice output
- [ ] Wake word
- [ ] Android companion
- [ ] Vision
- [ ] Smart-home integration
\---

**# Vision**

The long-term goal is to create a personal assistant that feels less like a chatbot and more like a persistent digital companion.

The intended interaction is:

\> \*\*User:\*\* "Jarvis."

\>

\> \*\*JARVIS:\*\* "Yes, Sergeant?"

\>

\> \*\*User:\*\* "What do I have planned today?"

\>

\> \*\*JARVIS:\*\* "You have two items scheduled today. I have also noticed you have been postponing the first one for three days. I thought you might appreciate the reminder."

The system should eventually be capable of:

\- Understanding natural language

\- Remembering useful information

\- Anticipating user needs

\- Performing computer tasks

\- Searching for information

\- Working with files

\- Managing applications

\- Responding through voice

\- Operating from a phone

\- Using vision when useful

\---

**# Design Philosophy**

**## Local First**

The core assistant should run locally whenever practical.

User data should not need to leave the computer simply to have a conversation with JARVIS.

**## No Paid APIs**

The project is designed around freely available and open-source technologies.

Paid APIs should not be required for the core assistant.

**## Modular**

Each major capability should be replaceable without rewriting the entire system.

**## Incremental**

Features are developed and tested one at a time.

Unnecessary frameworks and complexity should not be introduced before the architecture requires them.

**## Reliability Over Flashiness**

A smaller assistant that works reliably is preferred over a feature-rich assistant that frequently fails.

\---

**# Current Architecture**

\`\`\`text

User

 |

 v

JARVIS

 |

 +---- Fast Memory Router ----> SQLite

 |

 +---- Brain ----> Ollama ----> Qwen3 1.7B

 |

 v

Terminal

\`\`\`

The brain and memory are intentionally separate components.

SQLite is the source of truth for persistent memory. The LLM is not treated as the database.

**### Natural Memory Flow**

\`\`\`text

User

  |

  v

Fast Memory Router

  |

  +---- remember ----> SQLite

  |

  +---- forget ------> SQLite

  |

  +---- none --------> Normal Brain

                           |

                           v

                         Qwen

\`\`\`

The memory router uses deterministic rules and regular expressions rather than an LLM. This avoids unnecessary model calls and reduces latency on the current CPU-only hardware.

The router intentionally favors avoiding false memories over attempting to understand every possible phrasing.

\---

**# Memory System**

JARVIS currently supports natural memory operations such as:

\`\`\`text

My favorite programming language is Python.

I prefer VS Code.

I study Computer Engineering.

I work as a software developer.

\`\`\`

The system converts clear patterns into structured memory keys.

Examples:

\`\`\`text

My favorite programming language is Python.

-> favorite\_programming\_language = Python

I prefer VS Code.

-> preferred\_editor = VS Code

I use Windows.

-> preferred\_operating\_system = Windows

I study Computer Engineering.

-> field\_of\_study = Computer Engineering

I work as a software developer.

-> occupation = software developer

\`\`\`

Memory values are normalized to remove unnecessary punctuation, surrounding quotes, repeated whitespace, and unnecessary leading articles in descriptive values.

**### Memory Updates**

Existing memories are updated when a new value is supplied for a key.

For example:

\`\`\`text

My favorite programming language is Python.

My favorite programming language is Rust.

\`\`\`

results in:

\`\`\`text

favorite\_programming\_language = Rust

\`\`\`

The system also detects unchanged values and avoids unnecessary database updates.

**### Conflict Handling**

Some memories are considered more sensitive to silent replacement, including:

\- Name

\- Age

\- Birthday

\- Location

\- Origin

\- Phone

\- Laptop

\- Computer

When one of these memories conflicts with an existing value, JARVIS asks for confirmation before changing it.

Example:

\`\`\`text

JARVIS: Sergeant, I currently have your name recorded as 'John'.

Would you like me to change it to 'Alex'? (yes/no)

\`\`\`

**### Developer Commands**

The original database-style commands are retained for development and debugging:

\`\`\`text

/remember \<key> \<value>

/recall \<key>

/memories

/forget \<key>

/exit

\`\`\`

\---

**# Implemented Versions**

**## V0.1 — Local Brain**

\*\*Status: COMPLETE\*\*

Implemented:

\- Ollama integration

\- Qwen3 1.7B

\- Terminal interface

\- System prompt

\- JARVIS personality

\- Conversation context

\- Thinking disabled

\- Error handling

\- Clean shutdown

\- Honest capability limitations

**## V0.1.1 — Persistent Memory**

\*\*Status: COMPLETE\*\*

Implemented:

\- SQLite database

\- Memory storage

\- Memory retrieval

\- Memory deletion

\- Memory listing

\- Persistent memory across program restarts

**## V0.1.2 — Memory-Aware Brain**

\*\*Status: COMPLETE\*\*

Implemented:

\- Persistent memories supplied to the LLM

\- Natural questions can use stored memories

\- Memory remains separate from conversation history

**## V0.2 — Natural Memory**

\*\*Status: COMPLETE\*\*

Implemented:

\- Natural memory creation

\- Natural memory deletion

\- Persistent memory across restarts

\- Deterministic local memory routing

\- Prevention of obvious false memories

\- Memory-aware responses

**## V0.2.1 — Memory Refinement**

\*\*Status: COMPLETE\*\*

Implemented:

\- Better semantic memory keys

\- Cleaner memory values

\- Natural memory updates

\- Duplicate memory detection

\- Protected-memory conflict handling

\- Confirmation before protected memory updates

\- More natural memory phrasing

\- Expanded reliability testing

Verified behaviors include:

\- Memory creation

\- Memory recall

\- Duplicate detection

\- Memory updates

\- Value normalization

\- Protected conflict rejection

\- Protected conflict acceptance

\- Natural forgetting

\- Question protection

\- Persistence across sessions

\- Memory-aware responses

\---

**## V0.3 — Tool / Action System**

**Status: COMPLETE**

JARVIS now has a controlled local tool system for performing computer actions while preserving explicit permission boundaries.

Implemented capabilities:

- Tool architecture
- Tool registry and manager
- Structured tool commands
- Natural-language intent routing
- Tool executor
- Application control
- System information
- File and directory operations
- File search and metadata
- Tool permission classification
- Destructive-operation confirmation
- Restricted command execution
- Exact command allowlisting
- Safe subprocess execution with `shell=False`
- Dedicated tool and permission verification tests

### Tool Flow

```text
User
 |
 v
JARVIS
 |
 v
Tool Intent Detector
 |
 v
ToolCommand
 |
 v
Tool Executor
 |
 v
Tool Manager
 |
 v
Specific Tool
 |
 v
ToolResult
```

JARVIS does not receive unrestricted system access.

Destructive operations require confirmation, while command execution is restricted to an explicit allowlist.

Current allowed commands:

```text
git status
git branch
git log
python --version
```

V0.3 was verified through dedicated tool, intent, executor, permission, and command tests, along with Python compilation and whitespace validation.

**# Roadmap**

**## V0.3 — Tool / Action System**

Planned capabilities:

\- Open applications

\- Close applications

\- System information

\- File operations

\- Browser operations

\- Safe command execution

\- Tool permission system

\- Tool result handling

Important principle:

\> JARVIS should never receive unrestricted system access.

Tools should be explicitly defined, validated, and controlled.

**## V0.4 — Web and Knowledge**

Potential capabilities:

\- Web search

\- Web summarization

\- Local document search

\- PDF interaction

\- Knowledge retrieval

**## V0.5 — Voice**

Potential stack:

\- Speech-to-text

\- Text-to-speech

\- Wake word

\- Voice activity detection

\- Continuous conversation

**## V0.6 — Android Companion**

Target device:

\- Redmi 10 Prime

Potential functions:

\- Remote microphone

\- Remote speaker

\- Notifications

\- Voice interaction

\- Camera input

\- Local-network communication

The phone should initially act as an interface rather than the main AI processing device.

**## Future**

Potential capabilities:

\- Vision

\- Semantic memory

\- Long-term memory management

\- Proactive assistance

\- Multi-step task planning

\- Computer-use capabilities

\- Cross-device communication

\- Smart-home integration

Smart-home functionality is intentionally postponed until the core assistant is reliable.

\---

**# Technology Stack**

\- Python 3.12.1

\- Ollama

\- Qwen3 1.7B

\- SQLite

\- Terminal interface

\- Python virtual environment

Available but not currently used for memory:

\- \`embeddinggemma\:latest\`

Another installed model:

\- \`sweaterdog/andy-4\:micro-q8\_0\`

Qwen3 4B has been tested but is significantly slower on the current CPU-only configuration.

\---

**# Project Structure**

```text
Jarvis/
|
+-- brain/
|   +-- __init__.py
|   +-- llm.py
|
+-- config/
|   +-- __init__.py
|   +-- settings.py
|
+-- memory/
|   +-- __init__.py
|   +-- memory.py
|   +-- intent.py
|   +-- jarvis_memory.db
|
+-- tools/
|   +-- __init__.py
|   +-- base.py
|   +-- command.py
|   +-- create_directory.py
|   +-- create_file.py
|   +-- delete_directory.py
|   +-- delete_file.py
|   +-- executor.py
|   +-- get_file_info.py
|   +-- intent.py
|   +-- list_files.py
|   +-- manager.py
|   +-- move_file.py
|   +-- open_app.py
|   +-- permissions.py
|   +-- read_file.py
|   +-- rename_file.py
|   +-- result.py
|   +-- run_command.py
|   +-- search_files.py
|   +-- system_info.py
|   +-- write_file.py
|
+-- tests/
|   +-- test_permissions.py
|   +-- test_run_command.py
|   +-- test_tool_executor.py
|   +-- test_tool_intent.py
|   +-- test_tools.py
|
+-- .venv/
|
+-- main.py
+-- requirements.txt
+-- README.md
+-- PROJECT_CONTEXT.md
+-- .gitignore
```

The following should not be committed:

- `.venv/`
- `jarvis_memory.db`
- Other local databases
- Secrets
- Environment files
\---

**# Development Principle**

Every meaningful version should be:

\`\`\`text

Build

  |

  v

Test

  |

  v

Update README

  |

  v

Update PROJECT\_CONTEXT.md

  |

  v

git status

  |

  v

git add .

  |

  v

git commit

  |

  v

git push

\`\`\`

Do not move to the next major feature until the current feature has been tested and works reliably.

\---

**# License**

Open-source project. License details will be finalized as the repository matures.