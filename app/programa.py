import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# Funcion para dibujar el circulo de la matriz
def dibujar_circulo(matriz, centro, radio):
    for i in range(matriz.shape[0]):
        for j in range(matriz.shape[1]):
            if (i - centro) ** 2 + (j - centro) ** 2 < radio ** 2:
                matriz[i, j] = 255
    return matriz

# Funcion para obtener los contornos de una imagen y dibujarlos
def obtener_contornos(matriz):
    # Obtener los contornos
    _, thresh = cv.threshold(matriz, 127, 255, 0)
    contornos, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Convertir a BGR para dibujar en color
    matriz_color = cv.cvtColor(matriz, cv.COLOR_GRAY2BGR)
    resultado = cv.drawContours(matriz_color, contornos, -1, (0, 255, 0), 2)

    return resultado

# Crear matriz de 255x255
matriz = np.zeros((255, 255), dtype=np.uint8)

# Asegurar que el círculo quepa
centro = np.random.randint(15, 240)
print(f'Centro: {centro}')

# Dibujar el círculo en la matriz y obtener los contornos
matriz = dibujar_circulo(matriz, centro, 15)
im2 = obtener_contornos(matriz)

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
