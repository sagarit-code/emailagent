# 📧 Email Agent v0.1

An AI-powered **email drafting and sending agent** built with **LangGraph**.  
This project focuses on building a **memory-aware, automated email workflow** instead of manually writing emails with traditional SMTP libraries.

> v0.1 is intentionally **text-only and minimal** — correctness over complexity.

---

## 🚀 What this agent does (v0.1)

- Drafts emails automatically using an LLM
- Uses **LangGraph** for deterministic, debuggable agent workflows
- Sends emails via SMTP after generation
- Keeps logic modular (retrieval, generation, sending)
- Designed to be extended with memory and RAG

---

## 🧠 Why this exists

Traditional email libraries force you to:
- Manually write every email
- Handle formatting logic yourself
- Hard-code workflows

This agent treats email as a **reasoning problem**, not a string problem.

---

## 🧱 Architecture (v0.1)

