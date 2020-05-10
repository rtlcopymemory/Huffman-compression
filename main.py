import pickle
from bitstring import BitStream, BitArray
from tree import Node
import argparse

parser = argparse.ArgumentParser(description="Compresses a file using the Huffman algorithm")
parser.add_argument("-o", "--output", help="Sets output path")
parser.add_argument("input", type=str, help="input file path")
parser.add_argument("-d", "--decompress", help="decompress")

args = parser.parse_args()

out_path = args.output if args.output else "output.huff"


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


def compress(input_path: str, compression_dict: dict) -> BitArray:
    temp_result = ""
    with open(input_path, 'r') as f:
        for line in f:
            for char in line:
                temp_result += compression_dict[char]
    bits = BitArray(bin=temp_result)
    return bits


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    count, total = get_characters_count(args.input)
    queue = create_queue(count, total)
    tree = huffman(queue)
    save_obj(tree2dict(tree), out_path.split('.')[0])
    print(tree2dict(tree))
    with open(out_path, 'wb') as f:
        compress(args.input, tree2dict(tree)).tofile(f)
