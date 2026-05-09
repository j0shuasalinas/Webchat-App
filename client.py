"""
Simple TCP chat client.

Run this file in multiple terminals to chat through the server.
"""

import socket
import threading


HOST = "127.0.0.1"
PORT = 12345


def receive_messages(client_socket):
    """
    Receive messages from the server and print them right away.
    """
    try:
        while True:
            data = client_socket.recv(1024)

            if not data:
                print("\n[INFO] Disconnected from server.")
                break

            print(data.decode("utf-8"), end="")
    except ConnectionResetError:
        print("\n[ERROR] Server connection was reset.")
    except OSError:
        print("\n[INFO] Connection closed.")


def start_client():
    """
    Connect to the chat server and start send/receive behavior.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"[ERROR] Could not connect to server at {HOST}:{PORT}.")
        print("Make sure server.py is running first.")
        return
    except OSError as error:
        print(f"[ERROR] Could not connect: {error}")
        return

    print(f"Connected to chat server at {HOST}:{PORT}")
    print("Type a message and press Enter. Press Ctrl+C to quit.")

    # This thread listens for messages while the main thread sends messages.
    receiver_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True,
    )
    receiver_thread.start()

    try:
        while True:
            message = input()

            if not message.strip():
                # Ignore empty messages to keep the chat clean.
                continue

            client_socket.sendall(message.encode("utf-8"))
    except KeyboardInterrupt:
        print("\n[INFO] Leaving chat.")
    except EOFError:
        print("\n[INFO] Input stream closed.")
    except OSError as error:
        print(f"\n[ERROR] Could not send message: {error}")
    finally:
        try:
            client_socket.close()
        except OSError:
            pass


if __name__ == "__main__":
    start_client()
