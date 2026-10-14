# Cloud Event Management System

A cloud-based event management and attendance system designed to simplify college event administration using Flask, Microsoft Azure Cosmos DB, Docker, and HTML, CSS, and JavaScript.

## Project Overview

The system helps administrators manage college events and student registrations while tracking attendance. It provides separate dashboards for administrators and students.

## Features

- **Event Management:** Create and retrieve events.
- **Student Registration:** Register students for events and store registration details.
- **Attendance Tracking:** Record and retrieve attendance status.
- **Admin Dashboard:** Manage events, registrations, and attendance.
- **Student Dashboard:** View events and access registration functionality.
- **Cloud Database:** Store and retrieve application data using Azure Cosmos DB.
- **Containerization:** Package the Flask backend using Docker.
- **Production Preparation:** Configure the backend to support Gunicorn and environment-based port settings.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Database | Microsoft Azure Cosmos DB |
| API Communication | REST APIs, JSON |
| Containerization | Docker |
| Production Server | Gunicorn |
| Version Control | Git and GitHub |

## Project Structure

```text
CloudEventManagement/
├── BackEnd/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .dockerignore
│   └── .gitignore
├── FrontEnd/
│   ├── admin-dashboard.html
│   ├── student-dashboard.html
│   ├── index.html
│   ├── login.html
│   └── js/
│       └── app.js
├── .gitignore
└── README.md
```

## Backend API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check backend availability |
| GET | `/events` | Retrieve events |
| POST | `/events` | Create an event |
| POST | `/registrations` | Register a student |
| GET | `/registrations/<event_id>` | Retrieve registrations for an event |
| POST | `/attendance` | Record attendance |
| GET | `/attendance/<event_id>` | Retrieve attendance for an event |

## Local Setup and Testing

### Prerequisites

- Python
- Docker Desktop
- Microsoft Azure Cosmos DB account and configured database
- Git

### Configure environment variables

Create a `.env` file inside `BackEnd/` with the required database configuration:

```text
COSMOS_ENDPOINT=your_cosmos_endpoint
COSMOS_KEY=your_cosmos_key
COSMOS_DATABASE=your_database_name
COSMOS_CONTAINER=your_container_name
```

Use your own credentials. **Never commit `.env` or database keys to GitHub.**

### Build the backend Docker image

Run these commands from the project root:

```powershell
docker build -t cloud-event-backend:azure-test .\BackEnd
```

### Run the test container

```powershell
docker run -d --name cloud-event-backend-test --env-file .\BackEnd\.env -p 5001:5000 cloud-event-backend:azure-test
```

### Verify the backend

Open these URLs in a browser or test them with `curl.exe`:

```text
http://localhost:5001/
http://localhost:5001/events
http://localhost:5001/registrations/E009
http://localhost:5001/attendance/E009
```

The root endpoint should return a backend status message. The other endpoints return data according to the database contents.

After testing, remove the temporary container:

```powershell
docker stop cloud-event-backend-test
docker rm cloud-event-backend-test
```

## Testing Status

The following have been verified locally:

- Docker image builds successfully.
- The updated backend starts using Gunicorn.
- The backend health endpoint responds successfully.
- Events are retrieved from Azure Cosmos DB.
- Registration and attendance endpoints have been checked.
- The existing frontend dashboards have been opened and tested.

## Deployment Status

The project has been tested locally using Docker and Azure Cosmos DB. The backend has been configured for production preparation, including Gunicorn and environment-based port settings.

**Deployment to Azure hosting is pending.** Deployment will be completed separately after reviewing resource requirements and available Azure credits.

## Future Enhancements

- Complete Azure hosting deployment.
- Integrate and validate certificate generation.
- Improve input validation and error handling.
- Add authentication and role-based access control.
- Improve automated testing and application documentation.

## Repository

GitHub: https://github.com/Varlakshmi19/cloud-event-management-system
