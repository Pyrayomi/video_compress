from src.compressors.huffman import Huffman
from src.compressors.lz77 import LZ77
from src.compressors.lz78 import LZ78
from src.streaming import execute_streaming

if __name__ == '__main__':
    execute_streaming(Huffman)
    execute_streaming(LZ77, serialization=True)
    execute_streaming(LZ78, serialization=True)
