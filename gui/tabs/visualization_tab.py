"""
Moduł zawierający klasę zakładki wizualizacji.
"""
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
                             QComboBox, QPushButton, QSpinBox, QSplitter, QMessageBox,
                             QFileDialog)
from PyQt5.QtCore import Qt

from ..matplotlib_canvas import MatplotlibCanvas, NavigationToolbar


class VisualizationTab(QWidget):
    """Zakładka wizualizacji."""

    def __init__(self, data_visualizer, status_bar):
        """
        Inicjalizacja zakładki wizualizacji.

        Args:
            data_visualizer (DataVisualizer): Obiekt wizualizujący dane.
            status_bar (QStatusBar): Pasek stanu głównego okna.
        """
        super(VisualizationTab, self).__init__()

        self.data_visualizer = data_visualizer
        self.status_bar = status_bar

        # Inicjalizacja interfejsu
        self.init_ui()

    def init_ui(self):
        """Inicjalizacja interfejsu zakładki."""
        layout = QHBoxLayout(self)

        # Panel sterowania
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)

        # Typ wykresu
        plot_type_group = QGroupBox("Typ wykresu")
        plot_type_layout = QVBoxLayout()

        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems([
            "Histogram",
            "Wykres pudełkowy",
            "Wykres punktowy",
            "Szereg czasowy",
            "Wykres słupkowy",
            "Wykres kołowy",
            "Mapa ciepła",
            "Wykres par"
        ])
        self.plot_type_combo.currentIndexChanged.connect(self.update_visualization_controls)

        plot_type_layout.addWidget(QLabel("Wybierz typ wykresu:"))
        plot_type_layout.addWidget(self.plot_type_combo)

        plot_type_group.setLayout(plot_type_layout)
        control_layout.addWidget(plot_type_group)

        # Parametry wykresu
        self.plot_params_group = QGroupBox("Parametry wykresu")
        self.plot_params_layout = QVBoxLayout()

        # Domyślne kontrolki dla histogramu
        self.column_combo_label = QLabel("Wybierz kolumnę:")
        self.column_combo = QComboBox()

        self.bins_label = QLabel("Liczba przedziałów:")
        self.bins_spin = QSpinBox()
        self.bins_spin.setRange(2, 100)
        self.bins_spin.setValue(10)

        self.plot_params_layout.addWidget(self.column_combo_label)
        self.plot_params_layout.addWidget(self.column_combo)
        self.plot_params_layout.addWidget(self.bins_label)
        self.plot_params_layout.addWidget(self.bins_spin)

        # Dodatkowe kontrolki, które będą pokazywane/ukrywane
        self.x_column_label = QLabel("Kolumna X:")
        self.x_column_combo = QComboBox()

        self.y_column_label = QLabel("Kolumna Y:")
        self.y_column_combo = QComboBox()

        self.z_column_label = QLabel("Kolumna Z:")
        self.z_column_combo = QComboBox()

        self.hue_column_label = QLabel("Kolumna do kolorowania:")
        self.hue_column_combo = QComboBox()
        self.hue_column_combo.addItem("Brak")

        # Ukrywamy dodatkowe kontrolki
        self.x_column_label.hide()
        self.x_column_combo.hide()
        self.y_column_label.hide()
        self.y_column_combo.hide()
        self.z_column_label.hide()
        self.z_column_combo.hide()
        self.hue_column_label.hide()
        self.hue_column_combo.hide()

        self.plot_params_layout.addWidget(self.x_column_label)
        self.plot_params_layout.addWidget(self.x_column_combo)
        self.plot_params_layout.addWidget(self.y_column_label)
        self.plot_params_layout.addWidget(self.y_column_combo)
        self.plot_params_layout.addWidget(self.z_column_label)
        self.plot_params_layout.addWidget(self.z_column_combo)
        self.plot_params_layout.addWidget(self.hue_column_label)
        self.plot_params_layout.addWidget(self.hue_column_combo)

        self.plot_params_group.setLayout(self.plot_params_layout)
        control_layout.addWidget(self.plot_params_group)

        # Przycisk do generowania wykresu
        generate_button = QPushButton("Generuj wykres")
        generate_button.clicked.connect(self.generate_plot)
        control_layout.addWidget(generate_button)

        # Przycisk do zapisywania wykresu
        save_plot_button = QPushButton("Zapisz wykres")
        save_plot_button.clicked.connect(self.save_plot)
        control_layout.addWidget(save_plot_button)

        # Dodanie elastycznego odstępu
        control_layout.addStretch()

        # Panel wykresu
        plot_panel = QWidget()
        plot_layout = QVBoxLayout(plot_panel)

        self.plot_canvas = MatplotlibCanvas(self, width=8, height=6)
        self.plot_toolbar = NavigationToolbar(self.plot_canvas, self)

        plot_layout.addWidget(self.plot_toolbar)
        plot_layout.addWidget(self.plot_canvas)

        # Splitter do dzielenia paneli
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(control_panel)
        splitter.addWidget(plot_panel)
        splitter.setSizes([300, 700])

        layout.addWidget(splitter)

    def update_columns(self, columns):
        """
        Aktualizacja list kolumn.

        Args:
            columns (list): Lista nazw kolumn.
        """
        self.column_combo.clear()
        self.column_combo.addItems(columns)

        self.x_column_combo.clear()
        self.x_column_combo.addItems(columns)

        self.y_column_combo.clear()
        self.y_column_combo.addItems(columns)

        self.z_column_combo.clear()
        self.z_column_combo.addItems(columns)

        self.hue_column_combo.clear()
        self.hue_column_combo.addItem("Brak")
        self.hue_column_combo.addItems(columns)

    def update_visualization_controls(self):
        """Aktualizacja kontrolek wizualizacji w zależności od wybranego typu wykresu."""
        plot_type = self.plot_type_combo.currentText()

        # Ukrycie wszystkich kontrolek
        self.column_combo_label.hide()
        self.column_combo.hide()
        self.bins_label.hide()
        self.bins_spin.hide()
        self.x_column_label.hide()
        self.x_column_combo.hide()
        self.y_column_label.hide()
        self.y_column_combo.hide()
        self.z_column_label.hide()
        self.z_column_combo.hide()
        self.hue_column_label.hide()
        self.hue_column_combo.hide()

        # Pokazanie odpowiednich kontrolek w zależności od typu wykresu
        if plot_type == "Histogram":
            self.column_combo_label.show()
            self.column_combo.show()
            self.bins_label.show()
            self.bins_spin.show()
        elif plot_type == "Wykres pudełkowy":
            self.column_combo_label.show()
            self.column_combo.show()
        elif plot_type == "Wykres punktowy":
            self.x_column_label.show()
            self.x_column_combo.show()
            self.y_column_label.show()
            self.y_column_combo.show()
        elif plot_type == "Szereg czasowy":
            self.x_column_label.setText("Kolumna daty:")
            self.x_column_label.show()
            self.x_column_combo.show()
            self.y_column_label.setText("Kolumna wartości:")
            self.y_column_label.show()
            self.y_column_combo.show()
        elif plot_type == "Wykres słupkowy":
            self.x_column_label.setText("Kolumna kategorii:")
            self.x_column_label.show()
            self.x_column_combo.show()
            self.y_column_label.setText("Kolumna wartości (opcjonalnie):")
            self.y_column_label.show()
            self.y_column_combo.show()
        elif plot_type == "Wykres kołowy":
            self.column_combo_label.show()
            self.column_combo.show()
        elif plot_type == "Mapa ciepła":
            self.x_column_label.show()
            self.x_column_combo.show()
            self.y_column_label.show()
            self.y_column_combo.show()
            self.z_column_label.show()
            self.z_column_combo.show()
        elif plot_type == "Wykres par":
            self.hue_column_label.show()
            self.hue_column_combo.show()

    def generate_plot(self):
        """Generowanie wykresu na podstawie wybranych parametrów."""
        if self.data_visualizer.data is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do wizualizacji."
            )
            return

        # Pobranie typu wykresu
        plot_type = self.plot_type_combo.currentText()

        # Wyczyszczenie płótna
        self.plot_canvas.fig.clear()

        # Generowanie wykresu w zależności od typu
        if plot_type == "Histogram":
            column = self.column_combo.currentText()
            bins = self.bins_spin.value()

            fig = self.data_visualizer.create_histogram(
                column, bins=bins, title=f"Histogram dla {column}"
            )
        elif plot_type == "Wykres pudełkowy":
            column = self.column_combo.currentText()

            fig = self.data_visualizer.create_boxplot(
                column, title=f"Wykres pudełkowy dla {column}"
            )
        elif plot_type == "Wykres punktowy":
            x_column = self.x_column_combo.currentText()
            y_column = self.y_column_combo.currentText()

            fig = self.data_visualizer.create_scatter_plot(
                x_column, y_column, title=f"Wykres punktowy: {x_column} vs {y_column}"
            )
        elif plot_type == "Szereg czasowy":
            date_column = self.x_column_combo.currentText()
            value_column = self.y_column_combo.currentText()

            fig = self.data_visualizer.create_time_series_plot(
                date_column, value_column, title=f"Szereg czasowy: {value_column}"
            )
        elif plot_type == "Wykres słupkowy":
            x_column = self.x_column_combo.currentText()
            y_column = self.y_column_combo.currentText() if self.y_column_combo.currentIndex() > 0 else None

            fig = self.data_visualizer.create_bar_chart(
                x_column, y_column, title=f"Wykres słupkowy dla {x_column}"
            )
        elif plot_type == "Wykres kołowy":
            column = self.column_combo.currentText()

            fig = self.data_visualizer.create_pie_chart(
                column, title=f"Wykres kołowy dla {column}"
            )
        elif plot_type == "Mapa ciepła":
            x_column = self.x_column_combo.currentText()
            y_column = self.y_column_combo.currentText()
            z_column = self.z_column_combo.currentText()

            fig = self.data_visualizer.create_heatmap(
                x_column, y_column, z_column,
                title=f"Mapa ciepła: {z_column} według {x_column} i {y_column}"
            )
        elif plot_type == "Wykres par":
            hue_column = self.hue_column_combo.currentText() if self.hue_column_combo.currentIndex() > 0 else None

            fig = self.data_visualizer.create_pair_plot(
                hue=hue_column, title="Wykres par"
            )
        else:
            QMessageBox.warning(
                self, "Błąd", "Nieznany typ wykresu."
            )
            return

        if fig:
            # Kopiowanie wykresu z data_visualizer do canvas
            self.plot_canvas.fig = fig
            self.plot_canvas.draw()

            self.status_bar.showMessage(f"Wygenerowano wykres: {plot_type}")
        else:
            QMessageBox.warning(
                self, "Błąd", "Nie udało się wygenerować wykresu."
            )

    def save_plot(self):
        """Zapisywanie wykresu do pliku."""
        if not hasattr(self.plot_canvas, 'fig') or self.plot_canvas.fig is None:
            QMessageBox.warning(
                self, "Błąd", "Brak wykresu do zapisania."
            )
            return

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "Zapisz wykres", "", "Obraz PNG (*.png);;Obraz JPG (*.jpg);;Obraz SVG (*.svg);;Dokument PDF (*.pdf)"
        )

        if file_path:
            # Pobranie rozszerzenia pliku
            extension = os.path.splitext(file_path)[1].lower()

            if extension == '.png':
                format = 'png'
            elif extension == '.jpg' or extension == '.jpeg':
                format = 'jpg'
            elif extension == '.svg':
                format = 'svg'
            elif extension == '.pdf':
                format = 'pdf'
            else:
                format = 'png'
                file_path += '.png'

            # Zapisywanie wykresu
            success = self.data_visualizer.save_figure(self.plot_canvas.fig, file_path, dpi=300)

            if success:
                self.status_bar.showMessage(f"Zapisano wykres do pliku {os.path.basename(file_path)}")
            else:
                QMessageBox.warning(
                    self, "Błąd", "Nie udało się zapisać wykresu."
                )