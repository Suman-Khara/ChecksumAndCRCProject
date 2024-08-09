import sys
import socket
import random
from checksum import generate_checksum_codeword
from crc import generate_crc_codeword
from error_injector import inject_error_random, inject_error_manual

# Define the server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def break_into_packets(bitstream, packet_size, redundant_bits):
    dataword_size = packet_size - redundant_bits
    if dataword_size <= 0:
        raise ValueError("Packet size must be greater than the number of redundant bits.")
    return [bitstream[i:i + dataword_size] for i in range(0, len(bitstream), dataword_size)]

def generate_codeword(dataword, technique):
    if technique == 'checksum':
        return generate_checksum_codeword(dataword)
    elif technique in ['crc-8', 'crc-10', 'crc-16', 'crc-32']:
        return generate_crc_codeword(dataword, technique.upper())
    else:
        raise ValueError("Invalid technique specified")

def manual_error_injection(word):
    error_type = input("Enter error type (SINGLE, DOUBLE, ODD, BURST, NONE): ").upper()
    if error_type == 'NONE':
        return word, "No Error", None
    if error_type == 'SINGLE':
        index = int(input("Enter index for SINGLE error: "))
        infected_codeword = inject_error_manual(word, error_type, indices=[index])
        return infected_codeword, "SINGLE", None
    elif error_type == 'DOUBLE':
        index1 = int(input("Enter first index for DOUBLE error: "))
        index2 = int(input("Enter second index for DOUBLE error: "))
        infected_codeword = inject_error_manual(word, error_type, indices=[index1, index2])
        return infected_codeword, "DOUBLE", None
    elif error_type == 'ODD':
        indices = list(map(int, input("Enter indices for ODD error (comma-separated): ").split(',')))
        infected_codeword = inject_error_manual(word, error_type, indices=indices)
        return infected_codeword, "ODD", None
    elif error_type == 'BURST':
        start_index = int(input("Enter start index for BURST error: "))
        burst_length = int(input("Enter burst length: "))
        infected_codeword = inject_error_manual(word, error_type, start_index=start_index, burst_length=burst_length)
        return infected_codeword, "BURST", burst_length
    else:
        raise ValueError("Invalid error type specified")

def random_error_injection(codeword):
    error_type = random.choice(['SINGLE', 'DOUBLE', 'ODD', 'BURST', 'NONE'])
    if error_type == 'NONE':
        return codeword, "No Error", None
    if error_type == 'BURST':
        burst_length = random.randint(2, len(codeword))
        infected_codeword = inject_error_random(codeword, error_type, burst_length)
        return infected_codeword, "BURST", burst_length
    else:
        infected_codeword = inject_error_random(codeword, error_type)
        return infected_codeword, error_type, None

def send_to_server(s, packet):
    try:
        s.sendall(packet.encode())
        response = s.recv(1024).decode()
        return response
    except (socket.error, socket.timeout) as e:
        print(f"Error during communication with the server: {e}")
        return None

def main():
    if len(sys.argv) != 5:
        print("Usage: python client.py <file_path> <packet_size> <technique> <error_mode>")
        sys.exit(1)

    file_path = sys.argv[1]
    packet_size = int(sys.argv[2])
    technique = sys.argv[3].lower()
    error_mode = sys.argv[4].lower()

    redundant_bits = {
        'checksum': 16,
        'crc-8': 8,
        'crc-10': 10,
        'crc-16': 16,
        'crc-32': 32
    }.get(technique)

    if redundant_bits is None:
        print("Invalid technique specified")
        sys.exit(1)

    if packet_size <= redundant_bits:
        print("Packet size must be greater than the number of redundant bits.")
        sys.exit(1)

    bitstream = read_file(file_path)
    packets = break_into_packets(bitstream, packet_size, redundant_bits)

    results = []

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_ADDRESS, SERVER_PORT))

            for index, dataword in enumerate(packets):
                codeword = generate_codeword(dataword, technique)

                if error_mode == 'manual':
                    infected_codeword, error_type, burst_length = manual_error_injection(codeword)
                elif error_mode == 'random':
                    infected_codeword, error_type, burst_length = random_error_injection(codeword)
                else:
                    raise ValueError("Invalid error mode specified")

                acceptance = send_to_server(s, infected_codeword)
                if acceptance is None:
                    break

                result = {
                    "Packet Index": index,
                    "Error Type": error_type,
                    "Burst Length": burst_length if burst_length else "N/A",
                    "Accepted/Rejected": "Accepted" if acceptance == '1' else "Rejected"
                }
                results.append(list(result.values()))

            # Close the connection gracefully after sending all packets
            s.shutdown(socket.SHUT_RDWR)
            s.close()
    except (socket.error, socket.timeout) as e:
        print(f"Connection error: {e}")
    finally:
        for result in results:
            print(*result)

if __name__ == "__main__":
    main()
