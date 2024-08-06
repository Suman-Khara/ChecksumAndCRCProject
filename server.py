import sys
import socket
from checksum import validate_checksum_codeword
from crc import validate_crc_codeword

# Define the server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

def validate_packet(packet, technique):
    # Validate codeword based on the specified technique
    if technique == 'checksum':
        return validate_checksum_codeword(packet)
    elif technique in ['crc-8', 'crc-10', 'crc-16', 'crc-32']:
        return validate_crc_codeword(packet, technique.upper())
    else:
        raise ValueError("Invalid technique specified")

def main():
    if len(sys.argv) != 2:
        print("Usage: python server.py <technique>")
        sys.exit(1)

    technique = sys.argv[1].lower()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_ADDRESS, SERVER_PORT))
        s.listen()

        print(f"Server is listening on {SERVER_ADDRESS}:{SERVER_PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")

                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        break

                    is_valid = validate_packet(data, technique)
                    response = '1' if is_valid else '0'
                    conn.sendall(response.encode())
                print(f"Connection closed by {addr}")

if __name__ == "__main__":
    main()