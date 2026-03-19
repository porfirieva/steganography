from pathlib import Path
from PIL import Image
import second_part


def process_all_sets():
    sets = ['Set1', 'Set2', 'Set3']
    bits = [1, 2, 3]

    for set_name in sets:
        print(f"\nОбработка {set_name}...")

        # Папка с оригинальными изображениями
        input_folder = Path(f"./{set_name}")
        # Папка для результатов
        output_folder = Path(f"./2_result_all/{set_name}")
        output_folder.mkdir(parents=True, exist_ok=True)

        # Получаем все изображения
        images = list(input_folder.glob("*.bmp"))

        for img_path in images:
            print(f"  {img_path.name}")

            for bit in bits:
                second_part.main(img_path, bit, output_folder)

    print("\nГотово! Все изображения обработаны.")


if __name__ == "__main__":
    process_all_sets()