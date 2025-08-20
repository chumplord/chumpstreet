import pytest_asyncio
from fastmcp.client import Client
from chumpstreet.mcp_server import create_server


@pytest_asyncio.fixture
async def client():
    server = create_server()
    async with Client(server) as c:
        yield c
