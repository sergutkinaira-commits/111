import random
from collections import OrderedDict

import pytest
from src.lru_cache import LRUCache


def test_basic_put_and_get():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    assert cache.get("b") == 2
    assert len(cache) == 2


def test_get_missing_returns_default():
    cache = LRUCache(2)
    assert cache.get("x") is None
    assert cache.get("x", -1) == -1


def test_evicts_least_recently_used():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)  # "a" самый старый
    assert "a" not in cache
    assert cache.get("b") == 2
    assert cache.get("c") == 3


def test_get_refreshes_recency():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")      # теперь самый старый "b"
    cache.put("c", 3)
    assert "b" not in cache
    assert cache.get("a") == 1


def test_put_existing_updates_value_and_recency():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)  # обновили "a", самый старый теперь "b"
    cache.put("c", 3)
    assert cache.get("a") == 10
    assert "b" not in cache
    assert len(cache) == 2


def test_capacity_one():
    cache = LRUCache(1)
    cache.put("a", 1)
    cache.put("b", 2)
    assert "a" not in cache
    assert cache.get("b") == 2
    assert len(cache) == 1


def test_order_of_keys_most_recent_first():
    cache = LRUCache(3)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.put(3, "c")
    cache.get(1)
    assert cache.keys() == [1, 3, 2]


def test_contains_does_not_change_order():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert "a" in cache          # не должно освежать "a"
    cache.put("c", 3)
    assert "a" not in cache      # "a" остался самым старым


def test_stores_none_value():
    cache = LRUCache(2)
    cache.put("a", None)
    assert "a" in cache
    assert cache.get("a", "default") is None


@pytest.mark.parametrize("capacity", [0, -1])
def test_invalid_capacity(capacity):
    with pytest.raises(ValueError):
        LRUCache(capacity)


def test_random_operations_match_ordered_dict_model():
    rng = random.Random(3)
    capacity = 5
    cache, model = LRUCache(capacity), OrderedDict()
    for _ in range(5000):
        key = rng.randint(0, 12)
        if rng.random() < 0.5:
            cache.put(key, key * 2)
            model[key] = key * 2
            model.move_to_end(key)
            if len(model) > capacity:
                model.popitem(last=False)
        else:
            expected = model.get(key)
            if key in model:
                model.move_to_end(key)
            assert cache.get(key) == expected
        assert len(cache) == len(model)
        assert cache.keys() == list(reversed(model))