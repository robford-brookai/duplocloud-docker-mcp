from duplocloud_mcp.client import get_client
from duplocloud_mcp.errors import handle_duplo_errors, validate_required
from duplocloud_mcp.server import mcp


def _get_s3_resource(tenant_id: str):
    """Get an S3 resource configured for the given tenant."""
    validate_required(tenant_id, "Tenant ID")
    client = get_client()
    client.tenantid = tenant_id.strip()
    return client.load("s3")


@mcp.tool()
@handle_duplo_errors
def bucket_list(tenant_id: str) -> str:
    """List all S3 buckets in a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID to list buckets for.
    """
    s3 = _get_s3_resource(tenant_id)
    return s3.list()


@mcp.tool()
@handle_duplo_errors
def bucket_get(tenant_id: str, name: str) -> str:
    """Get details of a specific S3 bucket.

    Args:
        tenant_id: The tenant ID containing the bucket.
        name: The bucket name to look up.
    """
    validate_required(name, "Bucket name")
    s3 = _get_s3_resource(tenant_id)
    return s3.find(name)


@mcp.tool()
@handle_duplo_errors
def bucket_create(tenant_id: str, name: str) -> str:
    """Create a new S3 bucket in a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID to create the bucket in.
        name: Name for the new bucket.
    """
    validate_required(name, "Bucket name")
    s3 = _get_s3_resource(tenant_id)
    body = {"Name": name}
    return s3.create(body)


@mcp.tool()
@handle_duplo_errors
def bucket_update(tenant_id: str, name: str, versioning: bool | None = None) -> str:
    """Update an S3 bucket configuration.

    Args:
        tenant_id: The tenant ID containing the bucket.
        name: The bucket name to update.
        versioning: Enable or disable versioning (optional).
    """
    validate_required(name, "Bucket name")
    s3 = _get_s3_resource(tenant_id)
    current = s3.find(name)
    if versioning is not None:
        current["EnableVersioning"] = versioning
    return s3.update(name=name, body=current)


@mcp.tool()
@handle_duplo_errors
def bucket_delete(tenant_id: str, name: str) -> str:
    """Delete an S3 bucket from a DuploCloud tenant.

    Args:
        tenant_id: The tenant ID containing the bucket.
        name: The bucket name to delete.
    """
    validate_required(name, "Bucket name")
    s3 = _get_s3_resource(tenant_id)
    return s3.delete(name)
