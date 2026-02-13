import json
from unittest.mock import patch

from duplocloud_mcp.tools.databases import (
    database_create,
    database_delete,
    database_get,
    database_list,
    database_update,
)


@patch("duplocloud_mcp.tools.databases.get_client")
def test_database_list(mock_get_client, mock_duplo_client, mock_rds_resource):
    mock_duplo_client.load.return_value = mock_rds_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(database_list("tid-001"))
    assert len(result) == 1
    assert result[0]["Engine"] == "postgres"


@patch("duplocloud_mcp.tools.databases.get_client")
def test_database_get(mock_get_client, mock_duplo_client, mock_rds_resource):
    mock_duplo_client.load.return_value = mock_rds_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(database_get("tid-001", "mydb"))
    assert result["Engine"] == "postgres"
    mock_rds_resource.find.assert_called_once_with("mydb")


@patch("duplocloud_mcp.tools.databases.get_client")
def test_database_create(mock_get_client, mock_duplo_client, mock_rds_resource):
    mock_duplo_client.load.return_value = mock_rds_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(database_create("tid-001", "newdb", "postgres", "db.t3.micro", "admin", "pass123"))
    assert result["status"] == "success"
    mock_rds_resource.create.assert_called_once_with(
        {
            "Identifier": "newdb",
            "Engine": "postgres",
            "SizeEx": "db.t3.micro",
            "MasterUsername": "admin",
            "MasterPassword": "pass123",
        }
    )


@patch("duplocloud_mcp.tools.databases.get_client")
def test_database_update_size(mock_get_client, mock_duplo_client, mock_rds_resource):
    mock_duplo_client.load.return_value = mock_rds_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(database_update("tid-001", "mydb", size="db.t3.small"))
    assert "message" in result
    mock_rds_resource.set_instance_size.assert_called_once_with("mydb", "db.t3.small")


@patch("duplocloud_mcp.tools.databases.get_client")
def test_database_update_nothing(mock_get_client, mock_duplo_client, mock_rds_resource):
    mock_duplo_client.load.return_value = mock_rds_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(database_update("tid-001", "mydb"))
    assert "error" in result


@patch("duplocloud_mcp.tools.databases.get_client")
def test_database_delete(mock_get_client, mock_duplo_client, mock_rds_resource):
    mock_duplo_client.load.return_value = mock_rds_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(database_delete("tid-001", "mydb"))
    assert "message" in result
    mock_rds_resource.delete.assert_called_once_with("mydb")
