# Specify CLI Security Constitution

## 1. Trust Boundaries
- Treat CLI arguments, environment variables, project files, and integration metadata as untrusted input.
- Never assume generated content, manifest data, or user-supplied paths are safe without validation.
- Treat remote catalogs, download URLs, and ZIP archives from the network as untrusted until validated.

## 2. Authentication & Authorization Standards
- The CLI itself does not define an auth model; any future remote capability must rely on explicit external credentials and documented authorization checks.
- Local file operations must respect the active project root and must not cross into neighboring projects or parent directories.
- Credentials sourced from `~/.specify/auth.json`, `GITHUB_TOKEN`, `GH_TOKEN`, `token_env`, or `client_secret_env` must only be attached to the intended hosts and must never be forwarded to non-allowlisted redirect targets.
- Redirect handling for authenticated requests must strip `Authorization` when a request leaves the approved host set.

## 3. Data Isolation & Privacy Rules
- Project data must remain isolated to the initialized project root.
- Do not move, copy, or disclose user content outside the project without explicit intent from the command being executed.
- Never emit secrets, tokens, or private file contents in logs, banners, or error messages.

## 4. Secrets Management Policy
- Secrets must not be written into templates, manifests, or generated guidance files.
- If a command needs credentials, it must consume them from the user’s existing secure storage or environment rather than prompting the tool to persist them.
- Do not commit example values that look like live keys or private tokens.
- `~/.specify/auth.json` is sensitive configuration and must be treated as user-owned secret material; its host patterns must remain narrowly scoped and its permissions should be restricted to the owner when possible.

## 5. Secure-by-Design Patterns
- Resolve and validate all paths before file creation, deletion, or overwrite.
- Refuse symlink-based escapes and path traversal attempts.
- Use the least privileged mechanism available when invoking subprocesses or touching the file system.
- Preserve user-modified generated files unless the operation explicitly requires a forceful overwrite.
- Downloaded archives must be validated before extraction, and archive members must be checked so they cannot escape the intended extraction directory.
- Remote downloads must use HTTPS unless the code explicitly allows a localhost development exception.

## 6. API & Integration Security
- Any external network interaction must be opt-in and clearly documented.
- GitHub or other remote API helpers must keep credentials out of output and avoid broad-scoped operations when a narrower request is sufficient.
- Generated integration commands should not embed secrets or shell expansions that could expose sensitive data.
- Shared HTTP helpers should be used for authenticated GitHub access so token handling, host allowlisting, and redirect stripping stay centralized.
- Non-GitHub URLs must never receive GitHub credentials, even when a redirect chain is involved.

## 7. Audit, Logging & Monitoring Requirements
- Log enough context to diagnose failures, but never dump full environment variables, secrets, or unredacted sensitive files.
- Security-sensitive paths, manifest actions, and validation failures should be visible in logs or error output.
- Prefer deterministic error messages that help users correct unsafe input without exposing sensitive data.

## 8. Security Incident Response Triggers
- Block immediately on path traversal, symlink escape attempts, unexpected write destinations, or manifest tampering.
- Treat accidental secret disclosure, unauthorized file access, or auth bypass as release-blocking defects.

## 9. Compliance & Regulatory Mapping
- No formal compliance baseline is assumed yet.
- If a feature introduces compliance needs, document the applicable requirement in the feature spec and implementation plan before shipping.