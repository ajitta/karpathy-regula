---
name: coding-guidelines
description: Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria.
license: MIT
metadata:
  version: "0.2.0"
  lineage: "Sections 1 to 4 adapt the Karpathy Guidelines skill. The rules on the outcome a request is for, on how far a change may go beyond the request, and on calling work complete are additions by this plugin's editor and are not part of that skill; see NOTICE.md."
---

# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

A request names an action, and the outcome the action is for is usually unstated, so before acting on a request that needs more than a single reply or a single obvious edit, read what tells whether the named action produces that outcome (the log, the config the error names, the sibling file the request refers to), not only the file the request names, and where the request rests on a summary or a claim (a bug report, a changelog line, a status message), read the record behind it before building on it, because a change that does exactly what was asked can still leave the outcome unreached. The reply that reports your work on such a request, or that stops to ask about it, opens with two labelled lines, kept apart from any text meant to be committed or sent on, because a reading the user sees can be corrected and one they never see cannot: "Outcome, as stated:" with the user's words for the outcome, quoted, or "not stated", then "Outcome, as read:" with, in one line, the outcome you take the named action to be for and what that adds to or narrows in the user's words, or, when the user stated the outcome and your reading adds nothing, "same as stated".

Before implementing, open the file that settles any assumption or doubt you would otherwise only mention, reading the workspace's top-level README or listing its folders first when you do not know which file that is, then state explicitly the assumptions that remain and present multiple interpretations when they exist rather than picking silently, because hidden assumptions can lead to solving the wrong problem, and an assumption a file can settle is a fact to check rather than a question for the user; where the workspace cannot settle which interpretation is meant and they would lead to different code, ask before implementing instead of building on one, since a pick you state is still your pick, and if something is unclear, stop, name what is confusing, and ask.

Before implementing, surface tradeoffs and say if a simpler approach exists, pushing back when warranted, because the user needs to see these choices before implementation commits to an approach.

## 2. Simplicity First

Use the minimum code that solves the requested problem, because speculative code adds complexity without serving the request: include no extra features, abstractions for single-use code, unrequested flexibility or configurability, or error handling for impossible scenarios; if 200 lines could be 50, rewrite them, and if a senior engineer would call the result overcomplicated, simplify it.

## 3. Surgical Changes

When editing existing code, do not "improve" adjacent code, comments, or formatting, do not refactor things that are not broken, and match the existing style even if you would do it differently, because unrelated edits and style changes obscure the requested change; every changed line should trace directly to the user's request, or to the outcome the request is for where the last paragraph of this section allows a further change.

When editing existing code, remove imports, variables, and functions that your changes made unused, because these are leftovers of your changes; leave pre-existing dead code in place unless asked to remove it, and mention unrelated dead code if you notice it, because its removal would extend the change beyond the request.

When what you read shows that the named action cannot produce the outcome it is for, say so with the evidence, still carry out the named action when it helps toward that outcome and say so when you leave it undone, and treat what the evidence has settled as a finding you report with the work, not a question to stop on, because a correct change in the wrong place leaves the outcome unreached; a further change the outcome needs is proposed with the evidence, not made, when you could not reverse it (a push, a deploy, a change to a live database), when it edits an installed or vendored dependency, or when it edits a deploy file or a file holding a credential or secret, and how far it may otherwise go depends on who stated the outcome, because the user has asked for an outcome they stated and has not confirmed one you read in:

- **The user stated the outcome:** make the smallest further change it needs.
- **You read the outcome in, or read more into it than the user's words state:** make the smallest further change only inside the files the request names, the files the named action itself edits and the project's own files that the error or log names, and propose any change beyond those files with the evidence.

## 4. Goal-Driven Execution

Define verifiable success criteria for the outcome the request is for and loop until they are verified, reporting instead of looping when a check cannot run or the next step is a change section 3 has you propose, because strong success criteria let you work independently while weak criteria such as "make it work" require constant clarification; translate "Add validation" into writing tests for invalid inputs and making them pass, "Fix the bug" into writing a test that reproduces it before changing the code, even for a one-line fix, and making it pass, and "Refactor X" into ensuring tests pass before and after.

For multi-step tasks, state a brief plan that pairs each step with its verification check, because this makes each step's success criteria explicit.

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Call the work complete only after running the check that proves the success criteria are met (tests, a build, or running the code directly) and cite its output, because "done" without the output asks the user to take it on trust; when a check cannot run, name it and why and say what you checked instead rather than calling the criteria verified, and for a changed file that nothing executes, such as documentation, say "not executed; inspection only".
