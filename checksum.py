from error_injector import inject_error

def generate_checksum(chunks):
    res = ""
    size = len(chunks[0])
    for chunk in chunks:
        res = bin(int(res, 2) + int(chunk, 2)) if res != "" else chunk

    # Remove '0b' and ensure res is padded to at least size bits
    res = res[2:].zfill(size)
    
    # If res is still not long enough, pad it further to avoid slicing issues
    if len(res) < size:
        res = res.zfill(size)

    # Handle the case where res might not have enough bits for slicing
    if len(res) > size:
        res = bin(int(res[-size:], 2) + int(res[:-size], 2))
    else:
        res = bin(int(res, 2))

    # Return the checksum by flipping bits
    return ''.join('1' if x == '0' else '0' for x in res[2:].zfill(size))

def check_checksum(chunks, checksum):
    res = ""
    size = len(chunks[0])
    for chunk in chunks:
        if chunk == '':
            continue
        res = bin(int(res, 2) + int(chunk, 2)) if res != "" else chunk

    # Remove '0b' and ensure res is padded to at least size bits
    res = res[2:].zfill(size)
    
    # If res is still not long enough, pad it further to avoid slicing issues
    if len(res) < size:
        res = res.zfill(size)

    # Handle the case where res might not have enough bits for slicing
    if len(res) > size:
        res = bin(int(res[-size:], 2) + int(res[:-size], 2) + int(checksum, 2))
    else:
        res = bin(int(res, 2) + int(checksum, 2))

    # Check if the result is all 1s
    return res.count("1") == size

def generate_checksum_codeword(dataword):
    # Pad the dataword to ensure it's a multiple of 16 bits
    padded_dataword = dataword.ljust((len(dataword) + 15) // 16 * 16, '0')
    chunks = [padded_dataword[i:i+16] for i in range(0, len(padded_dataword), 16)]
    checksum = generate_checksum(chunks)
    return dataword + checksum

def validate_checksum_codeword(codeword):
    # Split the codeword into 16-bit chunks, excluding the last 16 bits for checksum
    padded_codeword = codeword[:-16].ljust((len(codeword) - 16 + 15) // 16 * 16, '0')
    chunks = [padded_codeword[i:i+16] for i in range(0, len(padded_codeword), 16)]
    checksum = codeword[-16:]
    return check_checksum(chunks, checksum)

# Example usage (for testing purposes)
if __name__ == "__main__":
    dataword = "11010110101101011010101101101010111111111111111"
    codeword = generate_checksum_codeword(dataword)
    print(f"Dataword: {dataword}")
    print(f"Codeword with Checksum: {codeword}")
    print(validate_checksum_codeword(codeword))
    
    error_types = ['SINGLE', 'DOUBLE', 'ODD', 'BURST']
    burst_length = 4

    for error_type in error_types:
        if error_type == 'BURST':
            infected_codeword = inject_error(codeword, error_type, burst_length)
        else:
            infected_codeword = inject_error(codeword, error_type)
        
        is_valid = validate_checksum_codeword(infected_codeword)
        print(f"\n{error_type} - Valid: {is_valid}")