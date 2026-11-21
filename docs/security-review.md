# Security Review

**Review scope:** Static inspection of the prototype files on the default branch. No live endpoints were contacted and no credentials were tested.

## Findings

| File | Observation | Portfolio-safe status |
|---|---|---|
| `Gro-Chat` | Contains instructional API configuration examples with placeholder credentials and sample private-range IP addresses. The sample curl command uses `-k`, which disables TLS certificate verification. The sample backend builds a search expression from user input without demonstrating strict IP validation or query-safe construction. | Keep as a design guide only. Replace `-k` with normal certificate validation and validate/parameterize all inputs before any real integration. |
| `clau-chat` | The UI builds connection details and command examples from editable configuration state. Authentication values can therefore appear in generated request/curl previews. Host placeholders use generic example domains. | Do not enter real tokens or credentials. Move integrations to a backend and return redacted request previews only. |
| `deep-chat` | Uses `innerHTML` to render response/error content and request snippets. Untrusted response text could become executable markup. | Use `textContent` or safe DOM construction for data; escape code before display. |
| `Per-chat` | FastAPI sketch has permissive CORS and no authentication/authorization layer. | Local prototype only; restrict CORS and add access controls before deployment. |
| `per-chat-tue` | Adapter sketch uses placeholder endpoints/tokens and accepts IP parameters without demonstrating validation. Calls are sequential despite the comment describing concurrent querying. | Adapter concept only; validate IPs, configure secrets server-side, add explicit timeout/error handling, and use bounded concurrency. |
| `Man-Chat`, `Per-Chat-1`, `Per-Chat-2`, `chatbot` | Contain sample IP addresses in private address ranges. These appear as demonstration inputs, not evidence of a real network inventory. | Keep only synthetic examples; do not replace them with operational addresses or customer data. |

## Credential scan

A static pattern scan did not identify an obvious non-placeholder credential in the reviewed source files. It did identify instructional placeholder fields such as `your-username`, `YOUR_*_TOKEN`, and generic host examples. This is not a substitute for Git history secret scanning or credential rotation if a real secret was ever committed.

## Required controls before any live integration

1. Keep tokens, passwords, and API keys in server-side environment variables or a secrets manager.
2. Never return credentials in browser JSON, generated curl commands, logs, or UI state.
3. Validate IPv4/IPv6 inputs and constrain query construction to allow-listed fields/operators.
4. Keep TLS certificate verification enabled.
5. Escape all remote data before rendering; prefer text nodes over `innerHTML`.
6. Restrict CORS, authenticate callers, authorize each data source, and apply rate limits.
7. Use synthetic fixtures for public demos and remove operational topology, logs, hostnames, and identifiers.
8. Add unit tests for parsing, validation, query construction, and hostile input cases.

## Review limitations

This was a source-level review only. No runtime, dependency, penetration, secret-history, or integration testing was performed. Treat every prototype as experimental until those checks are completed.
