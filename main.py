import sys

from src.compressors.huffman import Huffman
from src.compressors.lz77 import LZ77
from src.compressors.lz78 import LZ78
from src.streaming import execute_streaming

ALGORITHMS = {
    "huffman": (Huffman,),
    "lz77": (LZ77, True),
    "lz78": (LZ78, True)
}

if __name__ == '__main__':
    execute_streaming(*ALGORITHMS[sys.argv[1].lower()])
