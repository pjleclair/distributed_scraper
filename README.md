# AWS Lambda Data Pipeline

A serverless data processing pipeline built with AWS Lambda, Docker, and Terraform for automated data scraping and processing.

## Project Structure

```
.
├── src/                      # Source code for Lambda functions
│   ├── items.py             # Item data models and processing
│   ├── lambda_handler.py   # Main Lambda function entry point
│   ├── pipelines.py         # Data processing pipelines
│   ├── producer.py          # Data producer/message queue handler
│   └── scraper.py           # Web scraping functionality
├── terraform/               # Infrastructure as Code
│   ├── main.tf             # Main Terraform configuration
│   └── .terraform.lock.hcl # Terraform dependency lock file
├── docker-compose.yml       # Docker compose configuration (optional, for localstack)
├── Dockerfile              # Docker image definition
├── requirements.txt        # Python dependencies
├── build_tag_deploy.sh    # Build and deployment script
├── update_lambda.sh       # Lambda function update script
└── send_msg.sh           # Message sending utility script
```

## Features

- **Serverless Architecture**: Built on AWS Lambda for automatic scaling and cost efficiency
- **Web Scraping**: Automated data collection with `scraper.py`
- **Data Pipeline**: Modular pipeline architecture for data processing
- **Infrastructure as Code**: Terraform configurations for reproducible deployments
- **Containerized**: Docker support for consistent development and deployment environments
- **Message Queue Integration**: Producer pattern for reliable data processing

## Prerequisites

- Python 3.x
- Docker
- Terraform >= 1.0
- AWS CLI configured with appropriate credentials
- AWS Account with Lambda, and other required services

## Installation

1. **Clone the repository**

   ```bash
   git clone git@github.com:pjleclair/distributed_scraper.git
   cd distributed_scraper
   ```

2. **Set up Python virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure AWS credentials**
   ```bash
   aws configure
   ```

## Infrastructure Setup

1. **Initialize Terraform**

   ```bash
   cd terraform
   terraform init
   ```

2. **Review infrastructure changes**

   ```bash
   terraform plan
   ```

3. **Deploy infrastructure**
   ```bash
   terraform apply
   ```

## Docker Development (localstack)

1. **Build Docker image**

   ```bash
   docker-compose build
   ```

2. **Run locally with Docker Compose**
   ```bash
   docker-compose up
   ```

## Deployment

### Automated Deployment

Use the provided build and deploy script:

```bash
./build_tag_deploy.sh
```

### Update Lambda Function

To update only the Lambda function code:

```bash
./update_lambda.sh
```

## Development

### Project Components

- **`lambda_handler.py`**: Main entry point for AWS Lambda function execution
- **`scraper.py`**: Contains web scraping logic and data extraction
- **`pipelines.py`**: Defines data processing pipelines and transformations
- **`producer.py`**: Handles message production for queue-based processing
- **`items.py`**: Data models and item definitions

## Scripts

- **`build_tag_deploy.sh`**: Builds Docker image, tags it, and deploys to AWS
- **`update_lambda.sh`**: Updates Lambda function with latest code changes
- **`send_msg.sh`**: Utility for sending messages to the processing queue
