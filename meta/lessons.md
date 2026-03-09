# Lessons Learned

<!-- When codifying lessons from repeated corrections, use RFC 2119 keywords:
     MUST, MUST NOT, SHOULD, SHOULD NOT, MAY
     This makes learned patterns enforceable as standards.
     Example: "When X occurs, the agent MUST do Y" or "API calls SHOULD include timeouts" -->

## Context Engineering (2026-03)

**Source:** Anthropic, "Effective Context Engineering for AI Agents"

**Key insight:** Context rot is real — more tokens ≠ better performance. Every low-signal token actively degrades output quality. The goal is the smallest set of high-signal tokens.

**What was added:** `context/` directory with five guides (context.md, working-memory.md, long-horizon.md, tool-design.md, examples.md) covering Write/Select/Compress/Isolate strategies, vBRIEF integration for structured scratchpads and checkpoints, and surgical edits to main.md and REFERENCES.md for integration.
