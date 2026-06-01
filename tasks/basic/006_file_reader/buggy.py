def read_lines(filename):
    f = open(filename, "r")
    return [line.strip() for line in f.readlines()]
