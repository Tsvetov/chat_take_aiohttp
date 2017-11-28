CREATE DATABASE chat_take_aiohttp;
CREATE USER chat_user WITH password '123';

\connect chat_take_aiohttp

CREATE TABLE room(
  room_id SERIAL PRIMARY KEY,
  name VARCHAR
);
GRANT ALL PRIVILEGES ON TABLE room TO chat_user;
GRANT USAGE, SELECT ON SEQUENCE room_room_id_seq TO chat_user;


CREATE TABLE users(
  users_id SERIAL PRIMARY KEY,
  username VARCHAR,
  password VARCHAR
);
GRANT ALL PRIVILEGES ON TABLE users TO chat_user;
GRANT USAGE, SELECT ON SEQUENCE users_users_id_seq TO chat_user;


CREATE TABLE message(
  message_id SERIAL PRIMARY KEY,
  users_id INTEGER REFERENCES users,
  room_id INTEGER REFERENCES room,
  text TEXT,
  created_at TIMESTAMP
);
GRANT ALL PRIVILEGES ON TABLE message TO chat_user;
GRANT USAGE, SELECT ON SEQUENCE message_message_id_seq TO chat_user;
