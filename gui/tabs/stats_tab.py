"""
Moduł zawierający klasę zakładki analizy statystycznej.
ZAKTUALIZOWANY - używa prostych funkcji z utils zamiast obiektów.
"""
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel,
                             QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QSplitter, QMessageBox)
from PyQt5.QtCore import Qt


class StatsTab(QWidget):
    """Zakładka analizy statystycznej."""

    def __init__(self, status_bar):
        """
        Inicjalizacja zakładki analizy statystycznej.

        Args:
            status_bar (QStatusBar): Pasek stanu głównego okna.
        """
        super(StatsTab, self).__init__()
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

        # Wybór kolumny
        column_group = QGroupBox("Wybór kolumny")
        column_layout = QVBoxLayout()

        self.stats_column_combo = QComboBox()
        column_layout.addWidget(self.stats_column_combo)

        calculate_button = QPushButton("Oblicz statystyki")
        calculate_button.clicked.connect(self.calculate_statistics)
        column_layout.addWidget(calculate_button)

        column_group.setLayout(column_layout)
        control_layout.addWidget(column_group)

        # Dodanie elastycznego odstępu
        control_layout.addStretch()

        # Panel wyników
        results_panel = QWidget()
        results_layout = QVBoxLayout(results_panel)

        # Tabela statystyk
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setHorizontalHeaderLabels(["Statystyka", "Wartość"])
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        results_layout.addWidget(self.stats_table)

        # Splitter do dzielenia paneli
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(control_panel)
        splitter.addWidget(results_panel)
        splitter.setSizes([200, 800])

        # Przycisk do zapisywania statystyk
        save_stats_button = QPushButton("Zapisz statystyki do CSV")
        save_stats_button.clicked.connect(self.save_statistics)
        control_layout.addWidget(save_stats_button)

        layout.addWidget(splitter)

    def update_data(self, data):
        """
        Aktualizacja danych po wczytaniu nowego zbioru.

        Args:
            data (pandas.DataFrame): Nowe dane do analizy.
        """
        self.current_data = data
        if data is not None:
            columns = list(data.columns)
            self.update_columns(columns)
            print(f"StatsTab: zaktualizowano dane ({len(data)} wierszy, {len(columns)} kolumn)")

    def update_columns(self, columns):
        """
        Aktualizacja listy kolumn.

        Args:
            columns (list): Lista nazw kolumn.
        """
        self.stats_column_combo.clear()
        self.stats_column_combo.addItems(columns)

    def calculate_statistics(self):
        """Obliczanie statystyk dla wybranej kolumny."""
        if self.current_data is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do analizy."
            )
            return

        # Pobranie wybranej kolumny
        column = self.stats_column_combo.currentText()

        if not column:
            QMessageBox.warning(
                self, "Błąd", "Nie wybrano kolumny."
            )
            return

        try:
            # Import i użycie prostej funkcji z utils
            from utils.data_processor import calculate_basic_statistics
            stats = calculate_basic_statistics(self.current_data, column)

            if not stats:
                QMessageBox.warning(
                    self, "Błąd", "Nie udało się obliczyć statystyk dla wybranej kolumny."
                )
                return

            # Aktualizacja tabeli statystyk
            self.stats_table.setRowCount(len(stats))
            self.stats_table.setColumnCount(2)
            self.stats_table.setHorizontalHeaderLabels(["Statystyka", "Wartość"])

            for i, (stat, value) in enumerate(stats.items()):
                self.stats_table.setItem(i, 0, QTableWidgetItem(stat))

                # Formatowanie wartości w zależności od typu
                if isinstance(value, float):
                    formatted_value = f"{value:.4f}"
                else:
                    formatted_value = str(value)

                self.stats_table.setItem(i, 1, QTableWidgetItem(formatted_value))

            # Dopasowanie szerokości kolumn
            self.stats_table.resizeColumnsToContents()

            self.status_bar.showMessage(f"Obliczono statystyki dla kolumny {column}")
            print(f"Obliczono statystyki dla kolumny: {column}")

        except Exception as error:
            print(f"Błąd przy obliczaniu statystyk: {error}")
            QMessageBox.critical(
                self, "Błąd krytyczny", f"Wystąpił błąd: {str(error)}"
            )

    def save_statistics(self):
        """Zapisuje statystyki do pliku CSV."""
        if self.stats_table.rowCount() == 0:
            QMessageBox.warning(self, "Błąd", "Brak statystyk do zapisania.")
            return

        from PyQt5.QtWidgets import QFileDialog
        import pandas as pd

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Zapisz statystyki", "", "Pliki CSV (*.csv)"
        )

        if file_path:
            # Pobierz dane z tabeli
            data = []
            for i in range(self.stats_table.rowCount()):
                row = []
                for j in range(self.stats_table.columnCount()):
                    item = self.stats_table.item(i, j)
                    row.append(item.text() if item else "")
                data.append(row)

            # Stwórz DataFrame i zapisz
            df = pd.DataFrame(data, columns=["Statystyka", "Wartość"])
            df.to_csv(file_path, index=False)
            self.status_bar.showMessage(f"Zapisano statystyki do {file_path}")