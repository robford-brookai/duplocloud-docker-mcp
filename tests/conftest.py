from unittest.mock import MagicMock

import pytest

from duplocloud_mcp.client import reset_client


@pytest.fixture(autouse=True)
def _reset_client():
    """Reset the singleton client before each test."""
    reset_client()
    yield
    reset_client()


@pytest.fixture
def mock_env(monkeypatch):
    """Set DuploCloud environment variables for testing."""
    monkeypatch.setenv("DUPLO_HOST", "https://test.duplocloud.net")
    monkeypatch.setenv("DUPLO_TOKEN", "test-token-123")
    monkeypatch.setenv("DUPLO_TENANT", "default")


@pytest.fixture
def mock_duplo_client():
    """Create a mock DuploClient that returns mock resources."""
    client = MagicMock()
    client.tenantid = None
    client.tenant = "default"
    return client


@pytest.fixture
def mock_tenant_resource():
    """Create a mock tenant resource handler."""
    resource = MagicMock()
    resource.list.return_value = [
        {"AccountName": "dev", "TenantId": "tid-001", "PlanID": "plan-1"},
        {"AccountName": "staging", "TenantId": "tid-002", "PlanID": "plan-1"},
    ]
    resource.find.return_value = {"AccountName": "dev", "TenantId": "tid-001", "PlanID": "plan-1"}
    resource.create.return_value = {"message": "Tenant 'test' created"}
    resource.delete.return_value = {"message": "Tenant 'test' deleted"}
    return resource


@pytest.fixture
def mock_service_resource():
    """Create a mock service resource handler."""
    resource = MagicMock()
    resource.list.return_value = [
        {"Name": "web-app", "Image": "nginx:latest", "Replicas": 2},
        {"Name": "api", "Image": "node:18", "Replicas": 3},
    ]
    resource.find.return_value = {"Name": "web-app", "Image": "nginx:latest", "Replicas": 2}
    resource.create.return_value = {"message": "Successfully created service 'web-app'"}
    resource.delete.return_value = {"message": "Successfully deleted service 'web-app'"}
    resource.restart.return_value = {"message": "Successfully restarted service 'web-app'"}
    resource.update_image.return_value = {"message": "Successfully updated image"}
    resource.update_replicas.return_value = {"message": "Successfully updated replicas"}
    return resource


@pytest.fixture
def mock_host_resource():
    """Create a mock hosts resource handler."""
    resource = MagicMock()
    resource.list.return_value = [
        {"FriendlyName": "host-1", "InstanceId": "i-abc123", "Status": "running"},
    ]
    resource.find.return_value = {"FriendlyName": "host-1", "InstanceId": "i-abc123", "Status": "running"}
    resource.create.return_value = {"message": "Successfully created host 'host-1'", "id": "i-new123"}
    resource.delete.return_value = {"message": "Successfully deleted host 'host-1'"}
    resource.reboot.return_value = {"message": "Successfully rebooted host 'host-1'"}
    return resource


@pytest.fixture
def mock_rds_resource():
    """Create a mock RDS resource handler."""
    resource = MagicMock()
    resource.list.return_value = [
        {"Identifier": "duploMyDb", "Engine": "postgres", "SizeEx": "db.t3.micro"},
    ]
    resource.find.return_value = {"Identifier": "duploMyDb", "Engine": "postgres", "SizeEx": "db.t3.micro"}
    resource.create.return_value = None
    resource.delete.return_value = {"message": "aws/rds/instance/mydb deleted"}
    resource.set_instance_size.return_value = {"message": "DB instance mydb resized to db.t3.small"}
    return resource


@pytest.fixture
def mock_s3_resource():
    """Create a mock S3 resource handler."""
    resource = MagicMock()
    resource.list.return_value = [{"Name": "my-bucket", "EnableVersioning": False}]
    resource.find.return_value = {"Name": "my-bucket", "EnableVersioning": False}
    resource.create.return_value = {"Name": "my-bucket"}
    resource.update.return_value = {"Name": "my-bucket", "EnableVersioning": True}
    resource.delete.return_value = {"message": "aws/s3bucket/my-bucket deleted"}
    return resource


@pytest.fixture
def mock_ecs_resource():
    """Create a mock ECS resource handler."""
    resource = MagicMock()
    resource.list_services.return_value = [{"ServiceName": "my-ecs-svc"}]
    resource.list_task_def_family.return_value = [{"Family": "my-task-def"}]
    resource.list_tasks.return_value = [{"TaskArn": "arn:aws:ecs:task/abc123"}]
    resource.run_task.return_value = {"tasks": [{"taskArn": "arn:aws:ecs:task/new123"}]}
    resource.update_image.return_value = {"message": "Updating a task definition and its corresponding service."}
    resource.delete_service.return_value = {"message": "ECS service deleted"}
    return resource
