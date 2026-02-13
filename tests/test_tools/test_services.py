import json
from unittest.mock import patch

from duplocloud_mcp.tools.services import (
    service_create,
    service_delete,
    service_get,
    service_list,
    service_restart,
    service_update,
)


@patch("duplocloud_mcp.tools.services.get_client")
def test_service_list(mock_get_client, mock_duplo_client, mock_service_resource):
    mock_duplo_client.load.return_value = mock_service_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(service_list("tid-001"))
    assert len(result) == 2
    assert result[0]["Name"] == "web-app"
    assert mock_duplo_client.tenantid == "tid-001"


@patch("duplocloud_mcp.tools.services.get_client")
def test_service_list_empty_tenant(mock_get_client, mock_duplo_client):
    mock_get_client.return_value = mock_duplo_client
    result = json.loads(service_list(""))
    assert "error" in result


@patch("duplocloud_mcp.tools.services.get_client")
def test_service_get(mock_get_client, mock_duplo_client, mock_service_resource):
    mock_duplo_client.load.return_value = mock_service_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(service_get("tid-001", "web-app"))
    assert result["Name"] == "web-app"
    mock_service_resource.find.assert_called_once_with("web-app")


@patch("duplocloud_mcp.tools.services.get_client")
def test_service_create(mock_get_client, mock_duplo_client, mock_service_resource):
    mock_duplo_client.load.return_value = mock_service_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(service_create("tid-001", "web-app", "nginx:latest", 2))
    assert "message" in result
    mock_service_resource.create.assert_called_once_with({"Name": "web-app", "Image": "nginx:latest", "Replicas": 2})


@patch("duplocloud_mcp.tools.services.get_client")
def test_service_update_image(mock_get_client, mock_duplo_client, mock_service_resource):
    mock_duplo_client.load.return_value = mock_service_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(service_update("tid-001", "web-app", image="nginx:2.0"))
    assert "message" in result
    mock_service_resource.update_image.assert_called_once_with("web-app", "nginx:2.0")


@patch("duplocloud_mcp.tools.services.get_client")
def test_service_update_replicas(mock_get_client, mock_duplo_client, mock_service_resource):
    mock_duplo_client.load.return_value = mock_service_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(service_update("tid-001", "web-app", replicas=5))
    assert "message" in result
    mock_service_resource.update_replicas.assert_called_once_with("web-app", 5)


@patch("duplocloud_mcp.tools.services.get_client")
def test_service_update_nothing(mock_get_client, mock_duplo_client, mock_service_resource):
    mock_duplo_client.load.return_value = mock_service_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(service_update("tid-001", "web-app"))
    assert "error" in result


@patch("duplocloud_mcp.tools.services.get_client")
def test_service_delete(mock_get_client, mock_duplo_client, mock_service_resource):
    mock_duplo_client.load.return_value = mock_service_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(service_delete("tid-001", "web-app"))
    assert "message" in result
    mock_service_resource.delete.assert_called_once_with("web-app")


@patch("duplocloud_mcp.tools.services.get_client")
def test_service_restart(mock_get_client, mock_duplo_client, mock_service_resource):
    mock_duplo_client.load.return_value = mock_service_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(service_restart("tid-001", "web-app"))
    assert "message" in result
    mock_service_resource.restart.assert_called_once_with("web-app")
