import pickle
import sys

import cv2
import numpy as np

from src.utils import calculate_transmission_time


def execute_streaming(compressor_cls, serialization=False):
    # Inicialização da captura de vídeo
    cap = cv2.VideoCapture(1)

    # Define a resolução desejada
    desired_width = 1280
    desired_height = 720

    # Define a largura e altura do frame
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

    print(f"--------------- EXECUCAO "
          f"{compressor_cls.__name__} ---------------")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Processamento dos frames
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        byte_frame = gray_frame.tobytes()

        compressor = compressor_cls(byte_frame)
        encoded_bytes = compressor.compress()

        # Calculando tamanhos e tempos de transmissão
        size_original = len(byte_frame)

        if serialization:
            # Calculando o tamanho dos dados comprimidos usando serialização
            serialized_compressed = pickle.dumps(encoded_bytes)
            size_compressed = sys.getsizeof(serialized_compressed)
        else:
            size_compressed = len(encoded_bytes)

        transmission_time_original = calculate_transmission_time(size_original,
                                                                 10)
        transmission_time_compressed = calculate_transmission_time(
            size_compressed,
            10)

        print(
            f"Tamanho Original: {size_original} bytes, Tempo de Transmissão: {transmission_time_original:.6f} s")
        print(
            f"Tamanho Comprimido: {size_compressed} bytes, Tempo de Transmissão: {transmission_time_compressed:.6f} s")
        print("\n\n")
        # Descompressão e exibição do frame
        decoded_frame = compressor.decompress()
        decoded_frame = np.frombuffer(decoded_frame, dtype=np.uint8).reshape(
            gray_frame.shape)
        cv2.imshow('Frame', decoded_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
