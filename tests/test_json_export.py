import json


def test_json_created():

    with open(
        "output/diagnosis.json",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    assert "findings" in data


def test_root_causes():

    with open(
        "output/diagnosis.json",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    assert "root_causes" in data


def test_version():

    with open(
        "output/diagnosis.json",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    assert "version" in data


def test_severity():

    with open(
        "output/diagnosis.json",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    assert "severity" in data