import json
from unittest.mock import patch

from duplocloud_mcp.tools.tenants import tenant_create, tenant_delete, tenant_get, tenant_list


@patch("duplocloud_mcp.tools.tenants.get_client")
def test_tenant_list(mock_get_client, mock_duplo_client, mock_tenant_resource):
    mock_duplo_client.load.return_value = mock_tenant_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(tenant_list())
    assert len(result) == 2
    assert result[0]["AccountName"] == "dev"
    mock_tenant_resource.list.assert_called_once()


@patch("duplocloud_mcp.tools.tenants.get_client")
def test_tenant_get(mock_get_client, mock_duplo_client, mock_tenant_resource):
    mock_duplo_client.load.return_value = mock_tenant_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(tenant_get("dev"))
    assert result["AccountName"] == "dev"
    assert result["TenantId"] == "tid-001"
    mock_tenant_resource.find.assert_called_once_with("dev")


@patch("duplocloud_mcp.tools.tenants.get_client")
def test_tenant_get_empty_name(mock_get_client, mock_duplo_client):
    mock_get_client.return_value = mock_duplo_client
    result = json.loads(tenant_get(""))
    assert "error" in result
    assert result["code"] == 400


@patch("duplocloud_mcp.tools.tenants.get_client")
def test_tenant_create(mock_get_client, mock_duplo_client, mock_tenant_resource):
    mock_duplo_client.load.return_value = mock_tenant_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(tenant_create("test", "plan-1"))
    assert "message" in result
    mock_tenant_resource.create.assert_called_once_with({"AccountName": "test", "PlanID": "plan-1"})


@patch("duplocloud_mcp.tools.tenants.get_client")
def test_tenant_create_empty_name(mock_get_client, mock_duplo_client):
    mock_get_client.return_value = mock_duplo_client
    result = json.loads(tenant_create("", "plan-1"))
    assert "error" in result


@patch("duplocloud_mcp.tools.tenants.get_client")
def test_tenant_delete(mock_get_client, mock_duplo_client, mock_tenant_resource):
    mock_duplo_client.load.return_value = mock_tenant_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(tenant_delete("test"))
    assert "message" in result
    mock_tenant_resource.delete.assert_called_once_with("test")
