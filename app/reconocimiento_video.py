import cv2 as cv
import os

def verificar_ruta_video(ruta_video):
    """Verifica si la ruta del video existe."""
    return ruta_video and os.path.exists(ruta_video)

def inicializar_captura(origen=0):
    """Inicializa el objeto de captura de video."""
    cap = cv.VideoCapture(origen)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir el origen de video '{origen}'")
        return None
    return cap

def obtener_primer_frame(cap):
    """Lee el primer frame del video y lo convierte a escala de grises."""
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el primer frame.")
        return None
    return cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

def procesar_frame(frame):
    """Convierte el frame a escala de grises y aplica desenfoque gaussiano."""
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_blur = cv.GaussianBlur(frame_gray, (21, 21), 0)
    return frame_blur

def detectar_movimiento(frame_anterior, frame_actual, area_minima, umbral):
    """Detecta movimiento entre dos frames."""
    delta = cv.absdiff(frame_anterior, frame_actual)
    _, thresh = cv.threshold(delta, umbral, 255, cv.THRESH_BINARY)
    thresh = cv.dilate(thresh, None, iterations=2)
    contours, _ = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contornos_filtrados = [c for c in contours if cv.contourArea(c) >= area_minima]
    return thresh, contornos_filtrados, delta

def dibujar_contornos(frame, contornos):
    """Dibuja rectángulos alrededor de los contornos detectados."""
    for contour in contornos:
        (x, y, w, h) = cv.boundingRect(contour)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

def main():
    # Parámetros de entrada
    video_path = '../assets/Video.mp4'
    usar_webcam = True  # Cambiar a false para usar un video

    # Verificar la ruta del video si no se usará webcam
    if not usar_webcam and not verificar_ruta_video(video_path):
        print(f"Error: No se encontró el video en la ruta '{video_path}'")
        return

    # Inicializar captura de video
    origen = 0 if usar_webcam else video_path
    cap = inicializar_captura(origen)
    if cap is None:
        return

    # Obtener y procesar el primer frame
    frame1 = obtener_primer_frame(cap)
    if frame1 is None:
        cap.release()
        return
    frame1 = cv.GaussianBlur(frame1, (21, 21), 0)

    # Crear ventana y sliders para ajustar parámetros
    cv.namedWindow('Detección de Movimiento')
    cv.createTrackbar('Umbral', 'Detección de Movimiento', 20, 255, lambda x: None)
    cv.createTrackbar('Área mínima', 'Detección de Movimiento', 500, 5000, lambda x: None)

    while True:
        ret, frame2 = cap.read()
        if not ret:
            print("Fin del video o error al leer el frame.")
            break

        # Obtener valores actuales de los sliders
        umbral = cv.getTrackbarPos('Umbral', 'Detección de Movimiento')
        area_minima = cv.getTrackbarPos('Área mínima', 'Detección de Movimiento')

        # Procesar frame actual
        frame2_proc = procesar_frame(frame2)

        # Detectar movimiento usando valores de los sliders
        thresh, contornos, _ = detectar_movimiento(frame1, frame2_proc, area_minima, umbral)

        # Dibujar los contornos detectados sobre el frame original
        dibujar_contornos(frame2, contornos)

        # Mostrar resultados
        cv.imshow('Frame Original', frame2)
        cv.imshow('Detección de Movimiento', thresh)

        # Salir si se presiona 'q'
        if cv.waitKey(30) & 0xFF == ord('q'):
            break

        # Actualizar el frame anterior
        frame1 = frame2_proc

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
