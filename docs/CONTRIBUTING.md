# Authoring and independent acceptance

## Scope

Use the second edition (2006), and verify the exact printed exercise and every subpart. The immutable source inventory is `inventory/exercises.json`. Labels in that file distinguish repeated printed subpart letters and nested parts. Do not assume an unlabeled final request is optional. If the source inventory is ambiguous, correct it with page evidence before acceptance.

Create an original derivation, not a transcription of a solution manual. Use a concise exercise label and printed page reference. Do not paste complete problem statements, textbook pages, or private source files. State enough assumptions and definitions to make the argument understandable. Address equality cases, zero probabilities, support, limiting cases, and existence/attainment where relevant.

## Files and submission metadata

Use `solutions/ch02/ex-2-1.md` for Exercise 2.1, with a first-level title and a `## Solution` section. Recommended sections are source/scope, solution, checks, and numerical reproduction. Use fenced `math` display blocks and GitHub's dollar-backtick inline math syntax. Inside display math use `\lt ` rather than a literal less-than sign, which can be truncated as HTML. Use `\mathrm{Var}` and similar upright names instead of `\operatorname`, which GitHub's renderer rejects. Put equation numbers in adjacent prose instead of TeX tags; tags can be rejected or collapse the rendered layout.

Each chapter owns `coverage/submissions/ch02.json`:

```json
{
  "schema_version": 1,
  "solutions": [
    {
      "id": "2.1",
      "path": "solutions/ch02/ex-2-1.md",
      "author": "contributor-identifier",
      "covered_subparts": ["a", "b"],
      "numerical": false,
      "artifacts": []
    }
  ]
}
```

The subpart list must equal the inventory's exact list; the example is illustrative. A pure proof uses `numerical: false`. A computation, requested plot, or numerical verification uses `numerical: true` and adds `numerical_evidence`, a list of run-record paths. Additional dependencies, data, and figures belong in `artifacts` and must be repository files.

Do not list missing or partial solutions as complete submissions. Such exercises remain pending until a full draft is ready. Tests may illuminate a proof, but a finite sample cannot establish a universal mathematical statement.

## Independent review

A different contributor reads the actual source exercise, reviews the full solution, checks every subpart, and reruns any numerical work. They must explicitly assess source alignment, complete subpart coverage, the derivation, and edge cases. Numerical solutions also require numerical reproduction.

The reviewer creates an assessment JSON containing `summary` and boolean `checks` keys `source_alignment`, `all_subparts`, `derivation`, `edge_cases`, plus `visual_source_inspection` whenever the inventory flags visual inspection (currently every exercise), and `numerical_reproduction` if applicable. Inspect the actual PDF page, including tables, diagrams, displayed equations, and page continuations; text extraction alone is insufficient. The summary should explain the actual checks and any resolved issues. Only after those checks pass:

```sh
python scripts/record_review.py 2.1 --reviewer independent-reader --assessment /path/to/assessment.json
python scripts/validate.py
python scripts/build_index.py
```

The review command records an attestation; it does not do the review. It binds the independently verified full inventory and source lock, exercise inventory entry, submission metadata, solution, declared artifacts, executed source, and generated outputs by SHA-256. Self-review is rejected. Any changed dependency invalidates acceptance until a new review is completed. Reviewer names are descriptive attestations, not cryptographic identity verification. A passed integrity check is not formal proof verification.

Do not modify accepted content without arranging review of the changes. Preserve useful review findings in the replacement record. Drafts must never be described as accepted because they merely compile, execute, or resemble an expected answer.
