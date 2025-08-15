import boto3
from urllib.parse import urlparse
import os
import getpass

if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

from langchain.chat_models import init_chat_model

class S3Pipeline:
    def __init__(self, aws_bucket_name):
        if not aws_bucket_name:
            raise ValueError("S3_BUCKET_NAME must be set in settings")
        self.bucket_name = aws_bucket_name

        self.s3_client = boto3.client(
            "s3",
            region_name="us-east-1",
        )

    @classmethod
    def from_crawler(cls, crawler):
        # Get the bucket name from Scrapy settings
        return cls(aws_bucket_name=crawler.settings.get("S3_BUCKET_NAME"))

    def process_item(self, item, spider):
        # Create a unique filename from the URL
        parsed_url = urlparse(item["url"])
        # Creates a path like 'quotes.toscrape.com/index.html'
        s3_key = f"{parsed_url.netloc}{parsed_url.path}"
        if s3_key.endswith("/"):
            s3_key += "index.html"  # Default to index.html for root paths
        s3_key = os.path.normpath(s3_key)

        spider.logger.info(f"Uploading {s3_key} to S3 bucket {self.bucket_name}")

        # Upload the raw text to S3
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=item["raw_text"].encode("utf-8"),  # Encode text to bytes for upload
            ContentType="text/html; charset=utf-8",
        )

        return item  # Must return the item for other pipelines


class DynamoDBPipeline:
    def __init__(self, aws_table_name):
        self.table_name = aws_table_name
        dynamodb = boto3.resource(
            "dynamodb",
            region_name="us-east-1",
        )
        self.table = dynamodb.Table(self.table_name)

    @classmethod
    def from_crawler(cls, crawler):
        # Get the table name from a new setting
        return cls(aws_table_name=crawler.settings.get("DYNAMODB_TABLE_NAME"))

    def process_item(self, item, spider):
        model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

        schema = {
            "url": "The url of a website being scraped",
            "product_title": "The title of the product featured on the scraped page",
            "price": "The pricing of the product featured on the scraped page"
        }

        model_with_structure = model.with_structured_output(schema)
        structured_output = model_with_structure.invoke(item['raw_text'])

        # Only process items that have a price (or other key data)
        spider.logger.info(f"Writing item to DynamoDB: {item['product_title']}")
        self.table.put_item(structured_output)
        return item
