---
name: suggest-a-skill
description: Figure out whether a repeated need, confusing process, or recurring request should become a skill, executable tool, prompt template, project instruction, or ordinary response. Use when someone says “we keep doing this,” “should we make a helper,” “how do we stop reinventing this,” or asks where a recurring behavior belongs.
---

# Suggest a Skill

Use this skill to classify recurring guidance before designing it. Prefer the smallest reusable mechanism that solves the actual problem.

## Core distinction

- **Skill:** on-demand procedural guidance: instructions, heuristics, checklists, and workflows an agent can apply when relevant. It is loaded or invoked as needed and does not itself perform external side effects.
- **Executable tool:** an executable integration that performs an operation, accesses a system, or produces side effects through a defined interface.
- **Prompt template:** a reusable, user-invoked starting prompt that frames a task or supplies a desired structure; it is not an always-on rule or an external integration.
- **Project instruction:** repository- or project-scoped policy that should apply automatically or consistently within that project.
- **Ordinary response:** a one-off explanation or answer with no meaningful reuse requirement.

## Routing triggers

Use this evaluator when the user says or clearly implies things like:

- “We keep doing this over and over.”
- “Should we make a skill for this?”
- “Should this be a tool, a prompt, or something else?”
- “How do I make this reusable?”
- “I need help deciding where this should live.”
- “This keeps confusing me; can we make a helper or checklist?”

Use this evaluator when any of these occur:

- A user asks to turn repeated advice, a workflow, or a checklist into a reusable asset.
- Guidance may belong in a skill, tool, prompt, project instruction, or response, but the right boundary is unclear.
- A proposed skill includes commands, API calls, file writes, or other behavior that may actually require a tool.
- A rule is specific to one repository or team and may be better as project instruction.
- A request sounds reusable but is really a starting prompt or a one-time answer.

## Decision matrix

| Candidate | Choose it when | Signals it is the wrong choice |
|---|---|---|
| Skill | The value is repeatable reasoning or a procedural workflow that agents apply on demand; inputs and steps are understandable in prose. | It must call a service, mutate state, or run a deterministic operation; it is only project-local policy; it is a one-off answer. |
| Executable tool | The value is an operation, integration, computation, retrieval, or side effect with a callable interface. | The hard part is judgment, sequencing, or human/agent guidance rather than execution. |
| Prompt template | A user should deliberately start similar tasks with reusable framing, context fields, or output constraints. | It must apply automatically, encode a full procedure, or perform actions. |
| Project instruction | The guidance is a standing convention, constraint, or policy for one repository/project and should govern work there. | It is broadly useful across projects or should be user-invoked only. |
| Ordinary response | The request is isolated, low-reuse, or best answered directly without maintaining an artifact. | The same workflow or explanation is likely to recur and benefit from discoverability. |

### Tie-breakers

1. If execution or external side effects are essential, choose a **tool** (possibly with a skill explaining when and how to use it).
2. If the guidance should apply automatically within one project, choose a **project instruction**.
3. If the user should explicitly initiate a familiar task shape, choose a **prompt template**.
4. If agents need reusable, conditional procedure, choose a **skill**.
5. If none of those benefits justify an artifact, give an **ordinary response**.

## Questions to ask

Ask only questions that can change the routing decision:

1. Who invokes this, and should invocation be automatic, agent-selected, or explicitly user-started?
2. Is the value guidance and judgment, or an operation that must execute?
3. Does it need external systems, deterministic computation, file changes, or other side effects?
4. Is it useful across projects, or only inside one repository/team?
5. How often will it recur, and what makes it discoverable at the point of need?
6. What inputs, outputs, failure modes, and permissions are required?
7. Can a short procedure remain accurate, or will it need code and tests?

## Anti-patterns

- Do not make a skill a wrapper around a command or API that belongs in a tool.
- Do not put project-specific policy in a broadly available user-level skill.
- Do not create a skill for a single answer, trivial reminder, or stable fact.
- Do not use a prompt template for rules that must apply without user initiation.
- Do not use project instructions for general guidance needed across unrelated projects.
- Do not split one coherent workflow into many tiny skills without a discoverability benefit.
- Do not hide required inputs, permissions, side effects, or failure handling.
- Do not promise automation when the proposed artifact only supplies prose.

## Minimal skill-design template

When routing to a skill, start with the smallest useful file:

```markdown
---
name: <lowercase-name>
description: <what it does and when to use it>
---

# <Title>

## Use when
- <specific trigger>

## Procedure
1. <inspect or gather required context>
2. <apply the decision or workflow>
3. <produce the expected result>

## Constraints
- <scope, safety, permissions, or escalation rule>

## Output
- <concise, predictable result format>
```

Keep instructions operational and source-discoverable. Add examples or references only when they clarify a recurring decision; avoid speculative sections.

## Concise output format

Return:

```text
Recommendation: <skill | executable tool | prompt template | project instruction | ordinary response>
Why: <one or two sentences tied to invocation, execution, scope, and reuse>
Boundary: <what belongs elsewhere, if applicable>
Next step: <smallest concrete action>
```

If the recommendation is a skill, include its trigger, required inputs, and one-sentence procedure summary. If the evidence is insufficient, state the missing answer and ask the smallest decisive question.
