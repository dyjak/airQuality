"""
Moduł zawierający klasę głównego okna aplikacji.
ZAKTUALIZOWANY - używa prostych funkcji z utils zamiast klas.
"""
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTabWidget, QFileDialog,
                             QMessageBox, QDialog, QComboBox, QAction, QStatusBar,
                             QToolBar)
from PyQt5.QtCore import Qt

# importujemy nasze proste funkcje z utils
from utils.data_loader import load_csv_data, save_data_to_csv, check_basic_info
from utils.data_processor import calculate_basic_statistics, calculate_correlation
from utils.visualization import setup_plot_style

# importujemy taby GUI
from gui.tabs.data_previews import DataPreviewTab
from gui.tabs.stats_tab import StatsTab
from gui.tabs.correlation_tab import CorrelationTab
from gui.tabs.visualization_tab import VisualizationTab
from gui.tabs.data_processing_tab import DataProcessingTab
from gui.tabs.classification_tab import ClassificationTab


class MainWindow(QMainWindow):
    """Główne okno aplikacji - teraz prostsze i bardziej zrozumiałe!"""

    def __init__(self):
        """Inicjalizacja głównego okna aplikacji."""
        super(MainWindow, self).__init__()

        # Tytuł i rozmiar okna
        self.setWindowTitle("Analiza danych o jakości powietrza - Wersja 2.0")
        self.setGeometry(100, 100, 1200, 800)

        # zamiast obiektów mamy teraz proste zmienne
        self.current_data = None  # aktualne dane jako ramka pandas
        self.original_data = None  # oryginalne dane (do resetowania)
        self.current_file_path = None  # sciezka do aktualnego pliku

        # ustawiamy ladny styl wykresow od razu
        setup_plot_style()
        print("ustawiono ladny styl wykresow")

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
        self.statusBar.showMessage("Gotowy - wczytaj dane zeby zaczac analize")

        # Przyciski do wczytywania danych
        load_data_group = QWidget()
        load_data_layout = QHBoxLayout(load_data_group)
        load_data_layout.setContentsMargins(10, 10, 10, 10)

        self.load_data_button = QPushButton("Wczytaj dane z pliku CSV")
        self.load_data_button.clicked.connect(self.load_data_from_csv)
        self.load_data_button.setStyleSheet("font-size: 14px; padding: 10px;")

        load_data_layout.addWidget(self.load_data_button)

        main_layout.addWidget(load_data_group)

        # Zakładki dla różnych funkcjonalności
        self.tabs = QTabWidget()

        # POPRAWIONE konstruktory tabs - tylko status_bar
        self.data_preview_tab = DataPreviewTab()
        self.stats_tab = StatsTab(self.statusBar)
        self.correlation_tab = CorrelationTab(self.statusBar)
        self.visualization_tab = VisualizationTab(self.statusBar)
        self.data_processing_tab = DataProcessingTab(self.statusBar)
        self.classification_tab = ClassificationTab(self.statusBar)

        # Dodawanie zakładek
        self.tabs.addTab(self.data_preview_tab, "Podgląd danych")
        self.tabs.addTab(self.stats_tab, "Analiza statystyczna")
        self.tabs.addTab(self.correlation_tab, "Korelacje")
        self.tabs.addTab(self.visualization_tab, "Wizualizacja")
        self.tabs.addTab(self.data_processing_tab, "Przetwarzanie danych")
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
        """
        Wczytywanie danych z pliku CSV - teraz używa prostej funkcji!
        """
        try:
            # wybieramy plik
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(
                self, "Wczytaj plik CSV", "", "Pliki CSV (*.csv);;Wszystkie pliki (*.*)"
            )

            if not file_path:
                return  # anulowano wybor pliku

            # wybieramy separator
            separator = self.ask_for_separator()
            if separator is None:
                return  # anulowano wybor separatora

            # wczytujemy dane prostą funkcją!
            print(f"wczytuje dane z pliku: {file_path}")
            self.current_data = load_csv_data(file_path, separator=separator)

            if self.current_data is not None:
                # zapisujemy oryginalne dane do resetowania
                self.original_data = self.current_data.copy()
                self.current_file_path = file_path

                # pokazujemy podstawowe info
                info = check_basic_info(self.current_data)

                # aktualizujemy status
                self.statusBar.showMessage(
                    f"Wczytano {info['row_count']} wierszy, {info['column_count']} kolumn z {os.path.basename(file_path)}"
                )

                # aktualizujemy wszystkie taby
                self.update_all_tabs()

                print("dane wczytane pomyslnie!")

            else:
                QMessageBox.warning(self, "Błąd", "Nie udało się wczytać danych z pliku.")

        except Exception as error:
            print(f"blad przy wczytywaniu: {error}")
            QMessageBox.critical(self, "Błąd krytyczny", f"Wystąpił błąd: {str(error)}")

    def ask_for_separator(self):
        """
        Pyta uzytkownika o separator - pomocnicza funkcja
        """
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
            return separator_combo.currentText()
        else:
            return None

    def save_data_to_csv(self):
        """
        Zapisywanie danych do pliku CSV - teraz używa prostej funkcji!
        """
        if self.current_data is None:
            QMessageBox.warning(self, "Błąd", "Brak danych do zapisania.")
            return

        # wybieramy gdzie zapisac
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "Zapisz do pliku CSV", "", "Pliki CSV (*.csv);;Wszystkie pliki (*.*)"
        )

        if not file_path:
            return

        # wybieramy separator
        separator = self.ask_for_separator()
        if separator is None:
            return

        # zapisujemy prostą funkcją!
        success = save_data_to_csv(self.current_data, file_path, separator)

        if success:
            self.statusBar.showMessage(f"Zapisano dane do pliku {os.path.basename(file_path)}")
        else:
            QMessageBox.warning(self, "Błąd", "Nie udało się zapisać pliku.")

    def reset_data(self):
        """
        Resetowanie danych do stanu pierwotnego - teraz prostsze!
        """
        if self.original_data is None:
            QMessageBox.warning(self, "Błąd", "Brak danych do zresetowania.")
            return

        # po prostu kopiujemy oryginalne dane
        self.current_data = self.original_data.copy()

        # aktualizujemy wszystkie taby
        self.update_all_tabs()

        self.statusBar.showMessage("Zresetowano dane do stanu pierwotnego")
        print("dane zresetowane!")

    def update_all_tabs(self):
        """
        Aktualizuje wszystkie zakładki po wczytaniu/zmianie danych
        """
        try:
            if self.current_data is None:
                print("Brak danych do aktualizacji tabs")
                return

            print("Aktualizuję wszystkie zakładki...")

            # aktualizujemy każdą zakładkę - POPRAWIONA METODA
            self.data_preview_tab.update_data(self.current_data)
            self.stats_tab.update_data(self.current_data)
            self.correlation_tab.update_data(self.current_data)
            self.visualization_tab.update_data(self.current_data)
            self.data_processing_tab.update_data(self.current_data)
            self.classification_tab.update_data(self.current_data)

            print("wszystkie taby zaktualizowane!")

        except Exception as error:
            print(f"blad przy aktualizacji tabow: {error}")
            QMessageBox.critical(self, "Błąd aktualizacji", f"Wystąpił błąd: {str(error)}")

    def get_current_data(self):
        """
        Zwraca aktualne dane - pomocnicza funkcja dla tabow
        """
        return self.current_data

    def set_current_data(self, new_data):
        """
        Ustawia nowe dane - pomocnicza funkcja dla tabow
        """
        self.current_data = new_data
        # można powiadomić inne taby o zmianie
        # ale to zrobimy później jak będzie potrzeba

    def show_about_dialog(self):
        """Wyświetlanie okna dialogowego 'O programie'."""
        QMessageBox.about(
            self,
            "O programie",
            "Aplikacja do analizy danych o jakości powietrza\n\n"
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
            "- Reguły asocjacyjne\n\n"
            "Wersja 2.0 - Podejście funkcyjne"
        )