# Use an appropriate base image
FROM python:3.10-slim

# Set up environment variables
ENV DAGSTER_HOME=/opt/dagster

# Install dependencies
RUN pip install dagster dagster-webserver dagster_duckdb 
RUN pip install huggingface-hub --no-deps 

# Install setfit with CPU-only support
RUN pip install setfit[cpu] --no-deps

# Install the latest version of torch for CPU-only support
RUN pip install torch==1.11.0+cpu -f https://download.pytorch.org/whl/torch_stable.html --no-deps

# Set the working directory
WORKDIR /opt/dagster

# Copy your Dagster project code into the container
COPY . /opt/dagster

# Navigate to the project directory
WORKDIR /opt/dagster/tutorial

# Copy requirements file
COPY requirements.txt /opt/dagster/tutorial/requirements.txt 

# Install dependencies from requirements file, excluding setfit and torch
RUN pip install -r requirements.txt 

# Navigate back to the root directory
WORKDIR /opt/dagster

# Expose ports if necessary (for Dagster UI)
EXPOSE 3000

# Command to start your Dagster server
CMD ["dagster","dev", "-h", "127.0.0.1", "-p", "3000"]
