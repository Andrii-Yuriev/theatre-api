# Theatre API

A RESTful API for a theatre booking system, built with Django and Django REST Framework. This project allows users to browse plays and performances, register, and book tickets for available seats. The entire application is containerized using Docker for easy setup and deployment.

## Key Features

-   **User Management**: User registration and JWT-based authentication (login, token refresh).
-   **Theatre Content Management**: CRUD operations for Genres, Actors, Plays, and Theatre Halls.
-   **Performance Scheduling**: Ability to create and manage performances (show sessions) for specific plays in specific halls.
-   **Ticket Booking System**: Custom endpoint for creating reservations with multiple tickets in a single, atomic transaction.
-   **Role-Based Permissions**:
    -   Admin users can manage all content.
    -   Authenticated users can create reservations and view their own bookings.
    -   Anonymous users can browse plays and performance schedules.
-   **API Documentation**: Auto-generated documentation available via Swagger UI and ReDoc.
-   **Filtering & Pagination**: Support for filtering lists (e.g., performances by date) and pagination for all list endpoints.
-   **Containerized**: Fully containerized with Docker and Docker Compose for a consistent development and production environment.

## Tech Stack

-   **Backend**: Python, Django, Django REST Framework
-   **Database**: PostgreSQL
-   **Authentication**: Djoser, Simple JWT (JSON Web Tokens)
-   **API Documentation**: drf-spectacular (Swagger/OpenAPI)
-   **Testing**: Django's built-in test framework
-   **Containerization**: Docker, Docker Compose

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   [Docker](https://www.docker.com/get-started/)
-   [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

### Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Andrii-Yuriev/theatre-api.git
    cd theatre-api
    ```

2.  **Configure Environment Variables:**

    The project uses `.env` files for configuration. Sample files are provided.

    a. **Create Django environment file:**
    Copy the sample file:
    ```bash
    cp .envs/.local/.django.sample .envs/.local/.django
    ```
    Now, open `.envs/.local/.django` and set your `SECRET_KEY`. You can generate one with:
    ```bash
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```

    b. **Create PostgreSQL environment file:**
    Copy the sample file:
    ```bash
    cp .envs/.local/.postgres.sample .envs/.local/.postgres
    ```
    The default values should work fine for local development. Make sure the credentials here match the ones in your `DATABASE_URL` in the `.django` file.

3.  **Build and Run with Docker Compose:**

    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images and start the `web` (Django) and `db` (PostgreSQL) containers.

4.  **Apply Database Migrations:**

    In a **new terminal window**, run the migrations to set up the database schema:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Create a Superuser (Admin):**

    To access the Django Admin panel, create a superuser:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
    Follow the prompts to set a username, email, and password.

## Usage

The API is now running and available at `http://127.0.0.1:8000/`.

### API Documentation

-   **Swagger UI**: [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
-   **ReDoc**: [http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)

### Django Admin

-   **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
    -   Log in with the superuser credentials you created.

### Example API Usage (with `curl`)

1.  **Register a new user:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser", "email":"test@example.com", "password":"SomeSecurePassword123"}' http://127.0.0.1:8000/api/auth/users/
    ```

2.  **Obtain JWT token:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser", "password":"SomeSecurePassword123"}' http://127.0.0.1:8000/api/auth/jwt/create/
    ```
    *This will return `access` and `refresh` tokens.*

3.  **List all plays (as an authenticated user):**
    *Replace `<YOUR_ACCESS_TOKEN>` with the token from the previous step.*
    ```bash
    curl -X GET -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" http://127.0.0.1:8000/api/theatre/plays/
    ```

## Running Tests

To run the test suite, execute the following command:
```bash
docker-compose exec web python manage.py test