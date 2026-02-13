import json
from unittest.mock import patch

from duplocloud_mcp.tools.storage import bucket_create, bucket_delete, bucket_get, bucket_list, bucket_update


@patch("duplocloud_mcp.tools.storage.get_client")
def test_bucket_list(mock_get_client, mock_duplo_client, mock_s3_resource):
    mock_duplo_client.load.return_value = mock_s3_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(bucket_list("tid-001"))
    assert len(result) == 1
    assert result[0]["Name"] == "my-bucket"


@patch("duplocloud_mcp.tools.storage.get_client")
def test_bucket_get(mock_get_client, mock_duplo_client, mock_s3_resource):
    mock_duplo_client.load.return_value = mock_s3_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(bucket_get("tid-001", "my-bucket"))
    assert result["Name"] == "my-bucket"
    mock_s3_resource.find.assert_called_once_with("my-bucket")


@patch("duplocloud_mcp.tools.storage.get_client")
def test_bucket_create(mock_get_client, mock_duplo_client, mock_s3_resource):
    mock_duplo_client.load.return_value = mock_s3_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(bucket_create("tid-001", "new-bucket"))
    assert result["Name"] == "my-bucket"  # mock returns this
    mock_s3_resource.create.assert_called_once_with({"Name": "new-bucket"})


@patch("duplocloud_mcp.tools.storage.get_client")
def test_bucket_update_versioning(mock_get_client, mock_duplo_client, mock_s3_resource):
    mock_duplo_client.load.return_value = mock_s3_resource
    mock_get_client.return_value = mock_duplo_client

    json.loads(bucket_update("tid-001", "my-bucket", versioning=True))
    mock_s3_resource.find.assert_called_once_with("my-bucket")
    mock_s3_resource.update.assert_called_once()
    call_kwargs = mock_s3_resource.update.call_args
    assert call_kwargs.kwargs["body"]["EnableVersioning"] is True


@patch("duplocloud_mcp.tools.storage.get_client")
def test_bucket_delete(mock_get_client, mock_duplo_client, mock_s3_resource):
    mock_duplo_client.load.return_value = mock_s3_resource
    mock_get_client.return_value = mock_duplo_client

    result = json.loads(bucket_delete("tid-001", "my-bucket"))
    assert "message" in result
    mock_s3_resource.delete.assert_called_once_with("my-bucket")


@patch("duplocloud_mcp.tools.storage.get_client")
def test_bucket_get_empty_name(mock_get_client, mock_duplo_client):
    mock_get_client.return_value = mock_duplo_client
    result = json.loads(bucket_get("tid-001", ""))
    assert "error" in result
