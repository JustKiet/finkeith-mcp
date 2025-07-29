# Tests for FinKeith MCP

This directory contains test files for the FinKeith MCP project.

## Running Tests

### Prerequisites
Make sure you have the test dependencies installed:
```bash
uv add --group test pytest pytest-asyncio pytest-mock
```

### Running All Tests
```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_sepay_banking.py

# Run with coverage (after installing pytest-cov)
uv run pytest --cov=src/finkeith
```

### Running Specific Tests
```bash
# Run a specific test class
uv run pytest tests/test_sepay_banking.py::TestSePayBanking

# Run a specific test method
uv run pytest tests/test_sepay_banking.py::TestSePayBanking::test_get_transaction_history_success

# Run tests matching a pattern
uv run pytest -k "transaction_history"
```

## Test Structure

### test_sepay_banking.py
Comprehensive tests for the SePay banking client covering:

- **Initialization Tests**: API key handling, environment variables
- **Transaction History**: Success cases, empty responses, error handling
- **Balance Calculation**: Both accumulated and calculated balances
- **Transaction Count**: API endpoint testing
- **Single Transaction**: Retrieval and not-found scenarios
- **Error Handling**: HTTP errors, request errors, malformed responses
- **Parameter Validation**: Ensuring correct API calls

### Test Features
- Uses `pytest` with async support via `pytest-asyncio`
- Mocks HTTP requests using `unittest.mock`
- Comprehensive fixtures for reusable test data
- Tests both success and failure scenarios
- Validates API parameter passing

## Adding New Tests

When adding new banking clients or features:

1. Create test files following the naming pattern `test_*.py`
2. Use the existing `TestSePayBanking` class as a template
3. Mock external HTTP calls using `unittest.mock.patch`
4. Test both success and error scenarios
5. Use descriptive test method names that explain what is being tested

## Mock Data

The tests use sample transaction data that matches the expected SePay API response format. Update the `sample_transaction_data` fixture when the API response structure changes.
