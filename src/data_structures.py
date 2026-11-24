# Динамический массив (аналог list в Python, но реализованный вручную)
class DynamicArray:
    def __init__(self):
        self.capacity = 2
        self.size = 0
        self.data = [None] * self.capacity

    def append(self, item):
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = item
        self.size += 1

    def _resize(self):
        self.capacity *= 2
        new_data = [None] * self.capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data

    def get(self, index):
        if 0 <= index < self.size:
            return self.data[index]
        raise IndexError("Index out of bounds")

    def __len__(self):
        return self.size

# Односвязный список
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

# Дек (двусторонняя очередь) на основе двусвязного списка
class DequeNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class Deque:
    def __init__(self):
        self.front = None
        self.rear = None

    def append_left(self, data):
        new_node = DequeNode(data)
        if not self.front:
            self.front = self.rear = new_node
        else:
            new_node.next = self.front
            self.front.prev = new_node
            self.front = new_node

    def append_right(self, data):
        new_node = DequeNode(data)
        if not self.rear:
            self.front = self.rear = new_node
        else:
            new_node.prev = self.rear
            self.rear.next = new_node
            self.rear = new_node

    def pop_left(self):
        if not self.front:
            return None
        data = self.front.data
        self.front = self.front.next
        if self.front:
            self.front.prev = None
        else:
            self.rear = None
        return data

    def pop_right(self):
        if not self.rear:
            return None
        data = self.rear.data
        self.rear = self.rear.prev
        if self.rear:
            self.rear.next = None
        else:
            self.front = None
        return data

# AVL Дерево
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    """AVL-дерево как множество уникальных ключей.

    Методы работают с корнем: root = tree.insert(root, key).
    Повторная вставка существующего ключа ничего не меняет.
    """

    def insert(self, root, key):
        if not root:
            return AVLNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            # Дубликат: игнорируем, иначе ломается балансировка
            return root

        return self._rebalance(root)

    def delete(self, root, key):
        if not root:
            return None
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            # Два потомка: заменяем ключ минимальным из правого поддерева
            successor = self._min_node(root.right)
            root.key = successor.key
            root.right = self.delete(root.right, successor.key)

        return self._rebalance(root)

    def search(self, root, key):
        """Возвращает узел с ключом или None."""
        while root:
            if key < root.key:
                root = root.left
            elif key > root.key:
                root = root.right
            else:
                return root
        return None

    def inorder(self, root):
        """Ключи в порядке возрастания."""
        if not root:
            return []
        return self.inorder(root.left) + [root.key] + self.inorder(root.right)

    def _min_node(self, root):
        while root.left:
            root = root.left
        return root

    def _rebalance(self, root):
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

        if balance > 1:
            # Левый правый
            if self._get_balance(root.left) < 0:
                root.left = self._left_rotate(root.left)
            # Левый левый
            return self._right_rotate(root)
        if balance < -1:
            # Правый левый
            if self._get_balance(root.right) > 0:
                root.right = self._right_rotate(root.right)
            # Правый правый
            return self._left_rotate(root)

        return root

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _get_height(self, root):
        if not root:
            return 0
        return root.height

    def _get_balance(self, root):
        if not root:
            return 0
        return self._get_height(root.left) - self._get_height(root.right)