-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a function to initialize the public schema for multi-tenant setup
CREATE OR REPLACE FUNCTION init_public_schema() RETURNS VOID AS $$
BEGIN
    -- Create the public tenant if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename = 'core_tenant') THEN
        -- This will be created by Django migrations, so we don't need to create it here
        RAISE NOTICE 'Tables will be created by Django migrations';
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Call the function
SELECT init_public_schema();

-- Grant privileges to the database user
GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};

-- Create a function to create vector indexes
CREATE OR REPLACE FUNCTION create_vector_index(
    table_name text,
    column_name text,
    vector_dimensions integer
) RETURNS VOID AS $$
BEGIN
    EXECUTE format('ALTER TABLE %I ADD COLUMN IF NOT EXISTS %I vector(%s)', 
                  table_name, column_name, vector_dimensions);
    
    -- Create an index on the vector column
    EXECUTE format('CREATE INDEX IF NOT EXISTS %I_%I_idx ON %I USING ivfflat (%I vector_l2_ops)', 
                  table_name, column_name, table_name, column_name);
                  
    RAISE NOTICE 'Created vector column and index on %.%', table_name, column_name;
END;
$$ LANGUAGE plpgsql;

-- Example usage (commented out, to be used by application code):
-- SELECT create_vector_index('my_table', 'embedding', 1536);