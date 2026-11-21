# Prototype Catalog

This catalog describes the existing experiments without assuming they are duplicates. They remain separate until behavior and dependencies have been compared.

| File | Area | Notes |
|---|---|---|
| `Gro-Chat` | Multi-source IP search dashboard concept | Documentation and sample front-end/back-end approaches for aggregating search results. Contains placeholder API settings. |
| `Man-Chat` | Natural-language parsing and query generation | Python experiment for extracting IPs, time ranges, ports, protocols, and source/destination intent. |
| `Per-Chat-1` | React chat UI sketch | Minimal front-end workflow that invokes an IP-search helper. |
| `Per-Chat-2` | Streamlit search concept | Multi-source search aggregation example; contains placeholder functions. |
| `Per-chat` | FastAPI endpoint sketch | Demonstrates a request/response API with placeholder data. CORS is permissive and should be restricted before use. |
| `chatbot` | Security query assistant UI | React component for parsing investigation questions and displaying query previews. |
| `clau-chat` | Configurable query assistant variant | Extended UI with configuration fields; do not place secrets in client-side configuration. |
| `deep-chat` | Developer-mode search UI | Prototype showing request/response tabs; contains incomplete references and unsafe HTML rendering patterns. |
| `per-chat-tue` | FastAPI adapter experiment | Sample async API calls to external data sources with placeholder endpoints and tokens. This file previously included an organization-specific title; public portfolio documentation should remain generic. |

## Consolidation guidance
- The parsing/query-generation experiments and the dashboard/UI experiments are different layers.
- `Man-Chat` and `chatbot`/`clau-chat` may share intent-parsing concepts but differ in implementation and UI.
- `Per-chat` and `per-chat-tue` are backend sketches with different levels of integration.
- `deep-chat` is a developer presentation experiment.
- No file has been removed based only on names or high-level similarity. Perform a line-level and behavior-level comparison before consolidating.
