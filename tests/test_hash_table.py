import random

import pytest
from src.hash_table import HashTable


def test_put_and_get():
    table = HashTable()
    table.put("a", 1)
    table.put("b", 2)
    assert table.get("a") == 1
    assert table.get("b") == 2
    assert len(table) == 2


def test_get_missing_returns_default():
    table = HashTable()
    assert table.get("x") is None
    assert table.get("x", 42) == 42


def test_put_existing_key_overwrites_without_growing():
    table = HashTable()
    table.put("a", 1)
    table.put("a", 2)
    assert table.get("a") == 2
    assert len(table) == 1


def test_remove():
    table = HashTable()
    table.put("a", 1)
    assert table.remove("a") is True
    assert table.remove("a") is False
    assert "a" not in table
    assert len(table) == 0


def test_contains_and_keys():
    table = HashTable()
    table.put(1, "x")
    table.put(2, "y")
    assert 1 in table and table.contains(2)
    assert 3 not in table
    assert sorted(table.keys()) == [1, 2]


def test_dict_style_access():
    table = HashTable()
    table["k"] = "v"
    assert table["k"] == "v"
    del table["k"]
    with pytest.raises(KeyError):
        table["k"]
    with pytest.raises(KeyError):
        del table["k"]


def test_stores_none_value_distinct_from_missing():
    table = HashTable()
    table.put("a", None)
    assert "a" in table
    assert table["a"] is None
    assert table.get("a", "default") is None


def test_collisions_in_single_bucket():
    # Целые числа с шагом, равным числу ячеек, попадают в одну ячейку
    table = HashTable(capacity=4)
    keys = [0, 4, 8]
    for k in keys:
        table.put(k, k * 10)
    for k in keys:
        assert table.get(k) == k * 10
    assert table.remove(4) is True
    assert table.get(0) == 0 and table.get(8) == 80


def test_resize_keeps_all_data():
    table = HashTable(capacity=2)
    for i in range(1000):
        table.put(i, i * 2)
    assert len(table) == 1000
    assert len(table._buckets) > 2
    assert all(table.get(i) == i * 2 for i in range(1000))


def test_mixed_key_types():
    table = HashTable()
    for key, value in [(1, "int"), ("1", "str"), ((1, 2), "tuple"), (1.5, "float")]:
        table.put(key, value)
    assert table[1] == "int"
    assert table["1"] == "str"
    assert table[(1, 2)] == "tuple"
    assert table[1.5] == "float"


def test_invalid_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=0)


def test_random_operations_match_dict():
    rng = random.Random(7)
    table, reference = HashTable(), {}
    for _ in range(5000):
        key = rng.randint(0, 200)
        action = rng.random()
        if action < 0.5:
            table.put(key, action)
            reference[key] = action
        elif action < 0.8:
            assert table.remove(key) == (key in reference)
            reference.pop(key, None)
        else:
            assert table.get(key) == reference.get(key)
        assert len(table) == len(reference)
    assert sorted(table.keys()) == sorted(reference)