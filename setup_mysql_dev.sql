-- This files prepare Mysql server
-- for the project
CREATE DATABASE hbnb_dev_db IF NOT EXISTS;
CREATE USER "hbnb_dev"@"localhost" IDENTIFIED BY "hbnb_dev_pwd" IF NOT EXISTS;
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO hbnb_dev;
FLUSH PRIVILEGES;
CREATE DATABASE performance_schema;
GRANT SELECT PRIVILEGE ON performance_schema.* TO hbnb_dev;