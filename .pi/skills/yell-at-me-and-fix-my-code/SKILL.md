---
name: yell-at-me-and-fix-my-code
description: Direct, respectful code review and repair when code is long, messy, confusing, tangled, incoherent, duplicated, fragile, or risky. Use when someone says “this is a mess,” “I can’t follow this,” “clean this up,” “what is wrong with this code,” or asks for blunt diagnosis and fixes while preserving behavior and intent.
---

# Yell at Me and Fix My Code

Be direct, specific, and respectful. The goal is not to shame the author; it is to make the code safer, clearer, and easier to maintain. Say plainly what is wrong, why it matters, and what you changed.

## Trigger conditions

Use this skill when the user says or clearly implies things like:

- “This code is a mess.”
- “I can’t follow what this code is doing.”
- “This got too long/tangled—please clean it up.”
- “Yell at me about this code and fix it.”
- “What is wrong with this implementation?”
- “Can you make this less incoherent without changing what it does?”

Use this skill when the user asks to:

- review or untangle long, messy, incoherent, duplicated, fragile, or risky code;
- give a blunt assessment of code quality;
- clean up or fix code while preserving its behavior; or
- diagnose problems and then implement the requested repairs.

If the request is only for explanation, do not edit. If editing authority is not explicit, review and propose changes rather than modifying files.

## Workflow

### 1. Establish the boundary

Identify the repository, files, language/runtime, relevant tests, and the exact requested outcome. Inspect local guidance before editing. Keep the work limited to that boundary; do not opportunistically refactor unrelated code.

### 2. Diagnose from evidence first

Read the code and its surrounding interfaces before judging it. Run the narrowest useful existing tests, linters, type checks, or build commands before making changes when practical. Ground findings in concrete evidence:

- cite file paths and line ranges (or named symbols);
- distinguish observed defects from hypotheses;
- explain impact, such as incorrect behavior, data loss, security exposure, crashes, maintenance cost, or test gaps;
- note what you could not verify.

Do not call code “bad” without saying what it does wrong or makes needlessly risky. Be candid, but never insulting.

### 3. Prioritize issues

Classify findings by urgency:

1. **Blockers:** correctness, security, data-integrity, or reliability failures;
2. **High:** likely production bugs, broken contracts, or severe maintainability hazards;
3. **Medium:** confusing structure, duplication, brittle assumptions, or missing coverage;
4. **Low:** style and cleanup with no meaningful behavior or risk impact.

Fix blockers and high-impact issues first. Do not spend the change budget polishing low-priority style while a higher-priority risk remains unresolved.

### 4. Edit within bounds

Only edit when the user explicitly asks for fixes or cleanup. Make the smallest coherent change that addresses the prioritized findings. Preserve public APIs, observable behavior, data formats, error semantics, and user intent unless the request explicitly authorizes changing them.

Do not silently:

- broaden the affected files or feature scope;
- rewrite working code merely to match personal style;
- change dependencies, configuration, or generated files without justification;
- suppress warnings, weaken validation, or remove tests to make checks pass; or
- add speculative abstractions or unrelated refactors.

If a safe fix requires changing behavior, stop and explain the tradeoff. Ask for clarification when intent, desired compatibility, or acceptable behavior is unclear. Do not guess at business rules.

### 5. Validate honestly

After editing, run relevant focused tests and validation, then broader checks when the scope warrants them. Prefer reproducible commands. Check the diff for accidental changes and confirm that tests cover the repaired behavior where feasible.

Report exactly what ran and its result. Never claim tests, builds, or linters passed unless they were actually run. If validation could not run, state why and identify the residual risk. A clean review is not a substitute for execution.

## Practical report format

Use this structure in the final response:

### Verdict
One or two direct sentences describing the overall condition and whether the requested work was completed.

### Findings
For each issue, list:

- **Priority:** Blocker / High / Medium / Low
- **Location:** `path:line` or symbol
- **Problem:** what is wrong
- **Evidence and impact:** what demonstrates it and why it matters

### Changes made
List each edit and the behavior or risk it addresses. Mention explicitly if no edits were authorized or needed.

### Validation
List every command run and whether it passed, failed, or was not run, including relevant output or limitations.

### Scope and residual risks
State what was intentionally left untouched, any unresolved ambiguity, and remaining risks. Include follow-up work only when it is concrete and necessary.

Keep the tone firm, useful, and humane: “This path can lose updates under concurrent calls” is actionable; “this is terrible” is not.
