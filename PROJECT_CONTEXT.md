\# JARVIS — Project Context



\## Project Overview



JARVIS is a local-first, open-source personal AI assistant inspired by

JARVIS from Iron Man.



The project is being developed incrementally with a strong focus on:



\- Local execution

\- Privacy

\- No paid APIs

\- Modularity

\- Reliability

\- Natural interaction

\- Expandability



The goal is to build a useful personal assistant first and gradually

introduce more advanced capabilities.



\---



\# Developer



Primary developer: Sergeant



Role: Engineering student



\---



\# Development Hardware



Current development machine:



\- Laptop: HP Laptop 14s-fy1xxx

\- CPU: AMD Ryzen 7 5700U

\- CPU: 8 cores / 16 threads

\- RAM: 16 GB

\- GPU: AMD Radeon integrated graphics

\- OS: Windows 11 Home Single Language

\- Architecture: x64

\- Python: 3.12.1

\- Development environment: Python virtual environment

\- Primary development shell: PowerShell



Current free storage is approximately 40 GB.



The system currently performs local LLM inference using CPU.



\---



\# Secondary Device



Current phone:



\- Redmi 10 Prime



The phone is not part of the current implementation.



It is planned as a future companion/remote interface.



\---



\# Core Design Philosophy



\## Local First



The assistant should run locally whenever practical.



User conversations and persistent memories should remain local by default.



\## No Paid APIs



The core project should not depend on paid APIs.



Free/open-source technologies should be preferred.



\## Modular



Major components should be separated so that they can be replaced or

improved without rewriting the entire application.



\## Incremental



Features should be developed and tested one at a time.



Do not add unnecessary frameworks or complexity before the underlying

architecture requires them.



\## Reliability Over Flashiness



A smaller assistant that works reliably is preferred over a feature-rich

assistant that frequently fails.



\---



\# JARVIS Personality



JARVIS should maintain the following personality throughout the project:



\- Calm

\- Formal

\- Fiercely loyal

\- Highly attentive

\- Anticipatory

\- Precise

\- Polite

\- Subtle dry wit



JARVIS should feel inspired by the original JARVIS without becoming

theatrical or constantly roleplaying.



The personality should support usefulness rather than interfere with it.



Preferred communication style:



\- Concise by default

\- Formal but natural

\- Polite

\- Dry humor used sparingly

\- Addresses the user as "Sergeant" when appropriate

\- Does not unnecessarily explain simple statements

\- Does not repeat information unnecessarily



JARVIS must never claim to have performed an action unless the system

actually performed that action.



\---



\# Current Technology Stack



\## Runtime



\- Python 3.12.1



\## Local LLM Runtime



\- Ollama



\## Current Model



\- Qwen3 1.7B

\- Model runs at 100% CPU on current hardware

\- Thinking disabled for normal interaction



\## Database



\- SQLite



\## Current Embedding Model



Available but not currently used:



\- embeddinggemma:latest



\## Other Installed Model



Available:



\- sweaterdog/andy-4:micro-q8\_0



\## Larger Model Tested



\- Qwen3 4B



Qwen3 4B was tested but was significantly slower on the current

CPU-only configuration.



\---



\# Performance Observations



\## Qwen3 4B



Approximate observed performance:



\- CPU utilization: \~60%

\- Memory utilization: \~65%

\- Simple coding response: >45 seconds



Conclusion:



Not currently preferred for JARVIS V0.1.



\## Qwen3 1.7B



With thinking enabled:



\- Simple coding response: \~1 minute 40 seconds



With thinking disabled:



\- Simple coding response: \~12 seconds

\- Very simple response: \~5 seconds



Conclusion:



Qwen3 1.7B is currently the preferred model for the first versions.



\---



\# Current Architecture



Current architecture:



&#x20;   User

&#x20;     |

&#x20;     v

&#x20;   JARVIS

&#x20;     |

&#x20;     +---- Brain ---- Ollama ---- Qwen3 1.7B

&#x20;     |

&#x20;     +---- Memory -- SQLite

&#x20;     |

&#x20;     v

&#x20;   Terminal



The brain and memory are intentionally separate components.



SQLite is the source of truth for persistent memory.



The LLM should not be treated as the database.



\---



\# Project Structure



Current structure:



&#x20;   Jarvis/

&#x20;   |

&#x20;   +-- brain/

&#x20;   |   +-- \_\_init\_\_.py

&#x20;   |   +-- llm.py

&#x20;   |

&#x20;   +-- config/

&#x20;   |   +-- \_\_init\_\_.py

&#x20;   |   +-- settings.py

&#x20;   |

&#x20;   +-- memory/

&#x20;   |   +-- \_\_init\_\_.py

&#x20;   |   +-- memory.py

&#x20;   |   +-- intent.py

&#x20;   |   +-- jarvis\_memory.db

&#x20;   |

&#x20;   +-- tests/

&#x20;   |

&#x20;   +-- .venv/

&#x20;   |

&#x20;   +-- main.py

&#x20;   +-- requirements.txt

&#x20;   +-- README.md

&#x20;   +-- PROJECT\_CONTEXT.md

&#x20;   +-- .gitignore



The following should NOT be committed:



\- .venv/

\- jarvis\_memory.db

\- Other local databases

\- Secrets

\- Environment files



\---



\# Implemented Versions



\## V0.1 — Local Brain



Status: COMPLETE



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



\---



\## V0.1.1 — Persistent Memory



Status: COMPLETE



Implemented:



\- SQLite database

\- Memory storage

\- Memory retrieval

\- Memory deletion

\- Memory listing

\- Persistent memory across program restarts



Developer commands:



&#x20;   /remember <key> <value>

&#x20;   /recall <key>

&#x20;   /memories

&#x20;   /forget <key>

&#x20;   /exit



These commands are currently retained as developer/debugging tools.



\---



\## V0.1.2 — Memory-Aware Brain



Status: COMPLETE



Implemented:



\- Persistent memories supplied to the LLM

\- Natural questions can use stored memories

\- Memory remains separate from conversation history



Example:



&#x20;   User:

&#x20;   What is my favorite language?



&#x20;   JARVIS:

&#x20;   Sergeant, your favorite language is Python.



\---



# V0.2 — Natural Memory

Status: COMPLETE

Goal:

Allow users to manage memories naturally instead of requiring explicit
database-style commands.

Implemented:

- Natural memory creation
- Natural memory deletion
- Persistent memory across restarts
- Deterministic local memory routing
- Prevention of obvious false memories
- Memory-aware responses

Example:

    User:
    My favorite programming language is Python.

    JARVIS:
    Understood, Sergeant. I'll remember that.

And:

    User:
    Forget my favorite programming language.

    JARVIS:
    Consider it forgotten, Sergeant.


# V0.2 Implementation

A deterministic local memory intent detector is used for clear memory
patterns.

Current flow:

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

The memory router uses deterministic rules and regular expressions
rather than an LLM.

This avoids unnecessary LLM calls and reduces latency on the current
CPU-only hardware.

The router intentionally favors avoiding false memories over attempting
to understand every possible natural-language phrasing.

More advanced semantic memory detection may be introduced later if
needed.


# V0.2 Verification

The following tests have been successfully completed:

1. Natural memory creation
2. Natural memory recall
3. Natural memory deletion
4. General statements do not create obvious memories
5. Questions do not create memories
6. Memory survives complete program restart
7. The assistant can use persistent memories in a new conversation

Example verified flow:

    Session 1:

    User:
    My favorite programming language is Python.

    JARVIS:
    Understood, Sergeant. I'll remember that.

    /exit


    Session 2:

    User:
    What is my favorite programming language?

    JARVIS:
    Sergeant, your favorite programming language is Python.


# V0.2 Known Limitations

The current deterministic router only understands a limited set of
natural-language patterns.

For example, clear patterns such as:

    My favorite programming language is Python.
    I prefer VS Code.
    Forget my favorite programming language.

are supported.

More ambiguous statements may not be recognized as memory operations.

Current memory keys also need refinement.

For example:

    I prefer VS Code.

currently produces a generic key such as:

    preference = VS Code

Future versions should infer more useful keys such as:

    preferred_editor = VS Code

Memory value normalization also needs improvement so that punctuation
is not unnecessarily stored as part of values.


# V0.2.1 — Memory Refinement

Status: NEXT

Planned:

- Cleaner memory values
- Better semantic memory keys
- Natural memory updates
- Memory conflict handling
- More natural memory phrasing
- Improved memory confirmation
- Expanded memory reliability tests


# V0.3 — Tool / Action System

Status: PLANNED

Planned capabilities:

- Open applications
- Close applications
- System information
- File operations
- Browser operations
- Safe command execution
- Tool permission system
- Tool result handling

Important principle:

JARVIS must not receive unrestricted system access.

Tools should be explicitly defined, validated, and controlled.


# Current Next Step

Complete V0.2.1 Memory Refinement.

First improve:

1. Memory key generation
2. Memory value cleaning
3. Natural memory updates
4. Memory conflict handling
5. Additional natural-language patterns

After V0.2.1:

- Update README
- Update PROJECT_CONTEXT.md
- Commit the milestone
- Push to GitHub
- Begin V0.3 Tool System



## V0.2.1 — Memory Refinement

Planned:

- [ ] Cleaner memory values
- [ ] Better memory key generation
- [ ] Natural memory updates
- [ ] More natural memory phrasing
- [ ] Improved memory conflict handling
- [ ] Memory confirmation where appropriate
- [ ] Expanded reliability testing

## V0.3 — Tool / Action System

Planned capabilities:

- [ ] Open applications
- [ ] Close applications
- [ ] System information
- [ ] File operations
- [ ] Browser operations
- [ ] Safe command execution
- [ ] Tool permission system
- [ ] Tool result handling

Important principle:

JARVIS should never receive unrestricted system access.

Tools should be explicitly defined, validated, and controlled.



\## V0.4



Web and Knowledge



Potential capabilities:



\- Web search

\- Web summarization

\- Local document search

\- PDF interaction

\- Knowledge retrieval



\---



\## V0.5



Voice



Potential stack:



\- Speech-to-text

\- Text-to-speech

\- Wake word

\- Voice activity detection

\- Continuous conversation



\---



\## V0.6



Android Companion



Target device:



\- Redmi 10 Prime



Potential functions:



\- Remote microphone

\- Remote speaker

\- Notifications

\- Voice interaction

\- Camera input

\- Local-network communication



The phone should initially act as an interface rather than the main

AI processing device.



\---



\## Future



Potential capabilities:



\- Vision

\- Semantic memory

\- Long-term memory management

\- Proactive assistance

\- Multi-step task planning

\- Computer-use capabilities

\- Cross-device communication

\- Smart-home integration



Smart-home functionality is intentionally postponed until the core

assistant is reliable.



\---



\# Important Architectural Decisions



\## Decision 1 — Local LLM



Use Ollama for local model execution.



Reason:



\- Local

\- Simple

\- Easy model management

\- Python integration

\- No paid API required



\---



\## Decision 2 — Qwen3 1.7B for Early Versions



Use Qwen3 1.7B initially rather than the larger 4B model.



Reason:



\- Current hardware is CPU-bound

\- 1.7B is significantly faster

\- Sufficient for architecture testing

\- Smaller storage footprint



A larger model can be evaluated later.



\---



\## Decision 3 — SQLite Before Vector Memory



Use SQLite for initial memory.



Reason:



\- Simple

\- Reliable

\- Local

\- Easy to inspect

\- Easy to debug

\- No unnecessary infrastructure



EmbeddingGemma is available and may be introduced when semantic memory

actually becomes necessary.



\---



\## Decision 4 — No Heavy Agent Framework Yet



Do not introduce LangChain, LangGraph, CrewAI, or similar frameworks

unless the architecture genuinely requires them.



The project should first establish its own simple internal architecture.



\---



\## Decision 5 — No GUI Yet



The terminal is the current interface.



GUI development is postponed until the assistant's core behavior is

stable.



\---



\## Decision 6 — No Voice Yet



Voice is postponed until:



\- Brain works

\- Memory works

\- Tools work

\- Natural interaction works



Voice should be an interface layer rather than part of the core brain.



\---



\# Git Development Strategy



Every meaningful version should be committed.



Preferred workflow:



&#x20;   Build

&#x20;     |

&#x20;     v

&#x20;   Test

&#x20;     |

&#x20;     v

&#x20;   Update README

&#x20;     |

&#x20;     v

&#x20;   Update PROJECT\_CONTEXT.md

&#x20;     |

&#x20;     v

&#x20;   git status

&#x20;     |

&#x20;     v

&#x20;   git add .

&#x20;     |

&#x20;     v

&#x20;   git commit

&#x20;     |

&#x20;     v

&#x20;   git push



Commit messages should describe the actual change.



Examples:



&#x20;   feat: initialize local brain

&#x20;   feat: add persistent memory

&#x20;   feat: add natural memory detection

&#x20;   feat: add tool system

&#x20;   feat: add computer control

&#x20;   feat: add voice interface



\---



\# Current Development Rule



Do not move to the next major feature until the current feature has

been tested and works reliably.



The project should grow through verified milestones rather than

accumulating untested features.



\---



\# Current Next Step



Complete V0.2 Natural Memory.



First verify:



1\. Natural memory creation

2\. Natural memory recall

3\. Natural memory deletion

4\. Normal statements are not incorrectly memorized

5\. Questions do not create memories

6\. Memory survives restart

7\. Performance remains acceptable



After verification:



\- Improve the intent architecture

\- Update README

\- Update this context file

\- Commit V0.2 to Git

\- Push to GitHub

\- Begin V0.3 Tool System



