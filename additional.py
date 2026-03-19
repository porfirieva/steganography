# Дополнительное задание: Статистический анализ PSNR и дисперсии битовых плоскостей
# для трех наборов изображений (Set1, Set2, Set3)

import cv2
import numpy as np
from pathlib import Path
import scipy.stats as stats
import matplotlib.pyplot as plt
from psnr import PSNR

def calculate_bit_plane_variance(image, k):
    """
    Расчет дисперсии значений в k-й битовой плоскости
    k=1 - младший бит, k=8 - старший бит
    """
    bit_position = k - 1
    # Извлекаем k-ю битовую плоскость
    bit_plane = (image >> bit_position) & 1
    # Дисперсия бинарной плоскости
    return np.var(bit_plane)


def compute_confidence_interval(data, confidence=0.95):
    """Расчет доверительного интервала"""
    n = len(data)
    mean = np.mean(data)
    sem = stats.sem(data)  # стандартная ошибка среднего
    margin = sem * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean, margin


def analyze_sets():
    """Анализ всех трех наборов изображений"""
    sets = ['Set1', 'Set2', 'Set3']
    bits_to_analyze = [1, 2, 3]  # k = 1, 2, 3

    # Структуры для хранения результатов
    results_psnr = {f"Set{i}": {bit: [] for bit in bits_to_analyze} for i in range(1, 4)}
    results_variance = {f"Set{i}": {bit: [] for bit in bits_to_analyze} for i in range(1, 4)}

    for set_name in sets:
        print(f"\n--- Анализ {set_name} ---")

        # Путь к оригинальным изображениям
        orig_folder = Path(f"./{set_name}")
        # Путь к изображениям со встроенным сообщением
        result_folder = Path(f"./2_result_all/{set_name}")

        # Получаем список оригинальных файлов
        orig_files = list(orig_folder.glob("*.bmp"))

        for orig_file in orig_files:
            # Загружаем оригинал
            original = cv2.imread(str(orig_file), cv2.IMREAD_GRAYSCALE)
            if original is None:
                continue

            # Анализируем для каждого бита
            for bit in bits_to_analyze:
                # Путь к файлу со встроенным сообщением
                compressed_file = result_folder / f"{orig_file.stem}_bit{bit}.bmp"

                if compressed_file.exists():
                    compressed = cv2.imread(str(compressed_file), cv2.IMREAD_GRAYSCALE)
                    if compressed is not None:
                        # PSNR
                        psnr_val = PSNR(original, compressed)
                        results_psnr[set_name][bit].append(psnr_val)

                        # Дисперсия битовой плоскости
                        var_val = calculate_bit_plane_variance(original, bit)
                        results_variance[set_name][bit].append(var_val)

            print(f"  Обработан: {orig_file.name}")

    return results_psnr, results_variance


def print_results_table(results_psnr, results_variance):
    """Вывод результатов в виде таблицы"""

    bits = [1, 2, 3]
    sets = ['Set1', 'Set2', 'Set3']
    confidence = 0.95

    print("\n" + "=" * 80)
    print("РЕЗУЛЬТАТЫ СТАТИСТИЧЕСКОГО АНАЛИЗА")
    print("=" * 80)

    # Таблица для PSNR
    print("\n--- PSNR (dB) с доверительными интервалами (α=0.05) ---")
    print("-" * 70)
    print(f"{'Набор':<10} {'Бит':<8} {'Среднее':<12} {'ДИ нижн.':<12} {'ДИ верхн.':<12} {'Кол-во':<8}")
    print("-" * 70)

    for set_name in sets:
        for bit in bits:
            data = results_psnr[set_name][bit]
            if data:
                mean, margin = compute_confidence_interval(data, confidence)
                print(
                    f"{set_name:<10} {bit:<8} {mean:<12.2f} {mean - margin:<12.2f} {mean + margin:<12.2f} {len(data):<8}")

    # Таблица для дисперсии
    print("\n--- Дисперсия значений в битовых плоскостях с доверительными интервалами ---")
    print("-" * 70)
    print(f"{'Набор':<10} {'Бит':<8} {'Среднее':<12} {'ДИ нижн.':<12} {'ДИ верхн.':<12} {'Кол-во':<8}")
    print("-" * 70)

    for set_name in sets:
        for bit in bits:
            data = results_variance[set_name][bit]
            if data:
                mean, margin = compute_confidence_interval(data, confidence)
                print(
                    f"{set_name:<10} {bit:<8} {mean:<12.4f} {mean - margin:<12.4f} {mean + margin:<12.4f} {len(data):<8}")


def plot_confidence_intervals(results_psnr, results_variance):
    """Визуализация доверительных интервалов"""
    bits = [1, 2, 3]
    sets = ['Set1', 'Set2', 'Set3']
    colors = ['blue', 'green', 'red']

    # График для PSNR
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    x_pos = np.arange(len(bits))
    width = 0.25

    for i, set_name in enumerate(sets):
        means = []
        errors = []
        for bit in bits:
            data = results_psnr[set_name][bit]
            if data:
                mean, margin = compute_confidence_interval(data)
                means.append(mean)
                errors.append(margin)

        plt.bar(x_pos + i * width, means, width, label=set_name,
                color=colors[i], alpha=0.7, yerr=errors, capsize=5)

    plt.xlabel('Номер бита (k)')
    plt.ylabel('PSNR (dB)')
    plt.title('PSNR с доверительными интервалами\n(уровень значимости α=0.05)')
    plt.xticks(x_pos + width, [f'k={b}' for b in bits])
    plt.legend()
    plt.grid(True, alpha=0.3)

    # График для дисперсии
    plt.subplot(1, 2, 2)

    for i, set_name in enumerate(sets):
        means = []
        errors = []
        for bit in bits:
            data = results_variance[set_name][bit]
            if data:
                mean, margin = compute_confidence_interval(data)
                means.append(mean)
                errors.append(margin)

        plt.bar(x_pos + i * width, means, width, label=set_name,
                color=colors[i], alpha=0.7, yerr=errors, capsize=5)

    plt.xlabel('Номер бита (k)')
    plt.ylabel('Дисперсия')
    plt.title('Дисперсия битовых плоскостей\nс доверительными интервалами')
    plt.xticks(x_pos + width, [f'k={b}' for b in bits])
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('./analysis_results/confidence_intervals.png', dpi=150)
    plt.show()


def main():
    # Создаем папку для результатов
    Path('./analysis_results').mkdir(parents=True, exist_ok=True)

    # Анализируем все наборы
    results_psnr, results_variance = analyze_sets()

    # Выводим таблицы
    print_results_table(results_psnr, results_variance)

    # Строим графики
    plot_confidence_intervals(results_psnr, results_variance)



# Выводы: Знание доверительных интервалов, а не только средних значений PSNR,
# дает следующую практическую информацию:
#
# 1. Надежность оценки: ДИ показывает, насколько можно доверять
#    среднему значению. Чем уже интервал, тем надежнее оценка.
#
# 2. Сравнение наборов: Если ДИ двух наборов не пересекаются, можно
#    утверждать, что они статистически значимо различаются.
#
# 3. Выбор контейнера: Для стеганографии предпочтительнее наборы с
#    более высоким PSNR и одновременно узким ДИ - это гарантирует
#    стабильно высокое качество после внедрения.
#
# 4. Дисперсия битовых плоскостей: Показывает, насколько
#    "случайны" младшие биты в разных наборах. Чем выше дисперсия
#    и стабильнее ее значение (узкий ДИ), тем лучше набор подходит
#    для встраивания информации.



if __name__ == "__main__":
    main()