CREATE TABLE users(
  users_id SERIAL PRIMARY KEY,
  username VARCHAR,
  password VARCHAR
);
GRANT ALL PRIVILEGES ON TABLE users TO chat_user;
GRANT USAGE, SELECT ON SEQUENCE users_users_id_seq TO chat_user;