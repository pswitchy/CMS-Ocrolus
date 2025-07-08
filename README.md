# Content Management System (CMS) Backend

This is a backend service for a simple Content Management System built with Python, Flask, and PostgreSQL. It allows authenticated users to create, view, update, delete, and list articles. It also tracks the most recently viewed articles for each user.

## Features

-   **User Authentication**: JWT-based authentication (Register/Login). The token identity is the user's username.
-   **Article Management**: Full CRUDL (Create, Read, Update, Delete, List) functionality for articles.
-   **Authorization**: Users can only edit or delete articles they have authored.
-   **Recently Viewed**: An in-memory service tracks the 5 most recently viewed articles for each authenticated user. This data does not persist across application restarts.
-   **Pagination**: The article list endpoint (`GET /api/articles`) is paginated.
-   **Database Migrations**: Uses Flask-Migrate (Alembic) for robust database schema management.
-   **Containerized**: Fully containerized with Docker and Docker Compose for easy, consistent setup and deployment.
-   **Unit Tests**: Includes a testing suite using Pytest.

## Tech Stack

-   **Backend**: Python, Flask
-   **Database**: PostgreSQL
-   **ORM**: Flask-SQLAlchemy
-   **Migrations**: Flask-Migrate (Alembic)
-   **Authentication**: Flask-JWT-Extended
-   **Containerization**: Docker, Docker Compose
-   **Testing**: Pytest

---

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/) (v2.x is recommended)

---

### 1. Initial Project Setup

Follow these steps to set up the project for the first time.

**1. Clone the repository:**

```bash
git clone https://github.com/pswitchy/CMS-Ocrolus.git
cd CMS-Ocrolus
```

**2. Create the Environment File:**

Copy the example environment file. You can change the secret keys if you wish, but the default database values are configured to work with Docker Compose out of the box.

```bash
cp .env.example .env
```

**3. Initialize the Database Migration System:**

This is a **one-time command** that creates the `migrations/` directory needed by Flask-Migrate. We run this command inside a temporary Docker container to avoid installing Python dependencies on your host machine.

```bash
docker-compose run --rm api flask db init
```

**4. Create the First Migration Script:**

Now, generate the first migration script based on the models defined in `app/models.py`.

```bash
docker-compose run --rm api flask db migrate -m "Initial migration with user and article tables"
```


---

### 2. Running the Application

With the setup complete, running the entire stack is a single command.

```bash
docker-compose up --build
```

This command will:
-   Build the Docker image for the Flask API.
-   Start a PostgreSQL container (`db`).
-   Start the API container (`api`).
-   On startup, the `api` container will automatically run `flask db upgrade` to apply any pending migrations to the database, creating the necessary tables.
-   The API will then be available at `http://localhost:5000`.

To stop the application, press `Ctrl+C` in the terminal and then run:

```bash
docker-compose down
```

### Option 2: Running Locally (Alternative for Development)

This method is useful if you want to use your local IDE's debugger and tools directly.

**1. Set up a Virtual Environment:**
Create and activate a Python virtual environment to keep dependencies isolated.

```bash
python -m venv venv
venv\Scripts\Activate
```

**2. Install Dependencies:**
Install all required Python packages from the requirements file.

```bash
pip install -r requirements.txt
```

**3. Configure Environment for Local Database:**

**4. Setup and Migrate the Database:**
Run the Flask-Migrate commands to create and apply the database schema to your local database.

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

**5. Run the Development Server:**
Start the Flask application.

```bash
flask run
```
The API will be available at `http://localhost:5000`.

---

## API Documentation

All endpoints are prefixed with `/api`. A valid JWT token must be provided in the `Authorization: Bearer <token>` header for all protected endpoints.

### Authentication

| Method | Endpoint         | Description                       |
| :----- | :--------------- | :-------------------------------- |
| `POST` | `/auth/register` | Register a new user.              |
| `POST` | `/auth/login`    | Log in to get a JWT access token. |

### Articles

| Method   | Endpoint          | Description                                                    | Auth Required? |
| :------- | :---------------- | :------------------------------------------------------------- | :------------- |
| `POST`   | `/articles`       | Create a new article.                                          | **Yes**        |
| `GET`    | `/articles`       | List all articles (paginated).                                 | **Yes**        |
| `GET`    | `/articles/<id>`  | Get a single article by its ID.                                | **Yes**        |
| `PUT`    | `/articles/<id>`  | Update an article. (Must be the author).                       | **Yes**        |
| `DELETE` | `/articles/<id>`  | Delete an article. (Must be the author).                       | **Yes**        |

### Users

| Method | Endpoint                    | Description                                      | Auth Required? |
| :----- | :-------------------------- | :----------------------------------------------- | :------------- |
| `GET`  | `/users/me/recently-viewed` | Get the 5 most recently viewed articles for you. | **Yes**        |

### Example Payloads

-   **Register/Login:** `POST /api/auth/register`
    ```json
    {
        "username": "testuser",
        "password": "securepassword123"
    }
    ```

-   **Create Article:** `POST /api/articles`
    ```json
    {
        "title": "My Awesome Blog Post",
        "content": "Here is the content of the article..."
    }
    ```

### Pagination

The `GET /api/articles` endpoint supports pagination via query parameters:
-   `page` (integer, default: 1)
-   `per_page` (integer, default: 10)

Example: `GET /api/articles?page=2&per_page=5`

---

## Database Management

If you make changes to your database models in `app/models.py`, follow this process to update your database schema:

1.  **Generate a new migration script:**
    ```bash
    docker-compose run --rm api flask db migrate -m "Describe your model changes here"
    ```
2.  **Apply the migration:**
    The migration will be applied automatically the next time you run `docker-compose up`. You can also apply it manually:
    ```bash
    docker-compose run --rm api flask db upgrade
    ```

---

## Running Tests

To run the unit tests, use the following command. This will spin up a temporary container, run `pytest`, and then exit.

```bash
docker-compose run --rm api pytest
```
