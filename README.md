# story-game
# Setup
First of all you need install `poetry`:
```shell
pip install poetry
```
Create a virtual environment and activate it.
```shell
poetry install
poetry shell
```
Serverless Framework open-source CLI that helps deploy a sample Service on AWS that reports deployment information and operational metrics to the Serverless Framework Dashboard. The Serverless Framework also helps setup DynamoDB locally.
To get started, you'll need the Serverless Framework installed. You'll also need your environment configured with AWS credentials.

How to install `Serverless Framework` you can see in [here](https://www.serverless.com/framework/docs/providers/aws/guide/quick-start/).

Then, you need setup AWS credentials, [see more](https://www.serverless.com/framework/docs/providers/aws/guide/credentials/).

Install a few dependencies. We're going to use the serverless-wsgi plugin for negotiating the API Gateway event type into the WSGI format that Flask expects. We'll also use the serverless-python-requirements plugin for handling our Python packages on deployment.

```shell
npm install --save-dev serverless-wsgi serverless-python-requirements serverless-dynamodb-local
```
Create requirements.txt for Serverless Framework:
```shell
poetry export -f requirements.txt --output requirements.txt --without-hashes
```
Run a command to install DynamoDB local:
```shell
sls dynamodb install
```
Start DynamoDB locally:
```shell
sls dynamodb start
```
In the second window, start up your local WSGI server:
```shell
sls wsgi serve
```
Deploy on AWS:

Provide env file:
```.shell
STAGE=dev
REGION=region
LOCAL=0
DB_HOST=RDS-host-name
DB_PASS=RDS-password
DB_USER=user
DB_NAME=table-name
```
After, run
```shell
 sls deploy
```

## ALEMBIC
Create migration:
```shell
alembic revision --message="your message" --autogenerate
```
Apply all migrations
```shell
alembic upgrade head
```
Revert migration:
Assuming that you only want to go back one revision
```shell
alembic downgrade -1
```
List of all migrations
```shell
alembic history
```
Choose the identifier of the migration you want to go back to:
```shell
alembic downgrade 8ac14e223d1e
```

# How to test:
If you want to test dynamodb data source you can use package `moto`.
To test RDS data source you need up a test database. Up test database:
```shell
docker-compose up --build -d
```
Run tests:
```shell
export PYTHONPATH=./src
pytest tests
```

#WIKI
Great tutorial about alembic: https://habr.com/ru/company/yandex/blog/511892/
