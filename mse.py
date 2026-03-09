# MSE измеряет среднее различие в квадрате между
# фактическими и идеальными пиксельными значениями

import cv2
import numpy as np


def mse(imageA, imageB):
    # Ensure the images have the same size
    assert imageA.shape == imageB.shape, "Images must be the same size."

    # Calculate the MSE between the images
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err


original = cv2.imread('./2_result/MildG2 (1).bmp', cv2.IMREAD_GRAYSCALE)
compressed1 = cv2.imread('./2_result/MildG2 (1)_bit1.bmp', cv2.IMREAD_GRAYSCALE)
compressed2 = cv2.imread('./2_result/MildG2 (1)_bit2.bmp', cv2.IMREAD_GRAYSCALE)
compressed3 = cv2.imread('./2_result/MildG2 (1)_bit3.bmp', cv2.IMREAD_GRAYSCALE)

# Compute MSE
error1 = mse(original, compressed1)
error2 = mse(original, compressed2)
error3 = mse(original, compressed3)

print(f"Mean Squared Error: {error1}")
print(f"Mean Squared Error: {error2}")
print(f"Mean Squared Error: {error3}")
