# Checkit Backend

This repository contains the backend code for the Checkit application, built using FastAPI, SQLAlchemy, and SQLite.
The reasons why I used SQLite is because the university's server does not have Docker and cannot host database such as PostgreSQL.


## Overview

The Checkit backend manages tasks, teams, users, and authentication. It utilizes a structured directory layout:

- `main.py`: Entry point of the FastAPI application.
- `requirements.txt`: Contains the Python dependencies for the project.
- `Pipfile` and `Pipfile.lock`: Pipenv files for managing Python virtual environments.
- `checkit.db`: SQLite database file storing application data.

### Directory Structure

- `taskManagement`: Main module containing the backend code.
    - `database.py`: Handles database setup and connections using SQLAlchemy.
    - `encrypting.py`: Provides encryption-related functionalities.
    - `models.py`: Defines SQLAlchemy ORM models for database tables.
    - `oauth2.py`: Implements OAuth2 authentication for the API.
    - `routers`: Directory containing API route handlers.
        - `authentication.py`, `task.py`, `team.py`, `user.py`: Route handlers for different functionalities.
    - `schemas.py`: Defines Pydantic schemas for request and response validation.
    - `services`: Contains business logic for various entities.
        - `notification.py`, `task.py`, `team.py`, `user.py`: Service modules for different functionalities.
    - `token.py`: Implements JWT token handling for authentication.

## Access API Documentation

The API documentation for this backend can be accessed [here](http://161.246.5.61:9080/docs). This documentation provides detailed information about the available endpoints, request formats, and responses.

## Getting Started

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/thammanant/checkit_backend.git
   ```

2. Navigate to the project directory:

   ```bash
   cd checkit_backend
   ```

3. Install dependencies using Pipenv:

   ```bash
   pipenv install
   ```

### Running the Application

Run the FastAPI server using the following command:

```bash
uvicorn main:app --reload
```

This will start the server locally. Access the API documentation at `http://127.0.0.1:8000/docs`.

### Configuration

- Ensure your SQLite database configurations are correctly set in `database.py`.
- Adjust any environment-specific settings in the respective configuration files.

## Contributing

Contributions to the Checkit backend are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/awesome-feature`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push the changes to your branch (`git push origin feature/awesome-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).
