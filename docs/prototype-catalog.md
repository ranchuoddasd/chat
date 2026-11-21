# Prototype Catalog

This catalog records the purpose and status of each prototype. Similar concepts are not treated as duplicates unless their behavior and dependencies have been compared.

| Path | Area | Notes |
|---|---|---|
| `docs/multi-source-ip-search-design.md` | Multi-source IP search design | Design guide with illustrative front-end/back-end examples and placeholder API settings. |
| `src/intent_parser.py` | Natural-language parsing | Python experiment for extracting IPs, time ranges, ports, protocols, and source/destination intent. |
| `src/ui/chat_interface.jsx` | React chat UI sketch | Minimal front-end workflow that invokes an IP-search helper. |
| `src/ui/streamlit_app.py` | Streamlit search concept | Multi-source search aggregation example with placeholder functions. |
| `src/api/fastapi_app.py` | FastAPI endpoint sketch | Request/response API with placeholder data; CORS is permissive and must be restricted before use. |
| `src/ui/security_query_assistant.jsx` | Security query assistant UI | React component for parsing investigation questions and displaying query previews. |
| `src/ui/configurable_query_assistant.jsx` | Configurable query assistant | Extended UI with editable connection fields; never enter real credentials in this browser-side configuration. |
| `examples/developer_console.html` | Developer-mode search UI | Request/response tab prototype. Uses unsafe HTML rendering patterns and must not display untrusted data as HTML. |
| `src/adapters/async_search.py` | Async API adapter sketch | Placeholder endpoints and tokens for external data-source adapters; currently calls sources sequentially. |

## Consolidation guidance

- The parser, API adapter, backend, and user-interface experiments represent different layers.
- `src/intent_parser.py` and the React assistants overlap in intent-parsing concepts but are not equivalent implementations.
- `src/api/fastapi_app.py` and `src/adapters/async_search.py` are separate backend sketches with different responsibilities.
- `examples/developer_console.html` is a presentation experiment.
- No prototype has been removed as a duplicate. Consolidation should follow tests that compare parsing behavior, query generation, and data contracts.

## Security notes

See [Security Review](security-review.md) for file-by-file risks and controls. These are experimental design sketches, not approved live integrations. Do not enter real credentials into browser-side configuration panels or expose operational network data in this public repository.
