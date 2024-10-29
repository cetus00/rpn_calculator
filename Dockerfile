# Use the official Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables for Poetry and Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.4 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# Install Poetry
RUN pip install poetry==1.8.4

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy only the Poetry files first to cache dependencies
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --no-root --without dev

# Copy the entire project into the container
COPY calculator /app

# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask app with Poetry
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "calculator.api.main:create_app()"]