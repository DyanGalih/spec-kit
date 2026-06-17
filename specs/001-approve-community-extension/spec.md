# Feature Specification: Approve Community Extension Install

**Feature Branch**: `001-approve-community-extension`

**Created**: 2026-06-16

**Status**: Draft

**Input**: User description: "I want to have a feature to make user easier to accept community extension use specify command to avoid error like this: specify extension add security-review Error: 'security-review' is available in the 'community' catalog but installation is not allowed from that catalog. To enable installation, add 'security-review' to an approved catalog (install_allowed: true) in .specify/extension-catalogs.yml. In the current implmenetation, we need to run it manual"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Guided Community Approval (Priority: P1)

As a user, I can approve a community extension from within the normal `specify extension add` flow so I do not have to edit catalog settings by hand.

**Why this priority**: This removes the main point of friction and turns a failed install into a recoverable guided flow.

**Independent Test**: Start with a project where the community catalog is not approved, request a community extension, approve the prompt, and verify the extension installs successfully without manual file editing.

**Acceptance Scenarios**:

1. **Given** an extension is available only from a catalog that is not approved for installation, **When** the user chooses to approve that catalog during the add flow, **Then** the system updates the project’s catalog settings and installs the extension.
2. **Given** an extension is already available from an approved catalog, **When** the user runs the add command, **Then** the system installs it without requiring additional approval.

---

### User Story 2 - Safe Rejection Path (Priority: P2)

As a user, I can decline approval for a community extension and keep my project configuration unchanged.

**Why this priority**: Users need a safe way to stop the flow when they are not ready to trust a community catalog.

**Independent Test**: Start with a blocked community extension, decline the approval prompt, and verify no install occurs and no catalog settings are modified.

**Acceptance Scenarios**:

1. **Given** a community extension requires approval, **When** the user declines approval, **Then** the extension is not installed and the catalog configuration remains unchanged.
2. **Given** the user cancels the approval flow before confirmation, **When** the command ends, **Then** the project still reflects the original approval state.

---

### User Story 3 - Clear Recovery Guidance (Priority: P3)

As a user, I can understand why an extension is blocked and what action will let me continue.

**Why this priority**: Clear guidance reduces confusion when the install cannot proceed immediately.

**Independent Test**: Request a blocked community extension and verify the command explains the approval requirement and the next step before the flow ends.

**Acceptance Scenarios**:

1. **Given** the requested extension is found in a catalog that is not approved for installation, **When** the command cannot proceed automatically, **Then** the user sees a clear explanation of why the install is blocked.
2. **Given** the extension name does not exist in any active catalog, **When** the user runs the add command, **Then** the system keeps the not-found outcome and does not suggest approving unrelated catalogs.

### Edge Cases

- The requested extension is already installed.
- The requested extension exists in both an approved catalog and the community catalog.
- The user approves the prompt, but the catalog settings cannot be saved.
- The approval flow is interrupted before the user confirms or declines.
- The requested extension is not found in any active catalog.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The add flow MUST detect when a requested extension is available only from a catalog that is not approved for installation.
- **FR-002**: When installation is blocked by catalog approval, the system MUST present a guided approval choice instead of requiring manual file editing as the primary path.
- **FR-003**: Before applying approval, the system MUST explain what catalog setting will change and that the change affects future installs from that catalog.
- **FR-004**: If the user confirms approval, the system MUST update the project’s catalog settings and continue the install flow for the requested extension.
- **FR-005**: If the user declines approval, the system MUST leave the project configuration unchanged and must not install the extension.
- **FR-006**: If the extension is available from at least one approved source, the system MUST install it without requiring the approval flow.
- **FR-007**: If the requested extension cannot be found in any active catalog, the system MUST preserve the not-found outcome and provide clear guidance that approval is not the issue.
- **FR-008**: The system MUST not broaden approval beyond the catalog scope needed for the install flow.
- **FR-009**: The approval experience MUST be reachable through the same command path users already use to add extensions.

### Key Entities *(include if feature involves data)*

- **Extension Request**: The requested extension name and the catalog source that can satisfy the request.
- **Catalog Approval**: The project-level permission state that determines whether a catalog may be used for installs.
- **Approval Decision**: The user’s choice to approve, decline, or cancel the guided install flow.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 90% of users who encounter a community-catalog approval block can complete the approval-and-install flow without manually editing project files.
- **SC-002**: Users can resolve a blocked community extension install in a single guided session in under 1 minute for the common case.
- **SC-003**: The approval flow reduces support requests or follow-up questions about manual catalog edits by at least 50% within one release cycle.
- **SC-004**: Users who install from already-approved catalogs complete the add flow with no additional approval step in 100% of those cases.

## Assumptions

- The approval applies at the project level and uses the existing catalog approval model.
- The feature is limited to community-catalog approval for extension installation and does not change trust rules for other catalogs.
- Users can still edit catalog settings manually if they prefer a non-guided path.
