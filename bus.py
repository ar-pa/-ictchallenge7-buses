from typing import List
# import ssettings as settings
import settings as settings


class Node:
    id: int

    def __init__(self):
        self.first_not_delivered = [0] * settings.NUMBER_OF_NODES
        self.first_not_received = [0] * settings.NUMBER_OF_NODES
        self.neighbors: List[Node] = list()

    def add_transaction(self, number_of_new_transactions=1):
        self.first_not_received[self.id] += number_of_new_transactions

    def checkout_node(self, neighbor_node: 'Node'):
        cost = 0
        for i in range(settings.NUMBER_OF_NODES):
            if isinstance(neighbor_node, Center):
                self.first_not_delivered[i] = self.first_not_received[i]
            self.first_not_delivered[i] = max(self.first_not_delivered[i], neighbor_node.first_not_delivered[i])
            cost += max(0, neighbor_node.first_not_received[i] - max(self.first_not_received[i],
                                                                     self.first_not_delivered[i]))
            self.first_not_received[i] = max(self.first_not_received[i], neighbor_node.first_not_received[i])

        return cost


class Center(Node):
    pass
