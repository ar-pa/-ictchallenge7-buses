import random
from typing import List, Deque
from collections import deque
import settings as settings
from bus import Center, Node

random.seed(0)

nodes: List[Node] = [Center()] + [Node() for i in range(settings.NUMBER_OF_NODES - 1)]


def make_graph():
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


def calculate_distances():
    """
    Runs bfs and calculate the shortest distance of every node to the center.
    Also calculates node.parent which is the parent in bfs-tree.
    """
    bfs_queue: Deque[Node] = deque()
    bfs_queue.append(nodes[0])
    nodes[0].distance = 0
    while bfs_queue:
        vertex = bfs_queue.popleft()
        for neighbor in vertex.neighbors:
            if neighbor.distance == settings.INF:
                neighbor.distance = vertex.distance + 1
                neighbor.parent = vertex
                bfs_queue.append(neighbor)


def remove_unnecessary_neighbors():
    """
    Removes unnecessary neighbors (e.g. who are not in bfs-tree) from the neighbors.
    """
    print('Reduced number of neighbors from', sum(len(x.neighbors) for x in nodes), end='')
    calculate_distances()
    for v in nodes:
        v.neighbors = list(filter(lambda neighbor: neighbor.parent == v or v.parent == neighbor, v.neighbors))
    print(' to', sum(len(x.neighbors) for x in nodes))


make_graph()
remove_unnecessary_neighbors()

time_stamp = 0
total_cost = 0
while True:
    for node in nodes[1:]:
        node.add_transaction(settings.X)

    for node in nodes:
        for neighbor in node.neighbors:
            if node.id < neighbor.id and random.random() < settings.Y:
                total_cost += node.checkout_node(neighbor)
                total_cost += neighbor.checkout_node(node)
    current_created = settings.X * (time_stamp + 1) * (settings.NUMBER_OF_NODES - 1)
    current_received = sum(nodes[0].first_not_received)
    print(time_stamp, current_created, current_received, '{:.2f}%'.format(current_received * 100 / current_created),
          total_cost)
    if current_received >= settings.NUMBER_OF_PACKETS_TO_TRANSMIT:
        break
    time_stamp += 1
