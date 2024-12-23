# Kamina API

## Description
Kamina API is a Python-based project designed to [brief description of what your project does].

## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/kamina-api.git
  cd kamina-api
  ```

2. Create a virtual environment:
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```

3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Running the Project

To run the project, use the following command:
```bash
uvicorn app.main:app --reload
```

## Running Tests

To run the tests, use the following command:
```bash
pytest tests
```
To run tests by file use the following commands:
```bash
pytest tests/routes/test_user_routes.py
pytest tests/routes/test_author_routes.py
pytest tests/routes/test_book_routes.py
```

## Running Coverage

To run the test coverage, use the following command:
```bash
coverage run -m pytest
coverage report
```