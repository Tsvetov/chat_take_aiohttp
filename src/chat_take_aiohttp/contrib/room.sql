CREATE TABLE room(
  room_id SERIAL PRIMARY KEY,
  name VARCHAR
);
GRANT ALL PRIVILEGES ON TABLE room TO chat_user;
GRANT USAGE, SELECT ON SEQUENCE room_room_id_seq TO chat_user;