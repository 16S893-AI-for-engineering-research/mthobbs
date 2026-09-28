# Refactoring numerical code

Refactor with relevant tests passing. Change structure in small steps, rerun tests,
and separate changes to the scientific model or numerical method from cleanup.

Useful candidates:

- Extract repeated unit conversions or boundary-condition handling.
- Separate file loading and plotting from numerical kernels.
- Replace unexplained constants with named quantities, units, and provenance.
- Group related parameters in a small type when it makes conventions explicit.
- Replace hidden mutable state with caller-owned inputs and outputs.
- Consolidate wrappers that force callers to know internal execution order.

Do not impose classes on a numerical codebase that works well with functions and
arrays. Do not hide scientific controls merely to shorten a function signature.

Vectorization, parallel reductions, precision changes, and reordered sums can
change floating-point results. Check accuracy, conservation, convergence, and
performance with the agreed tolerances; numerical equivalence is not necessarily
bitwise equality. If the change requires a different accuracy contract, discuss
and document that choice rather than silently relaxing tests.

Keep unrelated improvements out of the patch. Report them separately.
