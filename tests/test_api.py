import pytest
import pytest_asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from openml_mcp_server.server import _fetch_openml_data

@pytest.mark.asyncio
async def test_fetch_openml_data_success(monkeypatch):
    class MockResponse:
        status_code = 200
        content = b'{"result": "ok"}'
        def json(self):
            return {"result": "ok"}
        def raise_for_status(self):
            pass

    class MockAsyncClient:
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def get(self, url, params=None, headers=None, timeout=None):
            return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient", lambda *a, **kw: MockAsyncClient())
    result = await _fetch_openml_data("/test")
    assert result == {"result": "ok"}
