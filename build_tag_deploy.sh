#!/bin/bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 016405558094.dkr.ecr.us-east-1.amazonaws.com
docker buildx build --platform linux/amd64 --provenance=false  -t scrapy-lambda-worker:latest --load .
docker tag scrapy-lambda-worker:latest 016405558094.dkr.ecr.us-east-1.amazonaws.com/scrapy-lambda-worker:latest
docker push 016405558094.dkr.ecr.us-east-1.amazonaws.com/scrapy-lambda-worker:latest
