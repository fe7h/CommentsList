ALTER ROLE userdb SET client_encoding TO 'utf8';
ALTER ROLE userdb SET default_transaction_isolation TO 'read committed';
ALTER ROLE userdb SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE comments TO userdb;

GRANT ALL PRIVILEGES ON SCHEMA public TO userdb;
ALTER SCHEMA public OWNER TO userdb;
