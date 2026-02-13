import functools
import json
import logging

from duplocloud.errors import DuploError

logger = logging.getLogger("duplocloud-mcp")


def handle_duplo_errors(func):
    """Decorator that catches DuploCloud exceptions and returns structured error messages."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None:
                return json.dumps({"status": "success"})
            if isinstance(result, (dict, list)):
                return json.dumps(result, default=str)
            return str(result)
        except DuploError as e:
            logger.error("DuploCloud API error: %s (code=%s)", e.message, e.code)
            error_detail = {"error": e.message, "code": e.code}
            if e.response:
                error_detail["response"] = str(e.response)
            return json.dumps(error_detail)
        except ValueError as e:
            logger.error("Validation error: %s", e)
            return json.dumps({"error": str(e), "code": 400})
        except Exception as e:
            logger.exception("Unexpected error in tool %s", func.__name__)
            return json.dumps({"error": f"Unexpected error: {e}", "code": 500})

    return wrapper


def validate_required(value: str | None, label: str) -> str:
    if not value or not value.strip():
        raise ValueError(f"{label} is required and cannot be empty")
    return value.strip()
