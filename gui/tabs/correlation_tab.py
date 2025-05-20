"""
Moduł zawierający klasę zakładki korelacji.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
                             QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from ..matplotlib_canvas import MatplotlibCanvas, NavigationToolbar


class CorrelationTab(QWidget):
    """Zakładka korelacji."""

    def __init__(self, data_processor, data_visualizer, status_bar):
        """
        Inicjalizacja zakładki korelacji.

        Args:
            data_processor (DataProcessor): Obiekt przetwarzający dane.
            data_visualizer (DataVisualizer): Obiekt wizualizujący dane.
            status_bar (QStatusBar): Pasek stanu głównego okna.
        """
        super(CorrelationTab, self).__init__()

        self.data_processor = data_processor
        self.data_visualizer = data_visualizer
        self.status_bar = status_bar

        # Inicjalizacja interfejsu
        self.init_ui()

    def init_ui(self):
        """Inicjalizacja interfejsu zakładki."""
        layout = QVBoxLayout(self)

        # Wybór metody korelacji
        method_group = QGroupBox("Metoda korelacji")
        method_layout = QHBoxLayout()

        self.correlation_method_combo = QComboBox()
        self.correlation_method_combo.addItems(["pearson", "kendall", "spearman"])
        method_layout.addWidget(QLabel("Metoda:"))
        method_layout.addWidget(self.correlation_method_combo)

        calculate_button = QPushButton("Oblicz korelacje")
        calculate_button.clicked.connect(self.calculate_correlation)
        method_layout.addWidget(calculate_button)

        method_layout.addStretch()

        method_group.setLayout(method_layout)
        layout.addWidget(method_group)

        # Widok macierzy korelacji
        correlation_group = QGroupBox("Macierz korelacji")
        correlation_layout = QVBoxLayout()

        self.correlation_table = QTableWidget()
        correlation_layout.addWidget(self.correlation_table)

        correlation_group.setLayout(correlation_layout)
        layout.addWidget(correlation_group)

        # Wykres macierzy korelacji
        heatmap_group = QGroupBox("Mapa ciepła korelacji")
        heatmap_layout = QVBoxLayout()

        self.correlation_canvas = MatplotlibCanvas(self, width=10, height=8)
        self.correlation_toolbar = NavigationToolbar(self.correlation_canvas, self)

        heatmap_layout.addWidget(self.correlation_toolbar)
        heatmap_layout.addWidget(self.correlation_canvas)

        heatmap_group.setLayout(heatmap_layout)
        layout.addWidget(heatmap_group)

    def update_data(self):
        """Aktualizacja danych po wczytaniu nowego zbioru."""
        # Czyścimy tabelę i wykres
        self.correlation_table.setRowCount(0)
        self.correlation_table.setColumnCount(0)
        self.correlation_canvas.fig.clear()
        self.correlation_canvas.draw()

    def calculate_correlation(self):
        """Obliczanie macierzy korelacji."""
        if self.data_processor.get_data() is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do analizy."
            )
            return

        # Pobranie metody korelacji
        method = self.correlation_method_combo.currentText()

        # Obliczenie macierzy korelacji
        corr_matrix = self.data_processor.calculate_correlation(method=method)

        if corr_matrix is None:
            QMessageBox.warning(
                self, "Błąd", "Nie udało się obliczyć macierzy korelacji."
            )
            return

        # Aktualizacja tabeli korelacji
        self.correlation_table.setRowCount(len(corr_matrix.index))
        self.correlation_table.setColumnCount(len(corr_matrix.columns))
        self.correlation_table.setHorizontalHeaderLabels(list(corr_matrix.columns))
        self.correlation_table.setVerticalHeaderLabels(list(corr_matrix.index))

        for i in range(len(corr_matrix.index)):
            for j in range(len(corr_matrix.columns)):
                value = corr_matrix.iloc[i, j]
                item = QTableWidgetItem(f"{value:.2f}")

                # Kolorowanie komórek w zależności od wartości korelacji
                if i != j:  # Pomijamy przekątną (zawsze 1.0)
                    if abs(value) > 0.7:
                        item.setBackground(QColor(255, 0, 0, 100))  # Czerwony (silna korelacja)
                    elif abs(value) > 0.5:
                        item.setBackground(QColor(255, 165, 0, 100))  # Pomarańczowy (umiarkowana korelacja)
                    elif abs(value) > 0.3:
                        item.setBackground(QColor(255, 255, 0, 100))  # Żółty (słaba korelacja)

                self.correlation_table.setItem(i, j, item)

        # Dopasowanie szerokości kolumn
        self.correlation_table.resizeColumnsToContents()

        # Utworzenie wykresu mapy ciepła
        self.correlation_canvas.fig.clear()

        # Utworzenie mapy ciepła korelacji
        fig = self.data_visualizer.create_correlation_heatmap(
            title=f"Macierz korelacji ({method})",
            annot=True,
            fmt='.2f'
        )

        if fig:
            # Kopiowanie wykresu z data_visualizer do canvas
            self.correlation_canvas.fig = fig
            self.correlation_canvas.draw()

        self.status_bar.showMessage(f"Obliczono macierz korelacji ({method})")