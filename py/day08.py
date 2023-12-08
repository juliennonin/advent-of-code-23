# %%
import re
import math
from itertools import cycle

from helpers.load_puzzle import puzzle


# %%
def parse_node(node_str):
    node, left, right = re.match(r"^(\w+) = \((\w+), (\w+)\)", node_str).groups()
    return node, left, right


def parse_data(data):
    navigation_str, network_data_str = data.split("\n\n")
    network_data = map(parse_node, network_data_str.splitlines())
    navigation = list(map(lambda s: int(s == "R"), navigation_str))

    network = dict()
    for node, left, right in network_data:
        network[node] = (left, right)

    return network, navigation


# %%
def travel_to_Z(network, navigation, node, stop_condition):
    for i, direction in enumerate(cycle(navigation)):
        if stop_condition(node):
            break
        node = network[node][direction]
    return i


def part1(network, navigation):
    return travel_to_Z(network, navigation, "AAA", lambda node: node == "ZZZ")


def part2(network, navigation):
    nodes = (node for node in network.keys() if node.endswith("A"))
    steps_in_loops = []
    for node in nodes:
        steps_in_loops.append(
            travel_to_Z(network, navigation, node, lambda node: node.endswith("Z"))
        )
    assert all(step % len(navigation) == 0 for step in steps_in_loops)
    return math.lcm(*steps_in_loops)


# %%
with open(puzzle(8), "r") as f:
    data = f.read()

network, navigation = parse_data(data)

print("Part 1 —", part1(network, navigation))
print("Part 2 —", part2(network, navigation))

# %%
