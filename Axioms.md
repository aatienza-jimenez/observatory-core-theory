**Title:** OBSERVATORY — Operational Axioms  
**Author:** Alfredo Atienza Jiménez  
**Affiliation:** Independent Researcher — a01.tech  
**Contact:** aaj@a01.tech  
**Project:** OBSERVATORY  
**Version:** v0.2  
**Status:** Stable (Core Foundation)  
**Normative:** YES  
**Layer:** docs/10_core  
**Depends on:** none (foundational document)  
**References:**  
- docs/10_core/Claim_State_Semantics_v0.1.md
- docs/30_model/Epistemic_Model_v0.1.md

**Language:** English (normative reference)  
**Scope:** Epistemic theory of computational evidence  
**License:** CC BY 4.0  
**Change policy:** Core axioms. Modification requires explicit revision of the theory.  

---

# OBSERVATORY — Operational Axioms

This document defines the **axiomatic constraints** governing OBSERVATORY.

These axioms impose epistemic discipline on how system behavior
may be represented, evaluated, and reasoned about through
canonical artifacts.

The axioms do not define a specific model. They define the
epistemic constraints that every admissible model of OBSERVATORY
must satisfy.

The formal model compatible with these axioms is described in:
docs/30_model/Epistemic_Model_v0.1.md

Derived theorems are located in:
docs/50_theorems/

---

# Axiom Categories

The axioms are grouped by their role in theory stability.

## Foundational Axioms

Without these axioms, OBSERVATORY cannot exist.

- A1 — Artifact Supremacy
- A2 — Externality
- A3 — Post-Hoc Reasoning
- A6 — No Inferred Causality
- A11 — Explanation Boundary
- A12 — Explicit Uncertainty

## Structural Axioms

These axioms impose discipline on claim formation and evaluation.

- A4 — Explicit Structure and Invariants
- A5 — Immutable History
- A8 — Claim Discipline

## Reserved Axioms (Future Work)

These axioms are declared but not operationalized in the current version.
They are retained for numbering stability and future development.

- A7 — Reserved (Eliminated — implied by A4 + A6 + A11)
- A9 — Reserved (Artifact-Level Determinism)
- A10 — Reserved (Projection Loss)

Weight MUST NOT be inferred from numbering.

---

# Primitive Terms

The following terms are used as primitives in the axioms.
They are not formally defined within the theory.

- **Run**: a completed execution of a system under observation
- **Event**: a discrete occurrence within a run
- **Provenance**: the declared origin and chain of custody
  of an artifact
- **Closure conditions**: the criteria under which a run's
  artifact set is considered complete

These terms are analogous to undefined primitives in axiomatic
geometry. Their meaning is constrained by the axioms that
reference them.

## Derived Terms

The following terms are defined in terms of the primitives above.

- **Declared closure**: the artifact set that satisfies the
  closure conditions of a run. When a run is closed, its
  declared closure is the complete admissible evidence set.

---

# Definition — Canonical Artifact

A canonical artifact is an immutable record admitted as epistemic
evidence within the declared closure of a run `R`.

An artifact `a` is canonical with respect to a run `R` iff:

1. `a` is included in the declared closure of `R`
2. the provenance of `a` is explicitly declared
3. `a` has not been modified since admission

Canonical artifacts define the **only admissible epistemic evidence**.

Canonical artifacts collectively define the **complete admissible
evidence set** for run `R`.

Canonical artifacts may originate from the observed system or from
the observational framework, provided their provenance is explicitly
recorded.

Canonicality guarantees provenance, not correctness.
Artifacts may be incomplete, contradictory, or ambiguous.

---

# A1 — Artifact Supremacy

Only canonical artifacts constitute admissible epistemic evidence.

Claims may summarize artifacts but MUST NOT introduce evidence
beyond the canonical artifact set.

Any claim relying on interpretation not grounded in artifacts
is invalid.

---

# A2 — Externality

OBSERVATORY operates strictly outside the observed system.

It MUST NOT:
- influence execution
- modify scheduling
- inject events
- alter internal state
- adapt observation based on runtime signals

Observation must never change system behavior.

---

# A3 — Post-Hoc Reasoning

OBSERVATORY reasoning operates only on **closed runs**.

All evaluation and epistemic reasoning occur only after the
run is closed.

A run is considered closed only when its canonical artifact set
is complete with respect to the declared closure conditions
of that run.

Open or streaming executions are outside the scope of the theory.

---

# A4 — Explicit Structure and Invariants

All semantic meaning arises from explicitly declared structure.

Valid semantics must be defined through:
- declared components
- declared relations
- declared invariants

Undeclared structure carries no meaning.

A failure without a declared invariant is epistemically undefined.

---

# A5 — Immutable History

Canonical artifacts form an append-only history.

Corrections or reinterpretations:
- MUST NOT erase prior artifacts
- MUST appear as new artifacts
- MUST preserve historical traceability

---

# A6 — No Inferred Causality

Causality MUST NOT be inferred.

Causal relations may exist only if:
- explicitly declared in structure
- explicitly encoded in artifacts

Temporal order or correlation do not imply causation.

When multiple interpretations remain compatible with canonical
artifacts, they MUST be treated as **epistemically
indistinguishable within the OBSERVATORY theory**.

No interpretation may be preferred without additional artifact
evidence.

---

# A7 — Reserved (Eliminated)

The original A7 attempted to formalize a **rupture detection
principle** for invariant violations.

Subsequent analysis showed that the intended constraint is fully
implied by the combination of:

- A4 — Explicit Structure and Invariants
- A6 — No Inferred Causality
- A11 — Explanation Boundary

Therefore A7 is retained only for numbering stability.
No independent axiom exists at this position.

---

# A8 — Claim Discipline

Every claim evaluated under OBSERVATORY MUST resolve to exactly
one epistemic state. Claims that do not resolve to a state are
invalid.

The admissible epistemic states are defined in:
docs/10_core/Claim_State_Semantics_v0.1.md

A claim is admissible only if it:
- references canonical artifacts (A1)
- references declared structure (A4)
- respects the explanation boundary (A11)

OBSERVATORY reasons only over closed runs that produce canonical
artifacts (A1, A3). A context with no artifacts admits no
evaluable claims — all claims in such a context are UNSUPPORTED
by the first admissibility condition.

---

# A9 — Reserved (Future Work)

A9 defines artifact-level determinism: two runs are deterministically
equivalent iff their canonical artifact sets admit a unique
artifact-preserving isomorphism.

This axiom is not operationalized in the current version of the theory.
No theorem, formalization, or validation document depends on it.

It is retained for numbering stability and future development.
The concept may become relevant when OBSERVATORY addresses
cross-run comparison.

---

# A10 — Reserved (Future Work)

A10 defines projection loss: any projection derived from canonical
artifacts is lossy and must declare its source artifacts,
discarded information, and validity domain.

This axiom is not operationalized in the current version of the theory.
The concept of "projection" as a formal object remains undefined.

It is retained for numbering stability and future development.
The concept may become relevant when OBSERVATORY addresses
derived representations and summaries.

---

# A11 — Explanation Boundary

Explanation MUST stop exactly where artifacts and declared
structure end.

Any explanation requiring:
- hidden state
- missing artifacts
- inferred structure
- invented causal continuation

is epistemically invalid.

Stopping is mandatory.

---

# A12 — Explicit Uncertainty

OBSERVATORY distinguishes four **fundamental epistemic uncertainty
conditions**:

Silence       : no event was expected and none occurred
Absence       : an expected event did not occur
Unknown       : evaluation cannot be performed
Indeterminate : multiple compatible interpretations exist

These categories describe **epistemic uncertainty conditions**,
not claim states.

Claim states are defined separately in:
docs/10_core/Claim_State_Semantics_v0.1.md

They MUST NOT be conflated.

Uncertainty is a first-class epistemic outcome.

---

# Closure

These axioms define the epistemic constraints of OBSERVATORY.

Any model, theorem, or implementation must respect them.

If the axioms cannot be jointly satisfied, the theory is
inconsistent and must be revised.

End of axioms.
