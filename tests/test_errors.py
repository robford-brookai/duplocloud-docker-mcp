import json
from unittest.mock import MagicMock

from duplocloud.errors import DuploError

from duplocloud_mcp.errors import handle_duplo_errors


def test_scalar_return():
    @handle_duplo_errors
    def returns_string():
        return "plain text"

    result = returns_string()
    assert result == "plain text"


def test_duplo_error_without_response():
    @handle_duplo_errors
    def raises_duplo_error():
        err = DuploError("not found", 404)
        err.response = None
        raise err

    result = json.loads(raises_duplo_error())
    assert result == {"error": "not found", "code": 404}


def test_duplo_error_with_response():
    @handle_duplo_errors
    def raises_duplo_error():
        err = DuploError("forbidden", 403)
        err.response = MagicMock()
        err.response.__str__ = lambda self: '{"detail": "access denied"}'
        raise err

    result = json.loads(raises_duplo_error())
    assert result["error"] == "forbidden"
    assert result["code"] == 403
    assert "response" in result


def test_generic_exception():
    @handle_duplo_errors
    def raises_runtime_error():
        raise RuntimeError("something broke")

    result = json.loads(raises_runtime_error())
    assert result["error"] == "Unexpected error: something broke"
    assert result["code"] == 500
