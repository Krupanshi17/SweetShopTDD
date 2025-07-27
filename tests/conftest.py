import pytest

# Fixture to specify which asynchronous backend to use for pytest-asyncio
# Here, we explicitly set the backend to "asyncio" for running async tests.
@pytest.fixture(scope="function")
def anyio_backend():
    return "asyncio"  # Tells pytest to use asyncio as the event loop backend
