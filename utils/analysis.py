import math

from tree import Node
from utils.tools import tree2dict


def expected_length(tree: Node, queue: list):
    dictionary: dict = tree2dict(tree)
    result = 0
    for item in queue:
        result += item.value[0] * len(dictionary[item.value[1]])
    return result


def symbol_entropy(queue: list):
    result = 0
    for item in queue:
        if item.value[0] == 0:
            continue
        result += item.value[0] * math.log2(1 / item.value[0])
    return result
