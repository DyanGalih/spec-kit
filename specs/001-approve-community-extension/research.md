# Research: Approve Community Extension Install

## Findings

- The current `specify extension add` flow already resolves catalog metadata and checks `_install_allowed` before download/install.
- The current behavior for blocked community extensions is a hard error that tells the user to edit `.specify/extension-catalogs.yml` manually.
- `ExtensionCatalog.get_extension_info()` already returns `_catalog_name` and `_install_allowed`, so the approval decision can be made without new catalog lookup behavior.
- `extension search` and `extension info` already surface catalog installability, which gives a consistent user-facing model to reuse in the add flow.
- The project already stores catalog approval state in `.specify/extension-catalogs.yml`, so the feature can persist a project-local change instead of introducing a new state file.

## Implications

- The new flow should be implemented as a guided decision in the CLI command layer, with helper logic only where it reduces duplication.
- The not-found path should stay distinct from the approval path so unrelated catalogs are not suggested when an extension is absent.
- Approval should remain catalog-scoped, because the existing model is explicitly per catalog and per project.
