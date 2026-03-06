**Title:** OBSERVATORY — Claim State Semantics  
**Author:** Alfredo Atienza Jiménez  
**Affiliation:** Independent Researcher — a01.tech  
**Contact:** aaj@a01.tech  
**Project:** OBSERVATORY  
**Version:** v0.2  
**Status:** Stable  
**Normative:** YES  
**Layer:** docs/10_core  
**Depends on:**  
- docs/10_core/Axioms.md

**References:**  
- docs/30_model/Epistemic_Model_v0.1.md
  (provides the formal model from which refinement properties
  are derived; the definitions in this document are logically
  independent of the model)

**Language:** English (normative reference)  
**Scope:** Epistemic state system for claims  
**License:** CC BY 4.0  
**Change policy:** Modifications require explicit revision of the epistemic model.  

---

# OBSERVATORY — Claim State Semantics

This document defines the **epistemic state system** used by
OBSERVATORY.

Every claim evaluated under OBSERVATORY MUST resolve to exactly
one epistemic state.

These states define the **epistemic outcome space** of the theory.

---

# Epistemic State Set

Let Σ denote the set of admissible epistemic states.

Σ = { ASSERTED, REJECTED, UNKNOWN, INDETERMINATE, UNSUPPORTED }

Each claim MUST resolve to exactly one element of Σ.

## Exhaustiveness

Σ is **exhaustive**: every possible epistemic outcome maps to
exactly one element of Σ. No outcome exists outside this set.

This follows from the model's structure. For an admissible claim
φ over a non-empty compatible world set Ω(X), the predicate
φ : Ω(X) → {true, false} produces exactly three mutually
exclusive outcomes:

- φ is uniformly true → ASSERTED
- φ is uniformly false → REJECTED
- φ is mixed → INDETERMINATE

The remaining two states cover failure modes outside evaluation:

- evaluation cannot proceed → UNKNOWN
- claim is inadmissible → UNSUPPORTED

No sixth state is possible without introducing a third truth
value, partial predicates, or quantitative measures — none of
which the theory admits.

---

# Informational Ordering

OBSERVATORY defines a partial order ≤ over Σ representing
**epistemic refinement potential**.

The covering relations are:

UNSUPPORTED ≤ UNKNOWN
UNSUPPORTED ≤ INDETERMINATE
UNKNOWN ≤ ASSERTED
UNKNOWN ≤ REJECTED
INDETERMINATE ≤ ASSERTED
INDETERMINATE ≤ REJECTED

The relation is reflexive: for every σ ∈ Σ, σ ≤ σ.

The transitive closure includes:
UNSUPPORTED ≤ ASSERTED (via UNKNOWN or INDETERMINATE)
UNSUPPORTED ≤ REJECTED (via UNKNOWN or INDETERMINATE)

UNKNOWN and INDETERMINATE are **incomparable**.
ASSERTED and REJECTED are **maximal and incomparable**.
UNSUPPORTED is the **minimum element**.

```
        ASSERTED    REJECTED
        ↑    ↑      ↑    ↑
        │     \    /     │
        │      \  /      │
     UNKNOWN   INDETERMINATE
        \         /
         \       /
        UNSUPPORTED
```

The six covering relations listed above define the complete
ordering. All four upward paths from the middle tier exist:

- UNKNOWN → ASSERTED
- UNKNOWN → REJECTED
- INDETERMINATE → ASSERTED
- INDETERMINATE → REJECTED

## Ordering Semantics

This ordering describes **refinement potential**, not a single
refinement mechanism. Two distinct processes can move states:

1. **Artifact extension** under fixed context: monotonic
   refinement governed by Information Monotonicity
   (see Refinement Behavior below).

2. **Context change** (new run or new declared structure):
   re-evaluation from scratch, which may move UNSUPPORTED
   claims into evaluable states.

The ordering itself is a static structural property of Σ.
The dynamics of transitions depend on which mechanism applies.

---

# Evaluation Precondition

Evaluation of a claim φ in context X = (R, S, A) requires that
the compatible world set Ω(X) is **non-empty**.

If Ω(X) = ∅ — because constraints from artifacts and declared
structure are mutually contradictory, eliminating all compatible
worlds — then evaluation cannot proceed.

In this case, the claim resolves to **UNKNOWN**.

Rationale: if Ω(X) = ∅, the universal quantifiers in the
definitions of ASSERTED and REJECTED are vacuously satisfied
simultaneously, which is incoherent. The empty case therefore
falls outside constructive evaluation and is classified as
UNKNOWN (evaluation cannot be performed).

---

# Interpretation of States

## ASSERTED

A claim is ASSERTED when the claim predicate evaluates to
**true in every compatible world**.

Formally:

∀ ω ∈ Ω(X) : φ(ω) = true

where |Ω(X)| ≥ 1.

Multiple compatible worlds may exist. ASSERTED does **not require
uniqueness of interpretation**.

---

## REJECTED

A claim is REJECTED when the claim predicate evaluates to
**false in every compatible world**.

Formally:

∀ ω ∈ Ω(X) : φ(ω) = false

where |Ω(X)| ≥ 1.

---

## INDETERMINATE

INDETERMINATE occurs when compatible worlds disagree.

Formally:

∃ ω₁, ω₂ ∈ Ω(X) such that
  φ(ω₁) = true and φ(ω₂) = false

Evaluation is possible, but the evidence does not resolve the
claim uniquely.

---

## UNKNOWN

UNKNOWN occurs when the claim **cannot be evaluated** in the
given context.

This includes:
- Ω(X) = ∅ (contradictory constraints eliminate all
  compatible worlds)
- Ω(X) cannot be constructed (required structure or artifacts
  are missing to the extent that the compatible world set
  cannot be determined)
- evaluation of φ would require reasoning beyond the
  explanation boundary (A11) — that is, the claim is
  admissible but answering it requires information not
  available in the context

In all cases the claim is **admissible but not evaluable**.

---

## UNSUPPORTED

UNSUPPORTED occurs when the claim violates admissibility rules
**at construction time**.

The admissibility conditions are defined in A8: a claim must
reference canonical artifacts (A1), reference declared
structure (A4), and respect the explanation boundary (A11).
Violation of any of these conditions renders the claim
UNSUPPORTED.

UNSUPPORTED claims **do not enter evaluation**.

## Distinguishing UNKNOWN from UNSUPPORTED

Both states represent evaluation failure, but for different
reasons:

- **UNSUPPORTED**: the claim itself is defective. It violates
  admissibility rules regardless of what evidence exists.
  No amount of additional artifacts can fix an inadmissible
  claim.

- **UNKNOWN**: the claim is well-formed and admissible, but
  the available evidence is insufficient to evaluate it, or
  the evidence is contradictory.

The distinction is between a defective claim and an insufficient
context.

---

# Refinement Behavior

## Scope of Monotonicity

Information Monotonicity (Ω(X′) ⊆ Ω(X) when A ⊆ A′) is
established in the Epistemic Model. It applies when Ω(X) is
constructible in both the original and extended contexts.

The following refinement rules apply under artifact extension
within a fixed context (R and S unchanged, A extended to
A′ where A ⊆ A′):

## When both Ω(X) and Ω(X′) are non-empty

The compatible world set can only shrink or remain the same.
Consequently:

- **ASSERTED remains ASSERTED**: φ was true in all worlds;
  removing worlds preserves this.
- **REJECTED remains REJECTED**: φ was false in all worlds;
  removing worlds preserves this.
- **INDETERMINATE may refine to ASSERTED or REJECTED**: if
  the removed worlds eliminate all true-witnesses or all
  false-witnesses.

Refinement moves only **upward** in the informational ordering.
Downward transitions are not possible when both Ω sets are
non-empty.

## When Ω(X′) becomes empty

If artifact extension introduces constraints that eliminate
all remaining compatible worlds (Ω(X′) = ∅ while Ω(X) was
non-empty), the claim transitions to **UNKNOWN** regardless
of its prior evaluable state.

This is a consequence of monotonicity (Ω(X′) ⊆ Ω(X)) combined
with the Evaluation Precondition (Ω = ∅ → UNKNOWN). It is
not a violation of the informational ordering — the "upward
only" guarantee applies when both Ω sets are non-empty.

## When Ω(X) = ∅

The empty world set is **stable under artifact extension**.
By monotonicity: Ω(X′) ⊆ Ω(X) = ∅, so Ω(X′) = ∅. Adding
constraints cannot restore eliminated worlds. UNKNOWN arising
from Ω(X) = ∅ is therefore stable, like ASSERTED and REJECTED
in the non-empty case.

## When Ω(X) is non-constructible

If Ω(X) was non-constructible (constraint extraction could not
be performed) and new artifacts make Ω(X′) constructible, the
claim enters evaluation for the first time. The resulting state
may be any evaluable state (ASSERTED, REJECTED, or
INDETERMINATE) or UNKNOWN (if the newly constructed Ω is empty).
This is **new evaluation**, not monotonic refinement.

## UNSUPPORTED under artifact extension

UNSUPPORTED reflects an admissibility violation at construction
time — the claim itself is defective (A8). Artifact extension
does not change the claim's construction, so UNSUPPORTED
claims generally remain UNSUPPORTED.

However, if a claim references an artifact a₂ ∉ A and artifact
extension adds a₂ to the context (A′ = A ∪ {a₂}), the
admissibility violation may be resolved. In this case the claim
becomes admissible in the extended context and enters evaluation.

This is permissible: the informational ordering allows
UNSUPPORTED to refine to any higher state. The transition is
not monotonic refinement of an evaluation result — it is a
change in admissibility status.

## Context Change

If the evaluation context itself changes (new run R′ or new
declared structure S′), Information Monotonicity does not apply.
The claim must be **re-evaluated from scratch** in the new
context. This is not refinement — it is new evaluation, and
any state may result.

Under context change, a previously UNSUPPORTED claim may become
admissible if the new structure resolves the admissibility
violation.

---

# Relation to Axioms

The claim state system operationalizes the following axioms:

A1 — Artifact Supremacy
A3 — Post-Hoc Reasoning
A4 — Explicit Structure and Invariants
A5 — Immutable History (via stability of ASSERTED/REJECTED
     and via monotonicity's dependence on artifact immutability)
A6 — No Inferred Causality
A8 — Claim Discipline
A11 — Explanation Boundary
A12 — Explicit Uncertainty

## Note on A12

A12 defines four epistemic **uncertainty conditions**: Silence,
Absence, Unknown, Indeterminate.

Two of these conditions share names with claim states (UNKNOWN,
INDETERMINATE). As required by A12, these MUST NOT be conflated.

Uncertainty conditions describe the **nature of epistemic
uncertainty in evidence**. Claim states describe the **outcome
of formal evaluation over compatible worlds**.

A claim may be UNKNOWN for reasons unrelated to the uncertainty
condition "Unknown," and vice versa.

---

# Closure

This state system defines the **epistemic outcome domain** for
all OBSERVATORY evaluations.

All models, theorems, and implementations MUST operate within
this domain.

End of document.
