# Tasks: Approve Community Extension Install

**Input**: Design documents from `/specs/001-approve-community-extension/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, security-constraints.md

**Tests**: Included because this feature changes a user-facing CLI flow and needs regression coverage.

**Organization**: Tasks are grouped by user story so each story can be implemented and verified independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story the task belongs to
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the current extension-add flow, approval metadata, and test seams before changing behavior.

- [x] T001 Review the blocked-install branch in `src/src/specify_cli/__init__.py` and the catalog metadata flow in `src/src/specify_cli/extensions.py` to confirm the existing approval gate and identify the smallest change surface.
- [x] T002 [P] Add or update any small reusable helper needed to persist catalog approval safely in `src/src/specify_cli/extensions.py` while keeping project-root validation and catalog scoping intact.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish the shared approval decision path before story-specific behavior is split out.

- [x] T003 Extract the guided approval decision path from the current hard-error branch in `src/src/specify_cli/__init__.py` so the add command can branch into approve, decline, or cancel outcomes.
- [x] T004 [P] Keep the approval write scoped to the triggering catalog entry in `.specify/extension-catalogs.yml` and preserve existing approved-catalog install behavior in `src/src/specify_cli/extensions.py`.
- [x] T005 Add regression test scaffolding in `src/tests/test_extensions.py` for the blocked approval flow, approved catalog install, and not-found lookup cases shared across the user stories.

**Checkpoint**: The add flow can now distinguish approval-required installs from normal installs, declines, and missing extensions.

---

## Phase 3: User Story 1 - Guided Community Approval (Priority: P1) 🎯 MVP

**Goal**: Let users approve a blocked community extension from the normal `specify extension add` flow and complete the install without manual config editing.

**Independent Test**: Run `specify extension add security-review` against a project where the community catalog is not approved, choose approval, and verify the install succeeds and the catalog config is updated.

### Tests for User Story 1

- [x] T006 [P] [US1] Add a CLI regression test in `src/tests/test_extensions.py` that approves a blocked community extension install and verifies `.specify/extension-catalogs.yml` is updated for the triggering catalog only.
- [x] T007 [P] [US1] Add a CLI regression test in `src/tests/test_extensions.py` that confirms an already-approved catalog still installs without the new approval prompt.

### Implementation for User Story 1

- [x] T008 [US1] Update `src/src/specify_cli/__init__.py` so `extension add` presents a clear approval explanation when `_install_allowed` is false and continues the flow only after explicit confirmation.
- [x] T009 [US1] Update `src/src/specify_cli/extensions.py` to apply the catalog approval change safely within the active project root and only for the catalog that triggered the block.
- [x] T010 [US1] Keep the install path unchanged for approved catalogs in `src/src/specify_cli/__init__.py` so successful installs still proceed directly to download and install.

**Checkpoint**: A user can approve the blocked community catalog and complete the install in one guided session.

---

## Phase 4: User Story 2 - Safe Rejection Path (Priority: P2)

**Goal**: Let users decline approval and exit without changing project configuration or installing anything.

**Independent Test**: Run the blocked add command, decline approval, and verify the extension is not installed and the catalog configuration remains unchanged.

### Tests for User Story 2

- [x] T011 [P] [US2] Add a CLI regression test in `src/tests/test_extensions.py` that declines a blocked community extension approval and verifies no config changes are written.
- [x] T012 [P] [US2] Add a CLI regression test in `src/tests/test_extensions.py` that cancels the approval prompt and confirms the command exits cleanly without installation.

### Implementation for User Story 2

- [x] T013 [US2] Ensure the decline/cancel branches in `src/src/specify_cli/__init__.py` leave the project configuration unchanged and stop before download or install work begins.
- [x] T014 [US2] Keep user-facing output in `src/src/specify_cli/__init__.py` explicit about the consequence of declining so the flow remains understandable and reversible.

**Checkpoint**: Declining or canceling the approval prompt leaves the project exactly as it was.

---

## Phase 5: User Story 3 - Clear Recovery Guidance (Priority: P3)

**Goal**: Make the blocked-install message understandable so users know why the install stopped and what the guided path changes.

**Independent Test**: Trigger a blocked community extension install and verify the command explains the approval requirement, the scope of the change, and the not-found case remains separate.

### Tests for User Story 3

- [x] T015 [P] [US3] Add a CLI regression test in `src/tests/test_extensions.py` that verifies the blocked-install message explains the catalog approval requirement and does not suggest manual file editing as the primary path.
- [x] T016 [P] [US3] Add a CLI regression test in `src/tests/test_extensions.py` that preserves the existing not-found behavior when the extension is absent from all active catalogs.

### Implementation for User Story 3

- [x] T017 [US3] Refine the blocked-install messaging in `src/src/specify_cli/__init__.py` so it clearly distinguishes approval-required failures from not-found failures.
- [x] T018 [US3] Review user-facing extension guidance in `specs/001-approve-community-extension/quickstart.md` and update it if the install flow text needs to match the new guided approval path.

**Checkpoint**: The failure path is clear, bounded, and consistent with the approval model.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Finish validation and align supporting docs or review notes.

- [x] T019 [P] Run focused regression coverage in `src/tests/test_extensions.py` for approve, decline, approved-catalog, and not-found scenarios.
- [x] T020 [P] Confirm the task list and security constraints in `specs/001-approve-community-extension/security-constraints.md` still match the implemented design.
- [x] T021 [P] Add a filesystem-safety regression test in `src/tests/test_extensions.py` that verifies approval writes stay inside the project root and fail closed on traversal or symlink-based path escapes.
- [x] T022 [P] Add a prompt-order regression test in `src/tests/test_extensions.py` that proves the approval prompt appears before any spinner or long-running install work starts.
- [x] T023 Review whether `specs/001-approve-community-extension/quickstart.md` needs any wording updates after implementation.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion and blocks user story work
- **User Stories (Phases 3+)**: Depend on Foundational completion
- **Polish (Phase 6)**: Depends on the desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after the foundational approval path is in place
- **User Story 2 (P2)**: Starts after the same foundational approval path
- **User Story 3 (P3)**: Starts after the same foundational approval path

### Parallel Opportunities

- T002 can run in parallel with T001 because it touches a different file.
- T004 and T005 can run in parallel once the approval branch shape is clear.
- The test tasks in each story can run in parallel with each other if they target different cases.

## Implementation Strategy

### MVP First

1. Complete Setup and Foundational tasks.
2. Deliver User Story 1 so blocked community installs can be approved and completed.
3. Validate with the approve-path regression test before moving on.

### Incremental Delivery

1. Add the approval flow.
2. Add the decline/cancel safety path.
3. Tighten the failure messaging and keep not-found behavior unchanged.
4. Finish with docs and regression verification.

## Notes

- Keep tasks scoped to the existing extension add flow and catalog approval model.
- Avoid introducing a new approval file or a new trust model.
- Preserve the current approved-catalog install path without extra prompts.
