# TaskFlow — Full Stack Task Management & Assignment Platform

TaskFlow is a production-style full-stack task management platform built with **Django REST Framework**, **React.js**, **PostgreSQL**, **Redis**, **Celery**, **Docker**, **Terraform**, **AWS EC2**, **Nginx**, and **GitHub Actions CI/CD**.

The application allows admins to create and assign tasks to users, track task progress, view dashboard analytics, and trigger asynchronous email notifications when tasks are assigned.

This project demonstrates practical full-stack development, backend API design, role-based access control, async processing, containerization, cloud deployment, Infrastructure as Code, and CI/CD automation.

---

## Live Deployment

```text
Frontend App : http://YOUR_EC2_PUBLIC_IP/
Django Admin : http://YOUR_EC2_PUBLIC_IP/admin/
Backend API  : http://YOUR_EC2_PUBLIC_IP/api/
```

> Replace `YOUR_EC2_PUBLIC_IP` with the deployed EC2 public IP.

---

## Project Highlights

- Built a complete full-stack task management system from scratch.
- Implemented JWT authentication with Admin/User role-based access.
- Designed REST APIs for user management, task assignment, status updates, and dashboards.
- Integrated PostgreSQL with relational models and indexed fields for faster querying.
- Added Redis and Celery for asynchronous email notification processing.
- Developed responsive React.js frontend with protected routes and role-based navigation.
- Added Postman API testing and PyTest automated backend test cases.
- Containerized the full application using Docker Compose.
- Deployed the application on AWS EC2 using Gunicorn and Nginx reverse proxy.
- Provisioned AWS infrastructure using Terraform.
- Automated deployment using GitHub Actions CI/CD.

---

## What This Application Can Do

### Admin Can

- Login securely using JWT authentication.
- View dashboard analytics.
- View all users.
- Create tasks.
- Assign tasks to users.
- Set task priority and due date.
- View all tasks.
- Filter tasks by status and priority.
- Update full task details.
- Delete tasks.
- Update task status.
- Trigger async email notification when a task is assigned.

### User Can

- Login securely using JWT authentication.
- View personal dashboard.
- View only assigned tasks.
- Track pending, in-progress, and completed tasks.
- Update status of assigned tasks.
- View upcoming due tasks.

---

## Why This Project Is Valuable

TaskFlow is not just a CRUD project. It includes several real-world engineering concepts used in production applications:

```text
Authentication
Authorization
REST API design
Relational database modeling
Query optimization
Async background jobs
Frontend route protection
Role-based UI rendering
Containerized deployment
Reverse proxy configuration
Infrastructure as Code
CI/CD automation
Cloud deployment
Automated testing
```

This makes the project suitable for roles involving:

```text
Python Developer
Django Developer
Full Stack Developer
Backend Developer
Cloud/DevOps Engineer
Python Full Stack Developer
```

---

## Architecture Overview

```text
User Browser
    |
    | HTTP
    v
Nginx Reverse Proxy
    |
    |-- /              → React Frontend
    |-- /api/          → Django REST API
    |-- /admin/        → Django Admin
    |-- /static/       → Django Static Files
                         |
                         v
                 Django REST Framework
                         |
        --------------------------------
        |                              |
        v                              v
   PostgreSQL                      Redis
   Database                        Broker
                                      |
                                      v
                                  Celery Worker
                                  Async Email Jobs
```

---

## Tech Stack

### Backend

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Web framework |
| Django REST Framework | REST API development |
| Simple JWT | JWT authentication |
| PostgreSQL | Relational database |
| Redis | Celery message broker |
| Celery | Background task processing |
| PyTest | Automated backend testing |
| Gunicorn | Production WSGI server |

### Frontend

| Technology | Purpose |
|---|---|
| React.js | Frontend UI |
| Vite | React build tool |
| Axios | API communication |
| React Router DOM | Routing and protected routes |
| Bootstrap | Responsive UI styling |
| JavaScript ES6+ | Frontend logic |

### DevOps and Cloud

| Technology | Purpose |
|---|---|
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Nginx | Reverse proxy and frontend serving |
| AWS EC2 | Cloud deployment |
| Terraform | Infrastructure as Code |
| GitHub Actions | CI/CD automation |

---

## Screenshots

Add screenshots here after final UI capture.

### Login Page

```text
assets/screenshots/login.png
```

### Admin Dashboard

```text
assets/screenshots/admin-dashboard.png
```

### Task List

```text
assets/screenshots/task-list.png
```

### Create Task

```text
assets/screenshots/create-task.png
```

### User Dashboard

```text
assets/screenshots/user-dashboard.png
```

---

## Core Features

### 1. JWT Authentication

The application uses JWT-based authentication.

After successful login, the backend returns:

```text
access token
refresh token
logged-in user details
role information
```

The frontend stores the token and sends it in protected API requests.

```text
Authorization: Bearer <access_token>
```

---

### 2. Role-Based Access Control

There are two roles:

```text
ADMIN
USER
```

Admin and User permissions are handled at both backend and frontend levels.

Backend permissions prevent unauthorized API access.

Frontend protected routes prevent users from accessing pages they are not allowed to view.

---

### 3. Task Management

TaskFlow supports:

```text
Task creation
Task assignment
Task status update
Task priority
Due date tracking
Task filtering
Task deletion
```

Task statuses:

```text
PENDING
IN_PROGRESS
COMPLETED
```

Task priorities:

```text
LOW
MEDIUM
HIGH
```

---

### 4. Dashboard Analytics

Admin dashboard shows:

```text
Total users
Total admins
Total tasks
Pending tasks
In-progress tasks
Completed tasks
High-priority tasks
Overdue tasks
```

User dashboard shows:

```text
My total tasks
My pending tasks
My in-progress tasks
My completed tasks
My high-priority tasks
Upcoming due tasks
```

---

### 5. Async Email Notification

When an admin assigns a new task, the backend creates the task immediately and sends the notification job to Celery.

Flow:

```text
Admin creates task
    ↓
Django saves task in PostgreSQL
    ↓
Django sends job to Redis
    ↓
Celery receives job
    ↓
Email notification is processed asynchronously
```

This prevents slow email processing from blocking the API response.

---

### 6. Dockerized Deployment

The project runs as multiple Docker containers:

| Container | Purpose |
|---|---|
| backend | Django REST API with Gunicorn |
| frontend | React production build |
| db | PostgreSQL database |
| redis | Redis broker |
| celery | Background worker |
| nginx | Reverse proxy |

---

### 7. Terraform Infrastructure

Terraform provisions AWS infrastructure:

```text
Custom VPC
Public subnet
Internet gateway
Route table
Security group
EC2 instance
Root EBS volume
```

This makes the infrastructure reproducible and version-controlled.

---

### 8. GitHub Actions CI/CD

Every push to the `main` branch triggers deployment.

CI/CD flow:

```text
git push origin main
    ↓
GitHub Actions workflow starts
    ↓
SSH into EC2
    ↓
Pull latest code
    ↓
Rebuild Docker containers
    ↓
Restart application
    ↓
Deployment complete
```

---

## API Endpoints

### Authentication APIs

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | Public | Register user |
| POST | `/api/auth/login/` | Public | Login and get JWT tokens |
| POST | `/api/auth/token/refresh/` | Public | Refresh access token |
| GET | `/api/auth/profile/` | Authenticated | Get logged-in user profile |
| GET | `/api/auth/users/` | Admin | List all users |

---

### Task APIs

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/tasks/` | Admin/User | List tasks |
| POST | `/api/tasks/` | Admin | Create task |
| GET | `/api/tasks/<id>/` | Admin/Assigned User | Get task detail |
| PUT | `/api/tasks/<id>/` | Admin | Full task update |
| PATCH | `/api/tasks/<id>/` | Admin | Partial task update |
| DELETE | `/api/tasks/<id>/` | Admin | Delete task |
| PATCH | `/api/tasks/<id>/status/` | Admin/Assigned User | Update task status |

---

### Dashboard APIs

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/dashboard/admin/` | Admin | Admin dashboard stats |
| GET | `/api/dashboard/user/` | Authenticated | User dashboard stats |

---

## Project Structure

```text
taskflow/
│
├── backend/
│   ├── accounts/
│   ├── dashboard/
│   ├── tasks/
│   ├── taskflow_backend/
│   ├── tests/
│   ├── Dockerfile
│   ├── manage.py
│   ├── pytest.ini
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── context/
│   │   └── pages/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── nginx/
│   └── default.conf
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── user_data.sh
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/taskflow-fullstack.git
cd taskflow-fullstack
```

---

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` inside `backend/`:

```env
SECRET_KEY=django-insecure-local-secret-key
DEBUG=True

DB_NAME=taskflow_db
DB_USER=taskflow_user
DB_PASSWORD=taskflow_password
DB_HOST=localhost
DB_PORT=5432

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@taskflow.local
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create admin:

```bash
python manage.py createsuperuser
```

Run backend:

```bash
python manage.py runserver
```

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173/
```

---

### 4. Redis and Celery

Start Redis:

```bash
sudo systemctl start redis-server
redis-cli ping
```

Expected:

```text
PONG
```

Start Celery:

```bash
cd backend
source venv/bin/activate
celery -A taskflow_backend worker -l info
```

---

## Docker Setup

Create `backend/.env.production`:

```env
SECRET_KEY=replace-with-secret-key
DEBUG=False

ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost,http://127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1

DB_NAME=taskflow_db
DB_USER=taskflow_user
DB_PASSWORD=taskflow_password
DB_HOST=db
DB_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@taskflow.local
```

Run:

```bash
docker compose up --build -d
```

Check containers:

```bash
docker compose ps
```

Access app:

```text
http://127.0.0.1/
```

---

## Testing

### PyTest

```bash
cd backend
source venv/bin/activate
pytest
```

Current result:

```text
17 passed
```

Test coverage includes:

```text
Admin login
User login
Profile API
User list permission
Task creation
Task access permissions
Task status update
Dashboard permissions
Celery trigger mocking
```

---

### Postman

Postman collection covers:

```text
Admin login
User login
Profile API
User list API
Task creation
Task listing
Task status update
Admin dashboard
User dashboard
Unauthorized access checks
```

Environment variables:

```text
base_url
admin_access_token
admin_refresh_token
user_access_token
user_refresh_token
task_id
```

---

## AWS Deployment Using Terraform

Terraform files are inside:

```text
terraform/
```

Run:

```bash
cd terraform
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Terraform creates:

```text
VPC
Public subnet
Internet gateway
Route table
Security group
EC2 instance
Docker-ready Ubuntu server
```

After deployment, Terraform outputs:

```text
EC2 public IP
EC2 public DNS
SSH command
App URL
Admin URL
```

---

## GitHub Actions CI/CD

Workflow:

```text
.github/workflows/deploy.yml
```

Required GitHub secrets:

```text
EC2_HOST
EC2_USER
EC2_SSH_KEY
EC2_PROJECT_PATH
```

On every push to `main`, GitHub Actions:

```text
Connects to EC2
Pulls latest code
Checks production env file
Stops containers
Rebuilds Docker images
Restarts containers
Shows running services
```

---

## Current Implementation Status

| Area | Status |
|---|---|
| Backend APIs | Completed |
| JWT Authentication | Completed |
| Role-Based Access | Completed |
| PostgreSQL Integration | Completed |
| Redis + Celery | Completed |
| React Frontend | Completed |
| Admin Dashboard | Completed |
| User Dashboard | Completed |
| Task Management | Completed |
| Postman Testing | Completed |
| PyTest Testing | Completed |
| Docker Setup | Completed |
| Nginx Reverse Proxy | Completed |
| Terraform EC2 Provisioning | Completed |
| AWS EC2 Deployment | Completed |
| GitHub Actions CI/CD | Completed |

---

## What Can Be Improved Next

This project already covers the complete full-stack deployment flow, but future improvements can make it even closer to production.

### 1. HTTPS Support

Current deployment uses HTTP.

Improvement:

```text
Add HTTPS using Certbot, Nginx SSL, or AWS Load Balancer with ACM certificate.
```

---

### 2. Real Email Provider

Current email notification uses console email backend.

Improvement:

```text
Integrate Gmail SMTP, AWS SES, SendGrid, or Mailgun.
```

---

### 3. AWS RDS

Current PostgreSQL runs inside Docker on EC2.

Improvement:

```text
Move PostgreSQL to AWS RDS for automated backups, better availability, and managed scaling.
```

---

### 4. AWS ElastiCache

Current Redis runs inside Docker on EC2.

Improvement:

```text
Move Redis to AWS ElastiCache for managed Redis performance and reliability.
```

---

### 5. File Attachments

Current tasks do not support attachments.

Improvement:

```text
Add file upload support using AWS S3.
```

---

### 6. Task Comments and Activity Logs

Current task module supports status updates but not comments.

Improvement:

```text
Add task comments, audit logs, and activity timeline.
```

---

### 7. Password Reset

Current auth supports login and registration.

Improvement:

```text
Add forgot password and password reset using email verification.
```

---

### 8. Pagination and Search

Current APIs support filters.

Improvement:

```text
Add pagination, search, and advanced sorting for larger datasets.
```

---

### 9. Frontend UI Enhancements

Current UI is functional and responsive.

Improvement:

```text
Add charts, better dashboard visuals, loading skeletons, toast notifications, and dark mode.
```

---

### 10. Stronger CI/CD Pipeline

Current CI/CD deploys on push.

Improvement:

```text
Add test execution before deployment, Docker image caching, build artifacts, rollback strategy, and deployment approvals.
```

---

## Key Engineering Decisions

### Why Django REST Framework?

DRF provides a strong structure for building secure REST APIs quickly with serializers, views, authentication, permissions, and browsable APIs.

### Why JWT?

JWT allows stateless authentication, which works well with React frontends and REST APIs.

### Why PostgreSQL?

PostgreSQL is reliable for relational data and supports indexing, constraints, and production-grade data handling.

### Why Redis + Celery?

Task assignment emails should not slow down API response time. Celery moves email processing to the background.

### Why Docker?

Docker makes the application portable and consistent across local, test, and production environments.

### Why Nginx?

Nginx works as a single public entry point and routes frontend, backend, admin, and static traffic cleanly.

### Why Terraform?

Terraform makes infrastructure reproducible and avoids manual AWS console configuration.

### Why GitHub Actions?

GitHub Actions automates deployment, reducing manual work and making releases more consistent.

---

## Challenges Faced and Solved

### 1. Custom User Model Setup

A custom user model was required to support Admin/User roles.

Solved by extending Django `AbstractUser` and configuring:

```python
AUTH_USER_MODEL = "accounts.User"
```

---

### 2. Role-Based API Protection

Users should not access admin APIs or other users' tasks.

Solved using custom permission classes and queryset filtering.

---

### 3. Celery Integration

Task assignment needed async email notification.

Solved using Redis as broker and Celery worker container.

---

### 4. Docker Networking

Backend needed to connect to PostgreSQL and Redis inside Docker.

Solved by using Docker service names:

```text
DB_HOST=db
CELERY_BROKER_URL=redis://redis:6379/0
```

---

### 5. Nginx Reverse Proxy

Frontend and backend originally ran on different ports.

Solved by using root Nginx proxy:

```text
/        → React
/api/    → Django
/admin/  → Django Admin
```

---

### 6. Terraform Default VPC Error

AWS region had no default VPC.

Solved by creating a custom VPC, subnet, internet gateway, and route table using Terraform.

---

### 7. GitHub Large File Rejection

Terraform provider binaries were accidentally staged.

Solved by cleaning Git history and ignoring:

```text
terraform/.terraform/
terraform/*.tfstate
terraform/*.tfvars
terraform/*.pem
```

---

### 8. GitHub Actions SSH Timeout

Security group allowed SSH only from local laptop IP.

Solved for demo by allowing SSH from GitHub Actions runners.

Production improvement would be AWS SSM or self-hosted runner.

---

## Resume Bullet Points

```text
• Built a full-stack task management application using Django REST Framework and React.js with JWT authentication and role-based access control.
• Designed REST APIs for user management, task creation, task assignment, status updates, and dashboard analytics.
• Integrated PostgreSQL with relational models, indexing, and optimized query handling.
• Implemented Redis and Celery for asynchronous email notifications and background task processing.
• Developed responsive frontend screens using React.js, JavaScript ES6+, HTML5, CSS3, Bootstrap, Axios, and React Router.
• Added API testing using Postman and automated backend testing using PyTest.
• Containerized the application using Docker Compose with Django, React, PostgreSQL, Redis, Celery, Gunicorn, and Nginx services.
• Provisioned AWS EC2 infrastructure using Terraform with custom VPC, subnet, route table, internet gateway, and security group.
• Deployed the application on AWS EC2 and automated deployments using GitHub Actions CI/CD.
```

---

## Interview Explanation

TaskFlow is a full-stack role-based task management application. The backend is built using Django REST Framework and exposes secure REST APIs. Authentication is handled using JWT, and users are divided into Admin and User roles.

Admins can create and assign tasks, while regular users can only view and update the status of tasks assigned to them. Dashboard APIs provide summary analytics for both admin and user roles.

The backend uses PostgreSQL for relational data storage, with indexed fields for task status, priority, due date, assigned user, and created user. Redis and Celery are used for asynchronous background processing. When a task is assigned, the API responds immediately while Celery handles the email notification in the background.

The frontend is built with React.js and includes protected routes, role-based navigation, dashboards, task listing, task creation, and status updates.

The entire application is containerized using Docker Compose. Nginx acts as the reverse proxy and routes traffic to React, Django APIs, Django admin, and static files. The application is deployed on AWS EC2, with infrastructure provisioned using Terraform. GitHub Actions is used for CI/CD, automatically deploying changes from the main branch to EC2.

---

## Author

**Abdul**
