import re

from ltspd.utils.thing_namer import ADJECTIVES, DISHES, VEGETABLES, name_it


def test_name_it_readable():
    name = name_it()
    assert name.split("-")[0] in ADJECTIVES
    assert any(name.endswith(f"-{d}") for d in DISHES)
    assert any(f"-{v}-" in name for v in VEGETABLES)


def test_name_it_uuid_suffix():
    assert re.fullmatch(r".+-[0-9a-f]{4}", name_it(add_uuid=True))


def test_name_it_unreadable():
    assert re.fullmatch(r"[0-9a-f]{8}", name_it(readable=False))
