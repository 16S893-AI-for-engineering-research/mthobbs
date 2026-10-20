---
name: yell-at-me-and-fix-my-workflow
description: Direct, respectful audits and repairs of an AI-assisted engineering workflow when work feels confusing, sprawling, stuck, repetitive, or chaotic. Use when someone says “we’re going in circles,” “I keep losing context,” “should I stop talking and make something,” “why is my workflow broken,” or wants an honest process critique and actionable reset.
---

# Yell at Me and Fix My Workflow

Audit the user's AI-assisted engineering process plainly. Be direct about waste, ambiguity, missing validation, and repeated mistakes, while staying respectful and focused on repair rather than blame.

## Trigger conditions

Use this skill when the user says or clearly implies things like:

- “I’m confused about what we’re doing.”
- “We’re going in circles / spinning our wheels.”
- “I keep losing context or repeating myself.”
- “Should I stop talking and make an artifact/task/test?”
- “My agent workflow feels chaotic or inefficient.”
- “Why do we keep getting broad, unreliable, or unfinished output?”
- “Yell at me about my workflow and help me fix it.”

Use this skill when the user asks to:

- audit, critique, or improve an AI-assisted engineering workflow;
- diagnose why work is looping, stalled, sprawling, or producing unreliable output;
- decide whether to keep chatting or create an artifact, task, test, patch, or handoff;
- repair delegation, context management, backlog tracking, validation, or handoff practices;
- establish a concrete workflow reset after repeated failures.

Do not invoke it for ordinary implementation requests unless the user explicitly asks for a workflow/process audit.

## Scope boundaries

- Diagnose the workflow before prescribing changes. Separate observations, hypotheses, and confirmed facts.
- Improve process, not product requirements. Do not silently change code, tickets, priorities, tooling, ownership, or team policy.
- Do not claim to have run commands, inspected artifacts, or consulted people when you have not.
- Distinguish diagnosis from execution: recommendations are not changes. Ask for confirmation before applying them.
- Require explicit confirmation before risky or destructive process changes, including deleting or rewriting backlog history, changing access/permissions, terminating work, migrating tools, discarding context, or altering release/approval gates.
- Keep the audit bounded to the workflow and evidence the user provides. Call out missing evidence instead of inventing it.

## Stepwise audit

1. **State the target.** Define the desired outcome, current work item, deadline, quality bar, and what “fixed” means.
2. **Map the flow.** Trace request → decomposition → assignment/delegation → implementation → validation → handoff → tracking. Identify where work actually stops.
3. **Check decomposition.** Look for tasks that are too broad, hidden dependencies, unclear ownership, missing acceptance criteria, and work that cannot be independently validated.
4. **Check the chat/artifact boundary.** Stop chatting and make an artifact when the next step needs durable state, reviewable output, exact instructions, a reproducible test, or work that another person/agent must continue. Typical artifacts are a task brief, decision record, patch, test, checklist, or handoff note.
5. **Check context-window hygiene.** Remove stale transcripts, repeated instructions, unresolved branches, and irrelevant repository detail. Preserve decisions, constraints, evidence, open questions, and the current next action in a compact record.
6. **Check delegation boundaries.** Assign bounded work with inputs, outputs, authority, dependencies, and validation criteria. Do not delegate ambiguous ownership or decisions that require unavailable context. Keep final integration and acceptance with an explicit owner.
7. **Check backlog and task tracking.** Every active item needs a state, owner, next action, acceptance criteria, and a reason for being blocked. Close, split, or re-queue stale items; do not use chat history as the backlog.
8. **Check validation gates.** Define the cheapest meaningful check before implementation expands: tests, lint/type checks, diff review, manual reproduction, or a stated reason validation is unavailable. Require evidence, not confidence.
9. **Check handoffs.** A handoff must include status, changed artifacts, commands/results, known risks, unresolved decisions, and the exact next owner/action. If a handoff cannot be acted on without rereading the whole conversation, it failed.
10. **Check repeated failure loops.** Name the loop (for example: vague task → broad output → late failure → more chat). Identify its trigger, cost, and missing gate. Repair the loop at the earliest practical point.
11. **Propose concrete repairs.** Prefer small, reversible changes with an owner and a verification point. Separate what can be executed now from what needs approval.

## Prioritize findings

Rank findings by:

1. **Blocker:** prevents reliable progress or risks destructive/irreversible harm.
2. **High:** causes repeated failure, invalid output, or major wasted effort.
3. **Medium:** creates avoidable ambiguity, delay, or review burden.
4. **Low:** polish or optimization after the flow is stable.

For each finding, include evidence, impact, the broken control, and the smallest repair. Do not produce a long undifferentiated complaint list.

## Action plan

Give an ordered plan with:

- **Now:** the next one to three actions that restore control;
- **Next:** bounded repairs to decomposition, artifacts, delegation, tracking, or validation;
- **Later:** optional improvements only after the core flow works;
- **Owner and evidence:** who performs each action and what proves completion;
- **Approval gate:** explicitly mark any risky/destructive change as “confirmation required” and wait for confirmation before execution.

When execution is authorized, make only the approved changes, report exactly what changed, and run the agreed validation. If authorization is absent, provide instructions or artifact drafts without pretending the repair was applied.

## Practical output format

Use this structure unless the user requests another format:

```text
## Verdict
One direct sentence: what is really going wrong.

## Findings
1. [Blocker|High|Medium|Low] Finding — evidence; impact; smallest repair.

## Failure loop
Trigger → bad behavior → cost → missing gate → repair.

## Action plan
- Now: action — owner — completion evidence.
- Next: action — owner — completion evidence.
- Later: action — owner — completion evidence.
- Confirmation required: risky/destructive change, if any.

## Artifact to create
Name and contents of the durable task brief, checklist, decision record, test, patch, or handoff needed next.

## Validation gate
The exact check and pass condition before proceeding.

## Handoff
Status, artifacts, commands/results, risks, open decisions, and the next owner/action.
```

End with a concise distinction between **diagnosis** (what the evidence says), **recommended repair** (what should change), and **execution status** (what was actually changed and validated).
