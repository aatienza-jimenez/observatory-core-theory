#!/usr/bin/env python3
"""
reproduce_tables.py — Reproduction script for:

  "Same Benchmark, Opposite Verdicts: Regulatory Indeterminacy
  in Benchmark-Based Safety Assessment under the EU AI Act"

  Atienza Jiménez, A. (2026)

Reconstructs Tables 1, 2, and 3 from publicly available
AIR-Bench 2024 data (Stanford CRFM, CC-BY-4.0).

Data sources:
  AIR-Bench 2024 per-instance results from HELM GCS bucket.
  https://storage.googleapis.com/crfm-helm-public/air-bench/

Methodology:
  DOI: 10.5281/zenodo.18892604

Usage:
  python reproduce_tables.py --data-dir /data/observatory/sources/airbench

  To see all categories and verify EU-aligned mapping:
  python reproduce_tables.py --data-dir ... --discover-categories

License: CC BY 4.0 (this script is part of the theory repository)
"""

import json
import sys
from pathlib import Path
from collections import Counter
from itertools import combinations, product
from dataclasses import dataclass
from typing import Optional

# ================================================================
# Configuration
# ================================================================

# EU-aligned level-1 category codes (AIR-Bench taxonomy).
# Verified against eu_mandatory.parquet from the HELM dataset.
#
# Code -> Name:
#   2  -> Operational Misuses
#   4  -> Hate/Toxicity
#   10 -> Deception
#   11 -> Manipulation
#   14 -> Discrimination/Bias
#   15 -> Privacy
EU_ALIGNED_CODES: set = {2, 4, 10, 11, 14, 15}

EXPECTED_TOTAL_INSTANCES = 5694
MIN_SAMPLE_SIZE = 50

MODELS = {
    "Model A": "gpt4o_per_instance_stats.json",
    "Model B": "claude3opus_per_instance_stats.json",
    "Model C": "llama31_405b_per_instance_stats.json",
}


# ================================================================
# Data structures
# ================================================================

@dataclass
class Instance:
    instance_id: str
    score: float
    category_code: int


@dataclass
class CategoryStats:
    code: int
    total: int = 0
    safe: int = 0
    ambiguous: int = 0
    unsafe: int = 0


# ================================================================
# Parsing
# ================================================================

def load_instances(path):
    """
    Load instances from a HELM per_instance_stats.json file.

    Extracts air_score and level-1 category code per instance.
    Deduplicates by instance_id.
    """
    with open(path) as f:
        data = json.load(f)

    seen = set()
    instances = []

    for entry in data:
        iid = entry["instance_id"]
        if iid in seen:
            continue
        seen.add(iid)

        score = None
        cat_code = None

        for stat in entry["stats"]:
            name = stat["name"]["name"]

            if name == "air_score":
                score = stat["mean"]

            elif name.startswith("air_category_") and name.endswith("_score"):
                inner = name[len("air_category_"):-len("_score")]
                if "_" not in inner:
                    cat_code = int(inner)

        if score is not None and cat_code is not None:
            instances.append(Instance(iid, score, cat_code))

    return instances


# ================================================================
# Statistics
# ================================================================

def compute_category_stats(instances):
    cats = {}
    for inst in instances:
        if inst.category_code not in cats:
            cats[inst.category_code] = CategoryStats(code=inst.category_code)
        s = cats[inst.category_code]
        s.total += 1
        if inst.score == 1.0:
            s.safe += 1
        elif inst.score == 0.5:
            s.ambiguous += 1
        else:
            s.unsafe += 1
    return cats


def safe_rate(cat, strict):
    if cat.total == 0:
        return 0.0
    numerator = cat.safe if strict else (cat.safe + cat.ambiguous)
    return numerator / cat.total


def overall_counts(instances):
    safe = sum(1 for i in instances if i.score == 1.0)
    amb = sum(1 for i in instances if i.score == 0.5)
    unsafe = sum(1 for i in instances if i.score == 0.0)
    return safe, amb, unsafe


def overall_safe_rate(instances, strict):
    total = len(instances)
    if total == 0:
        return 0.0
    safe, amb, _ = overall_counts(instances)
    numerator = safe if strict else (safe + amb)
    return numerator / total


# ================================================================
# World construction (Section 3)
# ================================================================

CLAIM_ORDER = [
    "toxicity_refusal",
    "uniform_safety",
    "category_coverage",
    "ambiguity_below_threshold",
    "majority_safe",
    "cross_category_consistency",
    "eu_compliance",
    "audit_completeness",
    "deployment_readiness",
]


def build_worlds():
    worlds = []
    for scoring, threshold, scope in product(
        ["strict", "lenient"],
        ["conservative", "standard"],
        ["comprehensive", "eu_aligned"],
    ):
        worlds.append({
            "scoring": scoring,
            "threshold": threshold,
            "scope": scope,
        })
    return worlds


# ================================================================
# Claim evaluation (Section 4.2)
# ================================================================

def evaluate_claims(world, cat_stats, instances):
    strict = world["scoring"] == "strict"
    conservative = world["threshold"] == "conservative"
    eu_only = world["scope"] == "eu_aligned"
    threshold = 0.90 if conservative else 0.75

    if eu_only:
        in_scope = {c: s for c, s in cat_stats.items() if c in EU_ALIGNED_CODES}
    else:
        in_scope = cat_stats

    results = {}

    # 1. toxicity_refusal
    results["toxicity_refusal"] = all(
        safe_rate(s, strict) >= threshold for s in in_scope.values()
    )

    # 2. uniform_safety
    if in_scope:
        rates = [safe_rate(s, strict) for s in in_scope.values()]
        results["uniform_safety"] = (max(rates) - min(rates)) < 0.20
    else:
        results["uniform_safety"] = True

    # 3. category_coverage
    results["category_coverage"] = all(
        s.total >= MIN_SAMPLE_SIZE for s in in_scope.values()
    )

    # 4. ambiguity_below_threshold
    total = len(instances)
    _, amb, _ = overall_counts(instances)
    results["ambiguity_below_threshold"] = (amb / total) < 0.10 if total > 0 else True

    # 5. majority_safe
    results["majority_safe"] = overall_safe_rate(instances, strict) > 0.50

    # 6. cross_category_consistency
    if in_scope:
        results["cross_category_consistency"] = min(
            safe_rate(s, strict) for s in in_scope.values()
        ) >= 0.30
    else:
        results["cross_category_consistency"] = True

    # 7. eu_compliance
    results["eu_compliance"] = results["majority_safe"] and results["category_coverage"]

    # 8-9. inadmissible
    results["audit_completeness"] = None
    results["deployment_readiness"] = None

    return results


# ================================================================
# Epistemic evaluation -- Definition 1
# ================================================================

def eval_x(values_across_worlds):
    """
    Apply EvalX (Definition 1).
    Theorem 1 (T5): this is the unique function satisfying the axioms.
    """
    if all(v is None for v in values_across_worlds):
        return "UNSUPPORTED"

    admissible = [v for v in values_across_worlds if v is not None]

    if not admissible:
        return "UNKNOWN"

    all_true = all(v for v in admissible)
    all_false = all(not v for v in admissible)

    if all_true:
        return "ASSERTED"
    if all_false:
        return "REJECTED"
    return "INDETERMINATE"


# ================================================================
# Quotient space
# ================================================================

def compute_quotient(all_claims):
    profiles = {}
    for i, claims in enumerate(all_claims):
        profile = tuple(claims[c] for c in CLAIM_ORDER if claims[c] is not None)
        profiles.setdefault(profile, []).append(i)

    atoms = []
    for idx, (profile, indices) in enumerate(sorted(profiles.items())):
        label = chr(0x03B1 + idx)
        atoms.append((label, indices, profile))
    return atoms


def compute_sensitivity(atom_values, state):
    if state in ("ASSERTED", "REJECTED"):
        return "Stable (inf)"
    if state in ("UNKNOWN", "UNSUPPORTED"):
        return "n/a"

    true_count = sum(1 for v in atom_values if v)
    false_count = sum(1 for v in atom_values if not v)
    s = min(true_count, false_count)
    total = true_count + false_count
    r = s / total if total > 0 else 0
    return "Fragile (%d); r = %.2f" % (s, r)


def compute_dimension(atoms, all_claims):
    varying = []
    for cn in CLAIM_ORDER:
        atom_vals = set()
        for _, indices, _ in atoms:
            v = all_claims[indices[0]][cn]
            if v is not None:
                atom_vals.add(v)
        if len(atom_vals) == 2:
            varying.append(cn)

    if not varying:
        return 0

    for r in range(len(varying), 0, -1):
        for subset in combinations(varying, r):
            patterns = set()
            for _, indices, _ in atoms:
                pattern = tuple(all_claims[indices[0]][cn] for cn in subset)
                patterns.add(pattern)
            if len(patterns) == 2 ** r:
                return r
    return 0


# ================================================================
# Output
# ================================================================

def print_separator(title):
    print("\n" + "=" * 72)
    print("  " + title)
    print("=" * 72)


def print_table1(worlds, all_claims, atoms):
    print_separator("TABLE 1: Truth values across eight candidate worlds")

    w2a = {}
    for label, indices, _ in atoms:
        for i in indices:
            w2a[i] = label

    print("%-7s %-9s %-11s %-9s %-10s %-10s %-12s %s" % (
        "World", "Scoring", "Threshold", "Scope",
        "maj_safe", "coverage", "compliance", "Atom"))
    print("-" * 78)

    for i, (w, c) in enumerate(zip(worlds, all_claims)):
        ms = "T" if c["majority_safe"] else "F"
        cv = "T" if c["category_coverage"] else "F"
        co = "T" if c["eu_compliance"] else "F"
        scoring = "Strict" if w["scoring"] == "strict" else "Lenient"
        threshold = "Conserv." if w["threshold"] == "conservative" else "Standard"
        scope = "Compr." if w["scope"] == "comprehensive" else "EU-al."
        print("w%-6d %-9s %-11s %-9s %-10s %-10s %-12s %s" % (
            i, scoring, threshold, scope, ms, cv, co, w2a.get(i, "?")))


def print_table2(states, sensitivities):
    print_separator("TABLE 2: Epistemic states for all nine claim schemas")

    print("%-35s %-18s %s" % ("Claim", "State", "Sensitivity"))
    print("-" * 72)

    for cn in CLAIM_ORDER:
        if cn == "audit_completeness":
            print("-" * 72)
        print("%-35s %-18s %s" % (cn, states[cn], sensitivities[cn]))


def print_table3(model_results):
    print_separator("TABLE 3: Cross-model comparison")

    rows = [
        ("Strict safe rate",     "strict_safe_rate",     "pct"),
        ("Lenient safe rate",    "lenient_safe_rate",    "pct"),
        ("|Om*(X)| (atoms)",     "atom_count",           "int"),
        ("Dimension n",          "dimension",            "int"),
        ("Shattered",            "shattered",            "str"),
        ("---",                  None,                   None),
        ("majority_safe",        "majority_safe",        "state"),
        ("category_coverage",    "category_coverage",    "state"),
        ("cross_cat_consistency","cross_cat_consistency", "state"),
        ("eu_compliance",        "eu_compliance",        "state"),
    ]

    sys.stdout.write("%-28s" % "Property")
    for name in model_results:
        sys.stdout.write("  %12s" % name)
    print()
    print("-" * (28 + 14 * len(model_results)))

    for label, key, fmt in rows:
        if key is None:
            print("-" * (28 + 14 * len(model_results)))
            continue
        sys.stdout.write("%-28s" % label)
        for data in model_results.values():
            val = data[key]
            if fmt == "pct":
                sys.stdout.write("  %11.1f%%" % (val * 100))
            elif fmt == "int":
                sys.stdout.write("  %12s" % val)
            else:
                sys.stdout.write("  %12s" % val)
        print()


# ================================================================
# Analysis
# ================================================================

def abbreviate_state(state):
    return {
        "ASSERTED": "assert.",
        "REJECTED": "reject.",
        "INDETERMINATE": "indet.",
        "UNKNOWN": "unknown",
        "UNSUPPORTED": "unsupp.",
    }.get(state, state)


def analyze_model(model_name, instances):
    cat_stats = compute_category_stats(instances)
    worlds = build_worlds()
    all_claims = [evaluate_claims(w, cat_stats, instances) for w in worlds]
    atoms = compute_quotient(all_claims)

    states = {}
    sensitivities = {}
    for cn in CLAIM_ORDER:
        world_values = [c[cn] for c in all_claims]
        state = eval_x(world_values)
        states[cn] = state

        atom_values = []
        for _, indices, _ in atoms:
            v = all_claims[indices[0]][cn]
            if v is not None:
                atom_values.append(v)
        sensitivities[cn] = compute_sensitivity(atom_values, state)

    dimension = compute_dimension(atoms, all_claims)
    atom_count = len(atoms)
    shattered = (
        atom_count == (2 ** dimension) if dimension > 0
        else atom_count <= 1
    )

    return {
        "worlds": worlds,
        "all_claims": all_claims,
        "atoms": atoms,
        "states": states,
        "sensitivities": sensitivities,
        "strict_safe_rate": overall_safe_rate(instances, strict=True),
        "lenient_safe_rate": overall_safe_rate(instances, strict=False),
        "atom_count": atom_count,
        "dimension": dimension,
        "shattered": "yes" if shattered else "no",
        "majority_safe": abbreviate_state(states["majority_safe"]),
        "category_coverage": abbreviate_state(states["category_coverage"]),
        "cross_cat_consistency": abbreviate_state(
            states["cross_category_consistency"]),
        "eu_compliance": abbreviate_state(states["eu_compliance"]),
    }


# ================================================================
# Category discovery
# ================================================================

def discover_categories(instances):
    cats = compute_category_stats(instances)

    print_separator("ALL CATEGORIES (16 level-1 codes)")
    print("%5s %7s %12s" % ("Code", "Count", "EU-aligned"))
    print("-" * 30)

    total_eu = 0
    for code in sorted(cats.keys()):
        s = cats[code]
        eu = "YES" if code in EU_ALIGNED_CODES else ""
        if eu:
            total_eu += s.total
        print("%5d %7d %12s" % (code, s.total, eu))

    print("-" * 30)
    print("%-5s %7d" % ("Total", len(instances)))
    print("%-5s %7d" % ("EU-al", total_eu))
    print()

    safe, amb, unsafe = overall_counts(instances)
    print("Score distribution:")
    print("  safe (1.0):      %5d (%.1f%%)" % (safe, safe / len(instances) * 100))
    print("  ambiguous (0.5): %5d (%.1f%%)" % (amb, amb / len(instances) * 100))
    print("  unsafe (0.0):    %5d (%.1f%%)" % (unsafe, unsafe / len(instances) * 100))

    small = [c for c in sorted(cats.keys()) if cats[c].total < MIN_SAMPLE_SIZE]
    if small:
        print("\nCategories with < %d instances:" % MIN_SAMPLE_SIZE)
        for c in small:
            eu = " (EU-aligned)" if c in EU_ALIGNED_CODES else ""
            print("  Code %d: %d instances%s" % (c, cats[c].total, eu))


# ================================================================
# Main
# ================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Reproduce tables from 'Same Benchmark, Opposite Verdicts'"
    )
    parser.add_argument(
        "--data-dir",
        default="/data/observatory/sources/airbench",
        help="Directory containing AIR-Bench per_instance_stats.json files",
    )
    parser.add_argument(
        "--discover-categories",
        action="store_true",
        help="Print all categories and exit",
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)

    if args.discover_categories:
        path = data_dir / MODELS["Model A"]
        if not path.exists():
            print("ERROR: %s not found" % path)
            sys.exit(1)
        instances = load_instances(path)
        discover_categories(instances)
        sys.exit(0)

    model_results = {}

    for model_name, filename in MODELS.items():
        path = data_dir / filename
        if not path.exists():
            print("\n  WARNING: %s not found -- skipping %s" % (filename, model_name))
            continue

        print("\nProcessing %s (%s)..." % (model_name, filename))
        instances = load_instances(path)

        safe, amb, unsafe = overall_counts(instances)
        print("  Instances: %d" % len(instances))
        print("  Scores: safe=%d  ambiguous=%d  unsafe=%d" % (safe, amb, unsafe))

        if len(instances) != EXPECTED_TOTAL_INSTANCES:
            print("  WARNING: expected %d instances, got %d" % (
                EXPECTED_TOTAL_INSTANCES, len(instances)))

        result = analyze_model(model_name, instances)
        model_results[model_name] = result

        if model_name == "Model A":
            print_table1(result["worlds"], result["all_claims"], result["atoms"])
            print_table2(result["states"], result["sensitivities"])

    if len(model_results) >= 2:
        print_table3(model_results)

    # -- Verification -------------------------------------------
    print_separator("VERIFICATION SUMMARY")
    print()

    all_indet = True
    for model_name, result in model_results.items():
        state = result["states"]["eu_compliance"]
        dim = result["dimension"]
        atoms = result["atom_count"]
        shattered = result["shattered"]
        match = "OK" if state == "INDETERMINATE" else "FAIL"

        print("  [%s] %s: eu_compliance = %s" % (match, model_name, state))
        print("       |Om*(X)| = %d, n = %d, shattered = %s" % (
            atoms, dim, shattered))

        if state != "INDETERMINATE":
            all_indet = False

    print()
    if all_indet:
        print("  All models: eu_compliance = INDETERMINATE")
        print("  Paper result confirmed.")
    else:
        print("  WARNING: Not all models produce INDETERMINATE.")

    if "Model A" in model_results:
        r = model_results["Model A"]
        print()
        print("  Model A verification:")
        print("    Strict safe rate:  %.1f%%  (paper: 49.3%%)" % (
            r["strict_safe_rate"] * 100))
        print("    Lenient safe rate: %.1f%%  (paper: 56.3%%)" % (
            r["lenient_safe_rate"] * 100))
        print("    Atoms:            %d     (paper: 4)" % r["atom_count"])
        print("    Dimension:        %d     (paper: 2)" % r["dimension"])

    print()
    print("Methodology: DOI 10.5281/zenodo.18892604")
    print("Data: AIR-Bench 2024 (Stanford CRFM, CC-BY-4.0)")


if __name__ == "__main__":
    main()
