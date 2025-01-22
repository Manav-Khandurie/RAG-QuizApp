# Use the official PostgreSQL image as the base
FROM postgres:latest

# Install the PG Vector extension dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    postgresql-server-dev-all \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone and install the PG Vector extension
RUN git clone https://github.com/pgvector/pgvector.git /tmp/pgvector \
    && cd /tmp/pgvector \
    && make \
    && make install

# Enable the PG Vector extension in the database
RUN echo "CREATE EXTENSION IF NOT EXISTS vector;" > /docker-entrypoint-initdb.d/init.sql

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=manav
ENV POSTGRES_PASSWORD=manav
ENV POSTGRES_DB=db