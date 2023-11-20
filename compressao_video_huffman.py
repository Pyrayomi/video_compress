import cv2
import numpy as np
from heapq import heapify, heappush, heappop
from collections import Counter
import sys

# Função para criar a árvore de Huffman
def huffman_tree(frequencies):
    heap = [[weight, [symbol, ""]] for symbol, weight in frequencies.items()]
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

# Função para codificar usando Huffman
def huffman_encoding(data, tree):
    return ''.join(tree[byte] for byte in data)

# Função para decodificar usando Huffman
def huffman_decoding(encoded_data, tree):
    reverse_tree = {v: k for k, v in tree.items()}
    current_code = ""
    decoded_bytes = bytearray()
    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_tree:
            decoded_bytes.append(reverse_tree[current_code])
            current_code = ""
    return bytes(decoded_bytes)


def bits_to_bytes(bits):
    # Certifique-se de que o tamanho dos bits seja múltiplo de 8
    padding_size = 8 - (len(bits) % 8)
    bits_padded = bits + '0' * padding_size
    return int(bits_padded, 2).to_bytes(len(bits_padded) // 8, byteorder='big'), padding_size

def bytes_to_bits(bytes_data, padding_size):
    bits = ''.join(f'{byte:08b}' for byte in bytes_data)
    return bits[:-padding_size]  # Remova o preenchimento

def calculate_transmission_time(data_size, bandwidth_mbps):
    """Calcula o tempo de transmissão com base no tamanho dos dados e na largura de banda."""
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

    # Processamento dos frames
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    byte_frame = gray_frame.tobytes()
    frequencies = Counter(byte_frame)
    tree = huffman_tree(frequencies)
    encoded_bits = huffman_encoding(byte_frame, tree)
    encoded_bytes = bits_to_bytes(encoded_bits)  # Conversão para bytes

    # Calculando tamanhos e tempos de transmissão
    size_original = len(byte_frame)
    size_compressed = len(encoded_bytes[0])
    transmission_time_original = calculate_transmission_time(size_original, 10)
    transmission_time_compressed = calculate_transmission_time(size_compressed, 10)

    print(f"Tamanho Original: {size_original} bytes, Tempo de Transmissão: {transmission_time_original:.6f} s")
    print(f"Tamanho Comprimido: {size_compressed} bytes, Tempo de Transmissão: {transmission_time_compressed:.6f} s")

    # Descompressão e exibição do frame
    encoded_bytes, padding_size = bits_to_bytes(encoded_bits)  # Note a adição da padding_size
    decoded_bits = bytes_to_bits(encoded_bytes, padding_size)
    decoded_frame = huffman_decoding(decoded_bits, tree)
    decoded_frame = np.frombuffer(decoded_frame, dtype=np.uint8).reshape(gray_frame.shape)
    cv2.imshow('Frame', decoded_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()