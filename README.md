# LLMs-Sevice
LLMs-Service is a service designed to solve multi-choice question answering tasks with several different LLMs. This service interacts only with [Common-Backend](https://github.com/LLM-Tests-Checker/Common-Backend/) using Kafka.

### How to launch?

1. Built docker image of LLMs-Service from project root directory:
```shell
docker build -t llms-service .
```

2. Run docker image:
```shell
docker run llms-service
```

### How to contribute?
1. Create new branch from main: `git branch <YOUR_NICKNAME>:<FEATURE_NAME>`
2. Checkout to your branch: `git checkout <BRANCH_NAME_FROM_POINT_1>`
3. Write code
4. Test code on development environment
5. Create Pull Request
6. Wait for approve
