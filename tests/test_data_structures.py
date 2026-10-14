import pytest
from src.data_structures import DynamicArray, LinkedList, Deque, AVLTree

def test_dynamic_array():
    arr = DynamicArray()
    for i in range(5):
        arr.append(i)
    assert len(arr) == 5
    assert arr.get(0) == 0
    assert arr.get(4) == 4
    with pytest.raises(IndexError):
        arr.get(5)

def test_linked_list():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.to_list() == [1, 2, 3]

def test_deque():
    dq = Deque()
    dq.append_left(1)
    dq.append_right(2)
    dq.append_left(0)
    assert dq.pop_left() == 0
    assert dq.pop_right() == 2
    assert dq.pop_left() == 1
    assert dq.pop_left() is None

def test_avl_tree():
    tree = AVLTree()
    root = None
    keys = [10, 20, 30, 40, 50, 25]
    for key in keys:
        root = tree.insert(root, key)
    # Проверяем, что корень сбалансирован (для данного набора корень будет 30)
    assert root.key == 30