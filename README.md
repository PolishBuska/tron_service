# TRON Wallet Service

A production-ready microservice for retrieving comprehensive TRON blockchain wallet information including balance, bandwidth, and energy resources.

## What is TRON?

TRON is a high-performance blockchain platform designed for building decentralized applications (dApps) and smart contracts. Key characteristics:

- **High Throughput**: Supports thousands of transactions per second
- **Low Fees**: Minimal transaction costs compared to other blockchains
- **Resource Model**: Uses bandwidth and energy instead of traditional gas fees
- **DPoS Consensus**: Delegated Proof of Stake for fast finality
- **Smart Contracts**: Full support for Ethereum-compatible smart contracts

## What is this service for?

This microservice provides a convenient REST API to retrieve essential information about TRON wallet addresses without requiring direct blockchain integration. It's designed for:

- **Financial Applications**: Check wallet balances for payment processing
- **DeFi Platforms**: Monitor user resources for transaction feasibility
- **Analytics Tools**: Gather wallet statistics and usage patterns
- **Monitoring Systems**: Track resource consumption and availability
- **Integration Services**: Provide TRON data to external systems

## Features

- Get TRON wallet information (balance, bandwidth, energy)
- Store all requests in SQLite database
- RESTful API with FastAPI
- Docker support
- Comprehensive testing
- Following SOLID principles and DRY
- Type annotations throughout

## Endpoints

### POST /api/v1/wallet/info
Get wallet information by TRON address.

**Request:**
```json
{
  "address": "TTestAddress123456789012345678901234567890"
}
```

**Response:**
```json
{
  "address": "TTestAddress123456789012345678901234567890",
  "balance": 100.5,
  "bandwidth": 1000.0,
  "energy": 500.0
}
```

### GET /api/v1/wallet/requests
Get paginated list of wallet requests.

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `page_size` (int): Page size (default: 10, max: 100)

**Response:**
```json
{
  "records": [...],
  "total": 100,
  "page": 1,
  "page_size": 10,
  "total_pages": 10
}
```

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd tron-wallet-service
```

2. Build and run with Docker Compose:
```bash
make docker-build
make docker-run
```

### Local Development

1. Install dependencies:
```bash
make install
```

2. Initialize database:
```bash
make init-db
```

3. Run the application:
```bash
make run
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Available configuration options:
- `APP_NAME`: Application name
- `DEBUG`: Enable debug mode
- `DATABASE_URL`: Database connection string
- `TRON_NETWORK`: TRON network (mainnet, shasta, nile)

## Testing

Run all tests:
```bash
make test
```

Run with coverage:
```bash
make test-coverage
```

Run only unit tests:
```bash
pytest tests/unit/
```

Run only integration tests:
```bash
pytest tests/integration/
```

## API Documentation

Once the service is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
tron-wallet-service/
├── app/
│   ├── api/            # API routes
│   ├── core/           # Core configuration and exceptions
│   ├── db/             # Database configuration
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic services
│   └── main.py         # FastAPI application
├── tests/
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── data/               # Database files
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── requirements.txt
```

## Development

### Available Make Commands

- `make help` - Show help
- `make install` - Install dependencies
- `make run` - Run the application locally
- `make test` - Run tests
- `make test-coverage` - Run tests with coverage
- `make lint` - Run linting
- `make format` - Format code
- `make clean` - Clean cache and temp files
- `make docker-build` - Build Docker image
- `make docker-run` - Run with Docker Compose
- `make docker-stop` - Stop Docker containers
- `make init-db` - Initialize database
- `make dev-setup` - Setup development environment

## Architecture

The service follows clean architecture principles:

- **API Layer** (`app/api/`): FastAPI routes and request/response handling
- **Service Layer** (`app/services/`): Business logic and external integrations
- **Data Layer** (`app/models/`, `app/db/`): Database models and connections
- **Core Layer** (`app/core/`): Configuration, exceptions, and utilities

### Dependencies

- **FastAPI**: Modern web framework for APIs
- **SQLAlchemy**: Database ORM
- **TronPy**: TRON blockchain interaction
- **Pydantic**: Data validation and serialization
- **Pytest**: Testing framework

## License

This project is licensed under the MIT License.
