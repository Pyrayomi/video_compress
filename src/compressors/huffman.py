from collections import Counter
from heapq import heapify, heappop, heappush

from src.compressors.compressor import Compressor
from src.utils import bits_to_bytes, bytes_to_bits


class Huffman(Compressor):

    def __init__(self, data):
        super().__init__(data)
        self.tree = self.huffman_tree()
        self._padding_size = None

    # Função para criar a árvore de Huffman
    def huffman_tree(self):
        frequencies = Counter(self.data)
        heap = [[weight, [symbol, ""]] for symbol, weight in
                frequencies.items()]
        heapify(heap)
        while len(heap) > 1:
            lo = heappop(heap)
            hi = heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        return {symbol: code for symbol, code in heap[0][1:]}

    def _compress(self):
        self._compressed_data, self._padding_size = bits_to_bytes(''.join(self.tree[byte] for byte in self.data))
        return

    def _decompress(self):
        reverse_tree = {v: k for k, v in self.tree.items()}
        current_code = ""
        decoded_bytes = bytearray()
        for bit in bytes_to_bits(self._compressed_data, self._padding_size):
            current_code += bit
            if current_code in reverse_tree:
                decoded_bytes.append(reverse_tree[current_code])
                current_code = ""
        return bytes(decoded_bytes)
