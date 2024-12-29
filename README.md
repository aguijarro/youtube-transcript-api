### FastAPI Project

This is a FastAPI project template. 

### Requirements

- Python 3.10+
- FastAPI 0.109.2
- Uvicorn 0.27.1


### Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r base.txt
```

### Installation

1. Clone the repository
2. Install the dependencies
3. Run the development server

```bash
pip install -r requirements/base.txt
uvicorn app.main:app --reload
uvicorn app.main:app --port 8001
```

### Installation

git checkout -b develop main
git checkout -b feature/MLO-1 develop
git checkout develop
git merge --no-ff feature/MLO-1
git branch -d feature/MLO-1
git push origin develop

### Docker
docker-compose -f docker-compose.dev.yml up -d --build
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans --rmi all
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans --rmi all --force-rm
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans --rmi all --force-rm --timeout 0
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans --rmi all --force-rm --timeout 0 --remove-orphans

cd endor_python
docker-compose -f infrastructure/docker/development/docker-compose.dev.yml up -d --build

docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
docker-compose -f docker-compose.dev.yml up -d --build

docker-compose -f docker-compose.dev.yml logs -f endor_python_dev


# Clean up everything
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
docker system prune -f
docker volume prune -f

# Rebuild
docker-compose -f docker-compose.dev.yml up -d --build

# Database
docker-compose -f docker-compose.dev.yml exec endor_python_db psql -U postgres

postgres=# \c endor_python_dev
postgres=# \q


# Tests
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
docker-compose -f docker-compose.dev.yml up -d --build
docker-compose -f docker-compose.dev.yml exec -u appuser endor_python_dev python -m pytest -v

# Database Migrations
# Create a new migration
docker-compose -f docker-compose.dev.yml exec -u appuser endor_python_dev alembic init app/migrations

docker-compose -f docker-compose.dev.yml exec -u appuser endor_python_dev alembic revision --autogenerate -m "create test table"

# Apply migrations
docker-compose -f docker-compose.dev.yml exec -u appuser endor_python_dev alembic upgrade head

# Rollback one migration
docker-compose -f docker-compose.dev.yml exec -u appuser endor_python_dev alembic downgrade -1

# Rebuild containers
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
docker-compose -f docker-compose.dev.yml up -d --build

# Generate migration
docker-compose -f docker-compose.dev.yml exec -u appuser endor_python_dev alembic revision --autogenerate -m "create test table"

# Apply migration
docker-compose -f docker-compose.dev.yml exec -u appuser endor_python_dev alembic upgrade head


# Validate migrations
docker-compose -f docker-compose.dev.yml exec endor_python_db psql -U postgres
\c endor_python_dev
\dt
\d test_table
SELECT * FROM test_table;
\q

Test EndPoints

# Start the services
docker-compose -f infrastructure/docker/development/docker-compose.dev.yml up -d

# Test the health endpoint
curl http://localhost:8005/api/v1/health/health

# Create a test record
curl -X POST "http://localhost:8005/api/v1/test/?name=test1"

# Get all test records
curl http://localhost:8005/api/v1/test/


### Test inserting data

docker-compose -f infrastructure/docker/development/docker-compose.dev.yml exec -u appuser endor_python_dev alembic upgrade head

docker-compose -f infrastructure/docker/development/docker-compose.dev.yml restart endor_python_dev

curl -X POST "http://localhost:8005/api/v1/test/?name=test1"



### MongoDB

# Remove services
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans

# Start the services
docker-compose -f infrastructure/docker/development/docker-compose.dev.yml up -d

docker-compose -f docker-compose.dev.yml up -d --build

# See logs
docker-compose -f docker-compose.dev.yml logs -f endor_python_dev



# Test the health endpoint
curl http://localhost:8005/api/v1/health

# Create a test record
curl -X POST "http://localhost:8005/api/v1/test/?name=test1"

# Get all test records
curl http://localhost:8005/api/v1/test/
