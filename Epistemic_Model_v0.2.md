**Title:** OBSERVATORY — Epistemic Model  
**Author:** Alfredo Atienza Jiménez  
**Affiliation:** Independent Researcher — a01.tech  
**Contact:** aaj@a01.tech  
**Project:** OBSERVATORY  
**Version:** v0.2  
**Status:** Stable  
**Normative:** YES  
**Layer:** docs/30_model  
**Depends on:**  
- docs/10_core/Axioms.md
- docs/10_core/Claim_State_Semantics_v0.1.md

**References:**  
- docs/40_formalization/Axis_1_Historiographic_Formalization_v0.1.md
- docs/40_formalization/Axis_2_Structural_Invariants_Formalization_v0.1.md

**Scope:** Formal epistemic model of OBSERVATORY evaluation  
**Language:** English (normative reference)  
**License:** CC BY 4.0  
**Change policy:** Modifications require explicit revision of the epistemic model.  

---

# OBSERVATORY — Epistemic Model

This document defines the **formal epistemic model** of OBSERVATORY.

The axioms constrain epistemic reasoning but do not themselves
define a mathematical model. This document provides that model.

The model specifies how canonical artifacts and declared structure
determine the epistemic status of claims.

All evaluations performed under OBSERVATORY must conform to
this model.

---

# 1. Core Domains

The epistemic model operates over three primary domains.

## Runs

Let `Run` denote the set of all closed executions.

Each run represents a completed execution of a system under
observation. A run is closed only when its canonical artifacts
satisfy the closure conditions declared for that run (A3).

## Structure

Let `Struct` denote the set of all declared system structures.

A structure defines:
- components
- relations
- invariants
- causal declarations (if any)

Structure is purely declarative. No structure may be inferred
from artifacts (A4).

## Artifacts

Let `Art` denote the set of all canonical artifacts.

Artifacts are immutable records admitted as epistemic evidence
and constitute the only admissible evidence (A1). Each artifact
must satisfy the canonicality conditions defined in Axioms.md:
inclusion in declared closure, explicit provenance, and
non-modification since admission (A5).

For each run `R`, define:

Art(R) ⊆ Art

as the set of canonical artifacts originating from run `R`.

---

# 2. Evaluation Context

All evaluation occurs within a context:

X = (R, S, A)

where

R ∈ Run
S ∈ Struct
A ⊆ Art(R)

such that:
- artifacts in A originate from run R
- structure S is the declared structure applicable to R

The context defines the complete epistemic information available
for evaluation.

---

# 3. Ordering Relations

Let Ord(R) denote the set of all ordering relations over the
events of run `R`, where "event" is a primitive term defined
in Axioms.md.

An ordering relation:
- may be partial
- may contain cycles
- is not required to be linear

OBSERVATORY does not privilege any ordering unless canonical
artifacts explicitly distinguish them.

The formalization of ordering discipline is developed in the
historiographic formalization layer (docs/40_formalization/).

---

# 4. Structural Interpretations

Let Interp(R, S, A) denote the set of all structural
interpretations of run `R` under declared structure `S` that
are not immediately excluded by artifacts `A`.

The artifact parameter `A` scopes which interpretations are
candidates: artifacts determine which components were observed,
which invariants can be checked, and which structural questions
are answerable. Interp(R, S, A) is the full candidate space
before compatibility filtering (sections 5–7). The compatibility
predicate then determines which candidates survive as compatible
worlds.

Interpretations represent possible consistent structural
explanations that respect declared invariants.

Since each artifact can only exclude interpretations (never
introduce new ones), Interp is monotone in the same sense
as Ω: if A ⊆ A′, then Interp(R, S, A′) ⊆ Interp(R, S, A).
This property is used in the monotonicity proof (section 11).

The formalization of structural discipline is developed in the
structural formalization layer (docs/40_formalization/).

---

# 5. Constraints

Canonical artifacts and declared structure impose **constraints**
on which worlds are admissible.

Define the constraint set:

C(X) = C_art(A) ∪ C_struct(S)

where:

- C_art(A) is the set of constraints explicitly encoded in
  canonical artifacts. Each artifact a ∈ A contributes zero
  or more constraints. A constraint from an artifact is an
  explicit assertion recorded in that artifact.

  Constraint extraction decomposes by artifact:

  C_art(A) = ∪_{a ∈ A} C_art({a})

  Each artifact's contribution is determined by that artifact
  alone, independent of what other artifacts are present in A.

- C_struct(S) is the set of constraints declared in structure S.
  These include declared components, relations, invariants,
  and causal declarations.

Each constraint c ∈ C(X) is a predicate over candidate worlds:

c : Ord(R) × Interp(R, S, A) → { satisfied, violated }

The codomain { satisfied, violated } is used for constraints
to distinguish them from claim predicates, which use
{ true, false }. Both are binary; the naming convention
reflects their distinct roles (structural filtering vs.
truth evaluation).

Note on domain: the type signature uses the contextual domain
Ord(R) × Interp(R, S, A) for notational convenience. Each
individual constraint is determined by its source (a single
artifact or a structural declaration) independently of A.
The A-parameterization of the domain reflects the evaluation
context in which the constraint is applied, not a dependency
of the constraint's definition on A.

Constraints are **independently evaluable**: the evaluation
of constraint c on world ω depends only on c and ω, not on
whether other constraints are satisfied or violated.

This independence property is required for Information
Monotonicity (section 11).

## Formalization Boundary

The constraint extraction function C_art — the mapping from
canonical artifacts to formal constraints — is the point where
the model interfaces with external artifact formats.

The model requires that C_art is **deterministic**: given the
same artifact set A, the same constraint set C_art(A) is
produced. This is a requirement on the application of the model,
not a property the model can derive internally.

Observer Invariance (section 12) holds conditional on this
requirement being satisfied.

---

# 6. Compatibility Predicate

A candidate world ω = (o, i) where o ∈ Ord(R) and
i ∈ Interp(R, S, A) is **compatible with context X** iff:

∀ c ∈ C(X) : c(ω) = satisfied

A world is compatible when it satisfies every constraint
imposed by canonical artifacts and declared structure.

Compatibility is determined by the **absence of violation**.
A world is admitted unless a constraint explicitly excludes it.

The compatibility predicate is a **deterministic function**
of ω and X: given the same world and the same context, the
predicate always returns the same result. This determinism
follows from the determinism of C(X) (section 5) and the
deterministic evaluation of each constraint c.

---

# 7. Compatible Worlds

Define the set of compatible worlds:

Ω(X) = { (o, i) ∈ Ord(R) × Interp(R, S, A) | ∀ c ∈ C(X) : c(o, i) = satisfied }

Each compatible world ω ∈ Ω(X) represents a fully specified
interpretation of execution history and structure that satisfies
all constraints from canonical artifacts and declared structure.

OBSERVATORY does not privilege any element of Ω(X) unless
canonical artifacts explicitly distinguish them.

## Evaluation Precondition

Evaluation requires |Ω(X)| ≥ 1.

If Ω(X) = ∅ — because constraints are mutually contradictory
and no candidate world satisfies all of them — evaluation
cannot proceed and claims resolve to UNKNOWN.

This precondition is defined normatively in:
docs/10_core/Claim_State_Semantics_v0.1.md

---

# 8. Claims

A claim begins as a **claim schema**: a structured assertion
referencing artifacts and declared structure, subject to the
admissibility rules of A8 (Claim Discipline).

A claim schema is **admissible** iff it:
- references canonical artifacts (A1)
- references declared structure (A4)
- does not presuppose information beyond the explanation
  boundary at construction time (A11)

A claim schema becomes **evaluable** when:
- the constraint set C(X) can be determined
- the compatible world set Ω(X) can be constructed
- |Ω(X)| ≥ 1

When evaluable, the claim is expressed as a predicate:

φ : Ω(X) → {true, false}

A claim is evaluable as a predicate only if φ is **total**
over Ω(X) — that is, a truth value is defined for every
compatible world.

If φ cannot assign a truth value to some ω ∈ Ω(X), this
means evaluation of the claim exceeds the explanation boundary
for that context, and the claim is classified as UNKNOWN.

---

# 9. Claim Domain and Evaluation Function

Let Claim_X denote the set of all claim schemas in context X,
including both admissible and inadmissible claims.

Define the evaluation function:

Eval_X : Claim_X → Σ

where Σ is the epistemic state set defined in:
docs/10_core/Claim_State_Semantics_v0.1.md

Eval_X maps every claim schema to exactly one epistemic state.
Inadmissible claims map to UNSUPPORTED. Admissible but
non-evaluable claims map to UNKNOWN. Evaluable claims map to
ASSERTED, REJECTED, or INDETERMINATE.

Given a claim φ, the evaluation result is written:

Eval_X(φ)

---

# 10. Evaluation Semantics

## Evaluable Claims

When |Ω(X)| ≥ 1 and φ is admissible and total:

ASSERTED
  iff ∀ ω ∈ Ω(X) : φ(ω) = true

REJECTED
  iff ∀ ω ∈ Ω(X) : φ(ω) = false

INDETERMINATE
  iff ∃ ω₁, ω₂ ∈ Ω(X) such that
  φ(ω₁) = true and φ(ω₂) = false

These three outcomes are mutually exclusive and exhaustive
for any total Boolean predicate over a non-empty set.

## Non-Evaluable Claims

UNKNOWN applies when:
- Ω(X) = ∅ (contradictory constraints)
- Ω(X) cannot be constructed (insufficient information to
  determine the constraint set or the candidate world space)
- φ is admissible but evaluation requires reasoning beyond
  the explanation boundary (A11) at evaluation time

UNSUPPORTED applies when:
- φ violates the admissibility conditions defined in A8:
  references to canonical artifacts (A1), declared
  structure (A4), or the explanation boundary (A11)
- φ is structurally malformed

## Distinguishing A11 violations

A11 (Explanation Boundary) can trigger either UNKNOWN or
UNSUPPORTED depending on when the violation occurs:

- If the claim **presupposes** information beyond the boundary
  in its construction (e.g., asserts a causal chain not
  declared in structure), the claim is **UNSUPPORTED**.

- If the claim is well-constructed but **answering it** would
  require information beyond the boundary (e.g., evaluating φ
  on some ω requires knowledge not in A or S), the claim is
  **UNKNOWN**.

The distinction is between a defective claim and an insufficient
context.

---

# 11. Information Monotonicity

Epistemic refinement may occur only through additional artifacts.

If A ⊆ A′ and the run R and declared structure S remain fixed,
then:

C(X) ⊆ C(X′)

where X = (R, S, A) and X′ = (R, S, A′).

That is, the constraint set can only grow. Each new artifact
may contribute additional constraints but cannot remove
constraints contributed by existing artifacts (A5 — Immutable
History guarantees that existing artifacts are not modified).
The per-artifact decomposition of C_art (section 5) ensures
that A ⊆ A′ implies C_art(A) ⊆ C_art(A′).

Since constraints are independently evaluable (section 5),
a world that satisfies all constraints in C(X′) also
satisfies all constraints in C(X). Therefore:

Ω(X′) ⊆ Ω(X)

Proof:
1. Let ω = (o, i) ∈ Ω(X′).
2. Then ω ∈ Ord(R) × Interp(R, S, A′) and
   ∀ c ∈ C(X′) : c(ω) = satisfied.
3. Since A ⊆ A′, every artifact in A is in A′, so every
   interpretation excluded by A is also excluded by A′.
   Therefore Interp(R, S, A′) ⊆ Interp(R, S, A), and
   i ∈ Interp(R, S, A). Thus ω ∈ Ord(R) × Interp(R, S, A).
4. Since A ⊆ A′, we have C(X) ⊆ C(X′).
5. Therefore ∀ c ∈ C(X) : c(ω) = satisfied.
6. Therefore ω ∈ Ω(X).

## Consequences for Evaluable Claims

Under artifact extension within a fixed context where both
Ω(X) and Ω(X′) are non-empty:
- ASSERTED and REJECTED are stable
- INDETERMINATE may refine to ASSERTED or REJECTED

If Ω(X′) = ∅ while Ω(X) was non-empty, the claim transitions
to UNKNOWN (Evaluation Precondition).

## Stability of Ω(X) = ∅

A direct consequence of monotonicity: if Ω(X) = ∅ and
A ⊆ A′, then Ω(X′) ⊆ ∅, so Ω(X′) = ∅.

The empty world set is **stable under artifact extension**.
Adding constraints cannot restore eliminated worlds. UNKNOWN
arising from Ω(X) = ∅ is therefore stable, like ASSERTED
and REJECTED in the non-empty case.

## Scope

This property applies when Ω(X) is constructible in both
the original and extended contexts.

When Ω(X) transitions from non-constructible to constructible
under artifact extension (because new artifacts make constraint
extraction possible), the result is new evaluation, not
monotonic refinement.

If the evaluation context itself changes (new run R′ or new
declared structure S′), this property does not apply. The claim
must be re-evaluated in the new context.

---

# 12. Observer Invariance

The evaluation result depends only on the context X and the
claim φ.

For any evaluators E₁ and E₂ that:
- operate on the same context X = (R, S, A)
- evaluate the same claim φ
- satisfy all axioms
- apply the same constraint extraction (section 5)

the evaluation function produces identical results:

Eval_X(φ) is unique

This follows from the model's construction:

1. C(X) is determined by X: the constraint set is derived
   from the artifacts A and declared structure S, both of
   which are given. This requires the constraint extraction
   function C_art to be deterministic (section 5,
   Formalization Boundary).
2. The compatibility predicate (section 6) is a deterministic
   function of (ω, C(X)): it checks whether ω satisfies all
   constraints.
3. Therefore Ω(X) is uniquely determined by X.
4. φ is a total predicate over Ω(X).
5. The evaluation semantics (section 10) are a deterministic
   classification of φ's truth distribution over Ω(X).

Each step is deterministic. Therefore the result depends only
on X and φ.

OBSERVATORY evaluations are **observer-independent**.

---

# 13. Indistinguishability Principle

If canonical artifacts do not distinguish between compatible
worlds, OBSERVATORY must not privilege any interpretation.

This principle enforces:

A6 — No Inferred Causality
A11 — Explanation Boundary

---

# 14. Explanation Boundary

Evaluation must respect the explanation boundary defined in A11.

If evaluating φ requires:
- artifacts not present in A
- structure not declared in S
- inferred causal relations

then evaluation must terminate with UNKNOWN.

This applies to claims that are admissible (well-constructed)
but whose evaluation exceeds the available evidence.

---

# Closure

This model defines the **formal semantics of epistemic evaluation**
under OBSERVATORY.

All theorems, formalizations, implementations, and domain profiles
must be compatible with this model.

End of document.
