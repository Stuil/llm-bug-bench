import csv
import io

def parse_csv(line):
    reader = csv.reader(io.StringIO(line))
    return next(reader)
