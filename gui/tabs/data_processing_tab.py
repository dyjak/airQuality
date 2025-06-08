"""
Moduł zawierający klasę zakładki przetwarzania danych.
ZAKTUALIZOWANY - używa prostych funkcji z utils zamiast obiektów.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
                             QComboBox, QPushButton, QListWidget, QAbstractItemView,
                             QLineEdit, QTableWidget, QTableWidgetItem, QSplitter,
                             QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt


class DataProcessingTab(QWidget):
    """Zakładka przetwarzania danych."""

    def __init__(self, status_bar):
        """
        Inicjalizacja zakładki przetwarzania danych.

        Args:
            status_bar (QStatusBar): Pasek stanu głównego okna.
        """
        super(DataProcessingTab, self).__init__()
        self.status_bar = status_bar
        self.current_data = None
        self.original_data = None

        # Inicjalizacja interfejsu
        self.init_ui()

    def init_ui(self):
        """Inicjalizacja interfejsu zakładki."""
        layout = QHBoxLayout(self)

        # Panel sterowania
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)

        # Grupa - obsługa brakujących wartości
        missing_group = QGroupBox("Obsługa brakujących wartości")
        missing_layout = QVBoxLayout()

        self.missing_method_combo = QComboBox()
        self.missing_method_combo.addItems([
            "Usuń wiersze",
            "Wypełnij średnią",
            "Wypełnij medianą",
            "Wypełnij modą",
            "Wypełnij wartością"
        ])

        missing_layout.addWidget(QLabel("Metoda:"))
        missing_layout.addWidget(self.missing_method_combo)

        # Pole do wpisania wartości
        self.missing_value_edit = QLineEdit()
        self.missing_value_edit.setPlaceholderText("Wpisz wartość...")
        missing_layout.addWidget(QLabel("Wartość do wypełnienia:"))
        missing_layout.addWidget(self.missing_value_edit)

        # Przycisk
        missing_button = QPushButton("Obsłuż braki")
        missing_button.clicked.connect(self.handle_missing_values)
        missing_layout.addWidget(missing_button)

        missing_group.setLayout(missing_layout)
        control_layout.addWidget(missing_group)

        # Grupa - skalowanie danych
        scaling_group = QGroupBox("Skalowanie danych")
        scaling_layout = QVBoxLayout()

        # Lista kolumn do skalowania
        self.scaling_columns_list = QListWidget()
        self.scaling_columns_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.scaling_columns_list.setMaximumHeight(150)

        scaling_layout.addWidget(QLabel("Wybierz kolumny do skalowania:"))
        scaling_layout.addWidget(self.scaling_columns_list)

        # Metoda skalowania
        self.scaling_method_combo = QComboBox()
        self.scaling_method_combo.addItems(["MinMax (0-1)", "Standard (z-score)"])

        scaling_layout.addWidget(QLabel("Metoda skalowania:"))
        scaling_layout.addWidget(self.scaling_method_combo)

        # Przycisk
        scaling_button = QPushButton("Skaluj dane")
        scaling_button.clicked.connect(self.scale_data)
        scaling_layout.addWidget(scaling_button)

        scaling_group.setLayout(scaling_layout)
        control_layout.addWidget(scaling_group)

        # Grupa - usuwanie duplikatów
        duplicates_group = QGroupBox("Usuwanie duplikatów")
        duplicates_layout = QVBoxLayout()

        # Lista kolumn do sprawdzania duplikatów
        self.duplicates_columns_list = QListWidget()
        self.duplicates_columns_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.duplicates_columns_list.setMaximumHeight(150)

        duplicates_layout.addWidget(QLabel("Kolumny do sprawdzenia (puste = wszystkie):"))
        duplicates_layout.addWidget(self.duplicates_columns_list)

        # Przycisk
        duplicates_button = QPushButton("Usuń duplikaty")
        duplicates_button.clicked.connect(self.remove_duplicates)
        duplicates_layout.addWidget(duplicates_button)

        duplicates_group.setLayout(duplicates_layout)
        control_layout.addWidget(duplicates_group)

        # Grupa - zamiana wartości
        replace_group = QGroupBox("Zamiana wartości")
        replace_layout = QVBoxLayout()

        # Wybór kolumny
        self.replace_column_combo = QComboBox()
        replace_layout.addWidget(QLabel("Kolumna:"))
        replace_layout.addWidget(self.replace_column_combo)

        # Stara wartość
        self.old_value_edit = QLineEdit()
        self.old_value_edit.setPlaceholderText("Wartość do zamiany...")
        replace_layout.addWidget(QLabel("Stara wartość:"))
        replace_layout.addWidget(self.old_value_edit)

        # Nowa wartość
        self.new_value_edit = QLineEdit()
        self.new_value_edit.setPlaceholderText("Nowa wartość...")
        replace_layout.addWidget(QLabel("Nowa wartość:"))
        replace_layout.addWidget(self.new_value_edit)

        # Przycisk
        replace_button = QPushButton("Zamień wartości")
        replace_button.clicked.connect(self.replace_values)
        replace_layout.addWidget(replace_button)

        replace_group.setLayout(replace_layout)
        control_layout.addWidget(replace_group)

        # Grupa - zapisywanie danych
        save_group = QGroupBox("Zapisywanie danych")
        save_layout = QVBoxLayout()

        save_button = QPushButton("Zapisz przetworzone dane do CSV")
        save_button.clicked.connect(self.save_processed_data)
        save_layout.addWidget(save_button)

        save_group.setLayout(save_layout)
        control_layout.addWidget(save_group)

        # Dodanie elastycznego odstępu
        control_layout.addStretch()

        # Panel wyników - tabela z przetworzonymi danymi
        results_panel = QWidget()
        results_layout = QVBoxLayout(results_panel)

        results_layout.addWidget(QLabel("Przetworzone dane:"))

        self.processed_data_table = QTableWidget()
        results_layout.addWidget(self.processed_data_table)

        # Splitter do dzielenia paneli
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(control_panel)
        splitter.addWidget(results_panel)
        splitter.setSizes([400, 600])

        layout.addWidget(splitter)

    def update_data(self, data):
        """
        Aktualizacja danych.

        Args:
            data (pandas.DataFrame): Nowe dane do przetwarzania.
        """
        self.current_data = data
        self.original_data = data.copy() if data is not None else None
        if data is not None:
            columns = list(data.columns)
            self.update_columns(columns)
            self.update_processed_data_table()
            print(f"DataProcessingTab: zaktualizowano dane ({len(data)} wierszy, {len(columns)} kolumn)")

    def update_columns(self, columns):
        """
        Aktualizacja list kolumn.

        Args:
            columns (list): Lista nazw kolumn.
        """
        # Aktualizacja listy kolumn do skalowania
        self.scaling_columns_list.clear()
        self.scaling_columns_list.addItems(columns)

        # Aktualizacja listy kolumn do sprawdzania duplikatów
        self.duplicates_columns_list.clear()
        self.duplicates_columns_list.addItems(columns)

        # Aktualizacja combo box do zamiany wartości
        self.replace_column_combo.clear()
        self.replace_column_combo.addItems(columns)

    def update_processed_data_table(self):
        """Aktualizacja tabeli z przetworzonymi danymi."""
        if self.current_data is None:
            self.processed_data_table.setRowCount(0)
            self.processed_data_table.setColumnCount(0)
            return

        try:
            data = self.current_data

            # Ograniczenie do 50 wierszy dla wydajności
            max_rows = min(50, len(data))

            self.processed_data_table.setRowCount(max_rows)
            self.processed_data_table.setColumnCount(len(data.columns))
            self.processed_data_table.setHorizontalHeaderLabels(list(data.columns))

            # Wypełnienie tabeli
            for i in range(max_rows):
                for j in range(len(data.columns)):
                    value = data.iloc[i, j]

                    # Sprawdź czy wartość się zmieniła
                    has_changed = False
                    if (self.original_data is not None and
                            i < len(self.original_data) and
                            j < len(self.original_data.columns) and
                            data.columns[j] in self.original_data.columns):
                        original_value = self.original_data.iloc[i][data.columns[j]]
                        has_changed = str(value) != str(original_value)

                    # Formatowanie wartości
                    if value is None or str(value) == 'nan':
                        display_value = "NaN"
                    elif isinstance(value, float):
                        display_value = f"{value:.4f}"
                    else:
                        display_value = str(value)

                    item = QTableWidgetItem(display_value)

                    # Oznacz zmienione komórki kolorem
                    if has_changed:
                        from PyQt5.QtGui import QColor
                        item.setBackground(QColor(255, 255, 0, 100))  # Żółte tło

                    self.processed_data_table.setItem(i, j, item)

            # Dopasowanie szerokości kolumn
            self.processed_data_table.resizeColumnsToContents()

        except Exception as error:
            print(f"Błąd przy aktualizacji tabeli: {error}")

    def handle_missing_values(self):
        """Obsługa brakujących wartości."""
        if self.current_data is None:
            QMessageBox.warning(self, "Błąd", "Brak danych do przetworzenia.")
            return

        # Pobranie metody obsługi
        method_text = self.missing_method_combo.currentText()

        try:
            from utils.data_processor import handle_missing_values

            # Mapowanie nazw metod
            if method_text == "Usuń wiersze":
                method = 'drop'
                fill_value = None
            elif method_text == "Wypełnij średnią":
                method = 'mean'
                fill_value = None
            elif method_text == "Wypełnij medianą":
                method = 'median'
                fill_value = None
            elif method_text == "Wypełnij modą":
                method = 'mode'
                fill_value = None
            elif method_text == "Wypełnij wartością":
                method = 'value'
                fill_value = self.missing_value_edit.text()
                if not fill_value:
                    QMessageBox.warning(self, "Błąd", "Nie wprowadzono wartości.")
                    return
            else:
                QMessageBox.warning(self, "Błąd", "Nieznana metoda.")
                return

            # Obsługa brakujących wartości
            processed_data = handle_missing_values(
                self.current_data,
                method=method,
                fill_value=fill_value
            )

            if processed_data is not None:
                self.current_data = processed_data
                self.update_processed_data_table()
                self.status_bar.showMessage("Przetworzono brakujące wartości")
            else:
                QMessageBox.warning(self, "Błąd", "Nie udało się przetworzyć danych.")

        except Exception as error:
            print(f"Błąd przy obsłudze brakujących wartości: {error}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(error)}")

    def scale_data(self):
        """Skalowanie danych."""
        if self.current_data is None:
            QMessageBox.warning(self, "Błąd", "Brak danych do przetworzenia.")
            return

        # Pobranie wybranych kolumn
        selected_items = self.scaling_columns_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Błąd", "Nie wybrano kolumn.")
            return

        columns = [item.text() for item in selected_items]

        # Pobranie metody skalowania
        method = 'minmax' if self.scaling_method_combo.currentText() == "MinMax (0-1)" else 'standard'

        try:
            # Import i użycie prostej funkcji z utils
            from utils.data_processor import scale_data

            # Skalowanie danych
            scaled_data = scale_data(self.current_data, columns, method=method)

            if scaled_data is not None:
                # Aktualizacja danych
                self.current_data = scaled_data

                # Aktualizacja interfejsu
                self.update_processed_data_table()
                self.update_columns(list(scaled_data.columns))

                self.status_bar.showMessage(f"Przeskalowano dane w kolumnach: {', '.join(columns)}")
            else:
                QMessageBox.warning(self, "Błąd", "Nie udało się przeskalować danych.")

        except Exception as error:
            print(f"Błąd przy skalowaniu: {error}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(error)}")

    def remove_duplicates(self):
        """Usuwanie duplikatów."""
        if self.current_data is None:
            QMessageBox.warning(self, "Błąd", "Brak danych do przetworzenia.")
            return

        try:
            from utils.data_processor import remove_duplicates

            # Pobranie wybranych kolumn (jeśli są wybrane)
            selected_items = self.duplicates_columns_list.selectedItems()

            if selected_items:
                columns = [item.text() for item in selected_items]
            else:
                columns = None  # Sprawdzenie wszystkich kolumn

            # Usunięcie duplikatów
            cleaned_data = remove_duplicates(self.current_data, column_names=columns)

            if cleaned_data is not None:
                self.current_data = cleaned_data
                self.update_processed_data_table()
                self.status_bar.showMessage("Usunięto duplikaty")
            else:
                QMessageBox.warning(self, "Błąd", "Nie udało się usunąć duplikatów.")

        except Exception as error:
            print(f"Błąd przy usuwaniu duplikatów: {error}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(error)}")

    def replace_values(self):
        """Zamiana wartości."""
        if self.current_data is None:
            QMessageBox.warning(self, "Błąd", "Brak danych do przetworzenia.")
            return

        # Pobranie parametrów
        column = self.replace_column_combo.currentText()
        old_value = self.old_value_edit.text()
        new_value = self.new_value_edit.text()

        if not column or not old_value:
            QMessageBox.warning(self, "Błąd", "Wypełnij wszystkie pola.")
            return

        try:
            from utils.data_processor import replace_values

            # Próba konwersji wartości na liczby jeśli to możliwe
            try:
                old_value = float(old_value)
            except ValueError:
                pass  # Zostaw jako string

            try:
                new_value = float(new_value)
            except ValueError:
                pass  # Zostaw jako string

            # Zamiana wartości
            processed_data = replace_values(
                self.current_data,
                column,
                old_value,
                new_value
            )

            if processed_data is not None:
                self.current_data = processed_data
                self.update_processed_data_table()
                self.status_bar.showMessage(f"Zamieniono wartości w kolumnie {column}")
            else:
                QMessageBox.warning(self, "Błąd", "Nie udało się zamienić wartości.")

        except Exception as error:
            print(f"Błąd przy zamianie wartości: {error}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd: {str(error)}")

    def save_processed_data(self):
        """Zapisuje przetworzone dane do pliku CSV."""
        if self.current_data is None:
            QMessageBox.warning(self, "Błąd", "Brak danych do zapisania.")
            return

        from PyQt5.QtWidgets import QFileDialog
        from utils.data_loader import save_data_to_csv

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Zapisz przetworzone dane", "", "Pliki CSV (*.csv)"
        )

        if file_path:
            success = save_data_to_csv(self.current_data, file_path)
            if success:
                self.status_bar.showMessage(f"Zapisano przetworzone dane do {file_path}")
            else:
                QMessageBox.warning(self, "Błąd", "Nie udało się zapisać pliku.")