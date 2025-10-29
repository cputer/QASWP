import time

def run_server():
    print("🌌 [QASWP Server] Awaiting connections...")
    # In a real server, this would be a loop listening on a socket.
    # For this demo, we just show a message. The client-side
    # simulation already includes the server's logic.
    while True:
        print("...listening...")
        time.sleep(10)

if __name__ == "__main__":
    run_server()
