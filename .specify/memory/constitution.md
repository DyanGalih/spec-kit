# Specify CLI Constitution

## 1. Project Identity
Specify CLI is a Python 3.11+ command-line tool that bootstraps and maintains Spec Kit projects. It is intentionally file-system driven, template-based, and agent-integration focused.

## 2. Engineering Philosophy
- Prefer small, explicit changes over broad refactors.
- Keep command behavior deterministic and reproducible from bundled assets.
- Preserve user customizations unless the user explicitly requests overwrite or refresh behavior.
- Treat generated scaffolding as project infrastructure, not throwaway output.
- Avoid introducing new dependencies or network reliance unless the feature requires them.

## 3. Security Expectations
- Treat all CLI input, project files, and environment data as untrusted.
- Validate paths before writing and never allow operations to escape the project root.
- Never log secrets, tokens, or private file contents.
- Preserve manifest-tracked user edits during uninstall and upgrade flows.

## 4. Testing Expectations
- New behavior must be covered by tests at the narrowest useful level.
- CLI changes that affect user-visible flows require command-level regression coverage.
- Bug fixes must add a regression test that fails before the fix and passes after it.
- File-system behavior must be tested for both happy path and safety checks where relevant.

## 5. Documentation Standards
- Keep README, AGENTS, template notes, and command docs aligned with actual behavior.
- When templates or commands change, update the corresponding user-facing guidance in the same change set when practical.
- Document installation, upgrade, and integration behavior in the relevant docs rather than relying on code comments alone.

## 6. Review Process
- Review changes for behavior, compatibility, and safety before merging.
- Prefer reviews that verify user-facing commands, generated files, and uninstall/upgrade paths.
- Changes that affect file placement, templates, or integration registration must be checked against existing conventions.

## 7. High-Level Architecture Intent
Detailed architecture rules live in [architecture_constitution.md](architecture_constitution.md).
This constitution sets governance and quality expectations; the architecture file defines enforceable layer boundaries and implementation contracts.

## 8. Governance and Evolution Policy
- This constitution is the source of truth for project-wide engineering norms.
- Any change to governance rules must be intentional, documented, and accompanied by a migration path when behavior changes.
- Architecture drift should be corrected through explicit updates to the architecture constitution rather than ad hoc code changes.

**Version**: 1.0.0 | **Ratified**: 2026-05-28 | **Last Amended**: 2026-05-28
