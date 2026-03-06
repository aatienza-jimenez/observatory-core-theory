**Title:** OBSERVATORY — Global Indistinguishability Theorem  
**Author:** Alfredo Atienza Jiménez  
**Affiliation:** Independent Researcher — a01.tech  
**Contact:** aaj@a01.tech  
**Project:** OBSERVATORY  
**Identifier:** T5  
**Version:** v0.2  
**Status:** Stable  
**Normative:** NO (Derived Theorem)  
**Layer:** docs/50_theorems  
**Depends on:**  
- docs/10_core/Axioms.md
- docs/10_core/Claim_State_Semantics_v0.1.md
- docs/30_model/Epistemic_Model_v0.1.md

**Scope:** Uniqueness of epistemic evaluation under OBSERVATORY axioms  
**Language:** English (normative reference)  
**License:** CC BY 4.0  
**Change policy:** Modifications must remain consistent with the epistemic model.  

---

# Global Indistinguishability Theorem (T5)

This theorem establishes that the evaluation function defined
in the Epistemic Model is the **unique** evaluation function
compatible with the OBSERVATORY axioms.

No alternative evaluation strategy can satisfy the axioms and
produce different results.

---

# 1. Context

Let X = (R, S, A) be an evaluation context as defined in
the Epistemic Model (EM §2).

Let C(X) = C_art(A) ∪ C_struct(S) be the constraint set (EM §5).

Let the compatible world set be:

Ω(X) = { (o, i) ∈ Ord(R) × Interp(R, S, A)
        | ∀ c ∈ C(X) : c(o, i) = satisfied }

as defined in EM §7.

Let Σ = { ASSERTED, REJECTED, UNKNOWN, INDETERMINATE, UNSUPPORTED }
be the epistemic state set defined in CSS.

Let Eval_X : Claim_X → Σ be the evaluation function defined
in EM §9–§10, where Claim_X is the set of all claim schemas
in context X.

---

# 2. Theorem Statement

**Theorem (Evaluation Uniqueness).** Let Eval' : Claim_X → Σ
be any function that:

(a) operates on evaluation contexts X = (R, S, A)
(b) bases its evaluation result on canonical artifact evidence —
    results must be determined by what the artifacts and
    declared structure establish, not by ignoring or
    discarding available evidence (A1)
(c) uses only declared structure for semantic meaning (A4)
(d) does not privilege compatible worlds that artifacts do
    not distinguish (A6)
(e) does not reason beyond artifacts and declared structure (A11)
(f) assigns exactly one state in Σ to every claim (A8)

Then for every claim φ ∈ Claim_X:

Eval'(φ) = Eval_X(φ)

That is, the evaluation function defined in the Epistemic Model
is the unique function satisfying the axioms.

## Note on condition (b)

Condition (b) encodes A1 (Artifact Supremacy) as a **grounding
requirement**: evaluation results must be determined by what
the canonical artifacts establish. This is stronger than merely
requiring that non-artifact evidence is excluded.

A function that ignores all evidence and returns a default
state does not "base its result on canonical artifact evidence"
— it bases its result on a default rule. Such a function
satisfies the weaker reading ("does not use non-artifact
evidence") but not the grounding reading ("result is determined
by what artifacts establish").

The grounding reading is the intended interpretation of A1.
A1 says "Only canonical artifacts constitute admissible epistemic
evidence" — the word "constitute" establishes artifacts as the
evidentiary basis, not merely as an exclusionary filter.

---

# 3. Proof

The proof proceeds by exhaustive case analysis over the
structure of Claim_X. For each claim φ, we show that the
axioms force Eval'(φ) to a single element of Σ, and that
this element is Eval_X(φ).

The epistemic states in Σ are defined normatively in CSS.
Condition (f) references A8, which references CSS for state
definitions. Therefore the semantic content of each state
(what it represents, when it applies) is incorporated into
the conditions via this chain.

## Case 1: φ is inadmissible

φ violates admissibility (A1, A4, or A11 at construction time).

By condition (f), Eval' must assign exactly one state in Σ.

Eval' cannot return ASSERTED, REJECTED, or INDETERMINATE:
these states require evaluating φ over Ω(X), which requires
the claim to be admissible and evaluable. Returning an
evaluable state for a claim that violates A1, A4, or A11
would endorse a conclusion derived from inadmissible
reasoning, contradicting conditions (b), (c), (e).

Eval' cannot return UNKNOWN: UNKNOWN applies to claims that
are admissible but not evaluable (CSS, UNKNOWN definition).
φ is not admissible. Returning UNKNOWN would misrepresent
the claim's status — the failure is in admissibility, not
in evidence insufficiency. A result not grounded in what the
evidence establishes about the claim's status violates
condition (b).

By elimination in Σ: Eval'(φ) = UNSUPPORTED.

This equals Eval_X(φ) (EM §10, UNSUPPORTED). ✓

## Case 2: φ is admissible but not evaluable

φ passes admissibility (A1, A4, A11 at construction) but
evaluation cannot proceed. This occurs when:

(i) Ω(X) = ∅ (contradictory constraints)
(ii) Ω(X) cannot be constructed
(iii) φ cannot be evaluated over Ω(X) (A11 at evaluation time)

By condition (f), Eval' must assign exactly one state.

### Elimination of ASSERTED and REJECTED

For sub-cases (i) and (ii): Ω(X) is empty or does not exist.
No compatible world provides evidence for or against φ.
Returning ASSERTED or REJECTED would assert a conclusion
about φ's truth value that is not established by the artifact
evidence — the artifacts determine the constraint set, and
the constraints eliminate all worlds (or prevent world
construction), but they do not determine φ's truth value.
This violates condition (b).

For sub-case (iii): φ is admissible and Ω(X) exists with
|Ω(X)| ≥ 1, but φ cannot assign truth values to all worlds
(non-total). Returning ASSERTED (requires ∀ω: φ(ω)=true) or
REJECTED (requires ∀ω: φ(ω)=false) would assert a complete
truth distribution that was not established. This violates
condition (e) — reasoning beyond what the evidence supports.

### Elimination of INDETERMINATE

For sub-cases (i) and (ii): INDETERMINATE requires witnesses
ω₁, ω₂ ∈ Ω(X) with φ(ω₁)=true and φ(ω₂)=false. When
Ω(X) = ∅ or is non-constructible, no witnesses exist.

For sub-case (iii): φ is non-total. INDETERMINATE requires
φ(ω₁)=true and φ(ω₂)=false — both values must be defined.
Since φ is non-total, the required truth distribution is not
fully determined. Returning INDETERMINATE would assert a
specific pattern of agreement and disagreement that was not
established by evaluation. This violates condition (e).

### Elimination of UNSUPPORTED

φ is admissible. UNSUPPORTED applies to inadmissible claims.
Returning UNSUPPORTED would misrepresent the claim's
admissibility status, violating condition (b).

By elimination: Eval'(φ) = UNKNOWN.

This equals Eval_X(φ) (EM §10, UNKNOWN). ✓

## Case 3: φ is admissible, evaluable, and total over Ω(X)

|Ω(X)| ≥ 1 and φ : Ω(X) → {true, false} is total.

The truth distribution of φ over Ω(X) falls into exactly
one of three mutually exclusive and exhaustive sub-cases
(CSS, Exhaustiveness):

### Case 3a: ∀ ω ∈ Ω(X) : φ(ω) = true

φ is true in every compatible world.

**Elimination of REJECTED:** The artifact evidence (via Ω(X))
establishes that φ is true in every compatible world.
Returning REJECTED (φ false in all worlds) directly
contradicts what the evidence establishes. Violates
condition (b).

**Elimination of INDETERMINATE:** The evidence establishes
uniform agreement across all compatible worlds. Returning
INDETERMINATE (asserting disagreement) introduces a claim
of disagreement not grounded in the evidence. Violates
conditions (b) and (d) — A6 requires treating indistinguishable
worlds uniformly, and all worlds agree.

**Elimination of UNKNOWN:** The preconditions for evaluation
are fully met: φ is admissible, Ω(X) is constructible,
|Ω(X)| ≥ 1, and φ is total. The artifacts establish a
determinate truth distribution (φ uniformly true). Returning
UNKNOWN claims that evaluation cannot be performed — but
the evidence establishes that it can and has produced a
determinate result. A result that ignores what the artifacts
establish violates condition (b).

**Elimination of UNSUPPORTED:** φ is admissible.

By elimination: Eval'(φ) = ASSERTED.

This equals Eval_X(φ) (EM §10, ASSERTED). ✓

### Case 3b: ∀ ω ∈ Ω(X) : φ(ω) = false

Symmetric to Case 3a.

φ is false in every compatible world. The evidence uniformly
establishes φ as false.

By the same reasoning:
- ASSERTED violates (b): contradicts evidence.
- INDETERMINATE violates (b), (d): claims nonexistent disagreement.
- UNKNOWN violates (b): ignores established evaluability and
  determinate result.
- UNSUPPORTED: φ is admissible.

By elimination: Eval'(φ) = REJECTED.

This equals Eval_X(φ) (EM §10, REJECTED). ✓

### Case 3c: ∃ ω₁, ω₂ ∈ Ω(X) : φ(ω₁) = true and φ(ω₂) = false

Compatible worlds disagree on φ.

**Elimination of ASSERTED:** Returning ASSERTED (φ true in
all worlds) would privilege the true-worlds over the
false-worlds, effectively dismissing ω₂ without artifact
evidence distinguishing it from ω₁. Violates condition (d)
— A6 prohibits privileging compatible worlds not
distinguished by artifacts.

**Elimination of REJECTED:** Symmetric. Would privilege
false-worlds over true-worlds. Violates condition (d).

**Elimination of UNKNOWN:** The preconditions for evaluation
are fully met: φ is admissible, Ω(X) is constructible,
|Ω(X)| ≥ 1, and φ is total. The artifacts establish a
determinate truth distribution (mixed). Returning UNKNOWN
claims that evaluation cannot be performed — but the evidence
establishes that it can. Furthermore, A6 imposes a positive
obligation: compatible worlds "MUST be treated as epistemically
indistinguishable." Returning UNKNOWN means refusing to
acknowledge the disagreement that the evidence establishes —
failing to treat the worlds at all, rather than treating them
as indistinguishable. This violates both condition (b)
(ignoring established evidence) and condition (d) (failing
to treat worlds as A6 requires).

**Elimination of UNSUPPORTED:** φ is admissible.

By elimination: Eval'(φ) = INDETERMINATE.

This equals Eval_X(φ) (EM §10, INDETERMINATE). ✓

## Conclusion

In every case, Eval'(φ) = Eval_X(φ). Since φ was arbitrary,
Eval' = Eval_X.

Therefore Eval_X is the unique evaluation function satisfying
the OBSERVATORY axioms. ∎

---

# 4. Consequence — Maximal Epistemic Resolution

A direct consequence of the uniqueness result:

Canonical artifacts define the **maximal epistemic resolution**
of OBSERVATORY. No evaluation strategy — however sophisticated —
can extract more information from the same evidence than Eval_X.

Any function that claims to distinguish what Eval_X classifies
as INDETERMINATE must either:
- use evidence beyond canonical artifacts (violating A1)
- privilege one compatible world over another (violating A6)
- reason beyond the explanation boundary (violating A11)

The resolution ceiling is set by artifact distinguishability.

---

# 5. Consequence — Observer Invariance

Evaluation Uniqueness strengthens the Observer Invariance
property stated in EM §12.

EM §12 shows that Eval_X is deterministic given the same
context and constraint extraction. T5 goes further: it shows
that even if an evaluator uses a DIFFERENT evaluation strategy
(not Eval_X), the axioms force the same result.

Observer Invariance (EM §12) is conditional on shared C_art.
T5 is conditional on axiom compliance. Together:

Any two evaluators that (a) apply the same constraint extraction
and (b) satisfy the axioms will produce identical results —
regardless of their internal evaluation strategy.

---

# 6. Structural Consequences

From T5 and the Epistemic Model, the following results are
derivable:

**T1 — Collapse Absorbent:** Under fixed evidence, UNKNOWN and
INDETERMINATE are stable. This follows from T5 (uniqueness
under fixed Ω(X)) combined with Information Monotonicity
(EM §11: artifact extension can only shrink Ω(X)).

**T2 — No Narrative Amplification:** Claims that violate
admissibility at construction time are UNSUPPORTED. This
follows directly from T5 Case 1. Note: claims that are
admissible but exceed the explanation boundary at evaluation
time are UNKNOWN (T5 Case 2), not UNSUPPORTED.

**T3 — Relative Completeness:** When |Ω(X)| = 1, every
admissible total claim resolves to ASSERTED or REJECTED.
This follows from T5 Cases 3a/3b: with a single world,
φ is either true or false, and the axioms force the
corresponding state.

---

# 7. Interpretation

T5 shows that OBSERVATORY's evaluation semantics are not a
design choice — they are the **only possible semantics**
compatible with the axioms.

The theory does not merely define how to evaluate claims.
It proves that any evaluation satisfying its epistemic
constraints must produce the same results.

This transforms the five-state system from a specification
into a **necessary consequence** of the axioms.

---

# Closure

The Global Indistinguishability Theorem establishes evaluation
uniqueness as the foundational result of OBSERVATORY.

All epistemic outcomes are forced by the axioms. No alternative
exists within the constraints.

End of theorem.
