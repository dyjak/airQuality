"""
Moduł zawierający klasę zakładki podglądu danych.
ZAKTUALIZOWANY - przyjmuje dane bezpośrednio zamiast przez data_loader.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QTextEdit,
                             QTableWidget, QTableWidgetItem, QHeaderView)


class DataPreviewTab(QWidget):
    """Zakładka podglądu danych."""

    def __init__(self):
        """Inicjalizacja zakładki podglądu danych."""
        super(DataPreviewTab, self).__init__()
        self.current_data = None

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
        self.data_info_text.setMaximumHeight(200)  # Ograniczenie wysokości

        info_layout.addWidget(self.data_info_text)
        info_group.setLayout(info_layout)

        # Tabela z danymi
        table_group = QGroupBox("Podgląd danych (pierwsze 1000 wierszy)")
        table_layout = QVBoxLayout()

        self.data_table = QTableWidget()

        table_layout.addWidget(self.data_table)
        table_group.setLayout(table_layout)

        # Dodanie widgetów do układu
        layout.addWidget(info_group, 1)
        layout.addWidget(table_group, 2)

    def update_data(self, data):
        """
        Aktualizacja wyświetlanych danych.

        Args:
            data (pandas.DataFrame): Nowe dane do wyświetlenia.
        """
        self.current_data = data

        if data is not None:
            # Aktualizacja informacji o danych
            self._update_data_info()

            # Aktualizacja tabeli danych
            self._update_data_table()

            print(f"DataPreviewTab: zaktualizowano dane ({len(data)} wierszy, {len(data.columns)} kolumn)")
        else:
            # Wyczyszczenie interfejsu
            self.data_info_text.clear()
            self.data_info_text.append("Brak danych do wyświetlenia")
            self.data_table.setRowCount(0)
            self.data_table.setColumnCount(0)

    def _update_data_info(self):
        """Aktualizacja informacji o danych."""
        if self.current_data is None:
            return

        try:
            # Podstawowe informacje
            shape = self.current_data.shape
            info_text = f"Liczba wierszy: {shape[0]}\n"
            info_text += f"Liczba kolumn: {shape[1]}\n\n"

            # Rozmiar w pamięci
            memory_usage = self.current_data.memory_usage(deep=True).sum()
            memory_mb = memory_usage / (1024 * 1024)
            info_text += f"Rozmiar w pamięci: {memory_mb:.2f} MB\n\n"

            # Typy danych
            info_text += "Typy kolumn:\n"
            for col, dtype in self.current_data.dtypes.items():
                info_text += f"  {col}: {dtype}\n"

            # Brakujące wartości
            missing = self.current_data.isnull().sum()
            total_missing = missing.sum()

            if total_missing > 0:
                info_text += f"\nBrakujące wartości (łącznie: {total_missing}):\n"
                for col, count in missing.items():
                    if count > 0:
                        percent = (count / len(self.current_data)) * 100
                        info_text += f"  {col}: {count} ({percent:.1f}%)\n"
            else:
                info_text += "\nBrak brakujących wartości.\n"

            # Duplikaty
            duplicates = self.current_data.duplicated().sum()
            if duplicates > 0:
                info_text += f"\nDuplikaty: {duplicates} wierszy\n"
            else:
                info_text += "\nBrak duplikatów.\n"

            # Podstawowe statystyki numeryczne
            numeric_columns = self.current_data.select_dtypes(include=['number']).columns
            if len(numeric_columns) > 0:
                info_text += f"\nKolumny numeryczne: {len(numeric_columns)}\n"

            # Kolumny tekstowe
            text_columns = self.current_data.select_dtypes(include=['object']).columns
            if len(text_columns) > 0:
                info_text += f"Kolumny tekstowe: {len(text_columns)}\n"

            # Aktualizacja pola tekstowego
            self.data_info_text.clear()
            self.data_info_text.append(info_text)

        except Exception as error:
            print(f"Błąd przy aktualizacji informacji o danych: {error}")
            self.data_info_text.clear()
            self.data_info_text.append(f"Błąd przy wyświetlaniu informacji: {str(error)}")

    def _update_data_table(self):
        """Aktualizacja tabeli danych."""
        if self.current_data is None:
            return

        try:
            data = self.current_data

            # Ograniczenie do 1000 wierszy dla wydajności
            max_rows = min(1000, len(data))

            # Aktualizacja tabeli
            self.data_table.setRowCount(max_rows)
            self.data_table.setColumnCount(len(data.columns))
            self.data_table.setHorizontalHeaderLabels(list(data.columns))

            # Wypełnienie tabeli danymi
            for i in range(max_rows):
                for j in range(len(data.columns)):
                    value = data.iloc[i, j]

                    # Formatowanie wartości
                    if value is None or (isinstance(value, float) and str(value) == 'nan'):
                        display_value = "NaN"
                    elif isinstance(value, float):
                        display_value = f"{value:.4f}"
                    else:
                        display_value = str(value)

                    # Ograniczenie długości tekstu
                    if len(display_value) > 50:
                        display_value = display_value[:47] + "..."

                    self.data_table.setItem(i, j, QTableWidgetItem(display_value))

            # Dopasowanie szerokości kolumn
            self.data_table.resizeColumnsToContents()

            # Ograniczenie maksymalnej szerokości kolumn
            header = self.data_table.horizontalHeader()
            for i in range(len(data.columns)):
                if header.sectionSize(i) > 200:
                    header.resizeSection(i, 200)

        except Exception as error:
            print(f"Błąd przy aktualizacji tabeli danych: {error}")
            self.data_table.setRowCount(0)
            self.data_table.setColumnCount(0)