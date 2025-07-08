import socket
import time

class RobotConnection:
    def __init__(self, host="192.168.3.11", port=3920):
        self.host = host
        self.port = port
        self.client_socket = None
        self.running = False
        self.cnt = 1
        self.reconnect_attempts = 3

    def increment_cnt(self):
        """Increment cnt and reset to 1 if it exceeds 9999."""
        self.cnt = (self.cnt % 9999) + 1
        return self.cnt

    def start(self):
        self.running = True
        attempt = 0
        while self.running and attempt < self.reconnect_attempts:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.settimeout(5.0)
                self.client_socket.connect((self.host, self.port))
                print("Connected to robot.")
                attempt = 0

                self.send_command("CRISTART 1 CMD GetVersion CRIEND\n")

                while self.running:
                    message = f"CRISTART {self.cnt} ALIVEJOG 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 CRIEND\n"
                    self.send_command(message)
                    self.increment_cnt()

                    try:
                        data = self.client_socket.recv(4096).decode('ascii')
                        if data:
                            print(f"Received from robot: {data}")
                        else:
                            print("No data received, continuing to wait...")
                    except socket.timeout:
                        print("Receive timeout, continuing to wait...")
                    except socket.error as e:
                        print(f"Socket error while receiving data: {e}")
                        break

                    time.sleep(0.1)

            except (ConnectionRefusedError, OSError) as e:
                print(f"Failed to connect to robot at {self.host}:{self.port}. Error: {e}")
                attempt += 1
                if attempt < self.reconnect_attempts:
                    print(f"Reconnecting... (Attempt {attempt + 1}/{self.reconnect_attempts})")
                    time.sleep(2)
                else:
                    print("Maximum reconnect attempts reached.")
                    break
            except Exception as e:
                print(f"Connection error: {e}")
                break
            finally:
                if not self.running:
                    self.stop()

    def stop(self):
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
                print("Socket closed.")
            except Exception as e:
                print(f"Error closing socket: {e}")
        print("RobotConnection stopped.")

    def send_command(self, command):
        if self.client_socket:
            try:
                self.client_socket.sendall(command.encode('ascii'))
                print(f"Sent command: {command.strip()}")
            except Exception as e:
                print(f"Error sending command: {e}")
                raise

if __name__ == "__main__":
    robot = RobotConnection()
    try:
        robot.start()
    except KeyboardInterrupt:
        robot.stop()