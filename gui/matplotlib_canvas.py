"""
Moduł zawierający klasę do osadzania wykresów Matplotlib w interfejsie PyQt5.
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QSizePolicy


class MatplotlibCanvas(FigureCanvas):
    """Klasa do osadzania wykresów Matplotlib w interfejsie PyQt5."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """
        Inicjalizacja płótna Matplotlib.

        Args:
            parent (QWidget, optional): Widget nadrzędny. Domyślnie None.
            width (int, optional): Szerokość w calach. Domyślnie 5.
            height (int, optional): Wysokość w calach. Domyślnie 4.
            dpi (int, optional): Rozdzielczość. Domyślnie 100.
        """
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super(MatplotlibCanvas, self).__init__(self.fig)
        self.setParent(parent)

        # Ustawienie rozmiaru płótna
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()