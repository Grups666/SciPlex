# SciPlex Agent Guide

This file defines the project-level goals and principles for future changes to
the SciPlex skill. All edits should preserve these constraints unless the user
explicitly asks to revise them.

## Project Goal

SciPlex is a general-purpose research operating system for Codex skills. Its
purpose is to help an agent conduct rigorous, auditable scientific inquiry from
question formulation to publication-quality synthesis.

SciPlex should not be a fixed script, a single-domain workflow, or a paper
generator. It should provide reusable research protocols, object schemas,
execution conventions, review gates, and audit trails that can adapt to many
fields, methods, data sources, and output formats.

Concrete research domains may be used as examples or tests, but the skill's
identity and core protocols must remain field-neutral.

## Core Scientific Principles

1. Problem before method.
   Start from a specific research problem, tension, contradiction, or
   falsifiable question. Do not start by blindly applying a method to available
   data.

2. Falsifiability.
   Hypotheses must make distinguishable predictions and be possible to support,
   refute, or mark as inconclusive.

3. Evidence-calibrated claims.
   Claim strength must match evidence strength. Weak evidence cannot justify
   strong language, causal language, broad generalization, or certainty.

4. Traceable evidence chains.
   Every finding should trace back through experiment, method, data, and source.
   Untraceable claims should be removed, completed, or explicitly limited.

5. Method fidelity.
   Implemented methods must match designed methods. If execution diverges from
   design, update the method object and manuscript claims rather than hiding the
   divergence.

6. Sanity before synthesis.
   Implausible values, unit mistakes, invalid assumptions, and method mismatch
   block synthesis. They require iteration, failure logging, or reframing.

7. Failure as memory.
   Failed attempts are first-class research objects. Record failure mode,
   lesson, context, and alternatives so later work avoids repeating mistakes.

8. Research as a cyclic graph.
   The workflow must support iteration and reframing. A later phase can return
   to formulation, literature review, method design, or data preparation when
   assumptions fail.

9. Higher bar for causality.
   Causal claims require stronger support than association claims: mechanism,
   temporal ordering, confounder handling, counterfactual logic, or an
   appropriate causal design.

10. Hostile self-review.
    Review should ask what would invalidate the whole study, whether claims
    match evidence, whether methods match implementation, and whether objectives
    were actually addressed.

## Engineering Principles

1. Strong generality.
   Avoid binding SciPlex to one discipline, dataset, API provider, model,
   statistical method, manuscript format, or execution environment.

2. Domain-neutral core.
   Keep the core abstractions generic: formulation, literature, method design,
   execution, evidence chains, review, state/event/object systems, and
   config/provider decoupling.

3. Strong decoupling.
   Keep formulation, literature, method design, execution, synthesis, review,
   writing, runtime state, and console visualization as separable modules with
   explicit contracts.

4. Minimal hardcoding.
   Do not hardcode domain assumptions, data locations, API names, model names,
   timeouts, file formats, or analysis choices unless they are defaults that can
   be overridden through configuration or objects.

5. Object-driven behavior.
   Research state should be driven by object state, event history, quality
   gates, and explicit transitions, not by an inflexible script sequence.

6. Stable protocols, replaceable tools.
   Object schemas, event schemas, state transitions, and method interfaces are
   the stable core. Search providers, analysis runners, visualization tools, and
   document exporters should be replaceable.

7. Clear interfaces.
   Every executable helper must document its input contract, output contract,
   side effects, required object fields, and failure behavior.

8. Configuration over code edits.
   API keys, provider selection, model names, iteration limits, timeouts, output
   formats, and workspace locations should be configurable.

9. Layered configuration.
   Project-level config in a research workspace overrides skill-level config;
   skill-level config overrides the driver agent environment and built-in
   defaults. The driver agent's LLM and SciPlex internal LLM providers must be
   treated as separate layers.

10. Explicit dependencies.
   Each phase should state which objects, files, tools, or credentials it
   depends on. Avoid hidden prerequisites.

11. Auditable side effects.
   Scripts that change research state should update the relevant objects,
   state index, event log, and console data or clearly document why they do not.

12. Backward-compatible evolution.
    When schemas or protocols change, preserve migration paths or document the
    version change clearly.

## Modification Rules

- Prefer improving reusable protocols and contracts over adding one-off
  behavior for a single example.
- When adding a script, keep it generic and object-driven.
- Scripts should handle bookkeeping, normalization, validation, provider access,
  and audit trails. They should not decide scientific meaning, evidence
  strength, research novelty, or final claims.
- When adding a new object type, update the object system, event examples,
  review rules, and console expectations as needed.
- When documenting a command or script, ensure the implementation exists.
- When promising automation, provide a concrete invocation path, not only
  pseudocode.
- Keep examples illustrative, not normative. Examples must not become hidden
  domain assumptions.
- Avoid letting examples from any single field dominate core documentation or
  become hidden defaults.
- Keep core schemas field-neutral. Put domain details under object `attributes`
  or optional domain modules.
- If a change introduces a hardcoded value, explain why it is necessary and how
  a user can override it.
- When adding config, document its precedence, secret-handling expectations,
  fallback behavior, and whether it belongs to project-level config or
  skill-level config.

## Non-Goals

- SciPlex is not a replacement for human scientific judgment.
- SciPlex should not fabricate literature, data, methods, citations, or results.
- SciPlex should not claim completion when evidence chains, quality gates, or
  objective coverage are incomplete.
- SciPlex should not be optimized for producing impressive prose at the expense
  of scientific validity.
