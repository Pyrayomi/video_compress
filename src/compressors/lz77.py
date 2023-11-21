from src.compressors.compressor import Compressor


class LZ77(Compressor):

    def __init__(self, data):
        super().__init__(data)

    def _compress(self, window_size=20):
        """Comprime os dados usando o algoritmo LZ77."""
        compressed_data = []
        i = 0

        while i < len(self.data):
            match_length = 0
            match_distance = 0
            current_window = max(0, i - window_size)

            # Encontra a maior correspondência na janela
            for j in range(current_window, i):
                length = 0
                while (i + length < len(self.data)) and (
                        self.data[i + length] == self.data[j + length]):
                    length += 1
                    if j + length == i:  # Evita sobreposição na mesma posição
                        break

                if length > match_length:
                    match_length = length
                    match_distance = i - j

            # Se uma correspondência for encontrada, adiciona uma
            # referência a ela
            if match_length > 0 and (i + match_length < len(self.data)):
                next_char = self.data[i + match_length]
                compressed_data.append(
                    (match_distance, match_length, next_char))
                i += match_length + 1
            else:
                # Caso contrário, adiciona o byte atual como um literal
                compressed_data.append((0, 0, self.data[i]))
                i += 1

        self._compressed_data = compressed_data
        return

    def _decompress(self):
        decompressed_data = bytearray()

        for distance, length, next_char in self._compressed_data:
            start = len(decompressed_data) - distance
            decompressed_data.extend(decompressed_data[start:start + length])
            decompressed_data.append(next_char)

        return bytes(decompressed_data)
