import csv

from ltspd.exchange.serial import DataSet, Row, Schema


def csv_to_dataset(fsource, schema_pointer, has_headers=True):
    if not has_headers:
        raise ValueError("LTSPD only supports CSVs with a header row")
    data = csv.reader(fsource)
    head = next(data)
    return DataSet(
        schema=Schema.from_pointer(schema_pointer, head),
        dataset=[Row.from_pointer(schema_pointer, row) for row in data],
    )
