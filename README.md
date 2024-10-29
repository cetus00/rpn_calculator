# RPN Calculator
Flask API with Swagger Frontend for Reverse Polish Notation (RPN) calculator.

## Core Features
- Supported mathematical operations: +, -, *, /
- Create an empty stack
- Delete a stack by id
- Add value to a stack
- List all stacks
- Apply an operand to a stack

## Project Setup
1. Install dependencies `poetry install`
2. Configure `.env` file for environment variables (see .env_example)
3. Set up PostgreSQL database and run migrations: `alembic upgrade head`
4. Run an API 
   - dev option: set the env variable `export FLASK_APP=calculator/api/main.py` then run `flask run --host=0.0.0.0 --port=5000`
   - production-like: `gunicorn -w 4 'calculator.api.main:create_app()'`

## Tests
Run tests `pytest`