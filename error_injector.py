import random

def inject_single_bit_error(codeword, index):
    if index < 0 or index >= len(codeword):
        raise ValueError("Index out of range")
    infected_codeword = codeword[:index] + ('0' if codeword[index] == '1' else '1') + codeword[index + 1:]
    return infected_codeword

def inject_two_isolated_single_bit_errors(codeword, index1, index2):
    if index1 < 0 or index1 >= len(codeword) or index2 < 0 or index2 >= len(codeword):
        raise ValueError("Indices out of range")
    if index1 == index2:
        raise ValueError("Indices must be different")
    infected_codeword = list(codeword)
    infected_codeword[index1] = '0' if codeword[index1] == '1' else '1'
    infected_codeword[index2] = '0' if codeword[index2] == '1' else '1'
    return ''.join(infected_codeword)

def inject_odd_number_of_errors(codeword, indices):
    if any(index < 0 or index >= len(codeword) for index in indices):
        raise ValueError("Indices out of range")
    infected_codeword = list(codeword)
    for index in indices:
        infected_codeword[index] = '0' if codeword[index] == '1' else '1'
    return ''.join(infected_codeword)

def inject_burst_error(codeword, start_index, burst_length):
    if start_index < 0 or start_index + burst_length > len(codeword):
        raise ValueError("Burst error out of range")
    infected_codeword = list(codeword)
    for i in range(start_index, start_index + burst_length):
        infected_codeword[i] = '0' if codeword[i] == '1' else '1'
    return ''.join(infected_codeword)

def inject_error_random(codeword, error_type, burst_length=None):
    if error_type == "SINGLE":
        index = random.randint(0, len(codeword) - 1)
        return inject_single_bit_error(codeword, index)
    elif error_type == "DOUBLE":
        index1 = random.randint(0, len(codeword) - 1)
        index2 = random.randint(0, len(codeword) - 1)
        while index1 == index2:
            index2 = random.randint(0, len(codeword) - 1)
        return inject_two_isolated_single_bit_errors(codeword, index1, index2)
    elif error_type == "ODD":
        num_errors = random.randint(1, len(codeword))
        while num_errors % 2 == 0:
            num_errors = random.randint(1, len(codeword))
        indices = random.sample(range(len(codeword)), num_errors)
        return inject_odd_number_of_errors(codeword, indices)
    elif error_type == "BURST":
        if burst_length is None:
            raise ValueError("Burst length must be provided for burst errors.")
        start_index = random.randint(0, len(codeword) - burst_length)
        return inject_burst_error(codeword, start_index, burst_length)
    else:
        raise ValueError("Invalid error type specified.")

def inject_error_manual(codeword, error_type, indices=None, start_index=None, burst_length=None):
    if error_type == "SINGLE":
        if indices is None or len(indices) != 1:
            raise ValueError("A single index must be provided for SINGLE error")
        return inject_single_bit_error(codeword, indices[0])
    elif error_type == "DOUBLE":
        if indices is None or len(indices) != 2:
            raise ValueError("Two indices must be provided for DOUBLE error")
        return inject_two_isolated_single_bit_errors(codeword, indices[0], indices[1])
    elif error_type == "ODD":
        if indices is None or len(indices) % 2 == 0:
            raise ValueError("An odd number of indices must be provided for ODD error")
        return inject_odd_number_of_errors(codeword, indices)
    elif error_type == "BURST":
        if start_index is None or burst_length is None:
            raise ValueError("Start index and burst length must be provided for BURST error")
        return inject_burst_error(codeword, start_index, burst_length)
    else:
        raise ValueError("Invalid error type specified.")

# Example usage (for testing purposes)
if __name__ == "__main__":
    codeword = "11010110101101011010101101101010"
    
    print(f"Original Codeword: {codeword}")
    
    infected_codeword = inject_error_random(codeword, "SINGLE")
    print(f"Random Single-bit Error Injected: {infected_codeword}")
    
    infected_codeword = inject_error_random(codeword, "DOUBLE")
    print(f"Random Two Isolated Single-bit Errors Injected: {infected_codeword}")
    
    infected_codeword = inject_error_random(codeword, "ODD")
    print(f"Random Odd Number of Errors Injected: {infected_codeword}")
    
    burst_length = 4  # Example burst length
    infected_codeword = inject_error_random(codeword, "BURST", burst_length)
    print(f"Random Burst Error (length {burst_length}) Injected: {infected_codeword}")

    # Manual error injection examples
    infected_codeword = inject_error_manual(codeword, "SINGLE", indices=[5])
    print(f"Manual Single-bit Error Injected at index 5: {infected_codeword}")
    
    infected_codeword = inject_error_manual(codeword, "DOUBLE", indices=[3, 12])
    print(f"Manual Two Isolated Single-bit Errors Injected at indices 3 and 12: {infected_codeword}")
    
    infected_codeword = inject_error_manual(codeword, "ODD", indices=[2, 5, 8])
    print(f"Manual Odd Number of Errors Injected at indices 2, 5, 8: {infected_codeword}")
    
    infected_codeword = inject_error_manual(codeword, "BURST", start_index=7, burst_length=4)
    print(f"Manual Burst Error Injected from index 7 to 10: {infected_codeword}")