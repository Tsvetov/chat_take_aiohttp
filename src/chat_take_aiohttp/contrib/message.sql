CREATE TABLE message(
  message_id SERIAL PRIMARY KEY,
  users_id INTEGER REFERENCES users,
  room_id INTEGER REFERENCES room,
  text TEXT,
  created_at TIMESTAMP
);
GRANT ALL PRIVILEGES ON TABLE message TO chat_user;
GRANT USAGE, SELECT ON SEQUENCE message_message_id_seq TO chat_user;