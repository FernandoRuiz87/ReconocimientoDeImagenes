import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# Crear matriz de 255x255
matriz = np.zeros((255, 255), dtype=np.uint8)

# Asegurar que el círculo quepa
centro = np.random.randint(15, 240)
print(f'Centro: {centro}')

# Dibujar el círculo en la matriz
radio = 15
for i in range(255):
    for j in range(255):
        if (i - centro) ** 2 + (j - centro) ** 2 < radio ** 2:
            matriz[i, j] = 255

# Obtener los contornos
ret, thresh = cv.threshold(matriz, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Convertir a BGR para dibujar en color
matriz_color = cv.cvtColor(matriz, cv.COLOR_GRAY2BGR)
im2 = cv.drawContours(matriz_color, contours, -1, (0, 255, 0), 2)

# Mostrar las imágenes
plt.subplot(1, 2, 1)
plt.imshow(matriz, cmap='gray')
plt.axis('off')
plt.title('Imagen Original')

plt.subplot(1, 2, 2)
plt.imshow(im2)
plt.axis('off')
plt.title('Imagen con Contornos')

plt.show()
