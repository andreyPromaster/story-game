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
Command for deploy on AWS:
Change LOCAL environment in serverless.yml to 0
```yml
environment:
  LOCAL: 0
```
After, run
```shell
 sls deploy
```
