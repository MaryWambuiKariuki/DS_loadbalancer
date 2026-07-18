class ConsistentHash:
    def __init__(self, slots=512, virtual_servers=9):
        self.slots = slots
        self.virtual_servers = virtual_servers

        # Circular hash ring
        self.ring = [None] * slots

        # Keeps track of where each physical server's
        # virtual servers are placed.
        self.server_slots = {}

    # ----------------------------------------
    # Request Hash Function
    # ----------------------------------------
    def request_hash(self, request_id):
        """
        Hashes a request ID into one of the 512 slots.
        """

        return (request_id + 2 * (request_id ** 2) + 17) % self.slots

    # ----------------------------------------
    # Virtual Server Hash Function
    # ----------------------------------------
    def virtual_hash(self, server_id, replica_id):
        """
        Computes the slot for a virtual server.
        """

        return (
            server_id
            + replica_id
            + 2 * (replica_id ** 2)
            + 25
        ) % self.slots

    # ----------------------------------------
    # Linear Probing
    # ----------------------------------------
    def find_empty_slot(self, slot):

        while self.ring[slot] is not None:

            slot = (slot + 1) % self.slots

        return slot

    # ----------------------------------------
    # Add Server
    # ----------------------------------------
    def add_server(self, server_name, server_id):

        occupied = []

        for replica in range(self.virtual_servers):

            slot = self.virtual_hash(server_id, replica)

            slot = self.find_empty_slot(slot)

            self.ring[slot] = server_name

            occupied.append(slot)

        self.server_slots[server_name] = occupied

    # ----------------------------------------
    # Remove Server
    # ----------------------------------------
    def remove_server(self, server_name):

        if server_name not in self.server_slots:
            return

        for slot in self.server_slots[server_name]:
            self.ring[slot] = None

        del self.server_slots[server_name]

    # ----------------------------------------
    # Find Server
    # ----------------------------------------
    def get_server(self, request_id):

        slot = self.request_hash(request_id)

        for _ in range(self.slots):

            if self.ring[slot] is not None:
                return self.ring[slot]

            slot = (slot + 1) % self.slots

        return None