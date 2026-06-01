def is_palindrome(s):
    chars = []
    for c in s:
        if c.isalpha():
            chars.append(c.lower())
    n = len(chars)
    for i in range(n // 2):
        if chars[i] != chars[n - i]:
            return False
    return True if n > 0 else False
