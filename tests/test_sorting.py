import pytest
from src.sorting import bubble_sort, quick_sort

@pytest.mark.parametrize("sort_func", [bubble_sort, quick_sort])
def test_sorting_algorithms(sort_func):
    assert sort_func([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9]
    assert sort_func([]) == []
    assert sort_func([1]) == [1]
    assert sort_func([3, 3, 3]) == [3, 3, 3]
    assert sort_func([-1, -5, 0, 10]) == [-5, -1, 0, 10]