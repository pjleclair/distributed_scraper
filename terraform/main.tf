terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.67.0"
    }
  }
}

provider "aws" {
  region                      = "us-east-1"
}

output "ecr_repository_url" { value = aws_ecr_repository.scraper_repo.repository_url }

output "sqs_queue_url" {
  value = aws_sqs_queue.url_queue.url
  description = "URL of the SQS queue for sending messages"
}
# --- Infrastructure Resources ---

# 1. S3 Bucket for scraper output
resource "aws_s3_bucket" "scrape_output" {
  bucket = "s3-bucket-cs6620"
}

# 2. SQS Queue for URLs to be scraped
resource "aws_sqs_queue" "url_queue" {
  name = "url-queue"
}

# 3. IAM Role for the Lambda function
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# 4. IAM Policy giving the Lambda permissions
resource "aws_iam_policy" "lambda_policy" {
  name = "lambda_policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
        Effect   = "Allow",
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Action   = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"],
        Effect   = "Allow",
        Resource = aws_sqs_queue.url_queue.arn
      },
      {
        Action   = ["s3:PutObject"],
        Effect   = "Allow",
        Resource = "${aws_s3_bucket.scrape_output.arn}/*"
      },
      {
        Action   = ["dynamodb:PutItem"],
        Effect   = "Allow",
        Resource = aws_dynamodb_table.pricing_data.arn
      }
    ]
  })
}

# 5. Attach the policy to the role
resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# 6. The Lambda Function itself
resource "aws_lambda_function" "scraper_lambda" {
  function_name = "scrapylambdaworker"
  role          = aws_iam_role.lambda_exec_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.scraper_repo.repository_url}:latest"
  timeout       = 30 # Seconds

  environment {
    variables = {
      S3_BUCKET_NAME = aws_s3_bucket.scrape_output.id
    }
  }

  depends_on = [aws_iam_role_policy_attachment.lambda_policy_attach]
}

# 7. Trigger to link the SQS queue to the Lambda
resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.url_queue.arn
  function_name    = aws_lambda_function.scraper_lambda.arn
  batch_size       = 1 # Process one URL at a time
}

# 8. DynamoDB table for processed data
resource "aws_dynamodb_table" "pricing_data" {
  name         = "competitor-pricing"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "url" # Use the scraped URL as the unique ID

  attribute {
    name = "url"
    type = "S"
  }
}

# 9. ECR repository to store the Scrapy container image
resource "aws_ecr_repository" "scraper_repo" {
  name = "scrapy-lambda-worker" # The name for your repository
  image_tag_mutability = "MUTABLE"
  # This setting cleans up old images to prevent storage costs
  image_scanning_configuration {
    scan_on_push = true
  }
}

