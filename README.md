# FinKEITH MCP Finance API 🏦

A production-grade REST API for finance operations built with FastAPI, featuring comprehensive transaction management, account balance checking, secure API key authentication and MCP integration

## 🚀 Features

- **🔒 Secure Authentication**: API key-based authentication
- **📊 Comprehensive Banking**: Full transaction and account management
- **⚡ High Performance**: Async/await throughout for optimal performance  
- **📝 Well Documented**: Complete OpenAPI/Swagger documentation
- **🛡️ Production Ready**: Robust error handling and validation
- **✅ Fully Tested**: Comprehensive test suite with 100% endpoint coverage
- **🏗️ Clean Architecture**: DTO-based client with domain service layer

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   External API  │ →  │    Client    │ →  │  Service Layer  │ →  │  API Endpoints  │
│    (SePay)      │    │  (Returns    │    │  (DTO → Domain) │    │   (FastAPI)     │
│                 │    │    DTOs)     │    │                 │    │                 │
└─────────────────┘    └──────────────┘    └─────────────────┘    └─────────────────┘
```

### Core Components

- **🔌 Clients**: External API integrations (SePay banking client)
- **📋 DTOs**: Data Transfer Objects for API communication
- **🏢 Services**: Business logic layer converting DTOs to domain entities
- **🌐 API**: FastAPI endpoints with Pydantic validation
- **📊 Schemas**: Production-grade request/response models

## 📁 Project Structure

```
src/finkeith/
├── api/v1/                     # API endpoints
│   └── banking.py              # Banking API routes
├── clients/                    # External service clients
│   ├── dtos/                   # Data Transfer Objects
│   ├── interfaces/             # Client contracts  
│   └── sepay_client.py         # SePay API client
├── services/                   # Business logic services
│   └── sepay_banking_service.py # Banking service layer
├── schemas/                    # Pydantic schemas
│   ├── base.py                 # Base response models
│   └── banking.py              # Banking request/response schemas
├── core/                       # Domain layer
│   ├── entities/               # Domain entities
│   ├── interfaces/             # Domain interfaces
│   └── exceptions.py           # Custom exceptions
└── app.py                      # FastAPI application
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.12+
- UV package manager (recommended) or pip

### Quick Start

1. **Clone and setup:**
   ```bash
   cd backend/src/finkeith_mcp
   uv sync  # Install dependencies
   ```

2. **Set environment variables:**
   ```bash
   export SEPAY_API_KEY="your_sepay_api_key_here"
   ```

3. **Run the API:**
   ```bash
   # Development mode
   python run_api.py
   
   # Or with uv
   uv run python run_api.py
   ```

4. **Access the API:**
   - 🌐 **API Docs**: http://localhost:10000/docs
   - 📖 **ReDoc**: http://localhost:10000/redoc
   - ❤️ **Health Check**: http://localhost:10000/health

## 📡 API Endpoints

### Health & Status

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | API health check |
| `GET` | `/v1/banking/health` | Banking service health check |

### Banking Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/banking/transactions/history` | Get transaction history |
| `POST` | `/v1/banking/transactions/count` | Count transactions |
| `POST` | `/v1/banking/account/balance` | Get account balance |
| `GET` | `/v1/banking/transactions/{id}` | Get transaction details |

## 📋 API Usage Examples

### Get Transaction History

```bash
curl -X POST "http://localhost:10000/v1/banking/transactions/history" \
  -H "Content-Type: application/json" \
  -d '{
    "account_number": "1234567890",
    "transaction_date_from": "2025-01-01T00:00:00Z",
    "transaction_date_to": "2025-01-31T23:59:59Z",
    "limit": 100
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "transactions": [
      {
        "id": "tx_123456",
        "transaction_date": "2025-01-15T10:30:00",
        "account_number": "1234567890",
        "bank_name": "MBBANK",
        "amount_in": "1000000.00",
        "amount_out": "0.00",
        "accumulated": "5000000.00",
        "transaction_content": "Transfer received"
      }
    ],
    "total_count": 1
  },
  "message": "Retrieved 1 transactions",
  "timestamp": "2025-01-29T12:00:00Z"
}
```

### Get Account Balance

```bash
curl -X POST "http://localhost:10000/v1/banking/account/balance" \
  -H "Content-Type: application/json" \
  -d '{
    "account_number": "1234567890"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "account_number": "1234567890",
    "balance": "5000000.00",
    "currency": "VND",
    "as_of": "2025-01-29T12:00:00Z"
  },
  "message": "Balance retrieved successfully",
  "timestamp": "2025-01-29T12:00:00Z"
}
```

### Error Response Format

```json
{
  "success": false,
  "error": "Validation failed",
  "details": [
    {
      "field": "account_number",
      "message": "Field required",
      "code": "missing"
    }
  ],
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2025-01-29T12:00:00Z"
}
```

## 🧪 Testing

### Run All Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/finkeith

# Run specific test file
uv run pytest tests/test_api.py -v

# Run specific test
uv run pytest tests/test_api.py::TestBankingAPI::test_transaction_history_success -v
```

### Test Coverage

- ✅ **API Endpoints**: All routes tested
- ✅ **Error Handling**: Validation and service errors
- ✅ **Authentication**: API key validation
- ✅ **Data Validation**: Pydantic schema validation
- ✅ **Business Logic**: Service layer functionality

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SEPAY_API_KEY` | SePay banking API key | ✅ Yes | - |
| `LOG_LEVEL` | Logging level | ❌ No | `INFO` |

### API Configuration

- **Host**: `0.0.0.0`
- **Port**: `10000`
- **CORS**: Enabled for development
- **Docs**: Available at `/docs` and `/redoc`

## 🛡️ Production Deployment

### Security Considerations

1. **API Key Security**: Store `SEPAY_API_KEY` securely
2. **CORS Configuration**: Restrict origins for production
3. **Rate Limiting**: Consider adding rate limiting middleware
4. **SSL/TLS**: Use HTTPS in production
5. **Input Validation**: All requests validated with Pydantic

### Production Checklist

- [ ] Set `SEPAY_API_KEY` environment variable
- [ ] Configure proper CORS origins
- [ ] Set up SSL/TLS certificates
- [ ] Configure logging and monitoring
- [ ] Set up health check endpoints for load balancers
- [ ] Consider adding rate limiting and authentication middleware

## 📚 Schema Validation

### Request Validation Features

- ✅ **Type Validation**: Automatic type checking
- ✅ **Range Validation**: Min/max values for numbers
- ✅ **String Validation**: Length limits and patterns
- ✅ **Date Validation**: Proper datetime handling
- ✅ **Decimal Precision**: Financial amounts with proper precision
- ✅ **Custom Validation**: Business rule validation

### Response Standards

- ✅ **Consistent Structure**: All responses follow standard format
- ✅ **Error Details**: Detailed error information for debugging
- ✅ **Timestamps**: UTC timestamps on all responses
- ✅ **Success Indicators**: Clear success/failure indicators
- ✅ **Message Context**: Helpful success/error messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**🏦 FinKeith MCP Finance API** - Production-ready banking integration made simple.
