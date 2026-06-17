# Implementation Plan: Approve Community Extension Install

**Branch**: `001-approve-community-extension` | **Date**: 2026-06-16 | **Spec**: [`spec.md`](./spec.md)

**Input**: Feature specification from [`specs/001-approve-community-extension/spec.md`](./spec.md)

## Summary

Allow users to resolve the current manual community-catalog approval step directly from the `specify extension add` flow. When an extension is blocked because its source catalog is not approved for installation, the command should offer a guided approval choice, persist the catalog setting only on confirmation, and keep the existing safe failure path when the user declines or the extension is not found.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Typer, Rich, PyYAML, packaging, pathspec

**Storage**: Project-local YAML config in `.specify/extension-catalogs.yml`

**Testing**: pytest with CLI integration tests in `src/tests/test_extensions.py`

**Target Platform**: Cross-platform CLI

**Project Type**: CLI application

**Performance Goals**: Preserve current add-flow responsiveness; approval prompts should not introduce noticeable delay for local project config writes

**Constraints**: Keep writes inside the project root, preserve existing install behavior for approved catalogs, do not broaden catalog approval beyond the intended catalog, continue to require HTTPS for remote catalog/download access

**Scale/Scope**: Single-command feature affecting extension install flows and catalog config updates for one project at a time

## Constitution Check

Status: Pass

Relevant constraints:

- Command handlers should stay thin and delegate reusable behavior to helper logic.
- Path validation must happen before file writes and remain scoped to the active project root.
- Extension catalog metadata remains the source of truth for install eligibility.
- User-customized generated files must not be overwritten without an explicit approval path.
- Remote catalog/download handling must continue to respect HTTPS and trust-boundary rules.

## Project Structure

### Documentation (this feature)

```text
specs/001-approve-community-extension/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── security-constraints.md
```

### Source Code

```text
src/src/specify_cli/__init__.py
src/src/specify_cli/extensions.py
src/src/specify_cli/catalogs.py
src/tests/test_extensions.py
```

**Structure Decision**: Keep user-facing orchestration in `src/src/specify_cli/__init__.py`, factor any reusable approval/catalog helper logic into `src/src/specify_cli/extensions.py`, and cover the new approval path with CLI regression tests in `src/tests/test_extensions.py`.

## Delivery Plan

1. Confirm the existing blocked-install branch in `extension_add()` and isolate the new approval decision from the current error-only path.
2. Add a guided approval step for catalogs where `_install_allowed` is false, including a clear explanation of what will change before saving any config.
3. Ensure the decline path leaves project config unchanged and exits cleanly without attempting installation.
4. Add or refine regression tests for:
   - blocked community extension install with approve
   - blocked community extension install with decline
   - approved catalog install still proceeds without extra prompts
   - not-found behavior remains unchanged
5. Update user-facing guidance if any command output or docs need to reflect the guided approval flow.

## Risks and Mitigations

- Risk: accidentally broadening approval beyond the source catalog. Mitigation: scope config updates to the specific catalog being approved and add a regression test for the exact catalog entry.
- Risk: confusing prompt ordering or output. Mitigation: keep the approval prompt before long-running work and mirror the existing confirmation patterns already used in the CLI.
- Risk: behavior drift between search/info/add flows. Mitigation: reuse existing catalog metadata and keep `search`/`info` output aligned with the new installation guidance.
