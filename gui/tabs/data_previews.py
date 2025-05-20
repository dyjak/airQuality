"""
Moduł zawierający klasę zakładki podglądu danych.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QTextEdit,
                             QTableWidget, QTableWidgetItem, QHeaderView)


class DataPreviewTab(QWidget):
    """Zakładka podglądu danych."""

    def __init__(self):
        """Inicjalizacja zakładki podglądu danych."""
        super(DataPreviewTab, self).__init__()

        # Inicjalizacja interfejsu
        self.init_ui()

    def init_ui(self):
        """Inicjalizacja interfejsu zakładki."""
        layout = QVBoxLayout(self)

        # Informacje o danych
        info_group = QGroupBox("Informacje o danych")
        info_layout = QVBoxLayout()

        self.data_info_text = QTextEdit()
        self.data_info_text.setReadOnly(True)

        info_layout.addWidget(self.data_info_text)
        info_group.setLayout(info_layout)

        # Tabela z danymi
        table_group = QGroupBox("Podgląd danych")
        table_layout = QVBoxLayout()

        self.data_table = QTableWidget()

        table_layout.addWidget(self.data_table)
        table_group.setLayout(table_layout)

        # Dodanie widgetów do układu
        layout.addWidget(info_group, 1)
        layout.addWidget(table_group, 2)

    def update_data(self, data_loader):
        """
        Aktualizacja wyświetlanych danych.

        Args:
            data_loader (DataLoader): Obiekt wczytujący dane.
        """
        if data_loader.get_data() is None:
            return

        # Aktualizacja informacji o danych
        self._update_data_info(data_loader)

        # Aktualizacja tabeli danych
        self._update_data_table(data_loader)

    def _update_data_info(self, data_loader):
        """
        Aktualizacja informacji o danych.

        Args:
            data_loader (DataLoader): Obiekt wczytujący dane.
        """
        # Pobranie informacji o danych
        info = data_loader.get_data_info()
        shape = data_loader.get_data_shape()

        # Aktualizacja pola tekstowego
        self.data_info_text.clear()
        self.data_info_text.append(f"Liczba wierszy: {shape[0]}")
        self.data_info_text.append(f"Liczba kolumn: {shape[1]}")
        self.data_info_text.append("\nInformacje o danych:")
        self.data_info_text.append(info)

    def _update_data_table(self, data_loader):
        """
        Aktualizacja tabeli danych.

        Args:
            data_loader (DataLoader): Obiekt wczytujący dane.
        """
        # Pobranie danych
        data = data_loader.get_data()

        # Aktualizacja tabeli
        self.data_table.setRowCount(min(100, len(data)))  # Ograniczenie do 100 wierszy dla wydajności
        self.data_table.setColumnCount(len(data.columns))
        self.data_table.setHorizontalHeaderLabels(list(data.columns))

        # Wypełnienie tabeli danymi
        for i in range(min(100, len(data))):
            for j in range(len(data.columns)):
                value = str(data.iloc[i, j])
                self.data_table.setItem(i, j, QTableWidgetItem(value))

        # Dopasowanie szerokości kolumn
        self.data_table.resizeColumnsToContents()