# 3) Извлечение сообщения из заданной битовой плоскости.
# Текстовое сообщение должно быть восстановлено без ошибок.
# Из предыдущего шага мы должны знать путь до изображения со встроенным текстом, номер бита, в который
# происходило встраивание и количество встроенных бит

from PIL import Image
from pathlib import Path

def main():
    bit_number = int(input("Введите номер бита для извлечения (1-8): "))
    if not 1 <= bit_number <= 8:
        print("Ошибка: номер бита должен быть от 1 до 8")
        return

    image_path = input("Введите путь к изображению: ")
    try:
        image = Image.open(image_path).convert('L')
    except FileNotFoundError:
        print("Файл изображения не найден.")
        return

    choice = input("Введите количество бит для извлечения (или 'all' для всех пикселей): ")
    if choice.lower() == 'all':
        bits_to_extract = image.width * image.height
    else:
        bits_to_extract = int(choice)

    total_pixels = image.width * image.height
    if bits_to_extract > total_pixels:
        print(f"Предупреждение: запрошено {bits_to_extract} бит, но в изображении только {total_pixels} пикселей. Будет извлечено {total_pixels} бит.")
        bits_to_extract = total_pixels

    pixels = image.load()
    extracted_bits = []

    for y in range(image.height):
        for x in range(image.width):
            if len(extracted_bits) >= bits_to_extract:
                break
            pixel = pixels[x, y]
            # Извлекаем бит через строку (как при встраивании)
            binary = format(pixel, '08b')
            bit = binary[8 - bit_number]   # для bit_number=1 это старший бит
            extracted_bits.append(bit)
        if len(extracted_bits) >= bits_to_extract:
            break

    bit_string = ''.join(extracted_bits)

    # Отбрасываем неполный последний байт (если нужно)
    if len(bit_string) % 8 != 0:
        print("Внимание: количество извлеченных бит не кратно 8. Неполный последний байт будет отброшен.")
        bit_string = bit_string[:len(bit_string) - len(bit_string) % 8]

    # Преобразуем биты в байты
    bytes_data = bytearray()
    for i in range(0, len(bit_string), 8):
        byte = bit_string[i:i+8]
        bytes_data.append(int(byte, 2))

    # Сохраняем результат
    output_path = Path(image_path).parent / "extracted_message.txt"
    with open(output_path, 'wb') as f:
        f.write(bytes_data)

    print(f"Извлеченное сообщение сохранено в {output_path}")
    print(f"Извлечено бит: {len(extracted_bits)} (из них сохранено байт: {len(bytes_data)})")


if __name__ == "__main__":
    main()