<!-- markdownlint-disable -->
<!-- This content will not be linted. -->

# Real Time Chat Application (FARM Stack Project)
---

This FARM (FastAPI, React, and MongoDB) project is a full-stack web application that combines the power of FastAPI for the backend, React for the frontend, and MongoDB for data storage. The project includes various features, such as JWT authentication, field validation, real-time chat with WebSocket integration, separate collections for private and group chat, and Docker configurations for both backend and frontend. 



## Table of Contents
---

- [Real Time Chat Application (FARM Stack Project)](#real-time-chat-application-farm-stack-project)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Getting Started](#getting-started)
  - [Project Structure](#project-structure)
  - [Docker Setup](#docker-setup)
  - [License](#license)

## Features
---

- **FastAPI Backend**: Provides RESTful API endpoints.
- **React Frontend**: User-friendly interface.
- **MongoDB Database**: Efficient data storage.
- **JWT Authentication**: Secure user access.
- **Field Validation**: Ensures data integrity.
- **WebSocket Integration**: Real-time chat functionality.
- **Separate Collections**: Distinct storage for private and group chat.
- **Docker Setup**: Containerized development environment.

## Prerequisites
---

Before you begin, ensure you have met the following requirements:

- Node.js and npm installed for React development
- Python and pip installed for FastAPI development
- MongoDB server up and running
- Clone or download this repository to your local machine

## Getting Started
---

1. **Backend Setup:**

   ```bash
   $ cd backend
   $ pip install -r requirements.txt
   $ uvicorn app.main:app --reload
   ```

   Your FastAPI server should be running on `http://localhost:8000`.

2. **Frontend Setup:**

   ```bash
   $ cd frontend
   $ npm install
   $ npm run dev
   ```

   Your React development server should be running on `http://localhost:5173`.

3. **Database Configuration:**

   - Set up your MongoDB connection in the backend.



## Project Structure
---

- **backend:** Contains the FastAPI backend code.
- **frontend:** Contains the React frontend code.
- **scripts:** Helpful scripts for development or deployment.
- **docs:** Documentation for your project.

<!-- ## API Endpoints

- List and describe the available API endpoints here.

## Frontend

- Describe the structure of your React frontend.
- Highlight any key components or features.

## Backend

- Describe the structure of your FastAPI backend.
- Explain how to add new routes or modify existing ones.

## Database

- Explain how to set up and configure your MongoDB database.
- Describe the organization of collections, including separate collections for private and group chat.

## WebSocket Integration

- Explain how WebSocket integration works for real-time chat.
- Describe the structure and functionality of WebSocket endpoints.

## Authentication
---

- Explain how JWT authentication is implemented for secure user access.
- Provide details on user registration and login processes. -->

## Docker Setup
---

- **Docker Files:**

  - `Dockerfile` in the `backend` directory for the FastAPI backend.
  - `Dockerfile` in the `frontend` directory for the React frontend.

- **Docker Compose:**

  - `docker-compose.yml` for setting up the development environment with both backend and frontend containers.

  To start the containers, use:

  ```bash
  $ docker-compose up --build
  ```

  The backend should be accessible at `http://localhost:8000`, and the frontend at `http://localhost:3000`.

## License
---

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.


<!-- markdownlint-restore -->
<!-- This content will be linted. -->