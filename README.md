# JARVIS

> A local-first, open-source personal AI assistant inspired by JARVIS from Iron Man.

JARVIS is an experimental personal AI assistant being built from the ground up with a focus on **local execution, privacy, modularity, and zero paid APIs**.

The goal is not to create another chatbot. The goal is to gradually build an assistant that can understand natural language, remember its user, perform computer tasks, and eventually provide a natural voice interface.

---

## Current Status

**Version: V0.1.2 — Memory-Aware Local Brain**

JARVIS currently runs locally on a Windows laptop using a local LLM through Ollama.

### Working

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
- [x] Memory-aware responses
- [x] No paid APIs

### Not Implemented Yet

- [ ] Natural-language memory commands
- [ ] Computer control
- [ ] Tool calling
- [ ] Web search
- [ ] File interaction
- [ ] Voice input
- [ ] Voice output
- [ ] Wake word
- [ ] Android companion
- [ ] Vision
- [ ] Advanced semantic memory
- [ ] Smart-home integration

---

# Vision

The long-term goal is to create a personal assistant that feels less like a chatbot and more like a persistent digital companion.

The intended interaction is:

> **User:** "Jarvis."

> **JARVIS:** "Yes, Sergeant?"

> **User:** "What do I have planned today?"

> **JARVIS:** "You have two items scheduled today. I have also noticed you have been postponing the first one for three days. I thought you might appreciate the reminder."

The system should eventually be capable of:

- Understanding natural language
- Remembering useful information
- Anticipating user needs
- Performing computer tasks
- Searching for information
- Working with files
- Managing applications
- Responding through voice
- Operating from a phone
- Using vision when useful

---

# Design Philosophy

## Local First

The core assistant should run locally whenever practical.

User data should not need to leave the computer simply to have a conversation with JARVIS.

## No Paid APIs

The project is designed around freely available and open-source technologies.

Paid APIs should not be required for the core assistant.

## Modular

Each major capability should be replaceable without rewriting the entire system.

For example:

```text
LLM
 ↓
Memory
 ↓
Tools
 ↓
Voice
 ↓
Android