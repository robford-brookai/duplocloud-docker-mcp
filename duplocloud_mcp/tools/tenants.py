from duplocloud_mcp.client import get_client
from duplocloud_mcp.errors import handle_duplo_errors, validate_required
from duplocloud_mcp.server import mcp


@mcp.tool()
@handle_duplo_errors
def tenant_list() -> str:
    """List all tenants accessible in the DuploCloud portal."""
    client = get_client()
    tenants = client.load("tenant")
    return tenants.list()


@mcp.tool()
@handle_duplo_errors
def tenant_get(name: str) -> str:
    """Get details of a specific DuploCloud tenant by name.

    Args:
        name: The tenant name to look up.
    """
    validate_required(name, "Tenant name")
    client = get_client()
    tenants = client.load("tenant")
    return tenants.find(name)


@mcp.tool()
@handle_duplo_errors
def tenant_create(account_name: str, plan_id: str) -> str:
    """Create a new DuploCloud tenant.

    Args:
        account_name: Name for the new tenant.
        plan_id: The infrastructure plan ID to associate with.
    """
    validate_required(account_name, "Account name")
    validate_required(plan_id, "Plan ID")
    client = get_client()
    tenants = client.load("tenant")
    body = {"AccountName": account_name, "PlanID": plan_id}
    return tenants.create(body)


@mcp.tool()
@handle_duplo_errors
def tenant_delete(name: str) -> str:
    """Delete a DuploCloud tenant by name.

    Args:
        name: The tenant name to delete.
    """
    validate_required(name, "Tenant name")
    client = get_client()
    tenants = client.load("tenant")
    return tenants.delete(name)
