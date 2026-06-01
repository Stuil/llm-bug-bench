def find_max(numbers):
    if not numbers:
        return None
    max_val = 0
    for n in numbers:
        if n > max_val:
            max_val = n
    return max_val
