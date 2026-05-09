# Simple Webchat Application

This project is a beginner-friendly chat app built with Python TCP sockets.

## Files

- `server.py` starts the chat server.
- `client.py` connects a user to the chat server.

## How it works

- The server listens on `127.0.0.1:12345`.
- Multiple clients can connect at the same time.
- Each client runs in its own server thread.
- When one client sends a message, the server broadcasts it to the other clients.

## How to run

1. Start the server:

   ```bash
   python server.py
   ```

2. Open two terminals.

3. In each terminal, start a client:

   ```bash
   python client.py
   ```

4. Type messages in either client and press Enter.

5. The other connected client should receive the messages in real time.

## Example test

1. Terminal 1:

   ```bash
   python server.py
   ```

2. Terminal 2:

   ```bash
   python client.py
   ```

3. Terminal 3:

   ```bash
   python client.py
   ```

4. Send a message from Terminal 2.

5. Confirm the message appears in Terminal 3.

## Notes

- If a client disconnects, the server removes it cleanly.
- If the server is not running, the client shows a helpful error message.
