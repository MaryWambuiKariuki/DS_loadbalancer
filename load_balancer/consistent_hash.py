import hashlib


class ConsistentHash:
    """
    Consistent Hash Ring

    M = 512 slots
    K = 9 virtual servers per physical server
    """

    def __init__(self, slots=512, virtual_servers=9):

        self.slots = slots
        self.virtual_servers = virtual_servers

        # Circular hash ring
        self.ring = [None] * slots

        # Keeps track of occupied slots for each server
        self.server_slots = {}

    # -----------------------------------------
    # Request Hash Function (Deterministic)
    # -----------------------------------------
    def request_hash(self, request_key):

        h = hashlib.sha256(
            str(request_key).encode()
        ).hexdigest()

        return int(h, 16) % self.slots

    # -----------------------------------------
    # Virtual Server Hash Function
    # -----------------------------------------
    def virtual_hash(self, server_id, replica):

        h = hashlib.sha256(
            f"{server_id}-{replica}".encode()
        ).hexdigest()

        return int(h, 16) % self.slots

    # -----------------------------------------
    # Linear Probing
    # -----------------------------------------
    def _find_empty_slot(self, slot):

        while self.ring[slot] is not None:
            slot = (slot + 1) % self.slots

        return slot

    # -----------------------------------------
    # Add Server
    # -----------------------------------------
    def add_server(self, server_name, server_id):

        occupied = []

        for replica in range(self.virtual_servers):

            slot = self.virtual_hash(server_id, replica)
            slot = self._find_empty_slot(slot)

            self.ring[slot] = server_name
            occupied.append(slot)

        self.server_slots[server_name] = occupied

    # -----------------------------------------
    # Remove Server
    # -----------------------------------------
    def remove_server(self, server_name):

        if server_name not in self.server_slots:
            return

        for slot in self.server_slots[server_name]:
            self.ring[slot] = None

        del self.server_slots[server_name]

    # -----------------------------------------
    # Route Request
    # -----------------------------------------
    def get_server(self, request_key):

        slot = self.request_hash(request_key)

        for _ in range(self.slots):

            if self.ring[slot] is not None:
                return self.ring[slot]

            slot = (slot + 1) % self.slots

        return None

    # -----------------------------------------
    # Print Ring
    # -----------------------------------------
    def display_ring(self):

        print("=" * 60)

        for index, server in enumerate(self.ring):

            if server is not None:
                print(f"Slot {index:3} -> {server}")

        print("=" * 60)