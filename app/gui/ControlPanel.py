import ttkbootstrap as ttk
import cv2
import os
from PIL import Image, ImageTk
from tkinter import filedialog


class ControlPanel(ttk.Frame):
    def __init__(self, parent, video_panel, width, height, *args, **kwargs):
        """Panel de control para la aplicación de detección de movimiento.
        Args:
            parent: Ventana principal donde se incrustará este panel.
            video_panel: Referencia al panel de video para interactuar con él.
            width: Ancho del panel.
            height: Alto del panel.
            *args, **kwargs: Argumentos adicionales para ttk.Frame.
        """
        super().__init__(parent, *args, **kwargs)
        self.configure(width=width, height=height, bootstyle="dark")
        self.pack_propagate(False)
        self.video_panel = video_panel  # Referencia al panel derecho

        # Widgets
        self._create_widgets()

    def _create_widgets(self):
        # Título
        ttk.Label(
            self,
            text="Controles de Video",
            font=("Segoe UI", 14),
            bootstyle="inverse-dark",
        ).pack(pady=20)

        # Botón para cargar video
        ttk.Button(
            self,
            text="📁 Cargar Video",
            command=self._load_video,
            bootstyle="primary",
            width=20,
        ).pack(pady=10)

        # Botón de play/pause
        self.play_btn = ttk.Button(
            self,
            text="▶️ Reproducir",
            command=self._toggle_play,
            bootstyle="success",
            width=20,
            state="disabled",
        )
        self.play_btn.pack(pady=10)

        # TODO : Implementar función de detener
        # Botón de detener
        self.stop_btn = ttk.Button(
            self,
            text="⏹️ Detener",
            bootstyle="danger",
            width=20,
            state="disabled",
        )
        self.stop_btn.pack(pady=10)

        # Ajustes de detección
        control_frame = ttk.Labelframe(
            self, text="Configuración de Detección", padding=10, bootstyle="dark"
        )
        control_frame.pack(pady=10, padx=5, fill="x")

        # Slider de Umbral
        ttk.Label(control_frame, text="Sensibilidad:").pack(anchor="w")
        self.threshold_slider = ttk.Scale(
            control_frame,
            from_=0,
            to=255,
            value=25,
            command=lambda v: self.video_panel.set_threshold(int(float(v))),
        )
        self.threshold_slider.pack(fill="x", pady=5)

        # Slider de Área Mínima
        ttk.Label(control_frame, text="Área Mínima:").pack(anchor="w")
        self.area_slider = ttk.Scale(
            control_frame,
            from_=100,
            to=5000,
            value=500,
            command=lambda v: self.video_panel.set_min_area(int(float(v))),
        )
        self.area_slider.pack(fill="x", pady=5)

    def _load_video(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Video Files", "*.mp4 *.avi *.mov")]
        )
        if file_path:
            self.video_panel.load_video(file_path)
            self.play_btn.config(state="normal")
            self.stop_btn.config(state="normal")

    def _toggle_play(self):
        if self.video_panel.toggle_play():
            self.play_btn.config(text="⏸️ Pausar")
        else:
            self.play_btn.config(text="▶️ Reproducir")
