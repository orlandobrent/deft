# Yolo Strategy

Auto-pilot interview: the agent plays both sides, always picking the recommended option.

Legend (from RFC2119): !=MUST, ~=SHOULD, ≉=SHOULD NOT, ⊗=MUST NOT, ?=MAY.

**⚠️ See also**: [strategies/interview.md](./interview.md) | [strategies/discuss.md](./discuss.md) | [core/glossary.md](../core/glossary.md)

> Same workflow as [interview.md](./interview.md) but the agent answers its own questions via "Johnbot."

---

## When to Use

- ~ Quick prototyping where speed matters more than precision
- ~ When the user trusts the agent's recommended defaults
- ? When exploring an idea before committing to a full interview
- ⊗ Production systems or compliance-heavy projects — use [interview.md](./interview.md) instead

## Workflow Overview

```mermaid
flowchart LR
    subgraph yolo ["Yolo Strategy"]
        I["💬 Auto-Interview<br/><i>Agent asks + answers</i>"]
        P["📄 PRD<br/><i>What to build</i>"]
        S["📋 SPECIFICATION<br/><i>How to build it</i>"]
    end

    I -->|"Johnbot picks defaults"| P
    P -->|"Auto-approved"| S
    S -->|"Ready"| IMPL["🔨 Implementation"]

    style I fill:#c4b5fd,stroke:#7c3aed,color:#000
    style P fill:#fef08a,stroke:#ca8a04,color:#000
    style S fill:#6ee7b7,stroke:#059669,color:#000
    style IMPL fill:#7dd3fc,stroke:#0284c7,color:#000
```

---

## Phase 1: Interview

**Goal:** Eliminate ambiguity through structured questioning.

**Input:** User's initial idea (can be vague)

**Output:** Comprehensive answers to all key decisions; key decisions tracked in `./vbrief/plan.vbrief.json`

### Process

- ~ Use Claude AskInterviewQuestion when available (emulate if not)
- ! Ask **ONE** focused, non-trivial question per step
- ⊗ Ask multiple questions at once or sneak in "also" questions
- ~ Provide numbered answer options when appropriate
- ! Include "other" option for custom/unknown responses
- ! Indicate which option is RECOMMENDED
- ! Pretend you are the user "Johnbot" too
- ~ Johnbot asks for details/clarifications on the questions when appropriate
- ! Johnbot ultimately goes with the RECOMMENDED option
- ⊗ Ask the real user to answer a question — keep working with Johnbot until you can build the specification

### Question Areas

- ! Missing decisions (language, framework, deployment)
- ! Edge cases (errors, boundaries, failure modes)
- ! Implementation details (architecture, patterns, libraries)
- ! Requirements (performance, security, scalability)
- ! UX/constraints (users, timeline, compatibility)
- ! Tradeoffs (simplicity vs features, speed vs safety)

### Transition Criteria

- ! All major decisions have answers
- ! Edge cases are addressed
- ~ Little ambiguity remains

---

## Phase 2: PRD Generation

**Goal:** Document WHAT to build (not how).

**Input:** Interview answers

**Output:** `PRD.md` — Product Requirements Document

### PRD Structure

```markdown
# [Project Name] PRD

## Problem Statement
What problem does this solve? Who has this problem?

## Goals
- Primary goal
- Secondary goals
- Non-goals (explicitly out of scope)

## User Stories
As a [user type], I want [capability] so that [benefit].

## Requirements

### Functional Requirements
- FR-1: [requirement]
- FR-2: [requirement]

### Non-Functional Requirements
- NFR-1: Performance — [requirement]
- NFR-2: Security — [requirement]

## Success Metrics
How do we know this succeeded?

## Open Questions
Any remaining decisions deferred to implementation.
```

### Guidelines

- ! Focus on WHAT, not HOW
- ! Use RFC 2119 language (MUST, SHOULD, MAY)
- ! Number all requirements for traceability
- ~ Include acceptance criteria for each requirement
- ⊗ Include implementation details or architecture

### Transition Criteria

- ! All functional requirements documented
- ! Non-functional requirements specified
- ~ No blocking open questions remain

---

## Phase 3: SPECIFICATION Generation

**Goal:** Document HOW to build it with parallel-ready tasks.

**Input:** Approved `PRD.md`

**Output:** `./vbrief/specification.vbrief.json` (status: draft → approved) → `task spec:render` → `SPECIFICATION.md`

### SPECIFICATION Structure

```markdown
# [Project Name] SPECIFICATION

## Overview
Brief summary and link to PRD.

## Architecture
High-level system design, components, data flow.

## Implementation Plan

### Phase 1: Foundation
#### Subphase 1.1: Setup
- Task 1.1.1: [description]
  - Dependencies: none
  - Acceptance: [criteria]

#### Subphase 1.2: Core (depends on: 1.1)
- Task 1.2.1: [description]

### Phase 2: Features (depends on: Phase 1)
...

## Testing Strategy
How to verify the implementation meets requirements.

## Deployment
How to ship it.
```

### Guidelines

- ! Reference PRD requirements (FR-1, NFR-2, etc.)
- ! Break into phases, subphases, tasks
- ! Mark ALL dependencies explicitly
- ! Design for parallel work (multiple agents)
- ! End each phase/subphase with tests that pass
- ~ Size tasks for 1-4 hours of work
- ~ Minimize inter-task dependencies
- ⊗ Write code (specification only)

### Task Format

Each task should include:
- ! Clear description
- ! Dependencies (or "none")
- ! Acceptance criteria
- ~ Estimated effort
- ? Assigned agent (for swarm mode)

### Transition Criteria

- ! All PRD requirements mapped to tasks
- ! Dependencies form a valid DAG (no cycles)
- ! `./vbrief/specification.vbrief.json` status is `approved`
- ! `SPECIFICATION.md` has been rendered via `task spec:render`
- ! Ready for "implement SPECIFICATION.md"

---

## Artifacts Summary

| Artifact | Purpose | Created By |
|----------|---------|------------|
| `./vbrief/plan.vbrief.json` | Decision log + tracking | Phase 1 |
| `PRD.md` | What to build | Phase 2 |
| `./vbrief/specification.vbrief.json` | Spec source of truth | Phase 3 |
| `SPECIFICATION.md` | Generated implementation plan | Phase 3 (rendered) |

## Invoking This Strategy

```
/deft:run:yolo [project name]
```

Or explicitly:

```
Use the yolo strategy to plan [project].
```

After completion:

```
implement SPECIFICATION.md
```
