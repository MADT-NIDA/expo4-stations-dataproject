-- 1. Create a login role (user) for your LLM database
CREATE ROLE guardrails_usr
  WITH
    LOGIN
    PASSWORD 'asdfasdf'   -- change to a secure password of your choice
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOINHERIT;

-- 2. Create the database owned by that user
CREATE DATABASE guardrails_db
  OWNER guardrails_usr
  ENCODING 'UTF8'
  LC_COLLATE = 'en_US.UTF-8'
  LC_CTYPE   = 'en_US.UTF-8'
  TEMPLATE = template0;

-- 3. Connect to the new database and install pgvector
\c guardrails_db

CREATE EXTENSION IF NOT EXISTS vector;

-- 4. Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE guardrails_db TO guardrails_usr;

-- 5. (Optional) If you have schemas or tables to grant later, you can use:
--    GRANT USAGE ON SCHEMA public TO llm1_user;
--    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO llm1_user;
--    ALTER DEFAULT PRIVILEGES IN SCHEMA public
--      GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO llm1_user;
