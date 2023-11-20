def bits_to_bytes(bits):
    # Certifique-se de que o tamanho dos bits seja múltiplo de 8
    padding_size = 8 - (len(bits) % 8)
    bits_padded = bits + '0' * padding_size
    return int(bits_padded, 2).to_bytes(len(bits_padded) // 8,
                                        byteorder='big'), padding_size


def bytes_to_bits(bytes_data, padding_size):
    bits = ''.join(f'{byte:08b}' for byte in bytes_data)
    return bits[:-padding_size]  # Remova o preenchimento


def calculate_transmission_time(data_size, bandwidth_mbps):
    """Calcula o tempo de transmissão com base no tamanho dos dados e na largura de banda."""
    data_size_bits = data_size * 8  # Conversão de bytes para bits
    bandwidth_bps = bandwidth_mbps * 1e6  # Conversão de Mbps para bps
    transmission_time = data_size_bits / bandwidth_bps  # Tempo em segundos
    return transmission_time
