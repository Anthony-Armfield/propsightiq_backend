# PropSightIQ Backend

A data-driven real estate tool to help realtors view enriched home listings.

## Technologies Used
- Python/Django
- PostgreSQL
- Docker/Docker Compose

## Local Development Setup
1. Clone this repository
2. Make sure Docker and Docker Compose are installed on your machine
3. Run \`docker-compose up\`
4. Access the application at http://localhost:8000

## Environment Variables
Configure the following variables in your .env file:
- DB_NAME - PostgreSQL database name
- DB_USER - Database username
- DB_PASSWORD - Database password
- DB_HOST - Database host (db for Docker setup)
- DB_PORT - Database port (default: 5432)
- SECRET_KEY - Django secret key
- DEBUG - Debug mode (True/False)
