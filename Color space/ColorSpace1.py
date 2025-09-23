import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('CP1.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def grayscale_weighted1(img):
    # Формула 1: взвешенное среднее
    return 0.299 * img[:,:,0] + 0.587 * img[:,:,1] + 0.114 * img[:,:,2]

def grayscale_weighted2(img):
    # Формула 2: альтернативные веса 
    return 0.2126 * img[:,:,0] + 0.7152 * img[:,:,1] + 0.0722 * img[:,:,2]

gray1 = grayscale_weighted1(image_rgb).astype(np.uint8)
gray2 = grayscale_weighted2(image_rgb).astype(np.uint8)

difference = cv2.subtract(gray1, gray2)

plt.figure(figsize=(15, 10))

plt.subplot(2, 3, 1)
plt.imshow(image_rgb)
plt.title('Исходное RGB')
plt.axis('off')

plt.subplot(2, 3, 2)
plt.imshow(gray1, cmap='gray')
plt.title('Формула 1 (0.299, 0.587, 0.114)')
plt.axis('off')

plt.subplot(2, 3, 3)
plt.imshow(gray2, cmap='gray')
plt.title('Формула 2 (0.2126, 0.7152, 0.0722)')
plt.axis('off')

plt.subplot(2, 3, 4)
plt.imshow(difference, cmap='coolwarm')
plt.title('Разность изображений')
plt.colorbar()
plt.axis('off')

plt.subplot(2, 3, 5)
plt.hist(gray1.ravel(), bins=256, range=[0, 256], alpha=0.7, color='red')
plt.title('Гистограмма Формулы 1')
plt.xlabel('Интенсивность')
plt.ylabel('Частота')

plt.subplot(2, 3, 6)
plt.hist(gray2.ravel(), bins=256, range=[0, 256], alpha=0.7, color='blue')
plt.title('Гистограмма Формулы 2')
plt.xlabel('Интенсивность')
plt.ylabel('Частота')

plt.tight_layout()
plt.show()

print(f"Максимальная разность: {np.max(difference)}")
print(f"Минимальная разность: {np.min(difference)}")
print(f"Средняя разность: {np.mean(difference):.2f}")
