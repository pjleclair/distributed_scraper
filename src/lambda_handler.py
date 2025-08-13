import json
import sys

# Add the src directory to Python path so we can import our modules
sys.path.insert(0, "/var/task/src")
from scrapy.crawler import CrawlerProcess
from scraper import Scraper


def handler(event, context):
    """
    Lambda handler function.
    This function is triggered by an SQS message.
    """
    # 1. Get the URL from the SQS event record
    # SQS sends messages in a 'Records' array
    message = event["Records"][0]
    url_to_scrape = message["body"]

    print(f"Message received. Scraping URL: {url_to_scrape}")

    # 2. Configure and run the scraper
    # These settings will be configured in the Lambda environment
    settings = {
        "ITEM_PIPELINES": {
            "pipelines.S3Pipeline": 300,  # Runs first
            "pipelines.DynamoDBPipeline": 400,  # Runs second
        },
        "S3_BUCKET_NAME": "s3-bucket-cs6620",
        "DYNAMODB_TABLE_NAME": "competitor-pricing",  # Add this setting
        "LOG_LEVEL": "INFO",
    }

    # The pipeline will handle pointing boto3 to AWS

    process = CrawlerProcess(settings=settings)
    process.crawl(Scraper, url=url_to_scrape)
    process.start()  # This blocks until the crawl is finished

    print("Scraping finished successfully.")

    # Lambda will automatically handle message deletion from SQS on success
    return {
        "statusCode": 200,
        "body": json.dumps(f"Successfully scraped {url_to_scrape}"),
    }
