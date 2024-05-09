FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /mlflow

# Install MLflow and any other dependencies
RUN pip install mlflow psycopg2-binary boto3

# Expose the MLflow tracking server port
EXPOSE 5000

# Start MLflow server with the custom configuration file and environment variables
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]
