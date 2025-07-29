import sys
import os

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import pytest

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
