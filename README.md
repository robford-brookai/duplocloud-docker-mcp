# DuploCloud Docker MCP Server

MCP server that exposes DuploCloud infrastructure management as tools consumable via Docker MCP Toolkit.

## Tools (31 total)

| Category | Tools |
|----------|-------|
| **Tenants** | `tenant_list`, `tenant_get`, `tenant_create`, `tenant_delete` |
| **Services** | `service_list`, `service_get`, `service_create`, `service_update`, `service_delete`, `service_restart` |
| **Hosts** | `host_list`, `host_get`, `host_create`, `host_delete`, `host_reboot` |
| **Databases** | `database_list`, `database_get`, `database_create`, `database_update`, `database_delete` |
| **Storage** | `bucket_list`, `bucket_get`, `bucket_create`, `bucket_update`, `bucket_delete` |
| **Containers** | `ecs_service_list`, `ecs_task_def_list`, `ecs_task_list`, `ecs_task_run`, `ecs_service_update`, `ecs_service_delete` |

## Setup

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- DuploCloud portal access with an API token

### Environment Variables

```bash
export DUPLO_HOST=https://your-company.duplocloud.net
export DUPLO_TOKEN=your-api-token
export DUPLO_TENANT=default  # optional
```

### Install & Run

```bash
uv sync
uv run main.py
```

### Docker

```bash
docker build -f docker/Dockerfile -t duplocloud-mcp .
docker run -i --rm \
  -e DUPLO_HOST=https://your-company.duplocloud.net \
  -e DUPLO_TOKEN=your-api-token \
  duplocloud-mcp
```

### Docker MCP Toolkit

```bash
docker mcp server add duplocloud-mcp
```

## Tool Reference

### Tenants

| Tool | Parameters | Description |
|------|-----------|-------------|
| `tenant_list` | — | List all tenants accessible in the DuploCloud portal |
| `tenant_get` | `name` | Get details of a specific tenant by name |
| `tenant_create` | `account_name`, `plan_id` | Create a new tenant |
| `tenant_delete` | `name` | Delete a tenant by name |

### Services

| Tool | Parameters | Description |
|------|-----------|-------------|
| `service_list` | `tenant_id` | List all services in a tenant |
| `service_get` | `tenant_id`, `name` | Get details of a specific service |
| `service_create` | `tenant_id`, `name`, `image`, `replicas=1` | Create a new service |
| `service_update` | `tenant_id`, `name`, `image?`, `replicas?` | Update service image and/or replicas |
| `service_delete` | `tenant_id`, `name` | Delete a service |
| `service_restart` | `tenant_id`, `name` | Restart a service (rolling redeployment) |

### Hosts

| Tool | Parameters | Description |
|------|-----------|-------------|
| `host_list` | `tenant_id` | List all hosts (VMs) in a tenant |
| `host_get` | `tenant_id`, `name` | Get details of a specific host |
| `host_create` | `tenant_id`, `friendly_name`, `capacity`, `agent_platform=0` | Create a new host (0=Linux Docker, 7=EKS Linux) |
| `host_delete` | `tenant_id`, `name` | Terminate a host |
| `host_reboot` | `tenant_id`, `name` | Reboot a host |

### Databases

| Tool | Parameters | Description |
|------|-----------|-------------|
| `database_list` | `tenant_id` | List all RDS instances in a tenant |
| `database_get` | `tenant_id`, `name` | Get details of an RDS instance |
| `database_create` | `tenant_id`, `identifier`, `engine`, `size`, `master_username="master"`, `master_password?` | Create an RDS instance |
| `database_update` | `tenant_id`, `name`, `size?` | Resize an RDS instance |
| `database_delete` | `tenant_id`, `name` | Delete an RDS instance |

### Storage

| Tool | Parameters | Description |
|------|-----------|-------------|
| `bucket_list` | `tenant_id` | List all S3 buckets in a tenant |
| `bucket_get` | `tenant_id`, `name` | Get details of an S3 bucket |
| `bucket_create` | `tenant_id`, `name` | Create a new S3 bucket |
| `bucket_update` | `tenant_id`, `name`, `versioning?` | Update bucket configuration (versioning) |
| `bucket_delete` | `tenant_id`, `name` | Delete an S3 bucket |

### Containers (ECS)

| Tool | Parameters | Description |
|------|-----------|-------------|
| `ecs_service_list` | `tenant_id` | List all ECS services in a tenant |
| `ecs_task_def_list` | `tenant_id` | List all ECS task definition families |
| `ecs_task_list` | `tenant_id`, `service_name` | List running tasks for a service |
| `ecs_task_run` | `tenant_id`, `family_name`, `replicas=1` | Run a task from a task definition family |
| `ecs_service_update` | `tenant_id`, `name`, `image` | Update the image of an ECS service |
| `ecs_service_delete` | `tenant_id`, `name` | Delete an ECS service |

## Troubleshooting

### Missing environment variables

```
DuploError: DUPLO_HOST environment variable is required
```

Set `DUPLO_HOST` and `DUPLO_TOKEN` before running. See `.env.example`.

### Invalid or expired token

```
{"error": "Unauthorized", "code": 401}
```

Generate a new API token from the DuploCloud portal: **User menu > Security > API Token**.

### Tenant not found

```
{"error": "Tenant 'xyz' not found", "code": 404}
```

Verify the tenant name with `tenant_list`. Tenant names are case-sensitive.

### Connection refused

```
{"error": "Unexpected error: Connection refused", "code": 500}
```

Verify `DUPLO_HOST` is correct and the DuploCloud portal is reachable from your network.

## Development

```bash
# Install with dev dependencies
uv sync

# Lint & format
uv run ruff check .
uv run ruff format .

# Tests
uv run pytest
uv run pytest --cov=duplocloud_mcp --cov-report=term-missing

# Single test
uv run pytest tests/test_tools/test_services.py::test_service_list
```

## Architecture

```
main.py                          # Entrypoint: mcp.run(transport="stdio")
duplocloud_mcp/
  server.py                      # FastMCP instance, imports tool modules
  client.py                      # DuploClient singleton wrapper
  errors.py                      # Error decorator, validators
  tools/
    tenants.py                   # Tenant CRUD tools
    services.py                  # Service CRUD + restart tools
    hosts.py                     # Host CRUD + reboot tools
    databases.py                 # RDS database CRUD tools
    storage.py                   # S3 bucket CRUD tools
    containers.py                # ECS service/task tools
```

Each tool module imports the shared `mcp` instance from `server.py` and registers tools via `@mcp.tool()`. The `@handle_duplo_errors` decorator translates DuploCloud exceptions into structured JSON error responses. The `duplocloud-client` library handles all REST API communication.

## License

MIT
