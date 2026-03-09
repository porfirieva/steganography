import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

histogram_name = 'histogram_1'
original = Image.open('./2_result/1.bmp').convert('L')
stego_k1 = Image.open('./2_result/1_bit1.bmp').convert('L')
stego_k2 = Image.open('./2_result/1_bit2.bmp').convert('L')
stego_k3 = Image.open('./2_result/1_bit3.bmp').convert('L')

# histogram_name = 'histogram_2'
# original = Image.open('./2_result/2.bmp').convert('L')
# stego_k1 = Image.open('./2_result/2_bit1.bmp').convert('L')
# stego_k2 = Image.open('./2_result/2_bit2.bmp').convert('L')
# stego_k3 = Image.open('./2_result/2_bit3.bmp').convert('L')

# histogram_name = 'histogram_3'
# original = Image.open('./2_result/MildG2 (1).bmp').convert('L')
# stego_k1 = Image.open('./2_result/MildG2 (1)_bit1.bmp').convert('L')
# stego_k2 = Image.open('./2_result/MildG2 (1)_bit2.bmp').convert('L')
# stego_k3 = Image.open('./2_result/MildG2 (1)_bit3.bmp').convert('L')

# Преобразуем в массивы
orig_arr = np.array(original).flatten()
stego1_arr = np.array(stego_k1).flatten()
stego2_arr = np.array(stego_k2).flatten()
stego3_arr = np.array(stego_k3).flatten()

# Строим гистограммы в порядке: оригинал, k=3, k=2, k=1
plt.figure(figsize=(15, 10))

# Верхний ряд: оригинал и k=3
plt.subplot(2, 2, 1)
plt.hist(orig_arr, bins=256, range=(0,255), color='blue', alpha=0.7)
plt.title('Оригинал')
plt.xlabel('Яркость')
plt.ylabel('Частота')
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 2)
plt.hist(stego3_arr, bins=256, range=(0,255), color='orange', alpha=0.7)
plt.title('Бит 3')
plt.xlabel('Яркость')
plt.ylabel('Частота')
plt.grid(True, alpha=0.3)

# Нижний ряд: k=2 и k=1
plt.subplot(2, 2, 3)
plt.hist(stego2_arr, bins=256, range=(0,255), color='green', alpha=0.7)
plt.title('Бит 2')
plt.xlabel('Яркость')
plt.ylabel('Частота')
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 4)
plt.hist(stego1_arr, bins=256, range=(0,255), color='red', alpha=0.7)
plt.title('Бит 1 (LSB)')
plt.xlabel('Яркость')
plt.ylabel('Частота')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{histogram_name}.png', dpi=150)
plt.show()