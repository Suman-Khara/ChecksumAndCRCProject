from error_injector import inject_error_random

# Define CRC polynomials
CRC_POLYNOMIALS = {
    "CRC-8": "111010101",
    "CRC-10": "11011000101",
    "CRC-16": "11000000000000101",
    "CRC-32": "100000100110000010001110110110111"
}

def xor(a, b):
    """
    Perform XOR operation between two binary strings
    """
    result = []
    for i in range(1, len(b)):
        result.append('0' if a[i] == b[i] else '1')
    return ''.join(result)

def mod2div(dividend, divisor):
    """
    Perform binary division (modulo 2) between dividend and divisor
    """
    pick = len(divisor)
    tmp = dividend[0:pick]

    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0' * pick, tmp) + dividend[pick]
        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    checkword = tmp
    return checkword

def generate_crc_codeword(dataword, crc_type):
    """
    Generates a codeword with CRC for the given dataword using the specified CRC type.

    Args:
    - dataword (str): The input dataword as a string of '0's and '1's.
    - crc_type (str): The CRC type ('CRC-8', 'CRC-10', 'CRC-16', 'CRC-32').

    Returns:
    - str: The codeword which includes the original dataword and the CRC.
    """
    polynomial = CRC_POLYNOMIALS[crc_type]
    l_key = len(polynomial)

    appended_data = dataword + '0' * (l_key - 1)
    remainder = mod2div(appended_data, polynomial)
    codeword = dataword + remainder
    return codeword

def validate_crc_codeword(codeword, crc_type):
    """
    Validates a codeword with CRC for the given dataword using the specified CRC type.

    Args:
    - codeword (str): The received codeword as a string of '0's and '1's.
    - crc_type (str): The CRC type ('CRC-8', 'CRC-10', 'CRC-16', 'CRC-32').

    Returns:
    - bool: True if the codeword is valid (no errors detected), False otherwise.
    """
    polynomial = CRC_POLYNOMIALS[crc_type]
    l_key = len(polynomial)

    remainder = mod2div(codeword, polynomial)
    return remainder.count('1') == 0

# Example usage (for testing purposes)
if __name__ == "__main__":
    dataword = "11010110101101011010101101101010111111111"
    crc_types = ["CRC-8", "CRC-10", "CRC-16", "CRC-32"]
    error_types = ['SINGLE', 'DOUBLE', 'ODD', 'BURST']
    burst_length = 4

    for crc_type in crc_types:
        print(f"\n{crc_type}:")
        codeword = generate_crc_codeword(dataword, crc_type)
        print(f"Dataword: {dataword}")
        print(f"Codeword with CRC: {codeword}")
        print(validate_crc_codeword(codeword, crc_type))
        for error_type in error_types:
            if error_type == 'BURST':
                infected_codeword = inject_error_random(codeword, error_type, burst_length)
            else:
                infected_codeword = inject_error_random(codeword, error_type)
            
            is_valid = validate_crc_codeword(infected_codeword, crc_type)
            print(f"\n{error_type} - Valid: {is_valid}")
