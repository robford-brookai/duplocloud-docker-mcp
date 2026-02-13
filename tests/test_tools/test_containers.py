import json
from unittest.mock import patch

from duplocloud_mcp.tools.containers import (
    ecs_service_delete,
    ecs_service_list,
    ecs_service_update,
    ecs_task_def_list,
    ecs_task_list,
    ecs_task_run,
)


@patch("duplocloud_mcp.tools.containers.get_client")
def test_ecs_service_list(mock_get_client, mock_duplo_client, mock_ecs_resource):
    mock_duplo_client.load.return_value = mock_ecs_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(ecs_service_list("tid-001"))
    assert len(result) == 1
    assert result[0]["ServiceName"] == "my-ecs-svc"


@patch("duplocloud_mcp.tools.containers.get_client")
def test_ecs_task_def_list(mock_get_client, mock_duplo_client, mock_ecs_resource):
    mock_duplo_client.load.return_value = mock_ecs_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(ecs_task_def_list("tid-001"))
    assert len(result) == 1
    assert result[0]["Family"] == "my-task-def"


@patch("duplocloud_mcp.tools.containers.get_client")
def test_ecs_task_list(mock_get_client, mock_duplo_client, mock_ecs_resource):
    mock_duplo_client.load.return_value = mock_ecs_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(ecs_task_list("tid-001", "my-ecs-svc"))
    assert len(result) == 1
    mock_ecs_resource.list_tasks.assert_called_once_with("my-ecs-svc")


@patch("duplocloud_mcp.tools.containers.get_client")
def test_ecs_task_run(mock_get_client, mock_duplo_client, mock_ecs_resource):
    mock_duplo_client.load.return_value = mock_ecs_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(ecs_task_run("tid-001", "my-task-def", 3))
    assert "tasks" in result
    mock_ecs_resource.run_task.assert_called_once_with("my-task-def", 3)


@patch("duplocloud_mcp.tools.containers.get_client")
def test_ecs_service_update(mock_get_client, mock_duplo_client, mock_ecs_resource):
    mock_duplo_client.load.return_value = mock_ecs_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(ecs_service_update("tid-001", "my-task-def", "myimage:v2"))
    assert "message" in result
    mock_ecs_resource.update_image.assert_called_once_with("my-task-def", "myimage:v2")


@patch("duplocloud_mcp.tools.containers.get_client")
def test_ecs_service_delete(mock_get_client, mock_duplo_client, mock_ecs_resource):
    mock_duplo_client.load.return_value = mock_ecs_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(ecs_service_delete("tid-001", "my-ecs-svc"))
    assert "message" in result
    mock_ecs_resource.delete_service.assert_called_once_with("my-ecs-svc")


@patch("duplocloud_mcp.tools.containers.get_client")
def test_ecs_task_list_empty_name(mock_get_client, mock_duplo_client):
    mock_get_client.return_value = mock_duplo_client
    result = json.loads(ecs_task_list("tid-001", ""))
    assert "error" in result
