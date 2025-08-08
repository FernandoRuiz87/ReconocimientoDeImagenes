from PIL import Image, ImageTk
import ttkbootstrap as ttk
import cv2


class VideoPanel(ttk.Frame):
    """Panel para mostrar el video procesado.
    Args:
        parent: Ventana principal donde se incrustará este panel.
        width: Ancho del panel.
        height: Alto del panel.
        video_processor: Instancia de VideoProcessor para manejar la lógica de video.
        *args, **kwargs: Argumentos adicionales para ttk.Frame.
    """

    def __init__(self, parent, width, height, video_processor, *args, **kwargs):
        super().__init__(parent, width=width, height=height, *args, **kwargs)
        self.pack_propagate(False)
        self.video_processor = video_processor  # Inyección de dependencia
        self.is_playing = False

        # Widgets
        self.video_label = ttk.Label(self)
        self.video_label.pack(expand=True, fill="both", padx=10, pady=10)

    def toggle_play(self):
        """Alterna reproducción/pausa"""
        self.is_playing = not self.is_playing
        if self.is_playing:
            self._update_frame()
        return self.is_playing

    def _update_frame(self):
        if self.is_playing and self.video_processor.cap:
            frame = self.video_processor.process_frame()
            if frame is not None:
                self._display_frame(frame)
                self.after(30, self._update_frame)
            else:
                self.video_processor.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self._update_frame()

    def _display_frame(self, frame):
        """Muestra el frame en el Label"""
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)

        # Redimensionamiento manteniendo aspect ratio
        panel_width = self.winfo_width() - 20
        panel_height = self.winfo_height() - 20
        img.thumbnail((panel_width, panel_height), Image.LANCZOS)

        img_tk = ImageTk.PhotoImage(image=img)
        self.video_label.config(image=img_tk)
        self.video_label.image = img_tk

    def load_video(self, video_path):
        """Puente para cargar video desde el panel"""
        self.video_processor.load_video(video_path)

    def set_threshold(self, value):
        """Actualiza el threshold de detección en el video processor."""
        self.video_processor.threshold = value

    def set_min_area(self, value):
        """Actualiza el área mínima de detección en el video processor."""
        self.video_processor.min_area = value
