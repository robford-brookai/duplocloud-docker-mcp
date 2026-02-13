import json
from unittest.mock import patch

from duplocloud_mcp.tools.hosts import host_create, host_delete, host_get, host_list, host_reboot


@patch("duplocloud_mcp.tools.hosts.get_client")
def test_host_list(mock_get_client, mock_duplo_client, mock_host_resource):
    mock_duplo_client.load.return_value = mock_host_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(host_list("tid-001"))
    assert len(result) == 1
    assert result[0]["FriendlyName"] == "host-1"


@patch("duplocloud_mcp.tools.hosts.get_client")
def test_host_get(mock_get_client, mock_duplo_client, mock_host_resource):
    mock_duplo_client.load.return_value = mock_host_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(host_get("tid-001", "host-1"))
    assert result["FriendlyName"] == "host-1"
    assert result["Status"] == "running"
    mock_host_resource.find.assert_called_once_with("host-1")


@patch("duplocloud_mcp.tools.hosts.get_client")
def test_host_get_empty_name(mock_get_client, mock_duplo_client):
    mock_get_client.return_value = mock_duplo_client
    result = json.loads(host_get("tid-001", ""))
    assert "error" in result


@patch("duplocloud_mcp.tools.hosts.get_client")
def test_host_create(mock_get_client, mock_duplo_client, mock_host_resource):
    mock_duplo_client.load.return_value = mock_host_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(host_create("tid-001", "my-host", "t3.medium"))
    assert "message" in result
    mock_host_resource.create.assert_called_once_with(
        {"FriendlyName": "my-host", "Capacity": "t3.medium", "AgentPlatform": 0}
    )


@patch("duplocloud_mcp.tools.hosts.get_client")
def test_host_delete(mock_get_client, mock_duplo_client, mock_host_resource):
    mock_duplo_client.load.return_value = mock_host_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(host_delete("tid-001", "host-1"))
    assert "message" in result
    mock_host_resource.delete.assert_called_once_with("host-1")


@patch("duplocloud_mcp.tools.hosts.get_client")
def test_host_reboot(mock_get_client, mock_duplo_client, mock_host_resource):
    mock_duplo_client.load.return_value = mock_host_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(host_reboot("tid-001", "host-1"))
    assert "message" in result
    mock_host_resource.reboot.assert_called_once_with("host-1")
