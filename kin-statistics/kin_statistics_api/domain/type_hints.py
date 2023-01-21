import csv
from tempfile import TemporaryFile

with TemporaryFile() as f:
    CSV_WRITER = type(csv.writer(f))
