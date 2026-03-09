# Пиковое отношение сигнала к шуму (англ. peak signal-to-noise ratio)
# обозначается аббревиатурой PSNR и является инженерным термином,
# означающим соотношение между максимумом возможного значения сигнала и
# мощностью шума, искажающего значения сигнала.

from math import log10, sqrt
import cv2
import numpy as np


def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if (mse == 0):  # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr


original = cv2.imread("./2_result/MildG2 (1).bmp")
compressed1 = cv2.imread("./2_result/MildG2 (1)_bit1.bmp", 1)
compressed2 = cv2.imread("./2_result/MildG2 (1)_bit2.bmp", 1)
compressed3 = cv2.imread("./2_result/MildG2 (1)_bit3.bmp", 1)

value1 = PSNR(original, compressed1)
value2 = PSNR(original, compressed2)
value3 = PSNR(original, compressed3)

print(f"PSNR value 1_bit is {value1} dB")
print(f"PSNR value 2_bit is {value2} dB")
print(f"PSNR value 3_bit is {value3} dB")

