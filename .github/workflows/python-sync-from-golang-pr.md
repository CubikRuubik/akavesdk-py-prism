---
description: Apply requested Python repository changes based on PR descriptions coming from the dependent Golang workflow and verify the code passes validation.
on:
  pull_request:
    types: [opened, edited, synchronize, reopened]
  workflow_dispatch:
permissions: read-all
tools:
  github:
    toolsets: [default]
timeout-minutes: 40
network:
  allowed:
    - defaults
    - python
safe-outputs:
  push-to-pull-request-branch:
  add-comment:
    max: 1
  noop:
---

# Python Sync From Golang PR

You are an AI coding agent working in this Python repository.

The triggering pull request contains the required change description, produced by automation from the Golang source repository. Your job is to convert that request into concrete Python code updates in this repository.

## Objectives

1. Read and understand the triggering pull request description, title, and relevant discussion context.
2. Apply only the requested Python-side changes in this repository.
3. Verify the updated code passes repository validation.
4. If successful, push the changes directly to the triggering PR branch.

## Implementation Rules

1. Treat the triggering PR body as the source of truth for required changes.
2. Make focused edits in Python-related files, such as `akavesdk/*.py`, `sdk/**/*.py`, `tests/**/*.py`, `pyproject.toml`, and `README.md` only when required by the change.
3. Keep changes minimal and avoid unrelated refactors.
4. If requirements are ambiguous, infer the most conservative implementation and document assumptions in the PR body.

## Validation

Run these checks after making changes:

```bash
python -m compileall src tests
pytest
```

If tests do not exist, still run `python -m compileall src` and report the result.

## Output Behavior

When you finish:

1. If no repository changes are required after analysis, call `noop` with a short explanation.
2. If changes are made but validation fails and you cannot fix the issue confidently:
   - Call `add-comment` on the triggering PR with:
     - What you changed
     - The exact failing check(s)
     - Next action required from maintainers
3. If changes are made and checks pass:
   - Push the changes directly to the triggering PR branch using `push-to-pull-request-branch`.
   - Call `add-comment` on the triggering PR with:
     - A concise summary of implemented changes
   - Validation output summary for `python -m compileall src tests` and `pytest`

## Safety

1. Never introduce secrets or credentials.
2. Do not touch CI or workflow files unless explicitly requested in the PR description.
3. Prefer deterministic commands and reproducible edits.
