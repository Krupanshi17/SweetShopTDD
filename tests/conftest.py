import asyncio
import pytest

@pytest.fixture(scope="session")
def event_loop():
    """Create a session-scoped event loop to avoid 'Event loop is closed' errors on Windows with Motor."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
