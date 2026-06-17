# Specify CLI Architecture Constitution

## 1. Architecture Style
Specify CLI follows a layered Python CLI architecture:
- entrypoints and Typer command modules orchestrate user flows
- shared runtime helpers own reusable orchestration logic
- integration subpackages own agent-specific setup, dispatch, and teardown behavior
- template, asset, manifest, and state modules provide shared infrastructure

## 2. Layer Boundaries
- `src/specify_cli/commands/` modules must orchestrate flows and delegate reusable work to helper modules.
- `src/specify_cli/integrations/` owns all integration-specific behavior.
- `_assets`, `_utils`, `_console`, `_agent_config`, `integration_state`, and `integration_runtime` are shared support layers and must not contain integration-specific branching when a dedicated integration class can own it.
- Public registry and manifest mechanisms are the supported coordination points between commands and integrations.

## 3. Business Logic Placement
- Integration-specific setup, teardown, and dispatch logic belongs in integration classes.
- Cross-integration behavior belongs in shared helpers or registry code, not duplicated in command modules.
- Command handlers should remain thin and defer file generation, path validation, and manifest handling to the appropriate helper or integration layer.

## 4. Contracts & Validation
- All external input is untrusted and must be validated at the boundary.
- Paths must be resolved relative to the project root before writing or deleting files.
- Generated command invocations must follow the active integration’s separator and naming contract.
- Registry, manifest, and state files are contracts; their shapes must remain stable unless a migration is explicitly designed and tested.

## 5. Data Access Rules
- `INTEGRATION_REGISTRY` is the source of truth for available integrations.
- Integration manifests are the source of truth for installed files and their hashes.
- Integration state files are the source of truth for selected or installed integration settings.
- No module may invent an alternate registry or tracking file for the same responsibility.

## 6. Async & Integration Rules
- Subprocess execution must remain explicit and isolated to the integration dispatch path or other approved helpers.
- Streaming and captured execution modes must preserve the same command contract, differing only in output handling.
- Network access should not be introduced into the normal init or command path unless the feature explicitly requires it.

## 7. Module Boundaries
- Integration subpackages must remain self-contained and use Python-safe package names internally.
- Built-in integrations must be registered centrally and in alphabetical order.
- Registry changes require matching integration tests and should preserve the existing discovery pattern.
- Template resolution should continue to use the bundled core pack and source checkout fallback model.

## 8. Framework-Specific Architecture Rules
For this project, the framework-specific rule set is CLI-specific:
- Typer command definitions own CLI surface area.
- Integration classes own agent-specific command files, context files, and setup conventions.
- Manifest-managed file generation must continue to honor project-local customizations.

## 9. Blocking Architecture Violations (P0)
- Writing outside the project root.
- Following symlinks when performing manifest or install operations in a way that can escape project boundaries.
- Bypassing the manifest for tracked integration files.
- Hard-coding integration behavior in command modules when an integration class should own it.
- Registering integrations inconsistently or breaking registry ordering and discovery.
- Overwriting user-customized generated files without an explicit force or refresh path.

## 10. Architecture Evolution Policy
- New architecture rules must be proposed explicitly before implementation changes become the norm.
- Prefer extending existing layers and contracts over introducing parallel abstractions.
- If a new integration deviates from standard patterns, encapsulate the deviation in a dedicated integration subclass or helper rather than scattering special cases.

## 11. Refactor & Drift Handling
- Repeated drift should be corrected by updating the relevant architecture rule and then aligning the code.
- Refactors should preserve command contracts, manifest semantics, and generated file locations unless the change is intentionally breaking.
- Any migration that changes installed file layout, registry keys, or context-file handling must include tests and upgrade guidance.