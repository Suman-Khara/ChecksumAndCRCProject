def generate_bitstream(length):
    return ''.join(random.choice('01') for _ in range(length))

def write_bitstream_to_file(bitstream, filename):
    with open(filename, 'w') as file:
        file.write(bitstream)

def main():
    length = 65536  
    filename = 'test.txt'

    bitstream = generate_bitstream(length)
    write_bitstream_to_file(bitstream, filename)

    print(f"Bitstream of length {length} has been written to {filename}")

if __name__ == "__main__":
    import random
    main()