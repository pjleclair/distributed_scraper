from scrapy import Request, Spider
from items import ScrapedSiteContent


class Scraper(Spider):
    name = "scraper"

    def start_requests(self):
        url = getattr(self, "url", None)
        if url:
            self.logger.info(f"⏳ Starting crawl with {url}...")
            yield Request(url=url, callback=self.parse)
        else:
            self.logger.error("No URL was provided! Pass it with -a url=your_url")

    def parse(self, response):
        self.logger.info(f"Successfully fetched {response.url}")

        item = ScrapedSiteContent()

        # Populate the item with data from the response
        item["url"] = response.url
        item["raw_text"] = response.text  # Use response.text for decoded text

        # Populate DynamoDB with structured product info
        item["product_title"] = response.css("h1.product-title::text").get()
        item["price"] = response.css("span.price::text").get()
        # Yield the item to the pipeline
        yield item
