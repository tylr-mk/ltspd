import csv

from pyarrow.csv import read_csv

from ltspd.exchange.serial import Schema, Row, DataSet


def csv_to_dataset(fsource, schema_pointer, has_headers=True):
    data = csv.reader(fsource)
    if has_headers:
        head = next(data)
    else:
        raise ValueError("LTSPD only supports CSVs with a header row")
    return DataSet(
        schema = Schema.from_pointer(schema_pointer,  head),
        dataset = [Row.from_pointer(schema_pointer, row) for row in data]
    )


# from pyarrow.csv import read_csv


# def read(fsourse):
#     return read_csv(fsourse)
