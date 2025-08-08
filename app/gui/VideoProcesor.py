import cv2
import numpy as np


class VideoProcessor:
    """Clase para manejar la lógica de procesamiento de video.
    Esta clase se encarga de cargar el video, procesar cada frame y detectar movimiento.
    Attributes:
            cap: Captura de video (cv2.VideoCapture).   
            threshold: Umbral para detección de movimiento.
            min_area: Área mínima para considerar un contorno como movimiento.
            prev_frame: Frame previo para comparación en detección de movimiento.
            *args, **kwargs: Argumentos adicionales.
    """
    def __init__(self):
        self.cap = None
        self.threshold = 25
        self.min_area = 500
        self.prev_frame = None

    def load_video(self, video_path):
        """Carga el video y reinicia el estado"""
        if self.cap:
            self.cap.release()
        self.cap = cv2.VideoCapture(video_path)
        self.prev_frame = None

    def process_frame(self):
        """Procesa un frame y devuelve el resultado con detecciones"""
        ret, frame = self.cap.read()
        if not ret:
            return None

        # Lógica de detección de movimiento
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.prev_frame is None:
            self.prev_frame = blurred
            return frame

        delta = cv2.absdiff(self.prev_frame, blurred)
        thresh = cv2.threshold(delta, self.threshold, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        for contour in contours:
            if cv2.contourArea(contour) > self.min_area:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        self.prev_frame = blurred
        return frame

    def release(self):
        """Libera recursos"""
        if self.cap:
            self.cap.release()
