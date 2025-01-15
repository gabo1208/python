# Basic App with Django and Express.js

This project is a basic web application that uses Django for the backend and Express.js for the frontend. It serves as a starting point for building more complex applications.

## Features

- Django backend
- Express.js frontend
- RESTful API
- User authentication
- Basic CRUD operations

## Requirements

- Python 3.x
- Django 3.x
- Node.js
- Express.js

## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/gabo1208/basic-app-expressjs.git
  cd basic-app-expressjs
  ```

2. Set up the Django backend:
  ```bash
  cd backend
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py runserver
  ```

3. Set up PostgreSQL
  - Install PostgreSQL
  - Create a super user and a DB, in this case the user is `postgres` and the DB is `my_site`
  - Create the `~/.pg_service.conf` file (adjust accordingly):
  ```bash
  [my_service]
  host=localhost
  user=postgres
  dbname=my_service
  port=5432
  ```
- Create the `.pgpass` file in the root of your Django project:
```bash
localhost:5432:my_service:postgres:postgres
```

4. Set up the Express.js frontend:
  ```bash
  cd ../frontend
  npm install
  npm start
  ```

## Usage

- Access the Django admin panel at `http://localhost:8000/admin`
- Access the Express.js frontend at `http://localhost:3000`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
