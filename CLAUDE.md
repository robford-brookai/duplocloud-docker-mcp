# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

DuploCloud MCP server — exposes DuploCloud infrastructure management as tools consumable via Docker MCP Toolkit. Python 3.13, managed with uv. Wraps `duplocloud-client` (v0.4.0) which abstracts the DuploCloud REST API.

## Commands

```bash
# Dependencies
uv sync

# Run
uv run main.py

# Lint & format
uv run ruff check .
uv run ruff format .

# Tests
uv run pytest
uv run pytest --cov=duplocloud_mcp --cov-report=term-missing
uv run pytest tests/path/to/test_file.py::test_name  # single test
```

## Architecture

- `main.py` — Entrypoint, runs `mcp.run(transport="stdio")`
- `duplocloud_mcp/server.py` — `FastMCP("duplocloud")` instance, imports all tool modules to register them
- `duplocloud_mcp/client.py` — Singleton `DuploClient` wrapper, reads `DUPLO_HOST`, `DUPLO_TOKEN`, `DUPLO_TENANT` from env
- `duplocloud_mcp/errors.py` — `@handle_duplo_errors` decorator (catches `DuploError` → JSON), `validate_required()` helper
- `duplocloud_mcp/tools/` — 6 tool modules (tenants, services, hosts, databases, storage, containers), 31 tools total

### Key patterns

- Each tool is a sync function decorated with `@mcp.tool()` and `@handle_duplo_errors`
- Tenant-scoped resources require `tenant_id` — the client's `tenantid` attribute is set before loading the resource
- `duplocloud-client` resources are loaded via `client.load("resource_name")` (e.g. `"tenant"`, `"service"`, `"hosts"`, `"rds"`, `"s3"`, `"ecs"`)
- DuploCloud exceptions: `DuploError(message, code)`, `DuploFailedResource`, `DuploStillWaiting`

## Conventions

- uv for package management (no pip, no poetry)
- ruff for linting and formatting
- Follow MCP protocol patterns from `mcp` Python SDK
- All tool functions return JSON strings (via `handle_duplo_errors` decorator)
- Tests mock `get_client()` and the resource handlers
