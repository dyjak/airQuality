"""
Moduł zawierający klasę głównego okna aplikacji.
"""
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTabWidget, QFileDialog,
                             QMessageBox, QDialog, QComboBox, QAction, QStatusBar,
                             QToolBar)
from PyQt5.QtCore import Qt

from data_loader import DataLoader
from data_processor import DataProcessor
from data_visualizer import DataVisualizer

from .tabs.data_previews import DataPreviewTab
from .tabs.stats_tab import StatsTab
from .tabs.correlation_tab import CorrelationTab
from .tabs.visualization_tab import VisualizationTab
from .tabs.data_processing_tab import DataProcessingTab
from .tabs.classification_tab import ClassificationTab


class MainWindow(QMainWindow):
    """Główne okno aplikacji."""

    def __init__(self):
        """Inicjalizacja głównego okna aplikacji."""
        super(MainWindow, self).__init__()

        # Tytuł i rozmiar okna
        self.setWindowTitle("Analiza danych o jakości powietrza")
        self.setGeometry(100, 100, 1200, 800)

        # Inicjalizacja obiektów do przetwarzania danych
        self.data_loader = DataLoader()
        self.data_processor = DataProcessor()
        self.data_visualizer = DataVisualizer()

        # Tworzenie interfejsu użytkownika
        self.init_ui()

    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika."""
        # Tworzenie głównego widgetu i układu
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Pasek narzędzi
        self.create_toolbar()

        # Pasek menu
        self.create_menu()

        # Pasek stanu
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Gotowy")

        # Przyciski do wczytywania danych
        load_data_group = QWidget()
        load_data_layout = QHBoxLayout(load_data_group)
        load_data_layout.setContentsMargins(10, 10, 10, 10)

        self.load_data_button = QPushButton("Wczytaj dane z pliku CSV")
        self.load_data_button.clicked.connect(self.load_data_from_csv)

        load_data_layout.addWidget(self.load_data_button)

        main_layout.addWidget(load_data_group)

        # Zakładki dla różnych funkcjonalności
        self.tabs = QTabWidget()

        # Zakładka podglądu danych
        self.data_preview_tab = DataPreviewTab()
        self.tabs.addTab(self.data_preview_tab, "Podgląd danych")

        # Zakładka analizy statystycznej
        self.stats_tab = StatsTab(self.data_processor, self.statusBar)
        self.tabs.addTab(self.stats_tab, "Analiza statystyczna")

        # Zakładka korelacji
        self.correlation_tab = CorrelationTab(self.data_processor, self.data_visualizer, self.statusBar)
        self.tabs.addTab(self.correlation_tab, "Korelacje")

        # Zakładka wizualizacji
        self.visualization_tab = VisualizationTab(self.data_visualizer, self.statusBar)
        self.tabs.addTab(self.visualization_tab, "Wizualizacja")

        # Zakładka przetwarzania danych
        self.data_processing_tab = DataProcessingTab(self.data_processor, self.data_visualizer, self.statusBar)
        self.tabs.addTab(self.data_processing_tab, "Przetwarzanie danych")

        # Zakładka klasyfikacji i grupowania
        self.classification_tab = ClassificationTab(self.data_processor, self.statusBar)
        self.tabs.addTab(self.classification_tab, "Klasyfikacja i grupowanie")

        main_layout.addWidget(self.tabs)

    def create_toolbar(self):
        """Tworzenie paska narzędzi."""
        toolbar = QToolBar("Pasek narzędzi")
        self.addToolBar(toolbar)

        # Akcje paska narzędzi
        load_action = QAction("Wczytaj", self)
        load_action.setStatusTip("Wczytaj dane z pliku CSV")
        load_action.triggered.connect(self.load_data_from_csv)
        toolbar.addAction(load_action)

        save_action = QAction("Zapisz", self)
        save_action.setStatusTip("Zapisz przetworzone dane do pliku CSV")
        save_action.triggered.connect(self.save_data_to_csv)
        toolbar.addAction(save_action)

        toolbar.addSeparator()

        reset_action = QAction("Resetuj", self)
        reset_action.setStatusTip("Resetuj dane do stanu pierwotnego")
        reset_action.triggered.connect(self.reset_data)
        toolbar.addAction(reset_action)

    def create_menu(self):
        """Tworzenie paska menu."""
        menu_bar = self.menuBar()

        # Menu Plik
        file_menu = menu_bar.addMenu("Plik")

        load_action = QAction("Wczytaj dane", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_data_from_csv)
        file_menu.addAction(load_action)

        save_action = QAction("Zapisz dane", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_data_to_csv)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction("Wyjście", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menu Edycja
        edit_menu = menu_bar.addMenu("Edycja")

        reset_action = QAction("Resetuj dane", self)
        reset_action.triggered.connect(self.reset_data)
        edit_menu.addAction(reset_action)

        # Menu Pomoc
        help_menu = menu_bar.addMenu("Pomoc")

        about_action = QAction("O programie", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def load_data_from_csv(self):
        """Wczytywanie danych z pliku CSV."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Wczytaj plik CSV", "", "Pliki CSV (*.csv);;Wszystkie pliki (*.*)"
        )

        if file_path:
            # Okno dialogowe do wyboru separatora
            separator_dialog = QDialog(self)
            separator_dialog.setWindowTitle("Wybierz separator")
            separator_layout = QVBoxLayout(separator_dialog)

            separator_combo = QComboBox()
            separator_combo.addItems([";", ",", "\t", "|", " "])

            separator_layout.addWidget(QLabel("Wybierz separator:"))
            separator_layout.addWidget(separator_combo)

            buttons_layout = QHBoxLayout()
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(separator_dialog.accept)
            cancel_button = QPushButton("Anuluj")
            cancel_button.clicked.connect(separator_dialog.reject)

            buttons_layout.addWidget(ok_button)
            buttons_layout.addWidget(cancel_button)

            separator_layout.addLayout(buttons_layout)

            result = separator_dialog.exec_()

            if result == QDialog.Accepted:
                delimiter = separator_combo.currentText()

                # Wczytywanie danych
                success = self.data_loader.load_data(file_path, delimiter=delimiter)

                if success:
                    self.statusBar.showMessage(f"Wczytano dane z pliku {os.path.basename(file_path)}")

                    # Aktualizacja danych w data_processor i data_visualizer
                    self.data_processor.set_data(self.data_loader.get_data())
                    self.data_visualizer.set_data(self.data_loader.get_data())

                    # Aktualizacja interfejsu
                    self.update_ui_after_data_load()
                else:
                    QMessageBox.warning(
                        self, "Błąd", "Nie udało się wczytać danych z pliku."
                    )

    def save_data_to_csv(self):
        """Zapisywanie przetworzonych danych do pliku CSV."""
        if self.data_processor.get_data() is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do zapisania."
            )
            return

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "Zapisz do pliku CSV", "", "Pliki CSV (*.csv);;Wszystkie pliki (*.*)"
        )

        if file_path:
            # Okno dialogowe do wyboru separatora
            separator_dialog = QDialog(self)
            separator_dialog.setWindowTitle("Wybierz separator")
            separator_layout = QVBoxLayout(separator_dialog)

            separator_combo = QComboBox()
            separator_combo.addItems([";", ",", "\t", "|", " "])

            separator_layout.addWidget(QLabel("Wybierz separator:"))
            separator_layout.addWidget(separator_combo)

            buttons_layout = QHBoxLayout()
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(separator_dialog.accept)
            cancel_button = QPushButton("Anuluj")
            cancel_button.clicked.connect(separator_dialog.reject)

            buttons_layout.addWidget(ok_button)
            buttons_layout.addWidget(cancel_button)

            separator_layout.addLayout(buttons_layout)

            result = separator_dialog.exec_()

            if result == QDialog.Accepted:
                delimiter = separator_combo.currentText()

                try:
                    # Zapisywanie danych
                    self.data_processor.get_data().to_csv(file_path, sep=delimiter, index=False)
                    self.statusBar.showMessage(f"Zapisano dane do pliku {os.path.basename(file_path)}")
                except Exception as e:
                    QMessageBox.warning(
                        self, "Błąd", f"Nie udało się zapisać danych do pliku: {e}"
                    )

    def reset_data(self):
        """Resetowanie danych do stanu pierwotnego."""
        if self.data_processor.get_data() is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do zresetowania."
            )
            return

        # Resetowanie danych
        success = self.data_processor.reset_data()

        if success:
            # Aktualizacja danych w data_visualizer
            self.data_visualizer.set_data(self.data_processor.get_data())

            # Aktualizacja interfejsu
            self.update_ui_after_data_load()

            self.statusBar.showMessage("Zresetowano dane do stanu pierwotnego")
        else:
            QMessageBox.warning(
                self, "Błąd", "Nie udało się zresetować danych."
            )

    def update_ui_after_data_load(self):
        """Aktualizacja interfejsu po wczytaniu danych."""
        # Aktualizacja wszystkich zakładek
        self.data_preview_tab.update_data(self.data_loader)
        self.stats_tab.update_columns(self.data_loader.get_column_names())
        self.correlation_tab.update_data()
        self.visualization_tab.update_columns(self.data_loader.get_column_names())
        self.data_processing_tab.update_columns(self.data_loader.get_column_names())
        self.classification_tab.update_columns(self.data_loader.get_column_names())

    def show_about_dialog(self):
        """Wyświetlanie okna dialogowego 'O programie'."""
        QMessageBox.about(
            self,
            "O programie",
            "Aplikacja do analizy danych o jakości powietrza\n\n"
            "Projekt hurtowni danych\n\n"
            "Funkcjonalności:\n"
            "- Odczyt danych z pliku CSV\n"
            "- Obliczanie miar statystycznych\n"
            "- Wyznaczanie korelacji cech\n"
            "- Ekstrakcja podzbioru danych\n"
            "- Zastępowanie wartości w tabelach danych\n"
            "- Skalowanie i standaryzacja kolumn\n"
            "- Usuwanie wierszy z brakującymi wartościami\n"
            "- Usuwanie powtarzających się miejsc w tabelach danych\n"
            "- Kodowanie binarne kolumn symbolicznych\n"
            "- Tworzenie wykresów dla danych\n"
            "- Klasyfikacja danych\n"
            "- Grupowanie danych\n"
            "- Reguły asocjacyjne"
        )