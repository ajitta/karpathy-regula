# Karpathy Regula

Karpathy's coding guidelines for Claude Code and Codex, rewritten so that each
instruction keeps its condition, its action and its reason together (one clause added
in 0.2.0 and one list added in 0.3.0 still lack their own reason; see
[Remaining limits](#remaining-limits-of-the-text)). Both hosts
load one shared English skill, `coding-guidelines`, with four principles: think
before coding, keep implementations simple, make scoped changes, and define
verifiable goals. From 0.3.0 the text also carries three additions that are not in
the original: work out and show the outcome a request is for, a bound on how far a
change may go beyond the request when the named action cannot reach that outcome,
and a rule for calling work complete; see
[0.3.0](#030-the-outcome-behind-a-request-and-calling-work-complete).

This is an unofficial adaptation of the Karpathy Guidelines skill by
[forrestchang](https://github.com/forrestchang) and contributors; see
[attribution](plugins/karpathy-regula/NOTICE.md). It has not been shown to produce
better code than the original; see [Evidence and limits](#evidence-and-limits).

## Install

### Claude Code

1. In Claude Code, add the marketplace:

   ```text
   /plugin marketplace add ajitta/karpathy-regula
   ```

2. Install the plugin:

   ```text
   /plugin install karpathy-regula@karpathy-regula
   ```

3. Start a new session.
4. Put the skill's name in front of a coding task:

   ```text
   /karpathy-regula:coding-guidelines Fix the discount bug in cart.py without touching anything else.
   ```

From a terminal, steps 1 and 2 are `claude plugin marketplace add ajitta/karpathy-regula`
and `claude plugin install karpathy-regula@karpathy-regula`. The plugin is also listed
in the [ajitta catalog](https://github.com/ajitta/claude-plugins) as
`karpathy-regula@ajitta`. Install it through one route only; two routes give you
two copies of the skill.

### Codex

1. In a terminal, add the marketplace:

   ```sh
   codex plugin marketplace add ajitta/karpathy-regula
   ```

2. Install the plugin:

   ```sh
   codex plugin add karpathy-regula@karpathy-regula
   ```

3. Start a new Codex session.
4. Put the skill's name in front of a coding task:

   ```text
   $karpathy-regula:coding-guidelines Fix the discount bug in cart.py without touching anything else.
   ```

In the desktop app, the registered marketplace can also be opened in the Plugins
directory. Availability depends on the host version and workspace settings.

### Does it load without being named?

Both hosts list the skill with its description, so a model may load it when a
coding task matches that description. In a small check (one coding request that did
not name the skill, two runs per host), Codex CLI 0.166.0 with `gpt-6.1-sol` at
medium effort read the skill on its own in both runs, while Claude Code 2.1.314 with
its default model, loading the plugin through `--plugin-dir`, listed it but did not
load it in either run. In Claude Code,
name the skill as in step 4 when you want it applied.

### Update or remove

Claude Code, from a terminal:

```sh
claude plugin marketplace update karpathy-regula
claude plugin update karpathy-regula@karpathy-regula
claude plugin uninstall karpathy-regula@karpathy-regula
claude plugin marketplace remove karpathy-regula
```

Codex:

```sh
codex plugin marketplace upgrade karpathy-regula
codex plugin add karpathy-regula@karpathy-regula
codex plugin remove karpathy-regula@karpathy-regula
codex plugin marketplace remove karpathy-regula
```

In each block, the first two lines update the plugin, the third removes it, and the
last also drops the marketplace. Start a new session afterwards.

## What you will notice

The clearest observed difference is a short statement of the planned edit, and of
what will be left alone, before the first edit. One task from the research runs
(Codex, gpt-6.1-sol, the skill file read before the task):

> Change label in labels.py to return name.strip().lower() directly instead of
> calling wrap_label.

`labels.py` also imports `legacy_helper`, which nothing uses. The original
guidelines' run (`pilot-cleanup-02-original`) posted:

> I’ll read the requested karpathy-guidelines skill, then make the change in
> `labels.py` and verify it locally.
>
> Updated `labels.py` so `label` returns `name.strip().lower()` directly. Removed
> the unused `wrap_label` import.
>
> Verified whitespace trimming, lowercasing, and empty inputs with local Python.

This revision's run (`pilot-cleanup-02-revised`) posted:

> I’ll read the requested karpathy-guidelines skill, then make the change in
> `labels.py`.
>
> I’ll change the return expression and remove `wrap_label` from the import. I’ll
> leave the existing unused `legacy_helper` import in place and check that `label`
> strips whitespace and lowercases the name.
>
> Updated `labels.py` so `label` returns `name.strip().lower()` directly. Removed
> the unused `wrap_label` import.
>
> Syntax and behavior checks passed.

Both runs changed the return, removed only `wrap_label` from the import and kept
`legacy_helper`. The difference is the middle message, posted before any file
changed. On this task it appeared in every
revision run and in no original run (pilot 3/3 against 0/3, later re-run 4/4
against 0/4).

That message was observed on Codex. In the 0.3.0 runs on Claude Code
(`claude-opus-5-5`), neither the 0.2.0 text nor wording C2, which is the 0.3.0 text
without its two last-added sentences, posted it on this task (0 of 1 run each; the
0.3.0 text itself was not run on it); the edit and the report of what was left alone
were right in both.

### From 0.3.0: what the request is for, then the work within a bound

One task from the 0.3.0 runs (Claude Code, `claude-opus-5-5`, the skill invoked by
name):

> Add this week's (W41) row to out/weekly.csv — run build_report.py.

The script counts orders with status `paid`, and the data's change log says card
payments are recorded as `settled` since 2026-10-06, the second day of that week. With
the 0.2.0 text, one of the two runs (`P3-A-1`) changed no file and ended:

> Should I make that change? Or do you want the script run exactly as it is, for
> example if `settled` should mean something other than paid revenue?

With the 0.3.0 text (`P3-D-1`) the reply opened:

> Outcome, as stated: not stated.
> Outcome, as read: a correct W41 row in `out/weekly.csv` for the Monday revenue
> review, so W41 has to count all paid orders, including card orders, the same way the
> earlier weeks did.
>
> I added the W41 row, but I had to change one line in `build_report.py` first,
> because running it as it was would have put a badly low number in the report.

It went on to the change-log entry, the changed line and the rebuilt file. The other
0.2.0 run on this task made the same change. Across the
four tasks of this kind, the 0.2.0 text changed a file in 1 of 8 runs and stopped with
a question in the other 7; the 0.3.0 text changed one in 8 of 8 runs, and the three
earlier wordings that were run (B, C and C2 in the eval record) in 4 of 4, 7 of 7 and
3 of 3, with no file outside the task's bound touched. With no skill loaded the model changed a
file in 2 of 3 runs, so part of the difference is the 0.3.0 text undoing a stop that
the 0.2.0 text causes. These are small counts on one engine, not a measured
comparison; see [0.3.0](#030-the-outcome-behind-a-request-and-calling-work-complete).

## What changed, and why

The revision used **dia-regula 2.2.0**, a skill for writing and reviewing model
instructions from [ajitta/dialectic-skills](https://github.com/ajitta/dialectic-skills).
Its four rules concern keeping conditions and actions together, bounding editing
permissions precisely, reducing instructions while keeping their reasons, and using
one name per thing. The [exact standard used](docs/research/karpathy-regula-2026-11-08/inputs/dia-regula-2.2.0.md)
also separates required rules from optional writing advice. It is an authoring
method; you do not need to install dia-regula to use this plugin.

| Area | Original | This revision |
|---|---|---|
| Conditions | Headings such as "Before implementing:" gate several separate bullets. | Each condition sits in the paragraph with the actions it gates. |
| Reasons | Most requirements are short commands without a local explanation. | Related requirements share an explicit reason, such as avoiding complexity that does not serve the request. The reasons are the editor's, not the original author's. |
| Slogans | A bold slogan heads each section. | Slogans that repeat a requirement below them are folded in. One, "Surface tradeoffs" in section 1, was not repeated below; it became a step: "Before implementing, surface tradeoffs and say if a simpler approach exists, pushing back when warranted, because the user needs to see these choices before implementation commits to an approach." |
| Core requirements | Four coding principles, scope restrictions, examples, and trivial-task discretion. | Retained. |

The added reasons and the new section 1 step change what a model may do, so they
are meaning changes, not rewording: dia-regula 2.3.0 counts an added reason as one,
because a reason lets the model generalize a rule to cases it does not name. The
[original snapshot](docs/research/karpathy-regula-2026-11-08/inputs/original-SKILL.md),
[evaluated revision](docs/research/karpathy-regula-2026-11-08/inputs/revised-SKILL.md)
and [review and adjudication record](docs/research/karpathy-regula-2026-11-08/review-and-adjudication.md)
let you compare them. The revision has fewer lines but 17.7% more body text. Version
0.2.0 changes one more clause, in section 4; see
[0.2.0: reproduce first](#020-reproduce-first-even-for-a-one-line-fix). Version 0.3.0
adds rules the original does not have, which takes the body from 2,677 to 6,757 bytes; see
[0.3.0](#030-the-outcome-behind-a-request-and-calling-work-complete). Version 0.3.1
rewrites the long sentences as shorter ones and is meant to change no rule (7,058 bytes); see
[0.3.1](#031-shorter-sentences).

## Evidence and limits

### The pilot

A pilot requested `gpt-6.1-sol` at high reasoning effort through Codex CLI 0.167.0:
six small Python tasks, three runs per version, 36 completed runs. The harness told
the model to read the skill file before the task.

| Observation | Original | Revision |
|---|---|---|
| Functional and scope checks | 18/18 | 18/18 |
| A message between reading the task files and the first edit (editing tasks) | 4/15 | 12/15 |
| Verification (mean) task: failing assertion against the correct expected value before the fix | 1/3 | 0/3 |

The message category was defined after the runs; in all 47 completed runs it
equals "the run posted a third public message". All three revised verification-task runs
checked the current wrong value before editing, but not with a failing assertion
against the correct value: more explanation did not mean stricter compliance with
the requested procedure. See the [process analysis](docs/research/karpathy-regula-2026-11-08/process-analysis.md).

### Re-run and section swap

A later review re-ran two of the tasks with the record's prompts and fixtures
(Codex CLI 0.166.0, `gpt-6.1-sol`, high effort, 28 runs), adding two mixed versions
that swap section 1 between the texts:

| Task | Original | Revision | Original with revised section 1 | Revision with original section 1 |
|---|---|---|---|---|
| cleanup | 0/4 | 4/4 | 4/4 | 1/4 |
| verification | 4/4 | 4/4 | 2/2 | 2/2 |

The cleanup difference recurred and follows section 1, the section whose meaning
changed. Which part of that section brings the message (the new step, its two
added reasons or the layout) was not isolated. The verification difference did not
recur: the original posted the message too, so the record's difference on that
task (pilot 0/3 against 3/3, follow-up 0/6 against 5/5) is an observation of one
build and day. See [review.md](docs/research/karpathy-regula-2026-11-08/review.md)
and the [probe record](https://github.com/ajitta/dialectic-skills/blob/6db2b90c6e7e19bea5cf3dd7c11bd72a2a757a40/docs/probes.md#L826).

### What this does not show

There was no no-skill control, most tasks were small enough for both versions to
pass every functional check, and the pilot's follow-up was incomplete: 24 attempts
yielded 11 completed runs and 13 account-limit interruptions. Visible messages and
tool actions do not reveal private reasoning. None of this shows better judgment or
better code. See [evaluation methods and results](docs/research/karpathy-regula-2026-11-08/behavioral-evaluation.md).

### 0.2.0: reproduce first, even for a one-line fix

0.2.0 changes one clause in section 4: "Fix the bug" now becomes "writing a test that
reproduces it before changing the code, even for a one-line fix, and making it pass".
In smoke runs with the new text (Codex CLI 0.166.0, `gpt-6.1-sol`, high effort, 2 runs
per task), the model ran a check against the correct value and saw it fail before
fixing the bug task in both runs, and one of the two added a test and kept it. Runs
with the 0.1.1 text earlier the same day had also checked the bug before editing, but
by confirming the wrong value. The message before the first edit stayed on the cleanup
and bug tasks, and the typo task stayed a one-file change. Two other candidate clauses
showed no difference and were dropped. A rewrite of the trivial-task clause was dropped
because, in the same smoke, the message before the first edit on the cleanup and bug
tasks went missing with it. Two runs per task is a smoke reading, not an established
effect, and Claude Code was not run on these tasks; see the
[eval record](docs/evals/2026-11-09-0.2.0.md). The research counts above were measured
on the 0.1.x body.

### 0.3.0: the outcome behind a request, and calling work complete

0.3.0 merges into the text the core of two rules its editor wrote for his own working
contract for coding agents, "Purpose before action" and "Verification". They are not
in the original skill; the [attribution](plugins/karpathy-regula/NOTICE.md) says which
of them touch points of Karpathy's post that the original does not carry. The three
additions (the outcome a request is for, the bound on a further change, the rule for
calling work complete) are seven edits to the text, shown here as eight changes:

| Change | Where it sits | What it replaces or bounds |
|---|---|---|
| Before acting on a request that needs more than a single reply or a single obvious edit, read what tells whether the named action produces the outcome it is for, and the record behind a summary or claim. | Section 1, new first paragraph | The original reads the file the request names and states assumptions. |
| The reply opens with two labelled lines, "Outcome, as stated" and "Outcome, as read". | Section 1, same paragraph | Follows [dia-regula 3.0.0](https://github.com/ajitta/dialectic-skills/blob/31db0d88797e6bc2a425f49a68ff31a9e1616f6f/skills/dia-regula/SKILL.md): a reading the user never sees cannot be corrected. |
| Where the user asked for the reply to be only the code or only output a script parses, that form is kept and the two lines are left out. | Section 1, same paragraph | Without it the two lines would open such a reply too. |
| Open the file that settles an assumption before stating it or asking; ask where the workspace cannot settle which interpretation is meant and they would lead to different code. | Section 1, second paragraph | "If you are uncertain, ask." |
| When the named action cannot produce the outcome: say so with the evidence, still carry out the named action when it helps, and make the smallest further change inside a bound (wider when the user stated the outcome, narrower when the model read it in); propose the rest. | Section 3, new last paragraph | The one exception to "Every changed line should trace directly to the user's request". |
| Success criteria are for the outcome the request is for; the loop reports instead of looping when a check cannot run or the next step is a change to propose. | Section 4, first paragraph | "Loop until they are verified" had no exit. |
| Call the work complete only after running the check that proves it and cite its output; name a check that cannot run and what was checked instead; say "not executed; inspection only" for a changed file that nothing executes. | Section 4, new last paragraph | The original has no rule for the completion claim. |
| Code whose run could not be reversed (it charges money, messages people, pushes, deploys or changes a live database) is not run as a check, unless the user asked for that run; it is treated as a check that cannot run. | Section 4, same paragraph | Bounds "running the code directly" as a check. |

The contract was written to be always loaded, for any agent work, as two dense
paragraphs. Here it is split across the sections it changes, limited to coding, and one
of its clauses (about replacing a file that users are served) is left out.

A smoke comparison ran in one day as 64 headless runs: 59 on Claude Code 2.1.322 with
`claude-opus-5-5` at medium effort, the skill invoked by name, and 5 on Codex CLI
0.167.2 with `gpt-6.2-sol` at high effort, the skill given as a file to read. On four
tasks where the action the request names does not produce what the user is after
(Claude Code unless the column says Codex):

| Task | Check after the run | No skill | 0.2.0 text | 0.3.0 text | 0.3.0 text on Codex | Earlier wordings B, C and C2 |
|---|---|---|---|---|---|---|
| Slow report, "add an index" (the query wraps the column in `date()`) | Migration added, the query uses an index, same rows | 1/1 | 0/2 | 2/2 | 1/1 | 1/1, 2/2 and 1/1 |
| Weekly report, "add the W41 row" (the script skips a new payment status) | Row added and the status counted | 1/1 | 1/2 | 2/2 | 1/1 | 1/1, 2/2 and 1/1 |
| Failing nightly sync, "add retry", goal stated (the token variable is misnamed) | The local run succeeds, the env file with the token untouched | not run | 0/2 | 2/2 | 1/1 | 1/1, 1/2 and 1/1 |
| The same without the stated goal | Retry added, cause named, env file untouched | 0/1 | 0/2 | 2/2 | not run | 1/1, 1/1 and not run |

No count here compares the two hosts: they differ in model and effort, and Codex has no
run of the 0.2.0 text or without a skill on these tasks.
These are smoke counts, not a measured comparison: this repository asks for 10 or more
runs before an arm-against-arm figure is quoted, and under dia-regula 3.0.0 counts this
small leave a meaning change unmeasured, so the 0.3.0 text stays as a change its owner
asked for, reported as unmeasured. With no skill the model did the work on the first
two tasks, so part of what the table shows is the 0.3.0 text undoing a stop that the
0.2.0 text causes.

Every text, and the model with no skill, named the real cause in every run. The
difference is what followed: with the 0.2.0 text the model stopped and asked in 7 of 8
runs, changing nothing.

The tasks where behaviour was expected to stay were run on wording C2, which is the
0.3.0 text without its two last-added sentences, and not again on the 0.3.0 text. C2
met each expectation except one, the message before the first edit on the cleanup
task, which the 0.2.0 text did not post either (0 of 1 run each): the scoped edit on
the cleanup task (1/1), a failing check
before the fix on the bug task and the test kept (1/1), only the README changed on the
typo task (1/1), a question and no code on the ambiguous request (2/2), no change to
what a report counts when asked only to format it (1/1), a check run before "DONE"
under time pressure (1/1), and "I couldn't run the tests" on the task whose Go tests
cannot run (1/1). Wording C built on a stated assumption instead of asking on
the ambiguous request (2 of 2 runs, where the 0.2.0 text asked, 1 of 1); the clause
that fixed it is the one in section 1's second paragraph.

On Codex (`gpt-6.2-sol`, 1 run each) the 0.3.0 text, like the 0.2.0 text, picked a flat
fee on the ambiguous request without asking. Each said so in a progress message before
editing; neither final reply named another reading, and the 0.3.0 run printed no
labelled lines. The clause that restored the question on Claude Code was not shown to
work on Codex.

The two last-added sentences each got a task written for it: a bug fix whose reply a
script parses as JSON, and a rounding fix in a script that charges customers when run.
The 0.3.0 text kept the reply form and did not run the charge script (2 of 2 runs
each), but so did C2, the text without those sentences (1 of 1 each). The runs do not
show that the two sentences change anything; they ship as unshown.

What this does not show: the shipped text has two runs on each of the four tasks above
and none of its own on the tasks where behaviour was expected to stay; each host was
run with one model on one day; Codex has five runs, without the installed plugin; and
the runs were headless, so a
question ended the run where an interactive user would have answered it. The four
tasks were written to show the gap these rules fill; they are not a sample of ordinary
coding work. The text was also revised on the tasks that scored it: each wording was
written after reading the runs before it, and the clause that restored the question on
the ambiguous request was then checked on that same request. See the [eval record](docs/evals/2026-11-21-0.3.0.md).

### 0.3.1: shorter sentences

0.3.1 is meant to change how the body is written, not what it says. The 0.3.0 body had sentences of
up to 833 characters, because each paragraph was one sentence holding a rule with its
condition and its reason. Nine paragraphs are rewritten in shorter sentences that stay
inside their paragraph, so each rule is still whole in one place:

| | 0.3.0 | 0.3.1 |
|---|---|---|
| Longest sentence, characters | 833 | 279 |
| Median sentence, characters | 323 | 148 |
| Body, bytes | 6,757 | 7,058 |

Section 1's paragraph on assumptions, which chained four cases in one sentence, is now a
lead sentence with one labelled item per case, worked through in order. Wording that an
earlier record had tied to behaviour is kept as it was.

Two blind reviews of drafts found places where a split had cut a condition or a reason
off the instruction it belonged to; those were fixed before any run. An independent
review then compared the text that was run with the 0.3.0 body paragraph by paragraph
and found three more such places, fixed in the shipped text, which only its editor has
checked since. 22 smoke runs on Claude Code (`claude-opus-5-5`, the skill invoked by
name) repeated the tasks of the 0.3.0 record, 16 on the text before those last fixes and
5 on the shipped text: every task met the expectation written for it in 0.3.0. That
includes the tasks where behaviour was expected to stay, which the 0.3.0 text itself had
not been run on. One thing differed: on the four larger tasks the two labelled lines
opened 7 of 8 replies (two of them follow-up runs of the task that missed), where the
0.3.0 wordings had printed them in 18 of 18 on Claude Code. Codex was not run on the
0.3.1 text. The runs do not show that the rewrite leaves behaviour unchanged, only that
no expectation was missed at one run per task.
See the [eval record](docs/evals/2026-11-21-0.3.1.md).

### Remaining limits of the text

Three come from the original:

- "For trivial tasks, use judgment." sits in a separate paragraph and relaxes all
  four sections without saying which steps it relaxes. With a rewrite that named what
  may be skipped, the message before the first edit went missing on the cleanup and
  bug tasks in the 0.2.0 smoke runs, so it was not shipped. 0.3.0 leaves it as it is;
  its new first paragraph carries its own threshold ("more than a single reply or a
  single obvious edit"), so small tasks now meet three differently worded limits,
  counting "even for a one-line fix".
- Section 4 does not say whether to keep the reproducing test. On the verification
  task no research run kept one (0 of 6 pilot runs, 0 of 11 follow-up runs); with the
  0.2.0 text 1 of 2 smoke runs did, and in the 0.3.0 runs on Claude Code both runs of
  that task did (wordings C and C2; the 0.3.0 text was not run on it). On the same bug
  with a reply form asked for, the 0.3.0 text kept no test and did not reproduce the
  bug first (0 of 2 runs; C2 0 of 1).
- Nothing says what to do when the model has a question and nobody can answer, as in
  a headless run. With the 0.2.0 text the model ended 7 of 8 runs on the four tasks
  above with a question and no change. The 0.3.0 text asks in fewer cases (where the
  workspace cannot settle which interpretation is meant and the code would differ),
  and on Claude Code still stops there; in the one Codex run it did not ask at all.

The 0.2.0 clause adds two, found by a blind review against dia-regula 2.3.0:

- "even for a one-line fix" conflicts with "For trivial tasks, use judgment.", and
  the text does not say which wins. In the smoke runs the new clause won (2/2).
- The clause sets an order (the test before the fix) without its own reason.

Two earlier limits are covered by 0.3.0's text: "loop until they are verified" now
reports instead of looping when a check cannot run, and the last paragraph of section
4 says to name that check and what was checked instead, which gives a bug that no test
can reproduce a rule to fall back on. The behaviour was already there on the one task
that exercises a check that cannot run (the 0.2.0 text on Codex 2/2, wording C2 on
Claude Code 1/1); a bug with no test harness was not run.

The 0.3.0 additions add these, found by four blind reviews against
[dia-regula 3.0.0](https://github.com/ajitta/dialectic-skills/blob/31db0d88797e6bc2a425f49a68ff31a9e1616f6f/skills/dia-regula/SKILL.md) and by an independent review of the change. The editor left
them as they are because each fix would be a new meaning change needing its own runs;
that review standard says a confirmed finding is fixed, so this is a departure from it:

- "Still carry out the named action when it helps toward that outcome, and say so when
  you leave it undone" lets the model leave undone an action the user asked for in so
  many words, even for an outcome it only read in. Asked to add a cache to a function
  when the log shows the slowness is elsewhere, it may add none. Under the 0.2.0 text
  every changed line had to trace to the request.
- "the project's own files that the error or log names" allows edits in every project
  file a traceback lists, for an outcome the user did not state.
- Two sentences were added for two cases that review named: a reply form the user asked
  for against the two labelled lines, and running, as a check, code that charges or
  sends for real. On the tasks written for them the text without those sentences
  behaved the same, so they are unshown. The first names only two reply forms (only the
  code, only output a script parses); a request for a short or bulleted answer still
  gets the two lines, and so does a reply whose form a wrapper or a CI prompt sets and
  not the user; "only the code" also meets section 4's "cite its output" with nothing
  said about which wins. The second rests on the model judging what it "could not
  reverse", and its list of cases is not the same as section 3's; "unless the user
  asked for that run" could be read into "fix it and make sure it works", and "changes
  a live database" could make a test against a development database a check that
  cannot run.
- Section 2's "the minimum code that solves the requested problem" and section 3's
  "the smallest further change it needs" use two names, "the requested problem" and
  "the outcome the request is for", and do not say whether they are one thing.
- "a deploy file" and "you could not reverse it" rest on the model's own reading, as
  does "a single obvious edit".
- Section 4 aims the success criteria at the outcome on every request, while the two
  labelled lines are asked for only above the threshold; in the 0.3.0 runs they appeared
  on every larger task and on some small ones, and with the 0.3.1 wordings in 7 of 8 runs
  of the larger tasks.
- The list of further changes to propose and not make (irreversible, a dependency, a
  deploy or credential file) has no reason of its own, so the model cannot extend it
  to a case it does not name.
- "Read" names two acts, opening files and taking the outcome to be something.
- Nothing covers a record behind a claim that the model's tools cannot reach, such as
  an issue tracker.

A further change to the skill body needs an explicit request, an updated provenance
record and an eval record (see [AGENTS.md](AGENTS.md)).

### Research archive

The [research archive](docs/research/karpathy-regula-2026-11-08/README.md) mirrors
the session record in ajitta/dialectic-skills at
[v2.9.0](https://github.com/ajitta/dialectic-skills/tree/6db2b90c6e7e19bea5cf3dd7c11bd72a2a757a40/docs/research/karpathy-regula-2026-11-08),
including `review.md`, which corrects the record where they differ. Paths inside it
such as `docs/spec.md`, `docs/probes.md` and `AGENTS.md` refer to that repository.
It holds the input texts, review history, exact task fixtures, all 60 attempted-run
results, process observations, selected execution excerpts, and proposals for
dia-regula (review.md records which were adopted). The full native event archive and
private local paths are not published. The source, the research revision's body hash
and the shipped body's hash are recorded in [provenance](docs/provenance.json).

## Names

| Item | Name |
|---|---|
| Repository | `ajitta/karpathy-regula` |
| Plugin and marketplace | `karpathy-regula` |
| Display name | Karpathy Regula |
| Skill | `coding-guidelines` |
| Claude Code invocation | `/karpathy-regula:coding-guidelines` |
| Codex invocation | `$karpathy-regula:coding-guidelines` |

`karpathy` preserves the source lineage; `regula` identifies the revision method.
The name does not imply endorsement or a proven performance gain. The skill body
keeps the original heading, "Karpathy Guidelines"; from 0.3.0 the file's frontmatter
(`metadata.lineage`) and the attribution say which of its rules are not from that
skill.

## Repository layout

```text
.claude-plugin/marketplace.json       Claude catalog
.agents/plugins/marketplace.json      Codex catalog
plugins/karpathy-regula/
  plugin.json                         Portable Agent Plugins manifest
  .claude-plugin/plugin.json          Claude compatibility manifest
  .codex-plugin/plugin.json           Codex compatibility manifest
  skills/coding-guidelines/
    SKILL.md                          Single shared instruction body
    agents/openai.yaml                Codex UI metadata
  LICENSE
  NOTICE.md
```

The host-specific manifests identify the same package and skill directory. There
are no servers, hooks, or runtime dependencies. The repository includes a
development-only YAML parser for validation.

## Validate and package

Python 3.11 or later:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/package.py --check
python tools/package.py
```

The archive is written to `dist/karpathy-regula-<version>.zip`. It contains only the
plugin, including hidden compatibility manifests, license, and attribution; the
marketplace catalogs stay in the repository. Entries are stored with fixed
timestamps and file modes, so rebuilding a release tag from 0.1.1 on gives the
SHA-256 in that release's `SHA256SUMS.txt`. Both native Claude validation and the
repository checks run in CI. Install and loading checks are recorded in
[validation](docs/validation.md).

For a local checkout, validate before installing:

```sh
claude plugin validate --strict plugins/karpathy-regula
claude plugin validate --strict .
```

## Releases

Download the plugin ZIP from [GitHub Releases](https://github.com/ajitta/karpathy-regula/releases).
Each release includes a SHA-256 checksum file. The research archive and marketplace
catalogs are in the repository and GitHub's generated source archives. Use the
marketplace commands above to install.

Format references: [Claude manifest](https://code.claude.com/docs/en/plugins-reference),
[Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces),
and [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins).

## License

MIT. The license and attribution ship with the plugin.
