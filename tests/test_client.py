from unittest.mock import MagicMock, patch

import pytest
from duplocloud.errors import DuploError

from duplocloud_mcp.client import get_client, reset_client


def test_get_client_missing_host(monkeypatch):
    monkeypatch.delenv("DUPLO_HOST", raising=False)
    monkeypatch.delenv("DUPLO_TOKEN", raising=False)
    with pytest.raises(DuploError, match="DUPLO_HOST"):
        get_client()


def test_get_client_missing_token(monkeypatch):
    monkeypatch.setenv("DUPLO_HOST", "https://test.duplocloud.net")
    monkeypatch.delenv("DUPLO_TOKEN", raising=False)
    with pytest.raises(DuploError, match="DUPLO_TOKEN"):
        get_client()


@patch("duplocloud_mcp.client.DuploClient.from_creds")
def test_get_client_success(mock_from_creds, mock_env):
    mock_client = MagicMock()
    mock_from_creds.return_value = mock_client

    client = get_client()
    assert client is mock_client
    mock_from_creds.assert_called_once_with(
        host="https://test.duplocloud.net",
        token="test-token-123",
        tenant="default",
    )


@patch("duplocloud_mcp.client.DuploClient.from_creds")
def test_get_client_singleton(mock_from_creds, mock_env):
    mock_client = MagicMock()
    mock_from_creds.return_value = mock_client

    client1 = get_client()
    client2 = get_client()
    assert client1 is client2
    assert mock_from_creds.call_count == 1


def test_get_client_no_tenant(monkeypatch, mock_env):
    monkeypatch.delenv("DUPLO_TENANT", raising=False)
    mock_client = MagicMock()

    with patch("duplocloud_mcp.client.DuploClient.from_creds", return_value=mock_client) as mock_creds:
        get_client()
        mock_creds.assert_called_once_with(
            host="https://test.duplocloud.net",
            token="test-token-123",
            tenant=None,
        )


def test_reset_client(mock_env):
    mock_client_1 = MagicMock()
    mock_client_2 = MagicMock()

    with patch("duplocloud_mcp.client.DuploClient.from_creds", side_effect=[mock_client_1, mock_client_2]):
        client1 = get_client()
        reset_client()
        client2 = get_client()
        assert client1 is not client2
        assert client1 is mock_client_1
        assert client2 is mock_client_2
