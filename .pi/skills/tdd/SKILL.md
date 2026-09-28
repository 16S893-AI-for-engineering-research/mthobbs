---
name: tdd
description: Build a scientific or numerical project from scratch, add features, or fix bugs with a test-first red-green-refactor loop. Use for greenfield TDD, test-first development, or numerical integration tests; not as a claim that passing tests validates a scientific model.
license: MIT
---

# Test-driven development for scientific code

Test observable behavior against an independent expectation. A small numerical
kernel is as valid a test boundary as a whole simulation. Use real computations;
NEVER replace the physics under test with mocks.

## Start from what exists

**Existing project:** Read relevant code, tests, terminology, and decision records.
Reuse its language, environment, and test runner. Run the relevant baseline tests
and distinguish pre-existing failures from failures introduced by the work.

**Empty directory or new project:** Agree on the scientific question, the smallest
useful result, language, and computational constraints. Choose a minimal environment
and test runner with the user when unspecified. For example, Python with pytest or
Julia with its built-in `Test` library. Create only the source entry point, dependency
metadata, and test directory needed to run one test; document the test command.
Do not scaffold a framework, plugin system, UI, or full simulation architecture.

For a new numerical method, first identify an analytical case, invariant, or other
independent expectation. If the method is still exploratory, agree on a small
experiment to establish a contract, then begin TDD. Do not fabricate expected
outputs to make an unknown method appear verified.

## Plan a small slice

Ask only about unresolved requirements; do not re-ask for approval of work the user
has already specified. Sketch the first public interface before implementing it.

Identify:

- The public function or workflow to test, including units, shapes, and conventions.
- The expected behavior: an analytical solution, conservation law, limiting case,
  convergence rate, error condition, or independently verified reference.
- Tolerances and their basis: truncation error, roundoff, solver stopping criterion,
  or reference uncertainty. Do not choose them from the failing output.
- A fast test for development and any slower system checks needed before delivery.

Use [tests.md](tests.md) for numerical examples and tolerance selection. Read
[interface-design.md](interface-design.md) when the interface needs design work,
and [mocking.md](mocking.md) when external tools or randomness are involved.

## Red → green → refactor

1. **Red:** Write one focused test and run it. Confirm it fails for the intended
   missing or incorrect behavior, not a broken environment or unrelated import.
   In a greenfield project, an intentional missing API can be the first failure;
   once importable, confirm the behavioral assertion fails before implementing it.
   For a bug, reproduce it before fixing it.
2. **Green:** Implement the smallest scientifically valid change that passes. Do
   not hard-code the fixture, copy the implementation into the expected value,
   weaken the assertion, or increase a tolerance to conceal an error.
3. **Refactor:** With relevant tests passing, improve the code in small steps and
   rerun them. See [refactoring.md](refactoring.md) and [deep-modules.md](deep-modules.md)
   as needed. Keep behavior changes separate from structural changes.
4. Repeat for the next behavior. Do not build a large speculative suite before
   checking that the first test exercises the intended path.

Check units, finite values, boundary conditions, and failure reporting as well as
nominal answers. Array shape and dtype are worth testing when callers depend on
them. Use parameterized cases when they express one behavior across inputs.

## Finish

Run the relevant regression and integration tests. Report commands, results, and
checks not run (for example, a long GPU or cluster job). Keep numerical settings
and reference-data provenance with the tests.

Distinguish **verification** (solving the specified equations correctly),
**validation** (whether the model represents observations for its intended use),
and **regression** (detecting change). Passing a regression test proves neither
verification nor validation. If no independent expectation is available, state that
limit and agree on an exploratory check; do not invent a reference value.
