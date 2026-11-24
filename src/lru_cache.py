class _CacheNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """LRU-кэш (вытесняет давно не использованные элементы).

    Словарь даёт доступ по ключу за O(1), двусвязный список хранит порядок
    использования: у головы самые свежие элементы, у хвоста самые старые.
    """

    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._map = {}
        # Фиктивные узлы-границы, чтобы не обрабатывать пустой список отдельно
        self._head = _CacheNode()
        self._tail = _CacheNode()
        self._head.next = self._tail
        self._tail.prev = self._head

    def get(self, key, default=None):
        node = self._map.get(key)
        if node is None:
            return default
        self._remove(node)
        self._add_front(node)
        return node.value

    def put(self, key, value):
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._remove(node)
            self._add_front(node)
            return
        if len(self._map) >= self.capacity:
            oldest = self._tail.prev
            self._remove(oldest)
            del self._map[oldest.key]
        node = _CacheNode(key, value)
        self._map[key] = node
        self._add_front(node)

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        node.next = self._head.next
        node.prev = self._head
        self._head.next.prev = node
        self._head.next = node

    def keys(self):
        """Ключи от самого свежего к самому старому."""
        result = []
        node = self._head.next
        while node is not self._tail:
            result.append(node.key)
            node = node.next
        return result

    def __len__(self):
        return len(self._map)

    def __contains__(self, key):
        # Проверка наличия не считается использованием
        return key in self._map