# Coverage

`submissions/chXX.json` records full solution drafts and their authors. `status.json` is generated from the textbook exercise inventory and current hash-bound independent reviews. It is never hand-edited.

- **pending:** no full draft has been submitted
- **draft:** a complete claimed solution has been submitted but not independently accepted
- **accepted:** a separate reviewer checked source alignment, all subparts, derivation, edge cases, and numerical reproduction when needed; the exact files still match the review hashes

A stale or malformed acceptance record fails validation rather than silently preserving a completed count. Run `python scripts/build_index.py` after an authorized content or review change.
