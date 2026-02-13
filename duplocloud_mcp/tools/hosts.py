from duplocloud_mcp.client import get_client
from duplocloud_mcp.errors import handle_duplo_errors, validate_required
from duplocloud_mcp.server import mcp


def _get_host_resource(tenant_id: str):
    """Get a hosts resource configured for the given tenant."""
    validate_required(tenant_id, "Tenant ID")
    client = get_client()
    client.tenantid = tenant_id.strip()
    return client.load("hosts")


@mcp.tool()
@handle_duplo_errors
def host_list(tenant_id: str) -> str:
    """List all hosts (virtual machines) in a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID to list hosts for.
    """
    hosts = _get_host_resource(tenant_id)
    return hosts.list()


@mcp.tool()
@handle_duplo_errors
def host_get(tenant_id: str, name: str) -> str:
    """Get details of a specific host by name.

    Args:
        tenant_id: The tenant ID containing the host.
        name: The host name to look up.
    """
    validate_required(name, "Host name")
    hosts = _get_host_resource(tenant_id)
    return hosts.find(name)


@mcp.tool()
@handle_duplo_errors
def host_create(tenant_id: str, friendly_name: str, capacity: str, agent_platform: int = 0) -> str:
    """Create a new host (VM) in a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID to create the host in.
        friendly_name: A friendly name for the host.
        capacity: The instance type/size (e.g. t3.medium).
        agent_platform: The agent platform type. 0=Linux Docker, 7=EKS Linux. Defaults to 0.
    """
    validate_required(friendly_name, "Friendly name")
    validate_required(capacity, "Instance capacity/type")
    hosts = _get_host_resource(tenant_id)
    body = {
        "FriendlyName": friendly_name,
        "Capacity": capacity,
        "AgentPlatform": agent_platform,
    }
    return hosts.create(body)


@mcp.tool()
@handle_duplo_errors
def host_delete(tenant_id: str, name: str) -> str:
    """Terminate a host in a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID containing the host.
        name: The host name to delete.
    """
    validate_required(name, "Host name")
    hosts = _get_host_resource(tenant_id)
    return hosts.delete(name)


@mcp.tool()
@handle_duplo_errors
def host_reboot(tenant_id: str, name: str) -> str:
    """Reboot a host in a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID containing the host.
        name: The host name to reboot.
    """
    validate_required(name, "Host name")
    hosts = _get_host_resource(tenant_id)
    return hosts.reboot(name)
