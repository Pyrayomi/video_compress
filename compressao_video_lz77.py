import cv2
import numpy as np
import sys, time
import pickle  # Para serialização


# Função de compressão usando LZ77
def lz77_compress(data, window_size=1000):
    """Comprime os dados usando o algoritmo LZ77."""
    compressed_data = []
    i = 0

    while i < len(data):
        match_length = 0
        match_distance = 0
        current_window = max(0, i - window_size)

        # Encontra a maior correspondência na janela
        for j in range(current_window, i):
            length = 0
            while (i + length < len(data)) and (data[i + length] == data[j + length]):
                length += 1
                if j + length == i:  # Evita sobreposição na mesma posição
                    break

            if length > match_length:
                match_length = length
                match_distance = i - j

        # Se uma correspondência for encontrada, adiciona uma referência a ela
        if match_length > 0 and (i + match_length < len(data)):
            next_char = data[i + match_length]
            compressed_data.append((match_distance, match_length, next_char))
            i += match_length + 1
        else:
            # Caso contrário, adiciona o byte atual como um literal
            compressed_data.append((0, 0, data[i]))
            i += 1

    return compressed_data


def lz77_decompress(compressed_data):
    """Descomprime os dados comprimidos usando o algoritmo LZ77."""
    decompressed_data = bytearray()

    for distance, length, next_char in compressed_data:
        start = len(decompressed_data) - distance
        decompressed_data.extend(decompressed_data[start:start + length])
        decompressed_data.append(next_char)

    return bytes(decompressed_data)



def calculate_transmission_time(data_size, bandwidth_mbps):
    data_size_bits = data_size * 8  # Conversão de bytes para bits
    bandwidth_bps = bandwidth_mbps * 1e6  # Conversão de Mbps para bps
    transmission_time = data_size_bits / bandwidth_bps  # Tempo em segundos
    return transmission_time

# Inicialização da captura de vídeo
cap = cv2.VideoCapture(1)

# Define a resolução desejada
desired_width = 1280
desired_height = 720

# Define a largura e altura do frame
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertendo o frame para escala de cinza e para bytes
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_bytes = gray_frame.tobytes()

    # Compressão com LZ77
    compressed_frame = lz77_compress(frame_bytes)

    # Calculando o tamanho dos dados comprimidos usando serialização
    serialized_compressed = pickle.dumps(compressed_frame)
    size_compressed = sys.getsizeof(serialized_compressed)

    # Descompressão
    decompressed_data = lz77_decompress(compressed_frame)

    # Calcula os tamanhos e os tempos de transmissão
    size_original = len(frame_bytes)
    transmission_time_original = calculate_transmission_time(size_original, 10)
    transmission_time_compressed = calculate_transmission_time(size_compressed, 10)

    print(f"Tamanho Original: {size_original} bytes, Tempo de Transmissão: {transmission_time_original:.6f} s")
    print(f"Tamanho Comprimido: {size_compressed} bytes, Tempo de Transmissão: {transmission_time_compressed:.6f} s")

    # Exibindo o frame descomprimido
    decompressed_frame = np.frombuffer(decompressed_data, dtype=np.uint8).reshape(gray_frame.shape)
    cv2.imshow('Frame', decompressed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()