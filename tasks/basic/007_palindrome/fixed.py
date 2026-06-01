def is_palindrome(s):
    chars = []
    for c in s:
        if c.isalpha():
            chars.append(c.lower())
    n = len(chars)
    if n == 0:
        return True
    for i in range(n // 2):
        if chars[i] != chars[n - 1 - i]:
            return False
    return True
