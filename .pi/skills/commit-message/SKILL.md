---
name: commit-message
description: Drafts a Git commit message in Madison's established repository style from the current diff, then waits for explicit approval before committing staged changes. Use when preparing a commit or when the user asks for a commit message.
---

# Commit message

Prepare a commit message from the repository changes, matching Madison's existing style.

## Style to preserve

Inspect recent history with `git log -8 --pretty=format:'%h%n%s%n%b%n---'` before drafting. The established style is:

- An imperative, sentence-case subject.
- No conventional-commit prefix such as `feat:` or `fix:`.
- End the subject with a period.
- A concise body after a blank line, usually one sentence or two short sentences.
- Write the body in past tense: `Replaced`, `Fixed`, `Simplified`, `Removed`, or similar.
- Use plain, human wording. Avoid unnecessary jargon such as `procedural`, `shock-aligned`, or implementation details unless they are necessary to understand the change.
- The body explains the main change and its purpose without listing every file.
- Preserve technical acronyms such as CFD, GIF, Astro, and Pi in their normal capitalization.

Examples from this repository include:

```text
Redesign the CFD project page and refine site visuals.

Added animated flow and mesh-refinement graphics, proposal PDF access, clearer
CFD verification criteria, and consistent site typography and colors.
```

```text
Improve repository documentation and Pi skill configuration.

Added portfolio README guidance, project instructions for coding agents, and
LaTeX build-file ignore rules.
```

## Workflow

1. Inspect the current state:
   - `git status --short`
   - `git diff --stat`
   - `git diff --cached --stat`
   - `git diff` and, when relevant, `git diff --cached`
   - recent commit history for style
2. Separate staged changes from unstaged or untracked changes. Never silently include changes that are not staged.
3. Draft one best subject and body. Mention the main user-visible or engineering-relevant result, not implementation trivia.
4. Show the proposed message in a copyable block and state whether it describes staged changes, unstaged changes, or both.
5. Ask exactly:

   `Approve this commit message? [y]es / [e]dit / [n]o`

6. Wait for the user's response. Do not run `git commit` before explicit approval.
7. If the user chooses:
   - **yes/approve**: commit only the already staged changes with the approved message. If nothing is staged, explain that the user must stage the intended files first and do not commit.
   - **edit**: ask what they want changed, revise the message, and ask for approval again.
   - **no**: stop without changing files or Git state.

Do not stage files, amend commits, force-push, or rewrite history unless the user separately requests it. After a successful approved commit, report the commit hash and subject.
