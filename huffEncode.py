from bitstring import BitArray
import argparse

from utils.analysis import expected_length, symbol_entropy
from utils.storeTree import save_obj
from utils.tools import get_characters_count, create_queue, huffman, tree2dict

parser = argparse.ArgumentParser(description="Compresses a file using the Huffman algorithm")
parser.add_argument("-o", "--output", help="Sets output path")
parser.add_argument("input", type=str, help="input file path")

args = parser.parse_args()

out_path = args.output if args.output else "output.huff"


def compress(input_path: str, compression_dict: dict) -> BitArray:
    temp_result = ""
    with open(input_path, 'r') as f:
        for line in f:
            for char in line:
                temp_result += compression_dict[char]
    end_padding = len(temp_result) % 8 if len(temp_result) % 8 != 0 else 0
    end_offset: str = bin(8 - end_padding)[2:].zfill(8)
    bits = BitArray(bin=end_offset + temp_result)
    return bits


if __name__ == "__main__":
    count, total = get_characters_count(args.input)
    queue = create_queue(count, total)
    tree = huffman(queue)
    save_obj(tree2dict(tree), out_path.split('.')[0])
    with open(out_path, 'wb') as f:
        compress(args.input, tree2dict(tree)).tofile(f)
    print("Compression finished with expected length: {}".format(expected_length(tree, create_queue(count, total))))
    print("Entropy per symbol: {}".format(symbol_entropy(create_queue(count, total))))
