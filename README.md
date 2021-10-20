# Forensic Pipeline

## Usage
### Installation
1. Build Docker containers: `cd setup && ./create_containers.sh`
2. Create and activate virtualenv, and install requirements from `requirements.txt`
3. Initialize database: `python manage.py migrate`

### Run
1. Start redis and Celery worker: `docker-compose up -d`
2. Start app (enable virtualenv first): `cd setup && ./run_application.sh`
