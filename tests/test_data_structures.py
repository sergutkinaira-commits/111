import random

import pytest
from src.data_structures import DynamicArray, LinkedList, Deque, AVLTree


# ---------- DynamicArray ----------

def test_dynamic_array():
    arr = DynamicArray()
    for i in range(5):
        arr.append(i)
    assert len(arr) == 5
    assert arr.get(0) == 0
    assert arr.get(4) == 4
    with pytest.raises(IndexError):
        arr.get(5)


def test_dynamic_array_empty_and_negative_index():
    arr = DynamicArray()
    assert len(arr) == 0
    with pytest.raises(IndexError):
        arr.get(0)
    arr.append(1)
    with pytest.raises(IndexError):
        arr.get(-1)


def test_dynamic_array_grows_and_keeps_order():
    arr = DynamicArray()
    for i in range(1000):
        arr.append(i)
    assert len(arr) == 1000
    assert arr.capacity >= 1000
    assert [arr.get(i) for i in range(1000)] == list(range(1000))


# ---------- LinkedList ----------

def test_linked_list():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.to_list() == [1, 2, 3]


def test_linked_list_empty():
    assert LinkedList().to_list() == []


def test_linked_list_single_and_duplicates():
    ll = LinkedList()
    ll.append("a")
    assert ll.to_list() == ["a"]
    ll.append("a")
    assert ll.to_list() == ["a", "a"]


# ---------- Deque ----------

def test_deque():
    dq = Deque()
    dq.append_left(1)
    dq.append_right(2)
    dq.append_left(0)
    assert dq.pop_left() == 0
    assert dq.pop_right() == 2
    assert dq.pop_left() == 1
    assert dq.pop_left() is None


def test_deque_empty_pops():
    dq = Deque()
    assert dq.pop_left() is None
    assert dq.pop_right() is None


def test_deque_single_element_from_either_end():
    dq = Deque()
    dq.append_right(7)
    assert dq.pop_right() == 7
    assert dq.front is None and dq.rear is None
    dq.append_left(8)
    assert dq.pop_left() == 8
    assert dq.front is None and dq.rear is None


def test_deque_works_as_stack_and_queue():
    dq = Deque()
    for i in range(5):
        dq.append_right(i)
    assert [dq.pop_left() for _ in range(5)] == [0, 1, 2, 3, 4]  # очередь
    for i in range(5):
        dq.append_right(i)
    assert [dq.pop_right() for _ in range(5)] == [4, 3, 2, 1, 0]  # стек


def test_deque_reusable_after_emptying():
    dq = Deque()
    dq.append_left(1)
    dq.pop_right()
    dq.append_right(2)
    dq.append_left(1)
    assert dq.pop_left() == 1
    assert dq.pop_left() == 2
    assert dq.pop_left() is None


# ---------- AVLTree ----------

def _height(node):
    return node.height if node else 0


def _is_balanced(node):
    """Проверяет баланс и что сохранённые высоты верны."""
    if not node:
        return True
    left, right = _height(node.left), _height(node.right)
    if abs(left - right) > 1 or node.height != 1 + max(left, right):
        return False
    return _is_balanced(node.left) and _is_balanced(node.right)


def _build(keys):
    tree, root = AVLTree(), None
    for key in keys:
        root = tree.insert(root, key)
    return tree, root


def test_avl_tree():
    tree = AVLTree()
    root = None
    keys = [10, 20, 30, 40, 50, 25]
    for key in keys:
        root = tree.insert(root, key)
    # Проверяем, что корень сбалансирован (для данного набора корень будет 30)
    assert root.key == 30


def test_avl_empty_tree():
    tree = AVLTree()
    assert tree.inorder(None) == []
    assert tree.search(None, 1) is None
    assert tree.delete(None, 1) is None


@pytest.mark.parametrize("keys", [
    [1, 2, 3],           # правый-правый, левый поворот
    [3, 2, 1],           # левый-левый, правый поворот
    [3, 1, 2],           # левый-правый
    [1, 3, 2],           # правый-левый
])
def test_avl_all_four_rotations_give_root_2(keys):
    _, root = _build(keys)
    assert root.key == 2
    assert root.left.key == 1 and root.right.key == 3
    assert root.height == 2


def test_avl_sorted_insert_stays_balanced():
    tree, root = _build(range(1, 1025))
    assert _is_balanced(root)
    assert root.height <= 11  # идеальное дерево: 10-11, у списка было бы 1024
    assert tree.inorder(root) == list(range(1, 1025))


def test_avl_ignores_duplicates():
    tree, root = _build([10, 20, 20, 20, 20, 20, 10])
    assert tree.inorder(root) == [10, 20]
    assert _is_balanced(root)


def test_avl_search():
    tree, root = _build([5, 3, 8, 1, 4])
    assert tree.search(root, 4).key == 4
    assert tree.search(root, 5).key == 5
    assert tree.search(root, 99) is None


def test_avl_delete_leaf_one_child_two_children():
    tree, root = _build([50, 30, 70, 20, 40, 60, 80, 10])
    root = tree.delete(root, 10)   # лист
    root = tree.delete(root, 20)   # теперь лист (потомок 10 уже удалён)
    root = tree.delete(root, 30)   # узел с одним потомком (40)
    root = tree.delete(root, 50)   # корень с двумя потомками
    assert tree.inorder(root) == [40, 60, 70, 80]
    assert _is_balanced(root)


def test_avl_delete_missing_key_changes_nothing():
    tree, root = _build([2, 1, 3])
    root = tree.delete(root, 42)
    assert tree.inorder(root) == [1, 2, 3]


def test_avl_delete_everything():
    tree, root = _build([4, 2, 6, 1, 3, 5, 7])
    for key in [4, 1, 7, 2, 6, 3, 5]:
        root = tree.delete(root, key)
        assert _is_balanced(root)
    assert root is None


def test_avl_delete_triggers_rebalancing():
    # После удаления 1 правая сторона становится тяжелее на 2
    tree, root = _build([2, 1, 4, 3, 5])
    root = tree.delete(root, 1)
    assert _is_balanced(root)
    assert tree.inorder(root) == [2, 3, 4, 5]


def test_avl_random_operations_match_set():
    rng = random.Random(1)
    for _ in range(100):
        tree, root = AVLTree(), None
        reference = set()
        for _ in range(80):
            key = rng.randint(0, 40)
            if rng.random() < 0.6:
                root = tree.insert(root, key)
                reference.add(key)
            else:
                root = tree.delete(root, key)
                reference.discard(key)
            assert _is_balanced(root)
            assert tree.inorder(root) == sorted(reference)