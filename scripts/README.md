# Utility Scripts

This directory contains utility scripts for the Talemo platform. These scripts automate various tasks related to development, deployment, and maintenance.

## Overview

The utility scripts provide automation for common tasks that are performed during development, deployment, and maintenance of the Talemo platform. These scripts help ensure consistency and reduce manual effort.

## File Structure

- `init-db.sql`: SQL script for initializing the PostgreSQL database with pgvector extension

## Script Details

### init-db.sql

The `init-db.sql` script is used to initialize the PostgreSQL database with the pgvector extension and set up the necessary functions for vector operations. This script is executed automatically when the PostgreSQL container starts in the development environment.

Key features of this script:

- Enables the pgvector extension for vector similarity search
- Creates a function to initialize the public schema for multi-tenant setup
- Grants necessary privileges to the database user
- Creates a utility function for creating vector indexes

## Usage

### Database Initialization

The `init-db.sql` script is mounted into the PostgreSQL container and executed automatically during container initialization:

```yaml
# In docker-compose.dev.yml
services:
  db:
    image: ankane/pgvector:latest
    volumes:
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
```

### Manual Execution

To execute the script manually:

```bash
# Connect to the database container
docker-compose -f docker/docker-compose.dev.yml exec db bash

# Run the script
psql -U postgres -d talemo -f /docker-entrypoint-initdb.d/init-db.sql
```

## Vector Index Creation

The `init-db.sql` script provides a utility function for creating vector indexes:

```sql
-- Example usage in your SQL queries:
SELECT create_vector_index('my_table', 'embedding', 1536);
```

This function:
1. Adds a vector column to the specified table
2. Creates an index on the vector column for efficient similarity search
3. Logs the operation for reference

## Adding New Scripts

When adding new scripts to this directory:

1. Use descriptive filenames that indicate the script's purpose
2. Include comments in the script to explain its functionality
3. Update this README.md to document the new script
4. Ensure the script is executable if it's a shell script (`chmod +x script.sh`)

## Best Practices

- Keep scripts focused on a single task
- Include proper error handling
- Add logging for important operations
- Make scripts idempotent (safe to run multiple times)
- Include usage examples in comments

## Related Components

- `docker/docker-compose.dev.yml`: Docker Compose configuration that uses these scripts
- `talemo/core/models/tenant.py`: Multi-tenant models that interact with the database
- `Makefile`: Contains commands that may use these scripts

## Related Documentation

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [Docker Entrypoint Scripts](https://docs.docker.com/engine/reference/builder/#entrypoint)