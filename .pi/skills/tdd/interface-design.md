# Interfaces for scientific tests

Make inputs, outputs, and numerical choices explicit. A small interface should not
hide information needed to reproduce or interpret a result.

## Separate computation from I/O

```python
# Load once at the boundary; the computation accepts arrays and settings.
data = load_observations(path)
result = fit_decay(data.time_s, data.concentration, model=model, tolerance=1e-8)
```

Avoid functions that silently read a fixed filename, select a model from environment
variables, plot results, and run a solver in the same call. Test file parsing with a
small real fixture as well as testing the numerical core.

## Define the contract

- Units, array axes, coordinate conventions, and valid input ranges.
- Precision and accepted dtypes when they affect behavior.
- Returned values, uncertainty estimates, and convergence status where applicable.
- Response to missing observations, invalid inputs, or nonconvergence.
- Settings needed for reproducibility, such as solver tolerance and random generator.

Return structured results when several quantities belong together. A test should
not need to inspect a private residual array to learn that a solve failed.

## Keep mutation explicit

An allocating API is not required. For large arrays, a caller-owned output buffer is
a testable public interface. For example, Julia's `mul!(y, A, x)` writes into `y`;
the test owns and checks that buffer. Document aliasing and input mutation rules.

## Pass dependencies at their boundary

Pass file paths, external solver adapters, random generators, or clocks explicitly
when needed. Do not add a substitution argument to every internal math function
solely to mock it. Use meaningful grouped parameters rather than an opaque options
bag or a long list of unexplained scalars.
