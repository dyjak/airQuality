"""
Moduł zawierający klasę zakładki przetwarzania danych.
"""
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel,
                             QComboBox, QPushButton, QLineEdit, QFormLayout, QListWidget,
                             QAbstractItemView, QSplitter, QTableWidget, QTableWidgetItem,
                             QMessageBox)
from PyQt5.QtCore import Qt


class DataProcessingTab(QWidget):
    """Zakładka przetwarzania danych."""

    def __init__(self, data_processor, data_visualizer, status_bar):
        """
        Inicjalizacja zakładki przetwarzania danych.

        Args:
            data_processor (DataProcessor): Obiekt przetwarzający dane.
            data_visualizer (DataVisualizer): Obiekt wizualizujący dane.
            status_bar (QStatusBar): Pasek stanu głównego okna.
        """
        super(DataProcessingTab, self).__init__()

        self.data_processor = data_processor
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

        # Ekstrakcja podzbioru
        subset_group = QGroupBox("Ekstrakcja podzbioru")
        subset_layout = QVBoxLayout()

        self.subset_columns_list = QListWidget()
        self.subset_columns_list.setSelectionMode(QAbstractItemView.MultiSelection)

        subset_layout.addWidget(QLabel("Wybierz kolumny:"))
        subset_layout.addWidget(self.subset_columns_list)

        extract_button = QPushButton("Wyodrębnij podzbiór")
        extract_button.clicked.connect(self.extract_subset)
        subset_layout.addWidget(extract_button)

        subset_group.setLayout(subset_layout)
        control_layout.addWidget(subset_group)

        # Zastępowanie wartości
        replace_group = QGroupBox("Zastępowanie wartości")
        replace_layout = QFormLayout()

        self.replace_column_combo = QComboBox()
        self.replace_old_value = QLineEdit()
        self.replace_new_value = QLineEdit()

        replace_layout.addRow("Kolumna:", self.replace_column_combo)
        replace_layout.addRow("Stara wartość:", self.replace_old_value)
        replace_layout.addRow("Nowa wartość:", self.replace_new_value)

        replace_button = QPushButton("Zastąp wartości")
        replace_button.clicked.connect(self.replace_values)
        replace_layout.addRow(replace_button)

        replace_group.setLayout(replace_layout)
        control_layout.addWidget(replace_group)

        # Skalowanie i standaryzacja
        scaling_group = QGroupBox("Skalowanie i standaryzacja")
        scaling_layout = QVBoxLayout()

        self.scaling_columns_list = QListWidget()
        self.scaling_columns_list.setSelectionMode(QAbstractItemView.MultiSelection)

        scaling_layout.addWidget(QLabel("Wybierz kolumny:"))
        scaling_layout.addWidget(self.scaling_columns_list)

        scaling_method_layout = QHBoxLayout()

        self.scaling_method_combo = QComboBox()
        self.scaling_method_combo.addItems(["MinMax", "Standaryzacja"])

        scaling_method_layout.addWidget(QLabel("Metoda:"))
        scaling_method_layout.addWidget(self.scaling_method_combo)

        scaling_layout.addLayout(scaling_method_layout)

        scale_button = QPushButton("Skaluj dane")
        scale_button.clicked.connect(self.scale_data)
        scaling_layout.addWidget(scale_button)

        scaling_group.setLayout(scaling_layout)
        control_layout.addWidget(scaling_group)

        # Obsługa brakujących wartości
        missing_group = QGroupBox("Obsługa brakujących wartości")
        missing_layout = QVBoxLayout()

        self.missing_method_combo = QComboBox()
        self.missing_method_combo.addItems(
            ["Usuń wiersze", "Wypełnij średnią", "Wypełnij medianą", "Wypełnij modą", "Wypełnij wartością"])

        missing_layout.addWidget(QLabel("Metoda:"))
        missing_layout.addWidget(self.missing_method_combo)

        self.missing_value_label = QLabel("Wartość:")
        self.missing_value_edit = QLineEdit()
        self.missing_value_label.hide()
        self.missing_value_edit.hide()

        missing_layout.addWidget(self.missing_value_label)
        missing_layout.addWidget(self.missing_value_edit)

        self.missing_method_combo.currentIndexChanged.connect(self.update_missing_value_controls)

        handle_missing_button = QPushButton("Przetwórz brakujące dane")
        handle_missing_button.clicked.connect(self.handle_missing_values)
        missing_layout.addWidget(handle_missing_button)

        missing_group.setLayout(missing_layout)
        control_layout.addWidget(missing_group)

        # Usuwanie duplikatów
        duplicates_group = QGroupBox("Usuwanie duplikatów")
        duplicates_layout = QVBoxLayout()

        self.duplicates_columns_list = QListWidget()
        self.duplicates_columns_list.setSelectionMode(QAbstractItemView.MultiSelection)

        duplicates_layout.addWidget(QLabel("Wybierz kolumny (puste = wszystkie):"))
        duplicates_layout.addWidget(self.duplicates_columns_list)

        remove_duplicates_button = QPushButton("Usuń duplikaty")
        remove_duplicates_button.clicked.connect(self.remove_duplicates)
        duplicates_layout.addWidget(remove_duplicates_button)

        duplicates_group.setLayout(duplicates_layout)
        control_layout.addWidget(duplicates_group)

        # Kodowanie binarne
        encoding_group = QGroupBox("Kodowanie binarne")
        encoding_layout = QVBoxLayout()

        self.encoding_columns_list = QListWidget()
        self.encoding_columns_list.setSelectionMode(QAbstractItemView.MultiSelection)

        encoding_layout.addWidget(QLabel("Wybierz kolumny:"))
        encoding_layout.addWidget(self.encoding_columns_list)

        self.encoding_method_combo = QComboBox()
        self.encoding_method_combo.addItems(["One-Hot", "Label"])

        encoding_method_layout = QHBoxLayout()
        encoding_method_layout.addWidget(QLabel("Metoda:"))
        encoding_method_layout.addWidget(self.encoding_method_combo)

        encoding_layout.addLayout(encoding_method_layout)

        encode_button = QPushButton("Koduj dane")
        encode_button.clicked.connect(self.encode_categorical)
        encoding_layout.addWidget(encode_button)

        encoding_group.setLayout(encoding_layout)
        control_layout.addWidget(encoding_group)

        # Panel z wynikami
        results_panel = QWidget()
        results_layout = QVBoxLayout(results_panel)

        # Tabela z przetworzonymi danymi
        self.processed_data_table = QTableWidget()

        results_layout.addWidget(QLabel("Przetworzone dane:"))
        results_layout.addWidget(self.processed_data_table)

        # Splitter do dzielenia paneli
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(control_panel)
        splitter.addWidget(results_panel)
        splitter.setSizes([400, 600])

        layout.addWidget(splitter)

    def update_columns(self, columns):
        """
        Aktualizacja list kolumn.

        Args:
            columns (list): Lista nazw kolumn.
        """
        self.subset_columns_list.clear()
        self.subset_columns_list.addItems(columns)

        self.replace_column_combo.clear()
        self.replace_column_combo.addItems(columns)

        self.scaling_columns_list.clear()
        self.scaling_columns_list.addItems(columns)

        self.duplicates_columns_list.clear()
        self.duplicates_columns_list.addItems(columns)

        self.encoding_columns_list.clear()
        self.encoding_columns_list.addItems(columns)

        # Aktualizacja tabeli
        self.update_processed_data_table()

    def update_processed_data_table(self):
        """Aktualizacja tabeli przetworzonych danych."""
        if self.data_processor.get_data() is None:
            return

        # Pobranie danych
        data = self.data_processor.get_data()

        # Aktualizacja tabeli
        self.processed_data_table.setRowCount(min(100, len(data)))  # Ograniczenie do 100 wierszy dla wydajności
        self.processed_data_table.setColumnCount(len(data.columns))
        self.processed_data_table.setHorizontalHeaderLabels(list(data.columns))

        # Wypełnienie tabeli danymi
        for i in range(min(100, len(data))):
            for j in range(len(data.columns)):
                value = str(data.iloc[i, j])
                self.processed_data_table.setItem(i, j, QTableWidgetItem(value))

        # Dopasowanie szerokości kolumn
        self.processed_data_table.resizeColumnsToContents()

    def update_missing_value_controls(self):
        """Aktualizacja kontrolek do obsługi brakujących wartości."""
        method = self.missing_method_combo.currentText()

        # Pokazanie lub ukrycie pola do wprowadzania wartości
        if method == "Wypełnij wartością":
            self.missing_value_label.show()
            self.missing_value_edit.show()
        else:
            self.missing_value_label.hide()
            self.missing_value_edit.hide()

    def extract_subset(self):
        """Ekstrakcja podzbioru danych."""
        if self.data_processor.get_data() is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do przetworzenia."
            )
            return

        # Pobranie wybranych kolumn
        selected_items = self.subset_columns_list.selectedItems()

        if not selected_items:
            QMessageBox.warning(
                self, "Błąd", "Nie wybrano kolumn."
            )
            return

        columns = [item.text() for item in selected_items]

        # Ekstrakcja podzbioru danych
        subset = self.data_processor.extract_subset(columns)

        if subset is not None:
            # Aktualizacja danych
            self.data_processor.set_data(subset)
            self.data_visualizer.set_data(subset)

            # Aktualizacja interfejsu
            self.update_processed_data_table()

            self.status_bar.showMessage(f"Wyekstrahowano podzbiór danych: {', '.join(columns)}")
        else:
            QMessageBox.warning(
                self, "Błąd", "Nie udało się wyekstrahować podzbioru danych."
            )

    def replace_values(self):
        """Zastępowanie wartości w wybranej kolumnie."""
        if self.data_processor.get_data() is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do przetworzenia."
            )
            return

        # Pobranie parametrów
        column = self.replace_column_combo.currentText()
        old_value = self.replace_old_value.text()
        new_value = self.replace_new_value.text()

        if not column or not old_value or not new_value:
            QMessageBox.warning(
                self, "Błąd", "Nie wprowadzono wszystkich parametrów."
            )
            return

        # Konwersja wartości na odpowiedni typ
        try:
            # Sprawdzenie, czy wartości są liczbami
            if old_value.replace('.', '', 1).isdigit():
                old_value = float(old_value)
            if new_value.replace('.', '', 1).isdigit():
                new_value = float(new_value)
        except ValueError:
            pass

        # Zastępowanie wartości
        success = self.data_processor.replace_values(column, old_value, new_value)

        if success:
            # Aktualizacja danych w data_visualizer
            self.data_visualizer.set_data(self.data_processor.get_data())

            # Aktualizacja interfejsu
            self.update_processed_data_table()

            self.status_bar.showMessage(f"Zastąpiono wartości w kolumnie {column}")
        else:
            QMessageBox.warning(
                self, "Błąd", "Nie udało się zastąpić wartości."
            )

    def scale_data(self):
        """Skalowanie danych."""
        if self.data_processor.get_data() is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do przetworzenia."
            )
            return

        # Pobranie wybranych kolumn
        selected_items = self.scaling_columns_list.selectedItems()

        if not selected_items:
            QMessageBox.warning(
                self, "Błąd", "Nie wybrano kolumn."
            )
            return

        columns = [item.text() for item in selected_items]

        # Pobranie metody skalowania
        method = 'minmax' if self.scaling_method_combo.currentText() == "MinMax" else 'standard'

        # Skalowanie danych
        success = self.data_processor.scale_data(columns, method=method)

        if success:
            # Aktualizacja danych w data_visualizer
            self.data_visualizer.set_data(self.data_processor.get_data())

            # Aktualizacja interfejsu
            self.update_processed_data_table()
            self.update_columns(self.data_processor.get_data().columns)

            self.status_bar.showMessage(f"Przeskalowano dane w kolumnach: {', '.join(columns)}")
        else:
            QMessageBox.warning(
                self, "Błąd", "Nie udało się przeskalować danych."
            )

    def handle_missing_values(self):
        """Obsługa brakujących wartości."""
        if self.data_processor.get_data() is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do przetworzenia."
            )
            return

        # Pobranie metody obsługi brakujących wartości
        method_text = self.missing_method_combo.currentText()

        if method_text == "Usuń wiersze":
            method = 'drop'
            fill_value = None
        else:
            method = 'fill'

            if method_text == "Wypełnij średnią":
                fill_value = 'mean'
            elif method_text == "Wypełnij medianą":
                fill_value = 'median'
            elif method_text == "Wypełnij modą":
                fill_value = 'most_frequent'
            elif method_text == "Wypełnij wartością":
                # Pobranie wprowadzonej wartości
                value_text = self.missing_value_edit.text()

                if not value_text:
                    QMessageBox.warning(
                        self, "Błąd", "Nie wprowadzono wartości do wypełnienia."
                    )
                    return

                # Konwersja wartości na odpowiedni typ
                try:
                    # Sprawdzenie, czy wartość jest liczbą
                    if value_text.replace('.', '', 1).isdigit():
                        fill_value = float(value_text)
                    else:
                        fill_value = value_text
                except ValueError:
                    fill_value = value_text
            else:
                QMessageBox.warning(
                    self, "Błąd", "Nieznana metoda obsługi brakujących wartości."
                )
                return

        # Obsługa brakujących wartości
        success = self.data_processor.remove_missing_values(method=method, fill_value=fill_value)

        if success:
            # Aktualizacja danych w data_visualizer
            self.data_visualizer.set_data(self.data_processor.get_data())

            # Aktualizacja interfejsu
            self.update_processed_data_table()

            self.status_bar.showMessage("Przetworzono brakujące wartości")
        else:
            QMessageBox.warning(
                self, "Błąd", "Nie udało się przetworzyć brakujących wartości."
            )

    def remove_duplicates(self):
        """Usuwanie duplikatów."""
        if self.data_processor.get_data() is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do przetworzenia."
            )
            return

        # Pobranie wybranych kolumn
        selected_items = self.duplicates_columns_list.selectedItems()

        if not selected_items:
            columns = None  # Wszystkie kolumny
        else:
            columns = [item.text() for item in selected_items]

        # Usuwanie duplikatów
        success = self.data_processor.remove_duplicates(columns)

        if success:
            # Aktualizacja danych w data_visualizer
            self.data_visualizer.set_data(self.data_processor.get_data())

            # Aktualizacja interfejsu
            self.update_processed_data_table()

            if columns:
                self.status_bar.showMessage(f"Usunięto duplikaty na podstawie kolumn: {', '.join(columns)}")
            else:
                self.status_bar.showMessage("Usunięto duplikaty na podstawie wszystkich kolumn")
        else:
            QMessageBox.warning(
                self, "Błąd", "Nie udało się usunąć duplikatów."
            )

    def encode_categorical(self):
        """Kodowanie binarne zmiennych kategorycznych."""
        if self.data_processor.get_data() is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do przetworzenia."
            )
            return

        # Pobranie wybranych kolumn
        selected_items = self.encoding_columns_list.selectedItems()

        if not selected_items:
            QMessageBox.warning(
                self, "Błąd", "Nie wybrano kolumn."
            )
            return

        columns = [item.text() for item in selected_items]

        # Pobranie metody kodowania
        method = 'onehot' if self.encoding_method_combo.currentText() == "One-Hot" else 'label'

        # Kodowanie binarne
        success = self.data_processor.encode_categorical(columns, method=method)

        if success:
            # Aktualizacja danych w data_visualizer
            self.data_visualizer.set_data(self.data_processor.get_data())

            # Aktualizacja interfejsu
            self.update_processed_data_table()
            self.update_columns(self.data_processor.get_data().columns)

            self.status_bar.showMessage(f"Zakodowano zmienne kategoryczne: {', '.join(columns)}")
        else:
            QMessageBox.warning(
                self, "Błąd", "Nie udało się zakodować zmiennych kategorycznych."
            )