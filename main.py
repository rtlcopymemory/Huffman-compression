from queue import PriorityQueue
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


def create_queue(x: list) -> PriorityQueue:
    Q: PriorityQueue = PriorityQueue()
    for item, i in enumerate(x):
        Q.put((item, chr(i)))
    return Q


if __name__ == "__main__":
    count, total = get_characters_count(args.input)
    queue = create_queue(count)
    print(count)
    print(total)
