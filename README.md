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

### Github commands

git checkout -b develop main
git checkout -b feature/MLO-1 develop
git checkout develop
git merge --no-ff feature/MLO-1
git branch -d feature/MLO-1
git push origin develop


### MongoDB

#### Remove services
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans

#### Start the services
docker-compose -f infrastructure/docker/development/docker-compose.dev.yml up -d

docker-compose -f docker-compose.dev.yml up -d --build

#### See logs
docker-compose -f docker-compose.dev.yml logs -f endor_python_mongodb_dev



#### Test the health endpoint
curl http://localhost:8005/api/v1/health

#### Create a test record
curl -X POST "http://localhost:8005/api/v1/test/?name=test1"

#### Get all test records
curl http://localhost:8005/api/v1/test/


#### Get transcript
curl http://localhost:8005/api/v1/transcript/Tm_2RZm8JB8
curl http://localhost:8005/api/v1/transcript/

docker-compose -f docker-compose.dev.yml exec -u appuser endor_python_mongodb_dev python -m pytest -v


curl -X POST http://localhost:8005/api/v1/transcript/batch \
-H "Content-Type: application/json" \
-d '{"video_ids": ["Tm_2RZm8JB8", "GAe1IQtHqVU"], "languages": ["en", "de"]}'


