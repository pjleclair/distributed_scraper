import boto3


def populate_queue():
    """
    Connects to AWS SQS and sends messages to a queue.
    """
    queue_name = "url-queue"

    try:
        sqs_client = boto3.client(
            "sqs",
            region_name="us-east-1",
        )

        # Get the URL for the queue
        response = sqs_client.get_queue_url(QueueName=queue_name)
        queue_url = response["QueueUrl"]

    except Exception as e:
        print(f"Error connecting to SQS. Error: {e}")
        return

    urls_to_scrape = [queue_url]

    print(f"Sending URLs to queue: {queue_url}")
    for url in urls_to_scrape:
        sqs_client.send_message(QueueUrl=queue_url, MessageBody=url)
        print(f"  -> Sent: {url}")


if __name__ == "__main__":
    populate_queue()
