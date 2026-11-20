# Attribution

This is an unofficial adaptation of the Karpathy Guidelines skill by
[forrestchang](https://github.com/forrestchang) and contributors (its frontmatter,
description and the sentence crediting Karpathy's observations came from
[szkocot](https://github.com/szkocot) in upstream pull request #3), published in
[multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills/blob/2c606141936f1eeef17fa3043a72095b4765b9c2/skills/karpathy-guidelines/SKILL.md).
That file declares the MIT license in its frontmatter, and the repository's README
states MIT. It attributes its coding observations to
[Andrej Karpathy](https://x.com/karpathy/status/2015883857489522876).

The revision was prepared by ajitta using dia-regula 2.2.0. It keeps each condition
with the actions it gates and adds reasons. In section 1 it also turns the slogan
"Surface tradeoffs" into a step to take before implementing, with a reason the
original does not give. Under dia-regula 2.3.0 these added reasons and that step
count as meaning changes. Packaging changes the skill's identifier to
`coding-guidelines`. Version 0.2.0 changes one clause in section 4: a bug fix starts
from a test that reproduces it before the code changes, as in the upstream
repository's EXAMPLES.md Example 3, "Test-First Verification" (commit 2c60614); "even
for a one-line fix" is this plugin's addition. The change and its measurement are
recorded in `docs/evals/` of this repository.

Version 0.3.0 adds rules that are not in the upstream skill and are not Karpathy's:
working out and showing the outcome a request is for, reading the evidence and the
record behind a claim before building on it, a bound on how far a change may go
beyond the request when the named action cannot produce that outcome, and a rule for
calling work complete. They adapt two rules ajitta wrote for his own working contract
for coding agents ("Purpose before action" and "Verification", not published); the
two labelled lines follow dia-regula 3.0.0. Three of these additions touch points of
Karpathy's post that the upstream skill does not carry. The post says models make
wrong assumptions "and just run along with them without checking", where the skill
says to state them; the 0.3.0 text opens the file that settles an assumption first.
The post lists "they don't surface inconsistencies"; the 0.3.0 text reports when the
named action cannot produce the outcome. The post advises users "Don't tell it what
to do, give it success criteria"; the 0.3.0 text has the model work the outcome out
when the user did tell it what to do, which is the editor's inference and not
something the post says. The rule for calling work complete has no counterpart in the
post.

Neither Andrej Karpathy, the upstream authors, nor the upstream maintainers are
claimed to endorse this plugin. dia-regula is an editing method, not a runtime dependency.

The [research record](https://github.com/ajitta/karpathy-regula/tree/v0.1.1/docs/research/karpathy-regula-2026-11-08)
documents the review, corrections, limited behavioral runs, process analysis, and a
later review (`review.md`) that corrects the record where they differ. It does not
establish a general performance improvement over the original.
