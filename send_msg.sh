#!/bin/bash
cd terraform
URL=$(terraform output -raw sqs_queue_url)
scrape_urls=(
  "https://www.storybookai.app/#pricing"
  "https://onceuponabot.com/"
)
for scrape_url in "${scrape_urls[@]}"; do \
  aws sqs send-message \
    --queue-url $URL \
    --message-body $scrape_url  \
    --region us-east-1; \
  sleep 0.5; \
done

