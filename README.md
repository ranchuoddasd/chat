# Network Security AI Assistant

A collection of prototypes exploring natural-language network investigations, IP-address lookup, intent extraction, and query generation for network telemetry and security data sources.

> **Status:** Experimental portfolio project. These files are design explorations and are not production-ready. No live integrations are provided by default.

## Goals
- Translate natural-language questions into structured network-search intent.
- Extract IP addresses, source/destination, ports, protocols, and time windows.
- Generate query examples for log and network data sources.
- Explore user interfaces for conversational and developer-oriented investigation workflows.
- Illustrate how independent data-source adapters could be orchestrated and normalized.

## Prototype inventory
See [Prototype Catalog](docs/prototype-catalog.md) for the existing variants and their purpose.

## Architecture concept
1. **Input** — natural-language question or IP address.
2. **Intent parsing** — identify IPs, direction, ports, protocol, and time range.
3. **Query generation** — produce source-specific query examples.
4. **Adapter layer** — optional, separately configured integrations.
5. **Normalization** — standardize results into a common structure.
6. **Presentation** — show intent, query previews, and results in a UI.

The current repository contains different experiments and partial implementations. They are not connected into one runnable application.

## Security review
See [Security Review](docs/security-review.md) for a static review of credential handling, query construction, browser rendering, CORS, and adapter limitations. No live integrations or runtime tests were performed.

## Safety and configuration
- Use synthetic IP addresses, log events, and API responses in examples.
- Never commit credentials, API tokens, internal endpoints, private topology, customer data, or organization-specific details.
- Validate user input and encode query parameters before sending requests.
- Treat generated queries as previews. Review and approve them before execution.
- Keep integrations behind a backend; do not expose secrets in browser code.
- Add authentication, authorization, rate limits, timeout handling, and audit logging before any real deployment.

## Limitations
- Intent extraction uses basic patterns and may misinterpret ambiguous text.
- Query examples and API integrations are placeholders.
- Several files are overlapping experiments; similarity in names or signatures does not prove equivalence.
- No comprehensive automated tests or end-to-end integration tests are included.

## Roadmap
- Consolidate shared intent extraction and validation into a reusable module.
- Add unit tests for parsing, edge cases, and query generation.
- Replace browser-side credentials/configuration with server-side environment configuration.
- Add typed adapter interfaces and structured per-source error reporting.
- Provide a mock-data mode and a safe query-preview workflow.
- Compare variants by behavior before merging or removing any files.

## License
No license is currently provided. Until one is added, reuse and redistribution are not granted by default.
