# Task Management API

## Overview

This is a FastAPI-based Task Management API that provides comprehensive endpoints for managing tasks and retrieving task-related statistics.


Here are clear instructions for setting up and running the backend server using your provided `Dockerfile` and `docker-compose.yml`. These instructions will include building the Docker image, starting the services, and running Alembic migrations.

---

## **Setup Instructions**

### **1. Prerequisites**
Ensure you have the following installed:
- **Docker**.
- **Docker Compose**.

### **2. Environment Variables**
Create a `.env` file in the root of your project to define the environment variables used in the `docker-compose.yml`. Here’s an example:

```sh
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=todo_db
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password

DB_HOST=db:3306
```

### **3. Build the Docker Images**
Run the following command to build the backend Docker image:
```bash
docker-compose build
```

This will:
- Build the `backend` service using the provided `Dockerfile`.
- Pull the `mysql:8.0` image for the `db` service.

### **4. Start the Services**
Start the MySQL database and the FastAPI backend using:
```bash
docker-compose up
```

This will:
- Launch the database container (`db`) and expose it on port 3306.
- Launch the backend container (`backend`) and expose it on port 8000.
- The `depends_on` directive ensures the `db` service starts before the `backend`.

### **5. Run Alembic Migrations**
To initialize the database schema, you need to run Alembic migrations. Execute the following command:
```bash
docker-compose exec backend alembic upgrade head
```

This will:
- Run the migrations inside the `backend` container.
- Apply the database schema changes as defined in your Alembic migrations.

### **6. Verify the Setup**
1. **Backend Service**: Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to access the FastAPI Swagger documentation.
2. **Database**: Connect to the MySQL database using a database client (e.g., DBeaver or MySQL Workbench) with the credentials from the `.env` file.

---


## API Routes

### Task Routes

1. **Create Task**
   - `POST /tasks/`
   - Creates a new task
   - Accepts task details in request body
   - Returns created task details

2. **List Tasks**
   - `GET /tasks/`
   - Retrieves a paginated list of tasks
   - Optional query parameters:
     - `page`: Page number (default: 1)
     - `limit`: Number of items per page (default: 10)
     - `order`: Sorting mode (ascending/descending)

3. **Get Single Task**
   - `GET /tasks/{task_id}`
   - Retrieves details of a specific task by its ID

4. **Update Task**
   - `PUT /tasks/{task_id}`
   - Updates an existing task
   - Accepts task update details in request body

5. **Delete Task**
   - `DELETE /tasks/{task_id}`
   - Deletes a specific task by its ID

6. **Bulk Delete Tasks**
   - `PATCH /tasks/bulk-delete`
   - Deletes multiple tasks at once
   - Accepts a list of task IDs to delete

7. **Bulk Complete Tasks**
   - `PATCH /tasks/bulk-complete`
   - Marks multiple tasks as complete
   - Accepts a list of task IDs to complete

### Statistics Routes

1. **Get Task Statistics**
   - `GET /statistics`
   - Retrieves overall task statistics

2. **Get Task Actions**
   - `GET /statistics/actions`
   - Retrieves paginated task action history
   - Optional query parameters:
     - `page`: Page number (default: 1)
     - `limit`: Number of items per page (default: 10)

## Documentation Routes

For detailed API documentation, visit:
- [http://localhost:8000/docs](http://localhost:8000/docs): Interactive Swagger UI documentation
- [http://localhost:8000/redocs](http://localhost:8000/redocs): ReDoc style documentation

## Dependency Injection in the Backend Implementation

In this codebase, dependency injection (DI) is used to manage the database session, which is injected into service functions and API routes. This design ensures flexibility, makes the code modular, and facilitates future testing by allowing dependencies to be mocked or replaced during tests.

## Technology Stack
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Docker

## Error Handling
The API uses a consistent error response format with:
- Error codes
- Descriptive error messages

## Pagination
List endpoints support pagination with metadata including:
- Total items
- Total pages
- Current page
- Page size
- Next/Previous page indicators
