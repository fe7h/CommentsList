ALTER ROLE your_db_user SET client_encoding TO 'utf8';
ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_db_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE comments TO your_db_user;

GRANT ALL PRIVILEGES ON SCHEMA public TO your_db_user;
ALTER SCHEMA public OWNER TO your_db_user;
