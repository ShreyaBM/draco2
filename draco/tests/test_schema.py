import csv
import datetime
import json
from pathlib import Path

import pandas as pd
import pytest
from draco import schema

SIMPLE_SCHEMA = {
    "number_rows": 2,
    "field": [
        {
            "__id__": "numbers",
            "data_type": "number",
            "unique": 2,
            "max": 2,
            "min": 1,
            "std": 0,
        },
        {"__id__": "text", "data_type": "string", "unique": 1, "freq": 2},
    ],
}


def test_load_df():
    df = pd.DataFrame(
        {
            "numbers": [1, 2],
            "text": ["a", "a"],
            "bools": [True, False],
            "dates": [datetime.datetime(2018, 1, 1), datetime.datetime(2021, 1, 1)],
        }
    )

    assert schema.schema_from_dataframe(df) == {
        "number_rows": 2,
        "field": [
            {
                "__id__": "numbers",
                "data_type": "number",
                "unique": 2,
                "max": 2,
                "min": 1,
                "std": 0,
            },
            {"__id__": "text", "data_type": "string", "unique": 1, "freq": 2},
            {
                "__id__": "bools",
                "data_type": "boolean",
                "unique": 2,
            },
            {
                "__id__": "dates",
                "data_type": "datetime",
                "unique": 2,
            },
        ],
    }


def test_load_unsupported_data():
    df = pd.DataFrame({"datetime": [pd.Timedelta("2 days")]})
    with pytest.raises(ValueError):
        schema.schema_from_dataframe(df)


@pytest.fixture(scope="session")
def csv_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test.csv")
    headers = ["numbers", "text"]
    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerow({"numbers": 1, "text": "a"})
        writer.writerow({"numbers": 2, "text": "a"})
    return Path(filename)


def test_csv_to_schema(csv_file):
    assert schema.schema_from_file(csv_file) == SIMPLE_SCHEMA


@pytest.fixture(scope="session")
def json_file(tmpdir_factory):
    filename = tmpdir_factory.mktemp("data").join("test.json")
    with open(filename, "w") as f:
        json.dump([{"numbers": 1, "text": "a"}, {"numbers": 2, "text": "a"}], f)
    return Path(filename)


def test_json_to_schema(json_file):
    assert schema.schema_from_file(json_file) == SIMPLE_SCHEMA


def test_unknown_file_type():
    with pytest.raises(ValueError):
        schema.schema_from_file(Path("foo.bar"))
