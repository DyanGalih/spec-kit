# Quickstart: Approve Community Extension Install

1. Start from a project that does not yet allow installs from the community catalog.
2. Run `specify extension add security-review`.
3. When the CLI explains that the extension is available from a catalog that is not approved for installation, choose to approve the catalog.
4. Confirm the command completes the install successfully.
5. Verify the project catalog settings were updated and the extension is now available.

## Decline path

1. Run the same add command for a blocked community extension.
2. Decline the approval prompt.
3. Confirm the extension is not installed and the project config is unchanged.

## Existing-approved path

1. Run `specify extension add <extension>` for an extension that already comes from an approved catalog.
2. Confirm the command installs it without asking for extra approval.
