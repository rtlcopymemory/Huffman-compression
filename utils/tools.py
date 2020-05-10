from tree import Node


def get_characters_count(input_path: str) -> tuple:
    X: list = [0] * 128
    possible_cases: int = 0
    with open(input_path, 'rb') as f:
        for line in f:
            for character in line:
                X[character] += 1
                possible_cases += 1
    return X, possible_cases


def create_queue(x: list, total: int) -> list:
    Q: list = []
    items: int = 0
    for i, item in enumerate(x):
        Q.append(Node((item / total, chr(i))))
        items += 1
    Q.sort(key=lambda x: x.value[0])
    return Q


def huffman(q: list) -> Node:
    for i in range(len(q) - 1):
        common_root: Node = Node(None)
        common_root.right = q.pop(0)
        common_root.left = q.pop(0)
        common_root.value = (common_root.right.value[0] + common_root.left.value[0], None)
        q.append(common_root)
        q.sort(key=lambda x: x.value[0])
    return q.pop(0)


def tree2dict(t: Node, prefix: str = "") -> dict:
    if t.right is None and t.left is None:
        return {t.value[1]: prefix}
    result: dict = {}
    result.update(tree2dict(t.left, prefix + "1"))
    result.update(tree2dict(t.right, prefix + "0"))
    return result
