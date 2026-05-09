"""
Simple TCP chat server.

This server accepts multiple client connections and broadcasts each
message to every other connected client.
"""

import socket
import threading


HOST = "127.0.0.1"
PORT = 12345

# We keep track of connected clients in a shared list.
clients = []

# A lock prevents two threads from changing the client list at the same time.
clients_lock = threading.Lock()


def broadcast(message, sender_socket):
    """
    Send a message to every client except the sender.
    """
    disconnected_clients = []

    with clients_lock:
        current_clients = list(clients)

    for client_socket in current_clients:
        if client_socket is sender_socket:
            continue

        try:
            client_socket.sendall(message)
        except OSError:
            # If sending fails, the client likely disconnected.
            disconnected_clients.append(client_socket)

    for client_socket in disconnected_clients:
        remove_client(client_socket)


def remove_client(client_socket):
    """
    Remove a disconnected client and close its socket safely.
    """
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)

    try:
        client_socket.close()
    except OSError:
        pass


def handle_client(client_socket, client_address):
    """
    Handle messages from one client in its own thread.
    """
    print(f"[NEW CONNECTION] {client_address} connected.")

    try:
        while True:
            data = client_socket.recv(1024)

            if not data:
                # An empty result means the client disconnected.
                print(f"[DISCONNECTED] {client_address} disconnected.")
                break

            message_text = data.decode("utf-8").strip()
            print(f"[MESSAGE] {client_address}: {message_text}")

            outgoing_message = f"{client_address}: {message_text}\n".encode("utf-8")
            broadcast(outgoing_message, client_socket)

    except ConnectionResetError:
        print(f"[DISCONNECTED] {client_address} connection was reset.")
    except OSError as error:
        print(f"[ERROR] Problem with {client_address}: {error}")
    finally:
        remove_client(client_socket)


def start_server():
    """
    Create the server socket and listen for new clients forever.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allows the port to be reused quickly after restarting the server.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}")
    print("Waiting for clients to connect...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()

            with clients_lock:
                clients.append(client_socket)

            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True,
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server is stopping.")
    finally:
        with clients_lock:
            current_clients = list(clients)
            clients.clear()

        for client_socket in current_clients:
            try:
                client_socket.close()
            except OSError:
                pass

        server_socket.close()


if __name__ == "__main__":
    start_server()
