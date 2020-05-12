from bitstring import BitArray
import argparse

from utils.analysis import expected_length, symbol_entropy
from utils.storeTree import load_obj
from utils.tools import get_characters_count, create_queue, huffman, tree2dict

parser = argparse.ArgumentParser(description="Decompresses a file using the Huffman algorithm")
parser.add_argument("-o", "--output", help="Sets output path")
parser.add_argument("input", type=str, help="huff compressed file path with corresponding .pkl file with the same name")

args = parser.parse_args()

out_path = args.output if args.output else "output.txt"


def get_bit_sequence(input_path: str) -> str:
    result: str = ""
    with open(input_path, 'rb') as f:
        for byte in f.read():
            result += bin(byte)[2:].zfill(8)
    return result


def consume(sequence: str, dictionary: dict) -> tuple:
    acc: str = ""
    for i, bit in enumerate(sequence):
        acc += bit
        for translation, compression in dictionary.items():
            if acc == compression:
                return translation, sequence[i + 1:]
    return "", ""
    # raise EOFError("No decompression found")


def decompress(input_path: str, dictionary: dict):
    file: str = get_bit_sequence(input_path)
    padding: int = int(file[:8], 2)
    file = file[8:-padding] if padding != 0 else file[8:]
    result: str = ""
    while len(file) > 0:
        character, new_file = consume(file, dictionary)
        result += character
        file = new_file
    return result


if __name__ == "__main__":
    input_dict: dict = load_obj(args.input.split(".")[0])
    with open(out_path, "w", newline='') as f:
        f.write(decompress(args.input, input_dict))
