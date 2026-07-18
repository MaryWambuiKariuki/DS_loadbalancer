import hashlib


class ConsistentHash:
    def __init__(self):
        self.ring = {}
        self.sorted_keys = []

    def hash_value(self, key):
        """
        Generate an integer hash using MD5.
        """
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_server(self, server):
        """
        Add a server to the hash ring.
        """
        key = self.hash_value(server)
        self.ring[key] = server
        self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_server(self, server):
        """
        Remove a server from the ring.
        """
        key = self.hash_value(server)

        if key in self.ring:
            del self.ring[key]
            self.sorted_keys.remove(key)

    def get_server(self, request_key):
        """
        Find the server responsible for a request.
        """
        if not self.sorted_keys:
            return None

        request_hash = self.hash_value(request_key)

        for key in self.sorted_keys:
            if request_hash <= key:
                return self.ring[key]

        # Wrap around to the first server
        return self.ring[self.sorted_keys[0]]