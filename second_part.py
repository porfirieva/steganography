# 2) Внедрение данных в заданную битовую плоскость.
# Пользователь указывает:
# - номер бита k ∈ {1,2,…,8}.
# - сообщение из текстового файла, размером не менее 30Кб.
# Программа замещает k-е биты пикселей исходного
# изображения битами сообщения (по одному биту на пиксель,
# слева направо, сверху вниз) от начала до конца контейнера,
# показывает сколько бит удалось записать. Выходное
# изображение сохраняется как 8-битное серое.

# Результат сохранен в папку ./2_result/<название исходного изображения>_bit<номер бита>

from PIL import Image
from pathlib import Path

bit_number = int(input("Введите номер бита для замены (1-8): "))

if not 1 <= bit_number <= 8:
    print('Задан некорректный номер бита')
    exit()

text_message_path = "./text.txt"
print("Используется путь к файлу с сообщением ./text.txt")

with open(text_message_path, 'rb') as file:
    content = file.read()
    binary_text_array = [bit for byte in content for bit in format(byte, "08b")]

if not binary_text_array:
    print("Файл сообщения пуст.")
    exit()

file = Path('./' + input(f"Введите путь к контейнеру: ./"))
if not file.is_file() or not file.suffix.lower() in ['.bmp', '.png', '.jpg', '.jpeg', '.tiff']:
    exit()

# Открываем изображение и преобразуем в градации серого (8 бит)
image = Image.open(file).convert('L')
pixels = image.load()

total_pixels = image.width * image.height
bits_to_write = min(len(binary_text_array), total_pixels)
written = 0

# Обход пикселей построчно (слева направо, сверху вниз)
for y in range(image.height):
    for x in range(image.width):
        if written >= bits_to_write:
            break
        # Текущее значение пикселя (число от 0 до 255)
        pixel = pixels[x, y]
        # Преобразуем в двоичную строку из 8 бит
        binary_pixel = format(pixel, '08b')
        # Заменяем k-й бит на бит сообщения
        # Преобразуем строку в список для замены символа
        bit_list = list(binary_pixel)
        bit_list[8 - bit_number] = binary_text_array[written]
        # Собираем обратно и преобразуем в число
        new_pixel = int(''.join(bit_list), 2)
        pixels[x, y] = new_pixel
        written += 1
    if written >= bits_to_write:
        break

# Сохраняем результат
output_folder = Path("./2_result")
output_folder.mkdir(parents=True, exist_ok=True)
output_path = output_folder / f"{file.stem}_bit{bit_number}.bmp"
image.save(output_path)

print(f"Сохранено: {output_path}")
print(f"Записано бит: {written} из {len(binary_text_array)}")