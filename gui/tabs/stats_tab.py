"""
Moduł zawierający klasę zakładki analizy statystycznej.
"""
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel,
                             QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QSplitter, QMessageBox)
from PyQt5.QtCore import Qt


class StatsTab(QWidget):
    """Zakładka analizy statystycznej."""

    def __init__(self, data_processor, status_bar):
        """
        Inicjalizacja zakładki analizy statystycznej.

        Args:
            data_processor (DataProcessor): Obiekt przetwarzający dane.
            status_bar (QStatusBar): Pasek stanu głównego okna.
        """
        super(StatsTab, self).__init__()

        self.data_processor = data_processor
        self.status_bar = status_bar

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

        layout.addWidget(splitter)

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
        if self.data_processor.get_data() is None:
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

        # Obliczenie statystyk
        stats = self.data_processor.calculate_statistics(column)

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
            self.stats_table.setItem(i, 1, QTableWidgetItem(str(value)))

        # Dopasowanie szerokości kolumn
        self.stats_table.resizeColumnsToContents()

        self.status_bar.showMessage(f"Obliczono statystyki dla kolumny {column}")