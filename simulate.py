import random
from typing import List
# import ssettings as settings
import settings as settings
from bus import Center, Node

nodes: List[Node] = [Center()] + [Node() for i in range(settings.NUMBER_OF_NODES - 1)]

for i in range(len(nodes)):
    nodes[i].id = i

while True:
    need_neighbor = list(filter(lambda node: len(node.neighbors) < settings.NUMBER_OF_NEIGHBORS, nodes[1:]))
    if len(need_neighbor) < 2:
        break
    v, u = random.sample(need_neighbor, 2)
    if u not in v.neighbors:
        v.neighbors.append(u)
        u.neighbors.append(v)

for bus in random.sample(nodes[1:], settings.NUMBER_OF_CENTER_NEIGHBORS):
    bus.neighbors.append(nodes[0])
    nodes[0].neighbors.append(bus)

time_stamp = 0
total_cost = 0
while True:
    for node in nodes[1:]:
        node.add_transaction(settings.X)

    # TODO: fix data flow in single time stamp (maybe make it atomic)
    for node in nodes:
        for neighbor in node.neighbors:
            if node.id < neighbor.id and random.random() < settings.Y:
                total_cost += node.checkout_node(neighbor)
                total_cost += neighbor.checkout_node(node)
    current_created = settings.X * (time_stamp + 1) * (settings.NUMBER_OF_NODES - 1)
    current_received = sum(nodes[0].first_not_received)
    print(current_created, current_received, '{:.2f}%'.format(current_received * 100 / current_created), total_cost)
    if current_received >= settings.NUMBER_OF_PACKETS_TO_TRANSMIT:
        break
    time_stamp += 1
