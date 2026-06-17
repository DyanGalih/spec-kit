# Data Model: Approve Community Extension Install

## Extension Request

- **Purpose**: Represents the requested extension the user wants to install
- **Key attributes**: extension name or ID, resolved extension ID, display name, source catalog name, install eligibility
- **Relationships**: maps to one or more catalog sources, may resolve to an approved or blocked source

## Catalog Source

- **Purpose**: Represents one active catalog in the project or user config
- **Key attributes**: catalog name, URL, priority, install permission, description
- **Relationships**: may contain many extensions; one extension may appear in multiple catalogs

## Approval Decision

- **Purpose**: Captures the user's response when installation is blocked by catalog approval
- **Key attributes**: approve, decline, or cancel
- **Relationships**: when approved, applies to the specific catalog source that triggered the block

## Project Catalog Config

- **Purpose**: Stores the active approval state used by extension installs
- **Key attributes**: catalog list, approval flag per catalog, catalog URL, priority, description
- **Relationships**: read by extension discovery and install flows; updated only when the user confirms approval
