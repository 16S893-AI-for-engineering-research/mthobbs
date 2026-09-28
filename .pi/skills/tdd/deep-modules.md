# Small interfaces, substantial implementations

John Ousterhout's *A Philosophy of Software Design* calls a module **deep** when it
hides substantial implementation behind a small, useful interface. Depth is about
reducing what callers must understand, not maximizing lines of code.

For example, `solve_diffusion(mesh, material, boundary_conditions, options)` can hide
assembly and sparse factorization. Callers should not have to orchestrate private
assembly helpers in a particular order.

Scientific assumptions must remain visible. Document the governing equation,
discretization, units, validity limits, and numerical settings. Expose diagnostics
and controls needed to reproduce results. Do not hide a correlation choice or
solver tolerance when it changes the interpretation of the study.

When simplifying a module, ask:

- Can callers express a scientific task without managing internal bookkeeping?
- Are inputs grouped by meaning, with explicit units and conventions?
- Can a small exact case be run through the same interface as a larger study?
- Are lower-level kernels still independently testable where they have a useful
  mathematical contract?

A thin wrapper can be justified at an external boundary. Do not merge independent
physics models merely to reduce the number of exported functions.
