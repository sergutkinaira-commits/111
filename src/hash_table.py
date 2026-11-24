class HashTable:
    """Простая хэш-таблица с цепочками (метод цепочек).

    Каждая ячейка хранит список пар [ключ, значение].
    Когда заполненность превышает 0.75, таблица увеличивается вдвое.
    """

    def __init__(self, capacity=8):
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size / len(self._buckets) > 0.75:
            self._resize()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def contains(self, key):
        for k, _ in self._bucket(key):
            if k == key:
                return True
        return False

    def _resize(self):
        old_buckets = self._buckets
        self._buckets = [[] for _ in range(len(old_buckets) * 2)]
        for bucket in old_buckets:
            for key, value in bucket:
                self._buckets[hash(key) % len(self._buckets)].append([key, value])

    def keys(self):
        return [k for bucket in self._buckets for k, _ in bucket]

    def __len__(self):
        return self._size

    def __contains__(self, key):
        return self.contains(key)

    def __getitem__(self, key):
        for k, v in self._bucket(key):
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        if not self.remove(key):
            raise KeyError(key)