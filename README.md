---

# Error Detection Techniques Project (CRC and Checksum)

This project demonstrates the implementation and testing of various error detection techniques, including checksum, CRC-8, CRC-10, CRC-16, and CRC-32. It uses socket programming to simulate communication between a client and a server, where the server validates the packets sent by the client.

## Features

- **Error injection**: Client-side error injection with both manual and automatic modes.
- **Checksum and CRC validation**: Server-side validation of packets using various error detection techniques.

## Requirements

- Python 3.x

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

## Usage

### Step 1: Start the Server

Start the server with the desired encoding technique:

```bash
python server.py <technique>
```

Replace `<technique>` with one of the following options:
- `checksum`
- `crc-8`
- `crc-10`
- `crc-16`
- `crc-32`

### Step 2: Send Packets Using the Client Program

Send bits divided into packets using the client program:

```bash
python client.py <filename> <packet_size> <technique> <error_method>
```

- `<filename>`: The name of the file containing the bitstream (e.g., `test.txt`).
- `<packet_size>`: The size of the packet (dataword + redundant bits).
- `<technique>`: The encoding technique to use (`checksum`, `crc-8`, `crc-10`, `crc-16`, or `crc-32`). It must be same as the one mentioned while starting the server.
- `<error_method>`: The method of error injection (`manual` for manual error input, `random` for automatic error injection).

Each output line is in the format: 
- `packet number/index`
- `type of error injected` (if no error, it shows "No Error")
- `length of burst error` (in case of burst errors, otherwise N/A)
- `whether the packet is accepted or rejected`

---
