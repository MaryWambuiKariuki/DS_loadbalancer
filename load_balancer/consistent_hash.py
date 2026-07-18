class ConsistentHash:
    def __init__(self, slots=512, virtual_servers=9):
        """
        Initialize the consistent hash ring.
        """
        self.slots = slots
        self.virtual_servers = virtual_servers

        # Hash ring (512 slots)
        self.ring = [None] * slots

        # Keeps track of each server's occupied slots
        self.server_slots = {}

    # ----------------------------------------------------
    # Request Hash Function
    # H(i) = i² + 2i + 17
    # ----------------------------------------------------
    def request_hash(self, request_id):
        return ((request_id ** 2) + (2 * request_id) + 17) % self.slots

    # ----------------------------------------------------
    # Virtual Server Hash Function
    # Φ(i,j) = i² + j² + 2j + 25
    # ----------------------------------------------------
    def virtual_hash(self, server_id, replica):
        return ((server_id ** 2) + (replica ** 2) + (2 * replica) + 25) % self.slots

    # ----------------------------------------------------
    # Linear Probing
    # ----------------------------------------------------
    def find_empty_slot(self, slot):

        while self.ring[slot] is not None:
            slot = (slot + 1) % self.slots

        return slot

    # ----------------------------------------------------
    # Add Server
    # ----------------------------------------------------
    def add_server(self, server_name, server_id):

        occupied_slots = []

        for replica in range(self.virtual_servers):

            slot = self.virtual_hash(server_id, replica)

            slot = self.find_empty_slot(slot)

            self.ring[slot] = server_name

            occupied_slots.append(slot)

        self.server_slots[server_name] = occupied_slots

    # ----------------------------------------------------
    # Remove Server
    # ----------------------------------------------------
    def remove_server(self, server_name):

        if server_name not in self.server_slots:
            return

        for slot in self.server_slots[server_name]:
            self.ring[slot] = None

        del self.server_slots[server_name]

    # ----------------------------------------------------
    # Find Server for a Request
    # ----------------------------------------------------
    def get_server(self, request_id):

        slot = self.request_hash(request_id)

        for _ in range(self.slots):

            if self.ring[slot] is not None:
                return self.ring[slot]

            slot = (slot + 1) % self.slots

        return None

    # ----------------------------------------------------
    # Display Ring (for debugging)
    # ----------------------------------------------------
    def display_ring(self):

        for i in range(self.slots):

            if self.ring[i] is not None:
                print(f"Slot {i} -> {self.ring[i]}")