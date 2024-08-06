import random

def inject_single_bit_error(codeword):
    index = random.randint(0, len(codeword) - 1)
    infected_codeword = codeword[:index] + ('0' if codeword[index] == '1' else '1') + codeword[index + 1:]
    return infected_codeword

def inject_two_isolated_single_bit_errors(codeword):
    index1 = random.randint(0, len(codeword) - 1)
    index2 = random.randint(0, len(codeword) - 1)
    while (index2 - index1)**2 <= 1:
        index2 = random.randint(0, len(codeword) - 1)
    
    infected_codeword = list(codeword)
    infected_codeword[index1] = '0' if codeword[index1] == '1' else '1'
    infected_codeword[index2] = '0' if codeword[index2] == '1' else '1'
    return ''.join(infected_codeword)

def inject_odd_number_of_errors(codeword):
    num_errors = random.randint(1, len(codeword))
    indices = random.sample(range(len(codeword)), num_errors)
    
    infected_codeword = list(codeword)
    for index in indices:
        infected_codeword[index] = '0' if codeword[index] == '1' else '1'
    return ''.join(infected_codeword)

def inject_burst_error(codeword, burst_length):
    start_index = random.randint(0, len(codeword) - burst_length)
    infected_codeword = list(codeword)
    for i in range(start_index, start_index + burst_length):
        infected_codeword[i] = '0' if codeword[i] == '1' else '1'
    return ''.join(infected_codeword)

def inject_error(codeword, error_type, burst_length=None):
    if error_type == "SINGLE":
        return inject_single_bit_error(codeword)
    elif error_type == "DOUBLE":
        return inject_two_isolated_single_bit_errors(codeword)
    elif error_type == "ODD":
        return inject_odd_number_of_errors(codeword)
    elif error_type == "BURST":
        if burst_length is None:
            raise ValueError("Burst length must be provided for burst errors.")
        return inject_burst_error(codeword, burst_length)
    else:
        raise ValueError("Invalid error type specified.")

# Example usage (for testing purposes)
if __name__ == "__main__":
    codeword = "11010110101101011010101101101010"
    
    print(f"Original Codeword: {codeword}")
    
    infected_codeword = inject_error(codeword, "SINGLE")
    print(f"Single-bit Error Injected: {infected_codeword}")
    
    infected_codeword = inject_error(codeword, "DOUBLE")
    print(f"Two Isolated Single-bit Errors Injected: {infected_codeword}")
    
    infected_codeword = inject_error(codeword, "ODD")
    print(f"Odd Number of Errors Injected: {infected_codeword}")
    
    burst_length = 4  # Example burst length
    infected_codeword = inject_error(codeword, "BURST", burst_length)
    print(f"Burst Error (length {burst_length}) Injected: {infected_codeword}")