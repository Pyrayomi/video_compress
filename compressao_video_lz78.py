import cv2
import numpy as np
import sys, time
import pickle  # Para serialização
# Função de compressão usando LZ78
def lz78_compress(data):
    dictionary = {b"": 0}
    dict_size = 1
    w = b""
    compressed_data = []

    for c in [data[i:i+1] for i in range(len(data))]:
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

    return compressed_data

# Função de descompressão usando LZ78
def lz78_decompress(compressed_data):
    dictionary = {0: b""}
    result = b""
    dict_size = 1

    for entry, next_symbol in compressed_data:
        string = dictionary[entry] + next_symbol
        result += string
        dictionary[dict_size] = string
        dict_size += 1

    return result

def calculate_transmission_time(data_size, bandwidth_mbps):
    data_size_bits = data_size * 8  # Conversão de bytes para bits
    bandwidth_bps = bandwidth_mbps * 1e6  # Conversão de Mbps para bps
    transmission_time = data_size_bits / bandwidth_bps  # Tempo em segundos
    return transmission_time

# Inicialização da captura de vídeo
cap = cv2.VideoCapture(1)

# Define a resolução desejada
desired_width = 128
desired_height = 128

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

    # Compressão com LZ78
    compressed_frame = lz78_compress(frame_bytes)

    # Serialização para calcular o tamanho exato em bytes
    serialized_compressed = pickle.dumps(compressed_frame)
    size_compressed = sys.getsizeof(serialized_compressed)

    # Descompressão
    decompressed_data = lz78_decompress(compressed_frame)

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