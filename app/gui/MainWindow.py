import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
import ttkbootstrap as ttk
from app.gui.VideoProcesor import VideoProcessor
from app.gui.VideoPanel import VideoPanel
from app.gui.ControlPanel import ControlPanel


class MainWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Detección de Movimiento - UNAM")
        self.geometry("1200x700")
        self.minsize(800, 500)  # Tamaño mínimo responsive

        # Configuración de grid responsive
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Inicializar el procesador de video (lógica)
        self.video_processor = VideoProcessor()

        # 2. Crear paneles
        self.control_panel = ControlPanel(
            parent=self,
            video_panel=None,  # Se actualizará después
            width=300,
            height=700,
        )

        self.video_panel = VideoPanel(
            parent=self, video_processor=self.video_processor, width=900, height=700
        )

        # Actualizar referencia cruzada
        self.control_panel.video_panel = self.video_panel

        # 3. Posicionamiento en grid
        self.control_panel.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)
        self.video_panel.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)

        # Manejo de cierre
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        """Liberar recursos al cerrar la ventana"""
        self.video_processor.release()
        self.destroy()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
