from pathlib import Path

import pytest

from ltspd.exchange.serial import IdxSchemaPointer
from ltspd.io.input.csv import csv_to_dataset

RESOURCES = Path(__file__).parents[2] / "resources"


def test_csv_to_dataset():
    pointer = IdxSchemaPointer(true_id=[0], attributes=[1, 2, 3], dimensions=[4, 5])
    with open(RESOURCES / "test_attendees.csv", newline="") as f:
        dataset = csv_to_dataset(f, pointer)

    assert dataset.schema.true_id.name == "id"
    assert [a.name for a in dataset.schema.attributes] == [
        "first_name",
        "last_name",
        "email",
    ]
    assert dataset.dataset[0].values[:3] == ["8211838729", "Gwynne", "Lawtie"]
    assert all(len(r.values) == 6 for r in dataset.dataset)


def test_csv_to_dataset_requires_headers():
    with pytest.raises(ValueError):
        csv_to_dataset([], IdxSchemaPointer([0], [], []), has_headers=False)
