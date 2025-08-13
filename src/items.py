import scrapy


class ScrapedSiteContent(scrapy.Item):
    # Raw data for S3
    url = scrapy.Field()
    raw_text = scrapy.Field()

    # Structured data for DynamoDB
    product_title = scrapy.Field()
    price = scrapy.Field()
