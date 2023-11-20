from abc import ABC, abstractmethod


class Compressor(ABC):

    def __init__(self, data):
        self.data = data
        self._compressed_data = None

    def compress(self, *args, **kwargs):
        if self._compressed_data is None:
            self._compress(*args, **kwargs)
        return self._compressed_data

    def decompress(self, *args, **kwargs):
        if self._compressed_data is None:
            raise NotImplementedError("Método 'compress' "
                                      "deve ser chamado primeiro.")
        return self._decompress(*args, **kwargs)

    @abstractmethod
    def _compress(self, *args, **kwargs):
        pass

    @abstractmethod
    def _decompress(self, *args, **kwargs):
        pass
