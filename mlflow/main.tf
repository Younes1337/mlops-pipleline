provider "aws" {
  region = "us-east-1" # Update with your desired AWS region
}

# Create an S3 bucket for MLflow artifacts
resource "aws_s3_bucket" "backendstore" {
  bucket = "backendstore" # Update with your desired bucket name

  tags = {
    Name        = "MLflow-s3-bucket"
    Environment = "Dev"
  }
}

# Create an S3 bucket for Queue artifacts
resource "aws_s3_bucket" "queuesys" {
  bucket = "queuesys" # Update with your desired bucket name

  tags = {
    Name        = "Queue-s3-bucket"
    Environment = "Dev"
  }
}

