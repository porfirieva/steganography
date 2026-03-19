# 1)Извлечение битовых плоскостей.
# По заданному номеру бита k ∈ {1,2,…,8}, где k=1 — младший бит
# (бит 0), k=8 — старший бит (бит 7), программа формирует чѐрно-
# белое изображение, в котором:
# - пиксель равен 0, если k-й бит соответствующего пикселя
# исходного изображения равен 0,
# - пиксель равен 255, если k-й бит равен 1.
# Таким образом, для каждого значения 𝑘 получается бинарное
# (чѐрно-белое) изображение, отражающее распределение k-го
# бита по всему исходному изображению.

# Для примера работы программы используем пять файлов из набора.

# Результат сохранен в папку ./1_result/<номер сета>/converted_<название исходного изображения>_bit<номер бита>

from PIL import Image
from pathlib import Path

from constants import SET_MESSAGE

def main():
    set_number = input(SET_MESSAGE)
    bit_number = int(input('Задайте номер бита: '))

    if not 0 < bit_number < 9:
        print('Задан некорректный номер бита')
        exit()

    folder_path = Path('./' + 'Set' + set_number)

    output_folder = Path(f"./1_result/Set{set_number}/")
    output_folder.mkdir(parents=True, exist_ok=True)

    for file in folder_path.iterdir():
        image = Image.open(file).copy()
        image_matrix = image.load()
        stem_name = file.stem

        for i in range(image.width):
            for j in range(image.height):
                pixel_value = int(image_matrix[i, j])
                binary_pixel_value = format(pixel_value, '08b')

                if binary_pixel_value[8 - bit_number] == '0':
                    image_matrix[i, j] = 0
                else:
                    image_matrix[i, j] = 255

        output_filename = f"converted_{stem_name}_bit{bit_number}.bmp"
        output_path = output_folder / output_filename
        image.save(output_path, "BMP")

        print(f"Сохранен файл: {output_path}")  # Для отслеживания процесса


if __name__ == "__main__":
    main()