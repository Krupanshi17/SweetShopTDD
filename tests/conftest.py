import pytest
import asyncio
from typing import Generator

# Fixture to create a single event loop for the entire test session
# This avoids "Event loop is closed" errors when using Motor (MongoDB) or Async I/O
@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()  # Create a new event loop
    yield loop  # Provide the loop to the tests
    loop.close()  # Close the loop after all tests complete

# Fixture to ensure AnyIO uses asyncio as the backend for all tests
@pytest.fixture(autouse=True)
def anyio_backend():
    """Force AnyIO to use asyncio backend."""
    return "asyncio"
