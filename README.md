# FaceMe Security API Testing Framework

This project is an automated testing framework for the FaceMe Security API. It provides a structured way to test various API endpoints and functionalities of the FaceMe Security system.

## Project Structure

```
Still Updating 25/06/06
FaceMe_Security_ATFramework/
├── api_client/           # API client implementations
│   ├── auth_client.py    # Authentication client
│   ├── person_client.py  # Person management client
│   └── setup_config.py   # Configuration setup
├── tests/               # Test cases
│   ├── test_auth.py
│   ├── test_person_delete.py
│   ├── test_person_import.py
│   ├── test_person_query.py
│   ├── test_person_update.py
│   ├── test_person_update_info.py
│   ├── test_order.py
│   └── conftest.py
├── config/             # Configuration files
├── data/              # Test data files
├── utils/             # Utility functions
├── requirements.txt   # Project dependencies
└── pytest.ini        # Pytest configuration
```

## Design Philosophy

This testing framework is designed with the following principles in mind:

1. **Environment Isolation**: The framework supports multiple environments (dev, staging, prod) to ensure tests can be run against different deployment stages without code changes.

2. **Modular Architecture**: 
   - API clients are separated from test cases for better maintainability
   - Each client handles specific domain functionality
   - Test cases are organized by feature/functionality

3. **Configuration Management**:
   - Environment-specific configurations are managed through the `config/` directory
   - Sensitive information is kept separate from test code
   - Easy to add new environments or modify existing ones

4. **Test Data Management**:
   - Test data is stored separately in the `data/` directory
   - Supports different data sets for different test scenarios
   - Easy to maintain and update test data

## Prerequisites

- Python 3.x
- pip (Python package manager)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running Tests in Different Environments

The framework supports multiple environments through the `--env` flag:

```bash
# Development environment
pytest --env dev -s -v

# Staging environment
pytest --env staging -s -v

# Production environment
pytest --env prod -s -v
```

Command line options explained:
- `--env`: Specifies the environment to run tests against
- `-s`: Shows print statements during test execution
- `-v`: Verbose output showing each test case

### Running Specific Test Files

To run specific test files in a particular environment:

```bash
# Run authentication tests in dev environment
pytest tests/test_auth.py --env dev -s -v

# Run person management tests in staging
pytest tests/test_person_*.py --env staging -s -v
```

### Configuration

The framework uses configuration files in the `config/` directory to manage test settings and environment variables. Each environment has its own configuration file:

- `config/dev_config.py`: Development environment settings
- `config/staging_config.py`: Staging environment settings
- `config/prod_config.py`: Production environment settings

## API Clients

### AuthClient

Handles authentication with the FaceMe Security API:
- Sign in functionality
- Token management
- Authentication information retrieval

### PersonClient

Manages person-related operations:
- Person creation
- Person updates
- Person queries
- Person deletion
- Person import/export

## Test Structure

The test suite is organized into different modules:
- Authentication tests
- Person management tests
- Order management tests

Each test module focuses on specific functionality and includes various test cases to ensure proper API behavior.

