from duplocloud_mcp.client import get_client
from duplocloud_mcp.errors import handle_duplo_errors, validate_required
from duplocloud_mcp.server import mcp


def _get_ecs_resource(tenant_id: str):
    """Get an ECS resource configured for the given tenant."""
    validate_required(tenant_id, "Tenant ID")
    client = get_client()
    client.tenantid = tenant_id.strip()
    return client.load("ecs")


@mcp.tool()
@handle_duplo_errors
def ecs_service_list(tenant_id: str) -> str:
    """List all ECS services in a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID to list ECS services for.
    """
    ecs = _get_ecs_resource(tenant_id)
    return ecs.list_services()


@mcp.tool()
@handle_duplo_errors
def ecs_task_def_list(tenant_id: str) -> str:
    """List all ECS task definition families in a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID to list task definitions for.
    """
    ecs = _get_ecs_resource(tenant_id)
    return ecs.list_task_def_family()


@mcp.tool()
@handle_duplo_errors
def ecs_task_list(tenant_id: str, service_name: str) -> str:
    """List running ECS tasks for a specific service.

    Args:
        tenant_id: The tenant ID containing the ECS service.
        service_name: The ECS service name to list tasks for.
    """
    validate_required(service_name, "Service name")
    ecs = _get_ecs_resource(tenant_id)
    return ecs.list_tasks(service_name)


@mcp.tool()
@handle_duplo_errors
def ecs_task_run(tenant_id: str, family_name: str, replicas: int = 1) -> str:
    """Run an ECS task from a task definition family.

    Args:
        tenant_id: The tenant ID to run the task in.
        family_name: The task definition family name.
        replicas: Number of task instances to run. Defaults to 1.
    """
    validate_required(family_name, "Task definition family name")
    ecs = _get_ecs_resource(tenant_id)
    return ecs.run_task(family_name, replicas)


@mcp.tool()
@handle_duplo_errors
def ecs_service_update(tenant_id: str, name: str, image: str) -> str:
    """Update the image of an ECS service's task definition.

    Args:
        tenant_id: The tenant ID containing the ECS service.
        name: The task definition family name.
        image: The new Docker image to deploy.
    """
    validate_required(name, "Task definition family name")
    validate_required(image, "Docker image")
    ecs = _get_ecs_resource(tenant_id)
    return ecs.update_image(name, image)


@mcp.tool()
@handle_duplo_errors
def ecs_service_delete(tenant_id: str, name: str) -> str:
    """Delete an ECS service from a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID containing the ECS service.
        name: The ECS service name to delete.
    """
    validate_required(name, "ECS service name")
    ecs = _get_ecs_resource(tenant_id)
    return ecs.delete_service(name)
