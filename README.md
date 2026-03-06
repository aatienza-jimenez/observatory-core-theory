**Title:** OBSERVATORY — Core Theory Deposit (v0.2)  
**Author:** Alfredo Atienza Jiménez  
**Affiliation:** Independent Researcher — a01.tech  
**Contact:** aaj@a01.tech  
**ORCID:** https://orcid.org/0009-0005-1051-2282  
**Project:** OBSERVATORY  
**Date:** March 2026  
**License:** CC BY 4.0  

---

# OBSERVATORY: An Axiomatic Epistemic Framework for Computational Evidence

## Abstract

OBSERVATORY is an axiomatic epistemic framework that determines
what can be reliably asserted about computational system
executions using only the canonical artifacts produced during
those executions.

The framework operates strictly post-hoc on closed runs and
enforces a discipline in which explanations must stop where
artifacts and declared structure end. It does not generate
explanations — it determines which explanations survive
artifact-based scrutiny.

The theory is built on nine operational axioms that constrain
evidence admissibility, claim formation, and epistemic reasoning.
These axioms give rise to a five-state epistemic outcome system
(ASSERTED, REJECTED, UNKNOWN, INDETERMINATE, UNSUPPORTED), a
formal model of compatible worlds determined by artifact
constraints, and an evaluation function that maps claims to
epistemic states.

The central result — the Global Indistinguishability Theorem
(T5) — proves that this evaluation function is the unique
function compatible with the axioms under their intended
grounding interpretation. No alternative evaluation strategy
can satisfy the axioms and produce different results. This
transforms the five-state system from a design choice into
a necessary consequence of the epistemic constraints.

This deposit contains the four theory files of OBSERVATORY
v0.2: the operational axioms, the claim state semantics, the
formal epistemic model, and the uniqueness theorem. Together
they constitute a self-contained axiomatic theory for reasoning
about computational evidence under strict artifact-based
epistemic constraints.

---

## Deposit Contents

This deposit contains four theory files plus this README,
listed in recommended reading order:

1. **Axioms.md** — Operational Axioms (v0.2)
   Nine active axioms defining the epistemic constraints.
   Includes primitive terms, the canonical artifact definition,
   and three reserved axioms for future development.

2. **Claim_State_Semantics_v0.2.md** — Claim State Semantics (v0.2)
   The five-state epistemic outcome system with formal
   definitions, informational ordering, exhaustiveness
   argument, and refinement behavior under artifact extension
   and context change.

3. **Epistemic_Model_v0.2.md** — Epistemic Model (v0.2)
   The formal mathematical model: evaluation contexts,
   constraint sets, compatibility predicate, compatible worlds,
   evaluation function, information monotonicity proof, and
   observer invariance.

4. **T5_Global_Indistinguishability.md** — Global
   Indistinguishability Theorem (v0.2)
   Uniqueness proof: the evaluation function defined in the
   Epistemic Model is the only function satisfying the axioms.
   Full proof by exhaustive case analysis with elimination.

The dependency chain is strictly acyclic:
Axioms → Claim State Semantics → Epistemic Model → T5.

## Note on Internal References

The theory files contain cross-references using internal
project paths (e.g., docs/10_core/, docs/30_model/). These
reflect the project's repository structure. In this deposit,
all files are in a flat directory. Additionally, some
cross-references cite v0.1 filenames for path stability
within the project; the content in this deposit is v0.2
as stated in each file's header.

Some files also reference formalization documents
(docs/40_formalization/) that extend the core theory with
ordering and structural discipline formalizations. These are
part of the broader OBSERVATORY research program but are not
required for the logical chain in this deposit.

---

## Origin and Research Context

OBSERVATORY's axioms were not designed top-down. They were
extracted inductively from constraints that emerged while
building a computational observation system for radio
communications training simulation.

During the development of that system, the author encountered
a recurring problem: the observation framework could produce
conclusions not supported by the evidence it had collected.
Log entries could be reinterpreted, causal chains could be
inferred from temporal correlation, and ambiguity could be
silently resolved by narrative completion.

The axioms formalize the discipline that emerged from resisting
these failures: artifact supremacy (only recorded evidence
counts), no inferred causality (correlation is not causation),
the explanation boundary (stop where evidence stops), and
explicit uncertainty (ambiguity is a legitimate outcome, not
a failure mode).

The formal theory presented here was refined through iterative
stress testing across multiple application domains and
successive revision cycles. The core documents in this deposit
represent the stabilized result of that process.

---

## Scope and Limitations

### What this deposit contains

A self-contained axiomatic theory with a uniqueness theorem.
The four theory files form a closed logical chain: a reader
can follow from axioms to model to proof without external
dependencies.

### What this deposit does not contain

- **Implementation.** The theory defines what a conforming
  evaluation engine must do, but provides no software.
  A reference implementation exists as a separate, unreleased
  artifact and is not part of this deposit.

- **Domain-specific instantiations.** The theory is
  domain-agnostic by design. Applying it to a specific domain
  (e.g., distributed systems, AI evaluation, compliance
  auditing) requires specifying how that domain's artifact
  formats map to the abstract constraint extraction function.
  Such instantiations are the subject of ongoing work.

- **Worked examples against real systems.** The theory operates
  at the formal level. Concrete demonstrations require
  domain-specific artifact mappings not included here.

- **Corollary theorems T1, T2, T3.** These are derivable from
  T5 and the Epistemic Model and are part of the broader
  research program. They are not included in this deposit to
  maintain a minimal, self-contained package.

### Known formal boundaries

The Epistemic Model's constraint extraction function (C_art)
— the mapping from canonical artifacts to formal constraints —
is declared as a **formalization boundary**. The model requires
this function to be deterministic and per-artifact decomposable,
but does not define it for any specific artifact format. This
is analogous to undefined primitives in axiomatic geometry:
the theory constrains what C_art must satisfy without
prescribing how it works. The framework's practical value
depends on future instantiations of C_art for specific domains.

The uniqueness theorem (T5) relies on a grounding interpretation
of Axiom A1 (Artifact Supremacy): evaluation results must be
determined by what artifacts establish, not merely constrained
to not use non-artifact evidence. This interpretation is
explicitly justified in T5's text and is anchored in A1's
own language. Under a weaker reading of A1, the uniqueness
result does not hold. A future revision may elevate the
grounding requirement to an explicit axiom clause.

---

## Instantiation Sketch

To illustrate how the abstract framework connects to concrete
systems, consider a minimal instantiation for structured logs.

**Artifacts:** Each log entry is a canonical artifact. A log
entry records a timestamp, a source component, an event type,
and a payload. The declared closure of a run is the complete
set of log entries between a start marker and an end marker.

**Structure:** The declared structure defines the system's
components, their expected interactions, and any invariants
(e.g., "component A always responds to component B within
100ms of a request"). If causal relations are to be evaluated,
they must be explicitly declared in the structure (A6 — No
Inferred Causality prohibits inferring causality from
temporal correlation or log proximity alone).

**Constraint extraction (C_art):** Each log entry contributes
constraints. For example, the entry "component A emitted event
E at time T" contributes: in any compatible world, component A
emits event E at time T.

The distinction between silence and absence (A12) matters:
if no log entry records an expected event, this is absence
(epistemically significant — an expectation was violated).
If no event was expected and none was recorded, this is
silence (epistemically inert).

**Evaluation:** Given the log entries and declared structure,
the compatible world set Ω(X) is the set of all execution
histories consistent with every logged event and every declared
invariant. A claim like "invariant I held throughout the run"
is evaluated over Ω(X). If all compatible worlds agree, the
claim is ASSERTED or REJECTED. If they disagree, it is
INDETERMINATE. If the logs are insufficient to construct
Ω(X), it is UNKNOWN. A claim referencing undeclared structure
or non-canonical evidence is UNSUPPORTED.

This sketch is illustrative, not normative. Formal
domain-specific instantiations are the subject of ongoing work.

---

## Related Work

OBSERVATORY draws on and contributes to several established
research traditions. The positioning below identifies
structural relationships; it does not claim equivalence with
these traditions.

### Epistemic and Doxastic Logic

The compatible worlds construction Ω(X) is structurally
related to Kripke semantics for epistemic logic (Hintikka 1962;
Fagin, Halpern, Moses & Vardi 1995), where an agent's knowledge
is defined by what holds across all accessible worlds.
OBSERVATORY's key departure: the accessibility relation is
determined by artifact constraints rather than agent
capabilities, shifting the framework from reasoning about what
agents know to reasoning about what evidence establishes.

### Belnap's Four-Valued Logic

Belnap's FOUR logic (1977) uses four truth values — True,
False, Both, Neither — designed for databases with potentially
contradictory or incomplete information. OBSERVATORY's
five-state system addresses a related problem: ASSERTED and
REJECTED correspond to True and False; INDETERMINATE captures
a form of evidential conflict (structurally related to Both);
UNKNOWN captures evidential insufficiency (related to Neither);
and UNSUPPORTED adds an admissibility layer with no direct
Belnap equivalent. The relationship is structural, not
formal — the two systems operate over different domains and
with different semantics.

### Runtime Verification

Runtime verification evaluates formal properties against
execution traces (Leucker & Schallhart 2009; Bartocci et al.
2018). OBSERVATORY addresses a related but distinct question:
rather than specifying how to monitor systems, it characterizes
the epistemic limits of what can be concluded from observations
under its axioms. The framework is positioned as an epistemic
discipline for trace-based reasoning, not as a replacement
for existing monitoring approaches.

### Constructive Empiricism

OBSERVATORY's insistence that evidence is what artifacts
record, not what can be inferred, echoes themes in the
constructive empiricism of van Fraassen (1980). The Explanation
Boundary axiom (A11) enforces a strict form of evidential
adequacy: the theory refuses to assert beyond what the evidence
directly supports. The connection is thematic rather than
structural — the two frameworks address different domains.

### Formal Measurement Theory

The treatment of canonical artifacts as the sole evidentiary
basis, with explicit provenance and immutability requirements,
parallels foundational concerns in measurement theory
(Suppes 1962) regarding the conditions under which observations
constitute reliable evidence.

---

## Acknowledgments

This work was developed independently without external funding.
The OBSERVATORY research program is conducted under the
affiliation of a01.tech.

---

## Citation

If you use or reference this work, please cite:

Atienza Jiménez, A. (2026). OBSERVATORY: An Axiomatic Epistemic
Framework for Computational Evidence — Core Theory (v0.2).
Zenodo. https://doi.org/10.5281/zenodo.18892604

---

## License

All files in this deposit are licensed under
Creative Commons Attribution 4.0 International (CC BY 4.0).

You are free to share and adapt this material for any purpose,
including commercial use, provided you give appropriate credit,
provide a link to the license, and indicate if changes were made.

The theory's mathematical content (axioms, definitions, theorems,
proofs) is not subject to copyright as such. The license applies
to the specific textual expression in these documents.

---

## Contact

Alfredo Atienza Jiménez
Independent Researcher
ORCID: https://orcid.org/0009-0005-1051-2282
aaj@a01.tech
https://a01.tech

---

End of deposit README.
