# SSIM (Structural Similarity Index Measure) —
# это метрика полного сопоставления, оценивающая
# визуальное качество изображений, имитируя
# человеческое восприятие (HVS)

from skimage.metrics import structural_similarity as ssim
import cv2


def compare_ssim(imageA, imageB):
    # Ensure the images have the same size
    assert imageA.shape == imageB.shape, "Images must be the same size."

    # Compute SSIM between two images
    score, diff = ssim(imageA, imageB, full=True)
    return score


# Load images
original = cv2.imread('./2_result/2.bmp', cv2.IMREAD_GRAYSCALE)
compressed1 = cv2.imread('./2_result/2_bit1.bmp', cv2.IMREAD_GRAYSCALE)
compressed2 = cv2.imread('./2_result/2_bit2.bmp', cv2.IMREAD_GRAYSCALE)
compressed3 = cv2.imread('./2_result/2_bit3.bmp', cv2.IMREAD_GRAYSCALE)

# Compute SSIM
ssim_score1 = compare_ssim(original, compressed1)
ssim_score2 = compare_ssim(original, compressed2)
ssim_score3 = compare_ssim(original, compressed3)

print(f"SSIM 1_bit: {ssim_score1}")
print(f"SSIM 2_bit: {ssim_score2}")
print(f"SSIM 3_bit: {ssim_score3}")
