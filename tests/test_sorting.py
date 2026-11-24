import random

import pytest
from src.sorting import bubble_sort, quick_sort

SORTS = [bubble_sort, quick_sort]


@pytest.mark.parametrize("sort_func", SORTS)
def test_sorting_algorithms(sort_func):
    assert sort_func([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9]
    assert sort_func([]) == []
    assert sort_func([1]) == [1]
    assert sort_func([3, 3, 3]) == [3, 3, 3]
    assert sort_func([-1, -5, 0, 10]) == [-5, -1, 0, 10]


@pytest.mark.parametrize("sort_func", SORTS)
def test_already_sorted_and_reversed(sort_func):
    data = list(range(100))
    assert sort_func(data[:]) == data
    assert sort_func(data[::-1]) == data


@pytest.mark.parametrize("sort_func", SORTS)
def test_two_elements(sort_func):
    assert sort_func([2, 1]) == [1, 2]
    assert sort_func([1, 2]) == [1, 2]


@pytest.mark.parametrize("sort_func", SORTS)
def test_floats_and_strings(sort_func):
    assert sort_func([2.5, -1.0, 0.0, 2.5]) == [-1.0, 0.0, 2.5, 2.5]
    assert sort_func(["b", "c", "a"]) == ["a", "b", "c"]


@pytest.mark.parametrize("sort_func", SORTS)
def test_random_against_builtin_sorted(sort_func):
    rng = random.Random(42)
    for _ in range(200):
        data = [rng.randint(-50, 50) for _ in range(rng.randint(0, 60))]
        assert sort_func(data[:]) == sorted(data)


def test_bubble_sort_sorts_in_place():
    data = [3, 1, 2]
    result = bubble_sort(data)
    assert result is data
    assert data == [1, 2, 3]


def test_quick_sort_does_not_modify_input():
    data = [3, 1, 2]
    assert quick_sort(data) == [1, 2, 3]
    assert data == [3, 1, 2]