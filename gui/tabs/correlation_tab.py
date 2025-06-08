"""
Moduł zawierający klasę zakładki korelacji.
ZAKTUALIZOWANY - używa prostych funkcji z utils zamiast obiektów.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
                             QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from ..matplotlib_canvas import MatplotlibCanvas, NavigationToolbar


class CorrelationTab(QWidget):
    """Zakładka korelacji."""

    def __init__(self, status_bar):
        """
        Inicjalizacja zakładki korelacji.

        Args:
            status_bar (QStatusBar): Pasek stanu głównego okna.
        """
        super(CorrelationTab, self).__init__()
        self.status_bar = status_bar
        self.current_data = None

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

        save_corr_button = QPushButton("Zapisz korelacje do CSV")
        save_corr_button.clicked.connect(self.save_correlation)
        method_layout.addWidget(save_corr_button)

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

    def update_data(self, data):
        """
        Aktualizacja danych po wczytaniu nowego zbioru.

        Args:
            data (pandas.DataFrame): Nowe dane do analizy.
        """
        self.current_data = data

        # Czyścimy tabelę i wykres
        self.correlation_table.setRowCount(0)
        self.correlation_table.setColumnCount(0)
        self.correlation_canvas.fig.clear()
        self.correlation_canvas.draw()

        if data is not None:
            print(f"CorrelationTab: zaktualizowano dane ({len(data)} wierszy, {len(data.columns)} kolumn)")

    def calculate_correlation(self):
        """Obliczanie macierzy korelacji."""
        if self.current_data is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do analizy."
            )
            return

        try:
            # Pobranie metody korelacji
            method = self.correlation_method_combo.currentText()

            # Import i użycie prostej funkcji z utils
            from utils.data_processor import calculate_correlation
            corr_matrix = calculate_correlation(self.current_data, method=method)

            if corr_matrix is None:
                QMessageBox.warning(
                    self, "Błąd", "Nie udało się obliczyć macierzy korelacji."
                )
                return

            # Aktualizacja tabeli korelacji
            self._update_correlation_table(corr_matrix)

            # Utworzenie wykresu mapy ciepła
            self._create_correlation_heatmap(corr_matrix, method)

            self.status_bar.showMessage(f"Obliczono macierz korelacji ({method})")
            print(f"Obliczono macierz korelacji metodą: {method}")

        except Exception as error:
            print(f"Błąd przy obliczaniu korelacji: {error}")
            QMessageBox.critical(
                self, "Błąd krytyczny", f"Wystąpił błąd: {str(error)}"
            )

    def _update_correlation_table(self, corr_matrix):
        """
        Aktualizacja tabeli korelacji.

        Args:
            corr_matrix (pandas.DataFrame): Macierz korelacji.
        """
        self.correlation_table.setRowCount(len(corr_matrix.index))
        self.correlation_table.setColumnCount(len(corr_matrix.columns))
        self.correlation_table.setHorizontalHeaderLabels(list(corr_matrix.columns))
        self.correlation_table.setVerticalHeaderLabels(list(corr_matrix.index))

        for i in range(len(corr_matrix.index)):
            for j in range(len(corr_matrix.columns)):
                value = corr_matrix.iloc[i, j]
                item = QTableWidgetItem(f"{value:.3f}")

                # Kolorowanie komórek w zależności od wartości korelacji
                if i != j:  # Pomijamy przekątną (zawsze 1.0)
                    if abs(value) > 0.7:
                        item.setBackground(QColor(255, 100, 100, 150))  # Czerwony (silna korelacja)
                    elif abs(value) > 0.5:
                        item.setBackground(QColor(255, 165, 0, 150))   # Pomarańczowy (umiarkowana korelacja)
                    elif abs(value) > 0.3:
                        item.setBackground(QColor(255, 255, 100, 150)) # Żółty (słaba korelacja)
                else:
                    # Przekątna - szare tło
                    item.setBackground(QColor(200, 200, 200, 100))

                self.correlation_table.setItem(i, j, item)

        # Dopasowanie szerokości kolumn
        self.correlation_table.resizeColumnsToContents()

    def _create_correlation_heatmap(self, corr_matrix, method):
        """
        Tworzenie wykresu mapy ciepła korelacji.

        Args:
            corr_matrix (pandas.DataFrame): Macierz korelacji.
            method (str): Metoda korelacji.
        """
        try:
            # Import i użycie funkcji wizualizacji z utils
            from utils.visualization import create_correlation_heatmap

            # Utworzenie mapy ciepła
            fig = create_correlation_heatmap(
                self.current_data,
                title=f"Macierz korelacji ({method})"
            )

            if fig:
                # Zastąpienie figury w canvas
                self.correlation_canvas.fig.clear()

                # Skopiowanie osi z utworzonej figury
                original_axes = fig.get_axes()
                if original_axes:
                    # Utworzenie nowej osi w canvas
                    new_ax = self.correlation_canvas.fig.add_subplot(111)

                    # Ponowne utworzenie mapy ciepła bezpośrednio na nowej osi
                    import seaborn as sns
                    sns.heatmap(
                        corr_matrix,
                        annot=True,
                        fmt='.2f',
                        cmap='coolwarm',
                        center=0,
                        square=True,
                        ax=new_ax,
                        cbar_kws={"shrink": 0.8}
                    )

                    new_ax.set_title(f"Macierz korelacji ({method})", fontsize=14, fontweight='bold')

                # Odświeżenie canvas
                self.correlation_canvas.draw()

            else:
                print("Nie udało się utworzyć mapy ciepła")

        except Exception as error:
            print(f"Błąd przy tworzeniu mapy ciepła: {error}")
            # Fallback - prosty wykres bez seaborn
            self._create_simple_heatmap(corr_matrix, method)

    def _create_simple_heatmap(self, corr_matrix, method):
        """
        Tworzenie prostej mapy ciepła bez seaborn (fallback).

        Args:
            corr_matrix (pandas.DataFrame): Macierz korelacji.
            method (str): Metoda korelacji.
        """
        try:
            self.correlation_canvas.fig.clear()
            ax = self.correlation_canvas.fig.add_subplot(111)

            # Prosty heatmap z matplotlib
            im = ax.imshow(corr_matrix.values, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)

            # Etykiety osi
            ax.set_xticks(range(len(corr_matrix.columns)))
            ax.set_yticks(range(len(corr_matrix.index)))
            ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
            ax.set_yticklabels(corr_matrix.index)

            # Dodanie wartości do komórek
            for i in range(len(corr_matrix.index)):
                for j in range(len(corr_matrix.columns)):
                    text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                 ha="center", va="center", color="black", fontsize=8)

            # Tytuł
            ax.set_title(f"Macierz korelacji ({method})", fontsize=14, fontweight='bold')

            # Colorbar
            self.correlation_canvas.fig.colorbar(im, ax=ax, shrink=0.8)

            # Dopasowanie layoutu
            self.correlation_canvas.fig.tight_layout()
            self.correlation_canvas.draw()

        except Exception as error:
            print(f"Błąd przy tworzeniu prostej mapy ciepła: {error}")

    def save_correlation(self):
        """Zapisuje macierz korelacji do pliku CSV."""
        if self.correlation_table.rowCount() == 0:
            QMessageBox.warning(self, "Błąd", "Brak macierzy korelacji do zapisania.")
            return

        from PyQt5.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Zapisz korelacje", "", "Pliki CSV (*.csv)"
        )

        if file_path:
            try:
                from utils.data_processor import calculate_correlation
                method = self.correlation_method_combo.currentText()
                corr_matrix = calculate_correlation(self.current_data, method=method)

                if corr_matrix is not None:
                    corr_matrix.to_csv(file_path)
                    self.status_bar.showMessage(f"Zapisano korelacje do {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Błąd", f"Nie udało się zapisać: {str(e)}")