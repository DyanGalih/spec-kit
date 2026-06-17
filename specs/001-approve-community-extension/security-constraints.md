# Security Constraints: Approve Community Extension Install

## Trust Boundaries

- Treat catalog metadata, extension names, and project config as untrusted input.
- Keep approval scoped to the specific catalog that triggered the install block.
- Do not allow approval to widen trust to unrelated catalogs or future catalog additions.

## File-System Safety

- Only write inside the active project root.
- Update `.specify/extension-catalogs.yml` through validated path handling.
- Do not follow symlinks or allow traversal outside the project when persisting approval state.

## Network and Download Safety

- Preserve existing HTTPS requirements for remote catalogs and downloads.
- Do not add new network behavior to the approval step itself.
- Keep download/install behavior unchanged for already-approved catalogs.

## User Safety

- Make the approval choice explicit so the user understands they are changing future install permissions.
- Leave the project unchanged if the user declines or cancels.
- Keep the not-found path separate so the command does not suggest approving unrelated catalogs.
