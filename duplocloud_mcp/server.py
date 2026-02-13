from mcp.server.fastmcp import FastMCP

mcp = FastMCP("duplocloud")

from duplocloud_mcp.tools import containers, databases, hosts, services, storage, tenants  # noqa: E402, F401
