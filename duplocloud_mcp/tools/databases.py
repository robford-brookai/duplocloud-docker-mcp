from duplocloud_mcp.client import get_client
from duplocloud_mcp.errors import handle_duplo_errors, validate_required
from duplocloud_mcp.server import mcp


def _get_rds_resource(tenant_id: str):
    """Get an RDS resource configured for the given tenant."""
    validate_required(tenant_id, "Tenant ID")
    client = get_client()
    client.tenantid = tenant_id.strip()
    return client.load("rds")


@mcp.tool()
@handle_duplo_errors
def database_list(tenant_id: str) -> str:
    """List all RDS database instances in a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID to list databases for.
    """
    rds = _get_rds_resource(tenant_id)
    return rds.list()


@mcp.tool()
@handle_duplo_errors
def database_get(tenant_id: str, name: str) -> str:
    """Get details of a specific RDS database instance.

    Args:
        tenant_id: The tenant ID containing the database.
        name: The database instance identifier.
    """
    validate_required(name, "Database name")
    rds = _get_rds_resource(tenant_id)
    return rds.find(name)


@mcp.tool()
@handle_duplo_errors
def database_create(
    tenant_id: str,
    identifier: str,
    engine: str,
    size: str,
    master_username: str = "master",
    master_password: str | None = None,
) -> str:
    """Create a new RDS database instance in a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID to create the database in.
        identifier: The database instance identifier.
        engine: Database engine (e.g. mysql, postgres, mariadb).
        size: Instance class (e.g. db.t3.micro).
        master_username: Master database username. Defaults to 'master'.
        master_password: Master database password. Required for most engines.
    """
    validate_required(identifier, "Database identifier")
    validate_required(engine, "Database engine")
    validate_required(size, "Instance size")
    rds = _get_rds_resource(tenant_id)
    body = {
        "Identifier": identifier,
        "Engine": engine,
        "SizeEx": size,
        "MasterUsername": master_username,
    }
    if master_password:
        body["MasterPassword"] = master_password
    return rds.create(body)


@mcp.tool()
@handle_duplo_errors
def database_update(tenant_id: str, name: str, size: str | None = None) -> str:
    """Update an RDS database instance. Currently supports resizing.

    Args:
        tenant_id: The tenant ID containing the database.
        name: The database instance identifier.
        size: New instance class (e.g. db.t3.small).
    """
    validate_required(name, "Database name")
    rds = _get_rds_resource(tenant_id)
    if size:
        return rds.set_instance_size(name, size)
    return {"error": "Provide at least one field to update (size)", "code": 400}


@mcp.tool()
@handle_duplo_errors
def database_delete(tenant_id: str, name: str) -> str:
    """Delete an RDS database instance from a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID containing the database.
        name: The database instance identifier to delete.
    """
    validate_required(name, "Database name")
    rds = _get_rds_resource(tenant_id)
    return rds.delete(name)
