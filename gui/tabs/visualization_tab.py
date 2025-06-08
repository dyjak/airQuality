"""
Moduł zawierający klasę zakładki wizualizacji.
ZAKTUALIZOWANY - używa prostych funkcji z utils zamiast obiektów.
"""
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
                             QComboBox, QPushButton, QSpinBox, QSplitter, QMessageBox,
                             QFileDialog)
from PyQt5.QtCore import Qt

from ..matplotlib_canvas import MatplotlibCanvas, NavigationToolbar


class VisualizationTab(QWidget):
    """Zakładka wizualizacji."""

    def __init__(self, status_bar):
        """
        Inicjalizacja zakładki wizualizacji.

        Args:
            status_bar (QStatusBar): Pasek stanu głównego okna.
        """
        super(VisualizationTab, self).__init__()
        self.status_bar = status_bar
        self.current_data = None

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
            "Mapa korelacji"
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
        self.bins_spin.setValue(20)

        self.plot_params_layout.addWidget(self.column_combo_label)
        self.plot_params_layout.addWidget(self.column_combo)
        self.plot_params_layout.addWidget(self.bins_label)
        self.plot_params_layout.addWidget(self.bins_spin)

        # Dodatkowe kontrolki
        self.x_column_label = QLabel("Kolumna X:")
        self.x_column_combo = QComboBox()

        self.y_column_label = QLabel("Kolumna Y:")
        self.y_column_combo = QComboBox()

        # Ukrywamy dodatkowe kontrolki
        self.x_column_label.hide()
        self.x_column_combo.hide()
        self.y_column_label.hide()
        self.y_column_combo.hide()

        self.plot_params_layout.addWidget(self.x_column_label)
        self.plot_params_layout.addWidget(self.x_column_combo)
        self.plot_params_layout.addWidget(self.y_column_label)
        self.plot_params_layout.addWidget(self.y_column_combo)

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

    def update_data(self, data):
        """
        Aktualizacja danych po wczytaniu nowego zbioru.

        Args:
            data (pandas.DataFrame): Nowe dane do wizualizacji.
        """
        self.current_data = data
        if data is not None:
            columns = list(data.columns)
            self.update_columns(columns)
            print(f"VisualizationTab: zaktualizowano dane ({len(data)} wierszy, {len(columns)} kolumn)")

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
            self.x_column_label.setText("Kolumna daty/czasu:")
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
        elif plot_type == "Mapa korelacji":
            # Mapa korelacji nie potrzebuje dodatkowych parametrów
            pass

    def generate_plot(self):
        """Generowanie wykresu na podstawie wybranych parametrów."""
        if self.current_data is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do wizualizacji."
            )
            return

        try:
            # Pobranie typu wykresu
            plot_type = self.plot_type_combo.currentText()

            # Import funkcji wizualizacji z utils
            from utils.visualization import (create_histogram, create_boxplot,
                                            create_scatter_plot, create_bar_chart,
                                            create_pie_chart, create_line_plot,
                                            create_correlation_heatmap)

            # Wyczyszczenie płótna
            self.plot_canvas.fig.clear()
            fig = None

            # Generowanie wykresu w zależności od typu
            if plot_type == "Histogram":
                column = self.column_combo.currentText()
                bins = self.bins_spin.value()

                if not column:
                    QMessageBox.warning(self, "Błąd", "Nie wybrano kolumny.")
                    return

                fig = create_histogram(
                    self.current_data, column, bins=bins,
                    title=f"Histogram - {column}"
                )

            elif plot_type == "Wykres pudełkowy":
                column = self.column_combo.currentText()

                if not column:
                    QMessageBox.warning(self, "Błąd", "Nie wybrano kolumny.")
                    return

                fig = create_boxplot(
                    self.current_data, column,
                    title=f"Wykres pudełkowy - {column}"
                )

            elif plot_type == "Wykres punktowy":
                x_column = self.x_column_combo.currentText()
                y_column = self.y_column_combo.currentText()

                if not x_column or not y_column:
                    QMessageBox.warning(self, "Błąd", "Nie wybrano kolumn X i Y.")
                    return

                fig = create_scatter_plot(
                    self.current_data, x_column, y_column,
                    title=f"Wykres punktowy - {x_column} vs {y_column}"
                )

            elif plot_type == "Szereg czasowy":
                x_column = self.x_column_combo.currentText()
                y_column = self.y_column_combo.currentText()

                if not x_column or not y_column:
                    QMessageBox.warning(self, "Błąd", "Nie wybrano kolumn.")
                    return

                fig = create_line_plot(
                    self.current_data, x_column, y_column,
                    title=f"Szereg czasowy - {y_column}"
                )

            elif plot_type == "Wykres słupkowy":
                x_column = self.x_column_combo.currentText()
                y_column = self.y_column_combo.currentText() if self.y_column_combo.currentText() else None

                if not x_column:
                    QMessageBox.warning(self, "Błąd", "Nie wybrano kolumny kategorii.")
                    return

                fig = create_bar_chart(
                    self.current_data, x_column, y_column,
                    title=f"Wykres słupkowy - {x_column}"
                )

            elif plot_type == "Wykres kołowy":
                column = self.column_combo.currentText()

                if not column:
                    QMessageBox.warning(self, "Błąd", "Nie wybrano kolumny.")
                    return

                fig = create_pie_chart(
                    self.current_data, column,
                    title=f"Wykres kołowy - {column}"
                )

            elif plot_type == "Mapa korelacji":
                fig = create_correlation_heatmap(
                    self.current_data,
                    title="Mapa korelacji"
                )

            else:
                QMessageBox.warning(
                    self, "Błąd", "Nieznany typ wykresu."
                )
                return

            # Wyświetlenie wykresu
            if fig:
                # Kopiowanie wykresu do canvas
                self._copy_figure_to_canvas(fig)
                self.status_bar.showMessage(f"Wygenerowano wykres: {plot_type}")
                print(f"Wygenerowano wykres: {plot_type}")
            else:
                QMessageBox.warning(
                    self, "Błąd", "Nie udało się wygenerować wykresu. Sprawdź dane i wybrane kolumny."
                )

        except Exception as error:
            print(f"Błąd przy generowaniu wykresu: {error}")
            QMessageBox.critical(
                self, "Błąd krytyczny", f"Wystąpił błąd: {str(error)}"
            )

    def _copy_figure_to_canvas(self, source_fig):
        """
        Kopiuje wykres z funkcji wizualizacji do canvas GUI.

        Args:
            source_fig: Figura matplotlib do skopiowania.
        """
        try:
            if source_fig is None:
                return

            # Prościej - po prostu zastąp figurę
            self.plot_canvas.fig.clear()

            # Skopiuj wszystkie axes z oryginalnej figury
            for i, ax in enumerate(source_fig.axes):
                new_ax = self.plot_canvas.fig.add_subplot(len(source_fig.axes), 1, i + 1)

                # Skopiuj linie
                for line in ax.lines:
                    new_ax.plot(line.get_xdata(), line.get_ydata(),
                                color=line.get_color(), linewidth=line.get_linewidth(),
                                linestyle=line.get_linestyle(), marker=line.get_marker(),
                                label=line.get_label())

                # Skopiuj scatter plots
                for collection in ax.collections:
                    if hasattr(collection, 'get_offsets') and len(collection.get_offsets()) > 0:
                        offsets = collection.get_offsets()
                        colors = collection.get_facecolors()
                        sizes = collection.get_sizes()
                        new_ax.scatter(offsets[:, 0], offsets[:, 1], c=colors, s=sizes)

                # Skopiuj histogramy i bar charts
                for patch in ax.patches:
                    if hasattr(patch, 'get_x') and hasattr(patch, 'get_width'):
                        new_ax.add_patch(type(patch)(
                            (patch.get_x(), patch.get_y()),
                            patch.get_width(),
                            patch.get_height(),
                            facecolor=patch.get_facecolor(),
                            edgecolor=patch.get_edgecolor()
                        ))

                # Skopiuj etykiety
                new_ax.set_title(ax.get_title())
                new_ax.set_xlabel(ax.get_xlabel())
                new_ax.set_ylabel(ax.get_ylabel())
                new_ax.set_xlim(ax.get_xlim())
                new_ax.set_ylim(ax.get_ylim())

                if ax.legend_:
                    new_ax.legend()

                if ax.get_xgridlines() or ax.get_ygridlines():
                    new_ax.grid(True)

            self.plot_canvas.fig.tight_layout()
            self.plot_canvas.draw()

        except Exception as error:
            print(f"Błąd przy kopiowaniu wykresu: {error}")
            # Fallback - bezpośrednie zastąpienie
            self.plot_canvas.fig = source_fig
            self.plot_canvas.draw()

    def save_plot(self):
        """Zapisywanie wykresu do pliku."""
        if not hasattr(self.plot_canvas, 'fig') or self.plot_canvas.fig is None:
            QMessageBox.warning(
                self, "Błąd", "Brak wykresu do zapisania."
            )
            return

        try:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(
                self, "Zapisz wykres", "",
                "Obraz PNG (*.png);;Obraz JPG (*.jpg);;Obraz SVG (*.svg);;Dokument PDF (*.pdf)"
            )

            if file_path:
                # Import funkcji zapisywania z utils
                from utils.visualization import save_plot

                success = save_plot(self.plot_canvas.fig, file_path, dpi=300)

                if success:
                    self.status_bar.showMessage(f"Zapisano wykres do pliku {os.path.basename(file_path)}")
                else:
                    QMessageBox.warning(
                        self, "Błąd", "Nie udało się zapisać wykresu."
                    )

        except Exception as error:
            print(f"Błąd przy zapisywaniu wykresu: {error}")
            QMessageBox.critical(
                self, "Błąd krytyczny", f"Wystąpił błąd: {str(error)}"
            )