# Exercise inventory

This is the source-verified inventory for Thomas M. Cover and Joy A. Thomas,
*Elements of Information Theory*, second edition (Wiley, 2006), print ISBN
9780471241959. It contains **378 numbered exercises** across chapters 2–17.
Chapter 1 has no numbered exercise set. The inspected contents and backmatter
contain no appendices or additional exercise sets.

## Source and provenance

- [Publisher identity and table of contents](https://onlinelibrary.wiley.com/doi/book/10.1002/047174882X)
- [University-hosted second-edition source](https://pages.hmc.edu/ruye/book2/ElementsofInformationTheory.pdf)
- Source accessed: 2026-10-10 UTC
- PDF: 774 pages; SHA-256 `fed9b82d0904c75b47027524e11a12b6dbac31cf4f25319414679050d125dd6f`
- Title page, copyright page, ISBN, chapter structure, every Problems section,
  and numbering sequences were checked. Two extraction methods (layout text and
  PDF font/position records) were reconciled, with visual checks of anomalous
  subpart layouts.
- Printed Arabic page *p* is one-based PDF page *p* + 26 (zero-based index
  *p* + 25) in this particular source.

The public files contain bibliographic facts, identifiers, page references,
hashes, structural labels, and original neutral labels, not problem statements.
The book PDF and source text are not distributed in this repository. Public
availability of the university-hosted file is not a redistribution license.
No instructor solutions manual was used to construct this inventory.

`source-page-evidence.json` records SHA-256 hashes for each Problems-section page
of the Poppler `pdftotext -layout` UTF-8 extraction, excluding its form-feed page
separator. The source PDF hash is the authoritative identity anchor. Exercise
text hashes refer to the private layout-extraction slices, including retained
running headers; they are provenance checks, not published problem text.

## Exact counts

| Chapter | Exercises | Labeled components |
|---|---:|---:|
| 1 | 0 | 0 |
| 2 | 48 | 73 |
| 3 | 13 | 23 |
| 4 | 35 | 77 |
| 5 | 45 | 102 |
| 6 | 18 | 37 |
| 7 | 37 | 74 |
| 8 | 11 | 11 |
| 9 | 22 | 26 |
| 10 | 20 | 31 |
| 11 | 29 | 36 |
| 12 | 22 | 33 |
| 13 | 11 | 25 |
| 14 | 14 | 27 |
| 15 | 36 | 51 |
| 16 | 12 | 20 |
| 17 | 5 | 0 |
| **Total** | **378** | **646** |

The 646 structural components include parent subparts, nested requested cases,
requested proof steps, and the four explicitly labeled hint steps in 9.20. They
are not 646 mutually exclusive exercises. Eleven labeled definition constraints
or algorithm steps are retained separately as `context_markers`. Unlabeled
requests remain within each exercise's scope, even when `subparts` is empty.

Independent authoring ranges: chapters 2–5 (141 exercises), chapters 6–11
(137), and chapters 12–17 (100).

## Schema and canonical paths

`exercises.json` has `edition`, `scope`, `errata`, `chapters`, and `exercises`.
Each exercise records its source number and starting page, labeled components,
and source-verification status. `source_verified: true` verifies the source
identifier and structure; it says nothing about solution correctness or review.
`kind: unspecified` deliberately avoids guessing whether a task is proof-only,
numerical, or mixed. The neutral `label` is not the textbook's problem title.

`subparts` contains unique canonical paths. `subpart_details` maps every path to
its printed label, role, parent where relevant, and printed/PDF page.

- Ordinary parts: `a`, `b`, etc.
- Nested requested cases: `c.i` through `c.vii` in 5.27; `b.i`, `b.ii` in 7.26;
  `c.i`, `c.ii` in 13.10.
- Repeated groups: `first.a`, `first.b`, `second.a`, `second.b` in 5.32;
  the second group in 6.17 additionally has `second.c`.
- Primed repetitions: `a-prime` through `e-prime` in 4.28, explicitly requested
  in prose for the second process.
- Labeled proof steps: 2.4(a–d), 2.17(a–e), 4.5(a–e), 10.15(c.a–c.f), and
  15.11(a–i). Part 4.5(f) is a further question.
- Hint steps: `hint.a` through `hint.d` in 9.20, role `hint_step`.
- Labeled conditions in 10.16 and 12.22, and algorithm steps in 13.11, are
  `context_markers`, not independently requested questions.

## Required source checks

**Text extraction is not sufficient to solve an exercise.** Entire tables and
figures may be missing and mathematical glyphs may be corrupted. In particular,
the joint-probability table in exercise 2.12 (printed page 46) disappears from
layout text. Every exercise therefore has `visual_check_required: true`.
Authors and reviewers must inspect its original PDF pages, including every
figure, table, and displayed formula.

`visual_dependency` and `visual_evidence`, when present, flag possible graphics,
tables, or displayed mathematics from image/vector geometry. These deliberately
broad flags are aids, not a complete semantic classification. Their absence does
not establish that extracted text is complete.

## Errata limitation

No official author/publisher errata list for this edition was verified during
research. The [companion website](https://www.elementsofinformationtheory.com/)
named in the preface was inaccessible. The publisher page and
[author's Stanford page](https://isl.stanford.edu/~cover/) were checked. This is
a limitation of the search, **not evidence that no errata exist**. Suspected
statement errors or missing assumptions must be called out and justified in the
corresponding original solution, rather than silently changing the task.
