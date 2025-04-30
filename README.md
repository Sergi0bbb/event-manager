# Event Management API

A Django REST API for managing events like conferences, meetups, etc. The application allows users to create, view, update, and delete events, as well as register for these events.

---

## Features

- Event Management: Create, read, update, and delete events
- User Authentication: Register, login, and manage user accounts
- Event Registration: Allow users to register for events
- API Documentation: Interactive API documentation using Swagger

---

## 📦 Tech Stack

- Python
- Django REST Framework  
- PostgreSQL
- Docker
- drf-yasg for API docs

---

## 🛠 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Sergi0bbb/event-manager
cd event-managemager
```

### 2. Create `.env` File  
Create a `.env` file with the necessary configuration (e.g., database settings).

### 3. Run with Docker
```bash
docker-compose up --build
```

### 4. Apply Migrations
```bash
docker-compose exec web python manage.py migrate
```

### 5. Create Superuser (optional)
```bash
docker-compose exec web python manage.py createsuperuser
```

---

## API Documentation

- Swagger UI: `http://localhost:8000/api/docs/`

---

## Authentication

Authentication is implemented using tokens.

- Get a token: `POST /api/token/`
- Add to request headers:  
  `Authorization: Token <your_token>`

---

## 📮 Example Endpoints

| Method | Endpoint                         | Description                     |
|--------|----------------------------------|---------------------------------|
| GET    | `/api/events/`                  | List all events                 |
| POST   | `/api/events/`                  | Create a new event              |
| GET    | `/api/events/<id>/`             | Retrieve an event by ID         |
| PUT    | `/api/events/<id>/`             | Update an event                 |
| DELETE | `/api/events/<id>/`             | Delete an event                 |
| POST   | `/api/register/`                | Register a new user             |
| POST   | `/api/login/`                   | Log in and get an auth token    |
| POST   | `/api/events/<id>/register/`    | Register for an event           |
