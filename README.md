<!-- markdownlint-disable -->
<!-- This content will not be linted. -->

# Real Time Chat Application (FARM Stack Project)

This FARM (FastAPI, React, and MongoDB) project is a full-stack web application that combines the power of FastAPI for the backend, React for the frontend, and MongoDB for data storage. The project includes various features, such as JWT authentication, validation in bosth client side and server side, real-time chat with WebSocket integration, separate collections for private and group chat, and Docker configurations for both backend and frontend.

## Table of Contents

- [Real Time Chat Application (FARM Stack Project)](#real-time-chat-application-farm-stack-project)
  - [Table of Contents](#table-of-contents)
  - [App Reality](#app-reality)
    - [Welcome Page](#welcome-page)
    - [Signup Page](#signup-page)
    - [Login Page](#login-page)
    - [FastAPI Docs](#fastapi-docs)
    - [Private Chat](#private-chat)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Getting Started](#getting-started)
  - [Frontend](#frontend)
  - [Backend](#backend)
  - [Docker Setup](#docker-setup)
  - [License](#license)

## App Reality

### Welcome Page

![Welcome](/chatp-root/img/welcome.png)

### Signup Page

![Signup](chatp-root/img/signup.png)

### Login Page

![Login](chatp-root/img/login.png)

### FastAPI Docs

![Api Docs](chatp-root/img/api.png)

### Private Chat

![Pvt Chat](chatp-root/img/pvt-chat.png)

## Features

-   **FastAPI Backend**: Provides RESTful API endpoints.
-   **React Frontend**: User-friendly interface.
-   **MongoDB Database**: Efficient data storage.
-   **JWT Authentication**: Secure user access.
-   **Email Verification**: Required verification of email addresses for account activation.
-   **Field Validation**: Ensures data integrity.
-   **WebSocket Integration**: Real-time chat functionality.
-   **Separate Collections**: Distinct storage for private and group chat.
-   **Docker Setup**: Containerized development environment.

## Prerequisites

Before you begin, ensure you have met the following requirements:

-   Node.js and npm installed for React (+ vite) development
-   Python and pip installed for FastAPI development
-   MongoDB server up and running
-   Clone or download this repository to your local machine

## Getting Started

1. **Backend Setup:**

    ```bash
    $ cd chatp-root/backend
    $ pip install -r requirements.txt
    $ uvicorn app.main:app --reload
    ```

    Your FastAPI server should be running on `http://localhost:8000`.

2. **Frontend Setup:**

    ```bash
    $ cd chatp-root/frontend
    $ npm install
    $ npm run dev
    ```

    Your React development server should be running on `http://localhost:5173`.

3. **Celery Setup**
    ```bash
    $ cd chatp-root/backend
    $ celery -A app.services.worker.celery.celery worker --loglevel=info
    ```
4. **Redis Configuration:**

    - Set up your Redis in the backend

5. **Database Configuration:**
    - Set up your MongoDB connection in the backend.

<!-- ## Project Structure

- **backend:** Contains the FastAPI backend code.
- **frontend:** Contains the React frontend code.
- **scripts:** Helpful scripts for development or deployment.
- **docs:** Documentation for your project. -->

<!-- ## API Endpoints

- List and describe the available API endpoints here. -->

## Frontend

The frontend of our Real Time Chat Application is built with React and Vite for a fast development experience. It offers a responsive user interface for real-time chat and includes the following technologies:

-   **React**: A powerful JavaScript library for building user interfaces.
-   **Vite**: A modern development environment that optimizes frontend development.
-   **Dependencies**: Axios, Framer Motion, React Router, and Websocket Client for efficient communication.
-   **DevDependencies**: ESLint and Tailwind CSS for code quality and styling.

Our frontend incorporates client-side authentication, enhancing security and user access control. This ensures that only authorized users can access certain features of the application.

## Backend

Our backend, powered by FastAPI, is the backbone of the Real Time Chat Application. It utilizes various dependencies to ensure high-performance and secure functionality, including:

-   **FastAPI**: A modern Python framework for efficient API development.
-   **Pydantic**: Ensures data validation and settings management.
-   **Motor and PyMongo**: Connects to MongoDB for database support.
-   **WebSockets**: Enables real-time chat using libraries like python-socketio and starlette.
-   **Cryptography and Passlib**: Provide security for communication and user password storage.
-   **Celery**: Implements asynchronous processing for tasks like email verification, enhancing the application's responsiveness and scalability.

Our backend offers robust user authentication and authorization, both on the client and server sides. Real-time chat functionality is seamlessly integrated with the security features. The development environment is optimized for speed and efficiency, using Uvicorn to serve the FastAPI application.

<!-- ## Database

- Explain how to set up and configure your MongoDB database.
- Describe the organization of collections, including separate collections for private and group chat. -->

<!-- ## WebSocket Integration

- Explain how WebSocket integration works for real-time chat.
- Describe the structure and functionality of WebSocket endpoints. -->

<!-- ## Authentication

- Explain how JWT authentication is implemented for secure user access.
- Provide details on user registration and login processes. -->

## Docker Setup

-   **Docker Files:**

    -   `Dockerfile` in the `backend` directory for the FastAPI backend.
    -   `Dockerfile` in the `frontend` directory for the React frontend.

-   **Docker Compose:**

    -   `docker-compose.yml` for setting up the development environment with both backend and frontend containers.

    To start the containers, use:

    ```bash
    $ cd chatp-root
    $ docker-compose up --build
    ```

    The backend should be accessible at `http://localhost:8000`, and the frontend at `http://localhost:5173`.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

<!-- markdownlint-restore -->
<!-- This content will be linted. -->
