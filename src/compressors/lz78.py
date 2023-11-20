from compressor import Compressor


class LZ78(Compressor):

    def __init__(self, data):
        super().__init__(data)

    def _compress(self, window_size=1000):
        """Comprime os dados usando o algoritmo LZ78."""
        dictionary = {b"": 0}
        dict_size = 1
        w = b""
        compressed_data = []

        for c in [self.data[i:i + 1] for i in range(len(self.data))]:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                compressed_data.append((dictionary[w], c))
                dictionary[wc] = dict_size
                dict_size += 1
                w = b""

        if w:
            compressed_data.append((dictionary[w], b''))

        self._compressed_data = compressed_data
        return

    def _decompress(self):
        dictionary = {0: b""}
        result = b""
        dict_size = 1

        for entry, next_symbol in self._compressed_data:
            string = dictionary[entry] + next_symbol
            result += string
            dictionary[dict_size] = string
            dict_size += 1

        return result
