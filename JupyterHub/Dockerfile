FROM jupyter/datascience-notebook

# Grant sudo privileges to jovyan user
USER root
RUN apt-get update && apt-get install -y sudo && \
    echo "jovyan ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER jovyan