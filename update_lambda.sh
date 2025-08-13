#!/bin/bash
aws lambda update-function-code \
  --function-name scrapylambdaworker \
  --image-uri 016405558094.dkr.ecr.us-east-1.amazonaws.com/scrapy-lambda-worker:latest

aws lambda wait function-updated --function-name scrapylambdaworker
