# Substitutes, fixtures, and randomness

Use real numerical code in tests of that code. Mocking a PDE solver's physics and
asserting that the wrapper returns the mock's answer does not verify the solver.

## External boundaries

A substitute is useful for a remote service, licensed solver, expensive subprocess,
or scheduler. Test wrapper behavior such as serialization, retries, parsing, and
failure reporting with small fixtures. Also keep a separate integration check
against the real dependency; a substitute can drift from its actual behavior.

```python
# An interface sketch: an external solver is supplied by the caller.
def run_study(problem, solver):
    result = solver.solve(problem)
    if not result.converged:
        raise RuntimeError("external solver did not converge")
    return result
```

Prefer small real files in temporary directories to mocking every file operation.
Do not fetch live datasets in fast tests. Record the source and license of fixtures,
and keep any sensitive experimental data out of the repository.

## Random computations

Pass a random generator; avoid resetting global state inside a library function.
A seed is useful for reproducing a failure within a recorded environment, not a
promise of identical output across environments.

For Monte Carlo or stochastic optimization tests:

- Test deterministic pieces against exact cases first.
- Check statistical quantities with a justified error bound or repeated-seed design.
- Choose and document an acceptable false-failure probability; do not use an
  arbitrary tight threshold on one random run.
- Save the seed, generator, package versions, and settings for failed experiments.

Test time-budget logic with a supplied clock. Treat wall-clock performance as a
benchmark under recorded hardware and workload conditions, not an ordinary unit
test that fails on a slower student's machine.
