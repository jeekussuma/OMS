# Organization Management System

## Overview
The **Organization Management System** is a robust, scalable web application designed to streamline organizational operations. Built using the **FastAPI** framework, it provides features for user management, role-based access control (RBAC), permission management, task management, and department/sub-department management. The system adheres to production-grade standards and aligns with international standards such as **ISO/IEC 27001** (security) and **ISO 9001** (quality management).

This system is ideal for organizations seeking to manage users, roles, permissions, tasks, and departments in a secure, efficient, and scalable manner. It supports RESTful APIs, secure authentication, and a modular architecture for easy maintenance and extensibility.

## Features
The system includes the following key features:

### 1. User Management
- **CRUD Operations**: Create, read, update, and delete users.
- **Authentication**: Secure JWT-based login with password hashing (bcrypt).
- **User Profiles**: Manage user details (username, email, full name, department).
- **Password Management**: Secure password storage and reset functionality.

### 2. Role Access Management
- **Role Creation**: Define roles (e.g., Admin, Manager, Employee).
- **Role Assignment**: Assign roles to users.
- **Role-Based Access Control (RBAC)**: Restrict access to resources based on roles.

### 3. Permission Management
- **Granular Permissions**: Define permissions (e.g., view, edit, delete) for specific resources.
- **Permission Assignment**: Map permissions to roles dynamically.
- **Access Control**: Enforce permissions at the API level.

### 4. Task Management
- **Task CRUD**: Create, update, assign, and track tasks.
- **Role-Based Visibility**: Tasks are visible based on user roles (e.g., Managers see department tasks).
- **Department-Based Assignment**: Assign tasks to users within departments.
- **Status Tracking**: Track task statuses (e.g., To Do, In Progress, Done).

### 5. Department Management
- **Department CRUD**: Manage departments and sub-departments.
- **Hierarchical Structure**: Support parent-child relationships (e.g., IT → Software Development).
- **User Assignment**: Assign users to departments or sub-departments.
- **Access Control**: Restrict access based on department membership.

## Technology Stack
The system is built with modern, production-ready technologies:
- **Backend**: FastAPI (Python) for high-performance RESTful APIs.
- **Database**: PostgreSQL for relational data, with SQLAlchemy as the ORM.
- **Authentication**: JWT with OAuth2 for secure user authentication.
- **Authorization**: Custom RBAC implementation.
- **Caching**: Redis (optional) for performance optimization.
- **Task Queue**: Celery with Redis/RabbitMQ for asynchronous tasks (e.g., notifications).
- **Testing**: Pytest for unit and integration tests.
- **Deployment**: Docker for containerization, Kubernetes (optional) for orchestration.
- **Monitoring**: Sentry for error tracking, Prometheus/Grafana for metrics, ELK Stack for logging.
- **Security**: HTTPS, OWASP Top 10 compliance, dependency scanning with Dependabot.

## Architecture
The system follows a modular, layered architecture for scalability and maintainability:
- **API Layer**: FastAPI endpoints organized by resource (users, roles, permissions, tasks, departments).
- **Service Layer**: Business logic for each module, ensuring separation of concerns.
- **Data Access Layer**: SQLAlchemy models and queries for database interactions.
- **Core Layer**: Configuration, security (JWT, password hashing), and dependency injection.
- **Utils Layer**: Helper functions for RBAC, notifications, and other utilities.

### Project Structure
```
organization_management_system/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app initialization
│   ├── api/                     # API endpoints
│   │   ├── v1/
│   │   │   ├── users.py         # User management endpoints
│   │   │   ├── roles.py         # Role management endpoints
│   │   │   ├── permissions.py   # Permission management endpoints
│   │   │   ├── tasks.py         # Task management endpoints
│   │   │   ├── departments.py   # Department management endpoints
│   ├── core/                    # Core configurations
│   │   ├── config.py            # Environment variables, settings
│   │   ├── security.py          # Authentication, JWT, password hashing
│   │   ├── dependencies.py      # Dependency injection (e.g., DB session)
│   ├── models/                  # SQLAlchemy models
│   ├── schemas/                 # Pydantic schemas for validation
│   ├── services/                # Business logic
│   ├── utils/                   # Helper functions
├── tests/                       # Test suite
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Local development setup
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore file
```

### Database Schema
The system uses PostgreSQL with the following core tables:
- **users**: Stores user details (id, username, email, hashed_password, department_id, etc.).
- **roles**: Defines roles (id, name, description).
- **permissions**: Defines permissions (id, name, description).
- **role_permissions**: Maps roles to permissions (many-to-many).
- **user_roles**: Maps users to roles (many-to-many).
- **departments**: Stores departments and sub-departments (id, name, parent_id).
- **tasks**: Stores tasks (id, title, description, status, assigned_to, department_id).

## Setup Instructions
### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Redis (optional, for caching/task queue)
- Docker (optional, for containerized deployment)
- Git

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-org/organization_management_system.git
   cd organization_management_system
   ```

2. **Set Up Environment Variables**:
   - Copy the `.env.example` to `.env` and update the values:
     ```env
     DATABASE_URL=postgresql://user:password@localhost:5432/dbname
     SECRET_KEY=your-secret-key
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up PostgreSQL**:
   - Create a database:
     ```bash
     psql -U postgres -c "CREATE DATABASE dbname;"
     ```
   - Apply migrations (if using Alembic):
     ```bash
     alembic upgrade head
     ```

5. **Run the Application**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   - Access the API at `http://localhost:8000`.
   - View API documentation at `http://localhost:8000/docs`.

6. **Run with Docker** (optional):
   ```bash
   docker-compose up --build
   ```

### Testing
Run tests using Pytest:
```bash
pytest tests/
```

## API Endpoints

### Authentication (Central Auth System)
- `POST /api/v1/users/login` - Login user and get JWT token
- `POST /api/v1/users/verify-token` - Verify JWT token (send token in body)
- `GET /api/v1/users/verify-token` - Verify JWT token (send token in Authorization header)
- `POST /api/v1/users/refresh-token` - Refresh JWT token
- `POST /api/v1/users/logout` - Logout user (token invalidation)
- `GET /api/v1/users/me` - Get current user information

### Users
- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/{id}` - Get user
- `PUT /api/v1/users/{id}` - Update user (including role assignment)
- `DELETE /api/v1/users/{id}` - Delete user

### Roles
- `GET /api/v1/roles/` - List roles
- `POST /api/v1/roles/` - Create role
- `GET /api/v1/roles/{id}` - Get role
- `PUT /api/v1/roles/{id}` - Update role (including permission assignment)
- `DELETE /api/v1/roles/{id}` - Delete role

### Permissions
- `GET /api/v1/permissions/` - List permissions
- `POST /api/v1/permissions/` - Create permission
- `GET /api/v1/permissions/{id}` - Get permission
- `PUT /api/v1/permissions/{id}` - Update permission
- `DELETE /api/v1/permissions/{id}` - Delete permission

### Departments
- `GET /api/v1/departments/` - List departments
- `POST /api/v1/departments/` - Create department
- `GET /api/v1/departments/{id}` - Get department
- `PUT /api/v1/departments/{id}` - Update department
- `DELETE /api/v1/departments/{id}` - Delete department

### Tasks
- `GET /api/v1/tasks/` - List tasks
- `POST /api/v1/tasks/` - Create task
- `GET /api/v1/tasks/{id}` - Get task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

## Central Authentication System Usage

### 1. Login
```bash
POST /api/v1/users/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### 2. Verify Token (Method 1 - Body)
```bash
POST /api/v1/users/verify-token
Content-Type: application/json

{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Verify Token (Method 2 - Header)
```bash
GET /api/v1/users/verify-token
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 4. Refresh Token
```bash
POST /api/v1/users/refresh-token
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 5. Logout
```bash
POST /api/v1/users/logout
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 6. Get Current User
```bash
GET /api/v1/users/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Role and Permission Assignment

### Assign Permissions to Role
```bash
PUT /api/v1/roles/1
Authorization: Bearer <superadmin_token>
Content-Type: application/json

{
  "name": "Manager",
  "description": "Department Manager",
  "permission_ids": [1, 2, 3, 4]
}
```

### Assign Roles to User
```bash
PUT /api/v1/users/5
Authorization: Bearer <superadmin_token>
Content-Type: application/json

{
  "role_ids": [1, 2]
}
```

## Production Standards & Compliance
The system is designed to meet production-grade and international standards:
- **Security (ISO/IEC 27001)**:
  - HTTPS with SSL/TLS.
  - JWT-based authentication with bcrypt password hashing.
  - OWASP Top 10 compliance (e.g., input validation, secure headers).
  - Dependency scanning with Dependabot.
- **Quality (ISO 9001)**:
  - Comprehensive testing (>80% coverage) with Pytest.
  - Code quality enforced with Flake8 and Black.
  - Automated CI/CD pipeline with GitHub Actions.
- **Scalability**:
  - Connection pooling with SQLAlchemy.
  - Caching with Redis (optional).
  - Containerized deployment with Docker.
- **Maintainability**:
  - Modular architecture with clear separation of concerns.
  - Auto-generated API documentation via FastAPI's Swagger UI.
  - Detailed logging with ELK Stack.

## Development Roadmap
1. **Phase 1: Core Features** (4-6 weeks)
   - Set up FastAPI, PostgreSQL, and authentication.
   - Implement user, role, and permission management.
2. **Phase 2: Task & Department Management** (4-6 weeks)
   - Build task management with role/department-based access.
   - Implement department/sub-department functionality.
3. **Phase 3: Testing & Optimization** (2-3 weeks)
   - Write unit and integration tests.
   - Optimize database queries and API performance.
4. **Phase 4: Production Deployment** (2-3 weeks)
   - Set up CI/CD with GitHub Actions.
   - Deploy to a cloud provider (e.g., AWS, GCP).
5. **Phase 5: Enhancements** (Ongoing)
   - Add notifications (email, in-app).
   - Implement audit logs for compliance.

## Troubleshooting
- **Database Connection Issues**:
  - Ensure the `DATABASE_URL` in `.env` is correct.
  - Check PostgreSQL logs for errors: `/var/log/postgresql/`.
  - Verify SQLAlchemy pool settings: `pool_pre_ping=True`, `pool_recycle=1800`.
- **Authentication Errors**:
  - Confirm the `SECRET_KEY` is set in `.env`.
  - Check JWT token validity and expiration.
- **Performance Issues**:
  - Add indexes on frequently queried columns (e.g., `users.email`).
  - Enable caching with Redis for high-traffic endpoints.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License
This project is licensed under the MIT License.

## Contact
For questions or support, contact the development team at [kusumacd9@gmail.com].

## Deployment Instructions

### 1. Database Deployment

1. **Start the Database**:
   ```bash
   # Create and start the database container
   docker-compose -f docker-compose.db.yml up -d
   
   # Check database status
   docker-compose -f docker-compose.db.yml ps
   
   # View database logs
   docker-compose -f docker-compose.db.yml logs -f
   ```

2. **Database Management**:
   ```bash
   # Stop the database
   docker-compose -f docker-compose.db.yml down
   
   # Stop and remove volumes (WARNING: This will delete all data)
   docker-compose -f docker-compose.db.yml down -v
   
   # Restart the database
   docker-compose -f docker-compose.db.yml restart
   ```

### 2. Application Deployment

1. **Start the Application**:
   ```bash
   # Build and start the application container
   docker-compose -f docker-compose.app.yml up --build
   
   # Or run in background
   docker-compose -f docker-compose.app.yml up -d
   
   # Check application status
   docker-compose -f docker-compose.app.yml ps
   
   # View application logs
   docker-compose -f docker-compose.app.yml logs -f
   ```

2. **Application Management**:
   ```bash
   # Stop the application
   docker-compose -f docker-compose.app.yml down
   
   # Restart the application
   docker-compose -f docker-compose.app.yml restart
   
   # Rebuild and restart the application
   docker-compose -f docker-compose.app.yml up --build -d
   ```

### 3. Combined Deployment

If you want to deploy both services together:

```bash
# Start both services
docker-compose -f docker-compose.db.yml -f docker-compose.app.yml up -d

# Stop both services
docker-compose -f docker-compose.db.yml -f docker-compose.app.yml down

# View logs for both services
docker-compose -f docker-compose.db.yml -f docker-compose.app.yml logs -f
```

### 4. Environment Configuration

1. **Database Environment**:
   - Configure database settings in `docker-compose.db.yml`:
     ```yaml
     environment:
       - POSTGRES_USER=postgres
       - POSTGRES_PASSWORD=postgres
       - POSTGRES_DB=org_management
     ```

2. **Application Environment**:
   - Configure application settings in `docker-compose.app.yml`:
     ```yaml
     environment:
       - DATABASE_URL=postgresql://postgres:postgres@db:5432/org_management
       - SECRET_KEY=your-secret-key-here
       - ALGORITHM=HS256
       - ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```

### 5. Access Points

- **Application**:
  - API Documentation: http://localhost:8000/docs
  - API Base URL: http://localhost:8000/api/v1

- **Database**:
  - Host: localhost
  - Port: 5432
  - Database: org_management
  - Username: postgres
  - Password: postgres

### 6. Default Superuser

After deployment, the system will create a default superuser:
- Email: admin@example.com
- Password: admin123

### 7. Troubleshooting

1. **Database Issues**:
   ```bash
   # Check database container status
   docker-compose -f docker-compose.db.yml ps
   
   # Check database logs
   docker-compose -f docker-compose.db.yml logs db
   
   # Check database health
   docker-compose -f docker-compose.db.yml exec db pg_isready -U postgres
   ```

2. **Application Issues**:
   ```bash
   # Check application container status
   docker-compose -f docker-compose.app.yml ps
   
   # Check application logs
   docker-compose -f docker-compose.app.yml logs web
   
   # Access application container shell
   docker-compose -f docker-compose.app.yml exec web bash
   ```

3. **Network Issues**:
   ```bash
   # Check network status
   docker network ls
   
   # Inspect network
   docker network inspect app-network
   ```