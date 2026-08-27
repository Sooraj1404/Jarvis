# JARVIS — Project Context

## Project Overview

JARVIS is a local-first, open-source personal AI assistant inspired by JARVIS from Iron Man.

The project is being developed incrementally with a strong focus on:

- Local execution
- Privacy
- No paid APIs
- Modularity
- Reliability
- Natural interaction
- Expandability

The goal is to build a useful personal assistant first and gradually introduce more advanced capabilities.

---

# Developer

Primary developer: Sergeant

Role: Engineering student

---

# Development Hardware

Current development machine:

- Laptop: HP Laptop 14s-fy1xxx
- CPU: AMD Ryzen 7 5700U
- CPU: 8 cores / 16 threads
- RAM: 16 GB
- GPU: AMD Radeon integrated graphics
- OS: Windows 11 Home Single Language
- Architecture: x64
- Python: 3.12.1
- Development environment: Python virtual environment
- Primary development shell: PowerShell

Current free storage is approximately 40 GB.

The system currently performs local LLM inference using CPU.

---

# Secondary Device

Current phone:

- Redmi 10 Prime

The phone is not part of the current implementation.

It is planned as a future companion/remote interface.

---

# Core Design Philosophy

## Local First

The assistant should run locally whenever practical.

User conversations and persistent memories should remain local by default.

## No Paid APIs

The core project should not depend on paid APIs.

Free/open-source technologies should be preferred.

## Modular

Major components should be separated so they can be replaced or improved without rewriting the entire application.

## Incremental

Features should be developed and tested one at a time.

Do not add unnecessary frameworks or complexity before the underlying architecture requires them.

## Reliability Over Flashiness

A smaller assistant that works reliably is preferred over a feature-rich assistant that frequently fails.

---

# JARVIS Personality

JARVIS should maintain the following personality:

- Calm
- Formal
- Fiercely loyal
- Highly attentive
- Anticipatory
- Precise
- Polite
- Subtle dry wit

JARVIS should feel inspired by the original JARVIS without becoming theatrical or constantly roleplaying.

Preferred communication style:

- Concise by default
- Formal but natural
- Polite
- Dry humor used sparingly
- Addresses the user as "Sergeant" when appropriate
- Does not unnecessarily explain simple statements
- Does not repeat information unnecessarily

JARVIS must never claim to have performed an action unless the system actually performed that action.

---

# Current Technology Stack

## Runtime

- Python 3.12.1

## Local LLM Runtime

- Ollama

## Current Model

- Qwen3 1.7B
- Model runs at 100% CPU on current hardware
- Thinking disabled for normal interaction

## Database

- SQLite

## Current Embedding Model

Available but not currently used:

- `embeddinggemma:latest`

## Other Installed Model

Available:

- `sweaterdog/andy-4:micro-q8_0`

## Larger Model Tested

- Qwen3 4B

Qwen3 4B was tested but was significantly slower on the current CPU-only configuration.

---

# Performance Observations

## Qwen3 4B

Approximate observed performance:

- CPU utilization: ~60%
- Memory utilization: ~65%
- Simple coding response: >45 seconds

Conclusion:

Not currently preferred for early JARVIS versions.

## Qwen3 1.7B

With thinking enabled:

- Simple coding response: ~1 minute 40 seconds

With thinking disabled:

- Simple coding response: ~12 seconds
- Very simple response: ~5 seconds

Conclusion:

Qwen3 1.7B is currently the preferred model for the first versions.

---

# Current Architecture

```text
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
```

The brain and memory are intentionally separate components.

SQLite is the source of truth for persistent memory.

The LLM should not be treated as the database.

---

# Project Structure

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

The following should NOT be committed:

- `.venv/`
- `jarvis_memory.db`
- Other local databases
- Secrets
- Environment files

# Implemented Versions

## V0.1 — Local Brain

**Status: COMPLETE**

Implemented:

- Ollama integration
- Qwen3 1.7B
- Terminal interface
- System prompt
- JARVIS personality
- Conversation context
- Thinking disabled
- Error handling
- Clean shutdown
- Honest capability limitations

---

## V0.1.1 — Persistent Memory

**Status: COMPLETE**

Implemented:

- SQLite database
- Memory storage
- Memory retrieval
- Memory deletion
- Memory listing
- Persistent memory across program restarts

Developer commands:

```text
/remember <key> <value>
/recall <key>
/memories
/forget <key>
/exit
```

These commands remain as developer/debugging tools.

---

## V0.1.2 — Memory-Aware Brain

**Status: COMPLETE**

Implemented:

- Persistent memories supplied to the LLM
- Natural questions can use stored memories
- Memory remains separate from conversation history

---

# V0.2 — Natural Memory

**Status: COMPLETE**

Goal:

Allow users to manage memories naturally instead of requiring explicit database-style commands.

Implemented:

- Natural memory creation
- Natural memory deletion
- Persistent memory across restarts
- Deterministic local memory routing
- Prevention of obvious false memories
- Memory-aware responses

The memory router uses deterministic rules and regular expressions rather than an LLM.

This avoids unnecessary LLM calls and reduces latency on the current CPU-only hardware.

The router intentionally favors avoiding false memories over attempting to understand every possible natural-language phrasing.

---

# V0.2 Verification

The following were verified:

1. Natural memory creation
2. Natural memory recall
3. Natural memory deletion
4. General statements do not create obvious memories
5. Questions do not create memories
6. Memory survives complete program restart
7. The assistant can use persistent memories in a new conversation

---

# V0.2 Known Limitations Addressed by V0.2.1

V0.2 had limitations around:

- Generic memory keys
- Unnormalized memory values
- No explicit distinction between new and updated memories
- Silent replacement of certain important memories
- Repetitive confirmation phrasing
- Limited reliability coverage

These were addressed in V0.2.1.

---

# V0.2.1 — Memory Refinement

**Status: COMPLETE**

Goal:

Refine the deterministic natural-memory system without introducing unnecessary frameworks or semantic infrastructure.

## Implemented

### 1. Better Memory Key Generation

Common descriptions are converted into more useful semantic keys.

Examples:

```text
My favorite programming language is Python.
-> favorite_programming_language = Python

I prefer VS Code.
-> preferred_editor = VS Code

I use Windows.
-> preferred_operating_system = Windows

I study Computer Engineering.
-> field_of_study = Computer Engineering

I work as a software developer.
-> occupation = software developer
```

The router remains deterministic and conservative.

### 2. Memory Value Normalization

Memory values now:

- Remove common trailing punctuation
- Remove surrounding quotes
- Normalize repeated whitespace
- Remove unnecessary leading articles such as `a` and `an` from descriptive values

Examples:

```text
Python!!! -> Python
"VS Code" -> VS Code
a software developer -> software developer
```

### 3. Natural Memory Updates

Existing memories are detected before writing.

The system distinguishes:

- New memory
- Existing unchanged memory
- Updated memory

A new value for a normal preference can replace the existing value for that semantic key.

### 4. Duplicate Detection

If a memory already contains the same value, JARVIS avoids performing an unnecessary database update.

### 5. Memory Conflict Handling

Protected memory keys are not silently overwritten.

Current protected categories include:

- name
- age
- birthday
- location
- origin
- phone
- laptop
- computer

When a conflicting value is detected, JARVIS asks for confirmation before updating the memory.

Example:

```text
JARVIS: Sergeant, I currently have your name recorded as 'John'.
Would you like me to change it to 'Alex'? (yes/no)
```

The user can accept or reject the update.

### 6. Natural Memory Phrasing

Memory confirmations now distinguish between:

- New memories
- Existing memories
- Updated memories
- Protected-memory conflicts
- Accepted conflicts
- Rejected conflicts

The wording remains concise and consistent with the JARVIS personality.

---

# V0.2.1 Verification

The following reliability tests were completed successfully:

1. New memory creation
2. Memory recall
3. Duplicate memory detection
4. Natural memory updates
5. Value normalization
6. Protected-memory conflict detection
7. Protected-memory conflict rejection
8. Protected-memory conflict acceptance
9. Natural memory deletion
10. Deleted memory remains absent
11. Questions do not create memories
12. Normal statements do not create obvious memories
13. Memory-aware responses continue to work
14. Persistent memory behavior from V0.2 remains intact

Example verified behavior:

```text
My favorite color is blue.
-> favorite_color = blue

My favorite color is green.
-> favorite_color = green
```

Protected-memory example:

```text
My name is John.
My name is Alex.

JARVIS:
Sergeant, I currently remember your name as 'John'.
Would you like me to update it to 'Alex'? (yes/no)
```

Both acceptance and rejection were verified.

---

# Current Memory Design

The memory system remains intentionally simple:

```text
Natural Language
       |
       v
Deterministic Intent Detector
       |
       +---- remember ----> Memory
       |
       +---- forget ------> Memory
       |
       +---- none --------> Brain
```

No vector database or embedding-based semantic memory has been introduced.

`embeddinggemma:latest` remains available but is not currently used.

---

# V0.2.1 Known Scope Limitations

The deterministic router still intentionally supports a limited set of natural-language patterns.

It is not intended to understand every possible way a user might express a memory.

Advanced semantic memory extraction and semantic memory search remain future work.

The LLM may also generate explanatory content beyond the exact information stored in memory. Improving grounding and memory-aware response behavior can be addressed separately from the deterministic memory router.

---

# V0.3 — Tool / Action System

**Status: COMPLETE**

Goal:

Give JARVIS a controlled ability to perform local computer actions while preserving explicit permission boundaries and deterministic behavior.

V0.3 was intentionally implemented without introducing a heavy agent framework or unrestricted shell access.

## Implemented

### Tool Architecture

A modular tool architecture was introduced using:

- `Tool`
- `ToolResult`
- `ToolCommand`
- `ToolRegistry`
- `ToolManager`
- `ToolExecutor`

Tools are independently implemented and registered with the tool manager.

### Application Control

Implemented:

- Open applications
- Close applications

Natural-language requests can be routed to these tools.

Examples:

```text
Open Notepad
Could you open Notepad?
Please launch Notepad
Close Notepad
```

### System Information

Implemented a system information tool capable of reporting local system information such as:

- Operating system
- OS version
- Computer name
- Architecture
- Python version
- Processor information

### File Operations

Implemented:

- List files and directories
- Read files
- Create files
- Write files
- Delete files
- Rename files
- Move files
- Search files
- Create directories
- Delete directories
- Get file information

The filesystem tools operate through structured `ToolCommand` objects rather than unrestricted shell commands.

### Natural-Language Intent Routing

The deterministic `ToolIntentDetector` converts supported natural-language requests into structured `ToolCommand` objects.

Examples:

```text
Could you open Notepad?
-> open_app

Can you read README.md for me?
-> read_file

Please remove test.txt
-> delete_file

Show me what's in this folder
-> list_files
```

The intent detector remains deliberately conservative.

Unsupported requests are allowed to fall through to the normal LLM conversation path rather than being converted into arbitrary system actions.

### Tool Executor

`ToolExecutor` provides the execution boundary between structured tool commands and `ToolManager`.

Flow:

```text
Natural Language
       |
       v
ToolIntentDetector
       |
       v
ToolCommand
       |
       v
ToolExecutor
       |
       v
ToolManager
       |
       v
Tool
       |
       v
ToolResult
```

### Permission System

A deterministic permission system was introduced.

Current permission levels:

```text
READ
MODIFY
DESTRUCTIVE
```

Current classification:

```text
READ
- system_info
- list_files
- read_file
- search_files
- get_file_info
- run_command

MODIFY
- open_app
- close_app
- create_file
- write_file
- create_directory
- rename_file
- move_file

DESTRUCTIVE
- delete_file
- delete_directory
```

Destructive operations require explicit user confirmation before execution.

Example:

```text
User: Please remove test.txt

JARVIS: Sergeant, 'delete_file' is a destructive operation.
Would you like me to proceed? (yes/no)

User: no

JARVIS: Very well, Sergeant. The operation has been cancelled.
```

If the user confirms, the operation is executed.

### Safe Command Execution

A restricted command execution tool was implemented.

The tool does **not** provide unrestricted shell access.

The current allowlist is:

```text
git status
git branch
git log
python --version
```

Commands are executed using:

```python
subprocess.run(..., shell=False)
```

Additional protections include:

- Exact command allowlisting
- Structured command arguments
- Argument type validation
- Execution timeout
- Return-code handling
- Standard output/error capture
- Rejection of unsupported commands
- Protection against command chaining through the allowlist

Examples:

```text
Run git status
-> allowed

Run python --version
-> allowed

Run del important.txt
-> rejected
```

The command tool is intentionally small and restricted.

Arbitrary PowerShell, `cmd.exe`, command chaining, arbitrary Python execution, package installation, and destructive shell commands are not supported.

### Verification

V0.3 was verified through:

```text
tests.test_tools
tests.test_tool_intent
tests.test_tool_executor
tests.test_permissions
tests.test_run_command
```

Additional verification included:

```text
python -m compileall brain tools tests
git diff --check
```

Real `main.py` testing also verified:

- Natural-language application control
- Natural-language filesystem operations
- Destructive-operation confirmation
- Confirmation rejection
- Confirmation acceptance
- Safe command execution
- Unsupported command rejection
- Normal conversation fallback

## V0.3 Known Scope Limitations

The deterministic `ToolIntentDetector` supports a defined set of natural-language patterns. It does not attempt to understand every possible phrasing.

Command execution is deliberately restricted to a small allowlist.

Browser control has not been implemented.

Advanced computer-use capabilities, arbitrary command execution, multi-step planning, and autonomous actions remain future work.

The permission system currently focuses on the local tool layer and is not intended to replace operating-system security boundaries.

# V0.4 — Web and Knowledge

Potential capabilities:

- Web search
- Web summarization
- Local document search
- PDF interaction
- Knowledge retrieval

---

# V0.5 — Voice

Potential stack:

- Speech-to-text
- Text-to-speech
- Wake word
- Voice activity detection
- Continuous conversation

Voice should be an interface layer rather than part of the core brain.

---

# V0.6 — Android Companion

Target device:

- Redmi 10 Prime

Potential functions:

- Remote microphone
- Remote speaker
- Notifications
- Voice interaction
- Camera input
- Local-network communication

The phone should initially act as an interface rather than the main AI processing device.

---

# Future

Potential capabilities:

- Vision
- Semantic memory
- Long-term memory management
- Proactive assistance
- Multi-step task planning
- Computer-use capabilities
- Cross-device communication
- Smart-home integration

Smart-home functionality is intentionally postponed until the core assistant is reliable.

---

# Important Architectural Decisions

## Decision 1 — Local LLM

Use Ollama for local model execution.

Reason:

- Local
- Simple
- Easy model management
- Python integration
- No paid API required

## Decision 2 — Qwen3 1.7B for Early Versions

Use Qwen3 1.7B initially rather than the larger 4B model.

Reason:

- Current hardware is CPU-bound
- 1.7B is significantly faster
- Sufficient for architecture testing
- Smaller storage footprint

A larger model can be evaluated later.

## Decision 3 — SQLite Before Vector Memory

Use SQLite for initial memory.

Reason:

- Simple
- Reliable
- Local
- Easy to inspect
- Easy to debug
- No unnecessary infrastructure

EmbeddingGemma may be introduced when semantic memory actually becomes necessary.

## Decision 4 — No Heavy Agent Framework Yet

Do not introduce LangChain, LangGraph, CrewAI, or similar frameworks unless the architecture genuinely requires them.

The project should first establish its own simple internal architecture.

## Decision 5 — No GUI Yet

The terminal is the current interface.

GUI development is postponed until the assistant's core behavior is stable.

## Decision 6 — No Voice Yet

Voice is postponed until:

- Brain works
- Memory works
- Tools work
- Natural interaction works

Voice should be an interface layer rather than part of the core brain.

---

# Git Development Strategy

Every meaningful version should be committed.

Preferred workflow:

```text
Build
  |
  v
Test
  |
  v
Update README
  |
  v
Update PROJECT_CONTEXT.md
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
```

Commit messages should describe the actual change.

Examples:

```text
feat: initialize local brain
feat: add persistent memory
feat: add natural memory detection
feat: add tool system
feat: add computer control
feat: add voice interface
```

---

# Current Development Rule

Do not move to the next major feature until the current feature has been tested and works reliably.

The project should grow through verified milestones rather than accumulating untested features.

---

# Current Development Status

**V0.3 — Tool / Action System is complete.**

The current implementation includes:

- Local LLM and persistent memory from V0.1–V0.2.1
- Controlled local tools
- Natural-language tool intent routing
- Tool execution
- Permission boundaries
- Destructive-operation confirmation
- Restricted command execution

The next major milestone is **V0.4 — Web and Knowledge**.

Before beginning V0.4, the V0.3 implementation should be committed and pushed to GitHub with the README and project context synchronized.

The project should continue to follow the same principles:

- Local first
- No paid APIs
- Modular
- Incremental
- Reliability over flashiness
- No unrestricted system access
