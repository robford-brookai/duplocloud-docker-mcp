from duplocloud_mcp.client import get_client
from duplocloud_mcp.errors import handle_duplo_errors, validate_required
from duplocloud_mcp.server import mcp


def _get_service_resource(tenant_id: str):
    """Get a service resource configured for the given tenant."""
    validate_required(tenant_id, "Tenant ID")
    client = get_client()
    client.tenantid = tenant_id.strip()
    return client.load("service")


@mcp.tool()
@handle_duplo_errors
def service_list(tenant_id: str) -> str:
    """List all services in a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID to list services for.
    """
    svc = _get_service_resource(tenant_id)
    return svc.list()


@mcp.tool()
@handle_duplo_errors
def service_get(tenant_id: str, name: str) -> str:
    """Get details of a specific service by name.

    Args:
        tenant_id: The tenant ID containing the service.
        name: The service name to look up.
    """
    validate_required(name, "Service name")
    svc = _get_service_resource(tenant_id)
    return svc.find(name)


@mcp.tool()
@handle_duplo_errors
def service_create(tenant_id: str, name: str, image: str, replicas: int = 1) -> str:
    """Create a new service in a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID to create the service in.
        name: Name for the new service.
        image: Docker image to deploy (e.g. nginx:latest).
        replicas: Number of replicas to run. Defaults to 1.
    """
    validate_required(name, "Service name")
    validate_required(image, "Docker image")
    svc = _get_service_resource(tenant_id)
    body = {
        "Name": name,
        "Image": image,
        "Replicas": replicas,
    }
    return svc.create(body)


@mcp.tool()
@handle_duplo_errors
def service_update(tenant_id: str, name: str, image: str | None = None, replicas: int | None = None) -> str:
    """Update an existing service. Provide only the fields to change.

    Args:
        tenant_id: The tenant ID containing the service.
        name: The service name to update.
        image: New Docker image (optional).
        replicas: New replica count (optional).
    """
    validate_required(name, "Service name")
    svc = _get_service_resource(tenant_id)
    if image:
        svc.update_image(name, image)
    if replicas is not None:
        svc.update_replicas(name, replicas)
    if not image and replicas is None:
        return {"error": "Provide at least one field to update (image or replicas)", "code": 400}
    return {"message": f"Service '{name}' updated"}


@mcp.tool()
@handle_duplo_errors
def service_delete(tenant_id: str, name: str) -> str:
    """Delete a service from a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID containing the service.
        name: The service name to delete.
    """
    validate_required(name, "Service name")
    svc = _get_service_resource(tenant_id)
    return svc.delete(name)


@mcp.tool()
@handle_duplo_errors
def service_restart(tenant_id: str, name: str) -> str:
    """Restart a service, triggering a rolling redeployment.

    Args:
        tenant_id: The tenant ID containing the service.
        name: The service name to restart.
    """
    validate_required(name, "Service name")
    svc = _get_service_resource(tenant_id)
    return svc.restart(name)
