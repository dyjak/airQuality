"""
Moduł zawierający klasę zakładki klasyfikacji i grupowania.
POPRAWIONY - używa prostych funkcji z utils.
"""
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel,
                             QComboBox, QPushButton, QListWidget, QAbstractItemView,
                             QSpinBox, QDoubleSpinBox, QSplitter, QTableWidget,
                             QTableWidgetItem, QTabWidget, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt

from ..matplotlib_canvas import MatplotlibCanvas, NavigationToolbar


class ClassificationTab(QWidget):
    """Zakładka klasyfikacji i grupowania."""

    def __init__(self, status_bar):
        """
        Inicjalizacja zakładki klasyfikacji i grupowania.

        Args:
            status_bar (QStatusBar): Pasek stanu głównego okna.
        """
        super(ClassificationTab, self).__init__()

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

        # Klasyfikacja
        classification_group = QGroupBox("Klasyfikacja")
        classification_layout = QVBoxLayout()

        # Wybór cech
        self.classification_features_list = QListWidget()
        self.classification_features_list.setSelectionMode(QAbstractItemView.MultiSelection)

        classification_layout.addWidget(QLabel("Wybierz cechy:"))
        classification_layout.addWidget(self.classification_features_list)

        # Wybór etykiety
        self.classification_target_combo = QComboBox()

        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Etykieta:"))
        target_layout.addWidget(self.classification_target_combo)

        classification_layout.addLayout(target_layout)

        # Wybór klasyfikatora
        self.classifier_combo = QComboBox()
        self.classifier_combo.addItems(["Decision Tree", "Random Forest", "SVM", "KNN"])

        classifier_layout = QHBoxLayout()
        classifier_layout.addWidget(QLabel("Klasyfikator:"))
        classifier_layout.addWidget(self.classifier_combo)

        classification_layout.addLayout(classifier_layout)

        # Parametry podziału danych
        test_size_layout = QHBoxLayout()

        self.test_size_spin = QDoubleSpinBox()
        self.test_size_spin.setRange(0.1, 0.9)
        self.test_size_spin.setValue(0.3)
        self.test_size_spin.setSingleStep(0.1)

        test_size_layout.addWidget(QLabel("Rozmiar zbioru testowego:"))
        test_size_layout.addWidget(self.test_size_spin)

        classification_layout.addLayout(test_size_layout)

        # Przycisk do klasyfikacji
        classify_button = QPushButton("Klasyfikuj")
        classify_button.clicked.connect(self.classify_data)
        classification_layout.addWidget(classify_button)

        classification_group.setLayout(classification_layout)
        control_layout.addWidget(classification_group)

        # Grupowanie
        clustering_group = QGroupBox("Grupowanie")
        clustering_layout = QVBoxLayout()

        # Wybór cech
        self.clustering_features_list = QListWidget()
        self.clustering_features_list.setSelectionMode(QAbstractItemView.MultiSelection)

        clustering_layout.addWidget(QLabel("Wybierz cechy:"))
        clustering_layout.addWidget(self.clustering_features_list)

        # Liczba klastrów
        clusters_layout = QHBoxLayout()

        self.n_clusters_spin = QSpinBox()
        self.n_clusters_spin.setRange(2, 10)
        self.n_clusters_spin.setValue(3)

        clusters_layout.addWidget(QLabel("Liczba klastrów:"))
        clusters_layout.addWidget(self.n_clusters_spin)

        clustering_layout.addLayout(clusters_layout)

        # Metoda grupowania
        self.clustering_method_combo = QComboBox()
        self.clustering_method_combo.addItems(["K-means", "Hierarchical", "DBSCAN"])

        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("Metoda:"))
        method_layout.addWidget(self.clustering_method_combo)

        clustering_layout.addLayout(method_layout)

        # Przycisk do grupowania
        cluster_button = QPushButton("Grupuj")
        cluster_button.clicked.connect(self.cluster_data)
        clustering_layout.addWidget(cluster_button)

        clustering_group.setLayout(clustering_layout)
        control_layout.addWidget(clustering_group)

        # Reguły asocjacyjne (uproszczone - bez implementacji)
        association_group = QGroupBox("Reguły asocjacyjne")
        association_layout = QVBoxLayout()

        association_info = QLabel("Funkcjonalność w trakcie implementacji...")
        association_layout.addWidget(association_info)

        association_group.setLayout(association_layout)
        control_layout.addWidget(association_group)

        # Panel z wynikami
        results_panel = QTabWidget()

        # Zakładka wyników klasyfikacji
        self.classification_results_tab = QWidget()
        classification_results_layout = QVBoxLayout(self.classification_results_tab)

        self.classification_results_text = QTextEdit()
        self.classification_results_text.setReadOnly(True)

        classification_results_layout.addWidget(self.classification_results_text)

        # Zakładka wyników grupowania
        self.clustering_results_tab = QWidget()
        clustering_results_layout = QVBoxLayout(self.clustering_results_tab)

        self.clustering_canvas = MatplotlibCanvas(self, width=8, height=6)
        self.clustering_toolbar = NavigationToolbar(self.clustering_canvas, self)

        clustering_results_layout.addWidget(self.clustering_toolbar)
        clustering_results_layout.addWidget(self.clustering_canvas)

        # Dodanie zakładek do panelu wyników
        results_panel.addTab(self.classification_results_tab, "Klasyfikacja")
        results_panel.addTab(self.clustering_results_tab, "Grupowanie")

        # Splitter do dzielenia paneli
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(control_panel)
        splitter.addWidget(results_panel)
        splitter.setSizes([400, 600])

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
            print(f"ClassificationTab: zaktualizowano dane ({len(data)} wierszy, {len(columns)} kolumn)")

    def update_columns(self, columns):
        """
        Aktualizacja list kolumn.

        Args:
            columns (list): Lista nazw kolumn.
        """
        self.classification_features_list.clear()
        self.classification_features_list.addItems(columns)

        self.classification_target_combo.clear()
        self.classification_target_combo.addItems(columns)

        self.clustering_features_list.clear()
        self.clustering_features_list.addItems(columns)

    def classify_data(self):
        """Klasyfikacja danych - uproszczona implementacja."""
        if self.current_data is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do klasyfikacji."
            )
            return

        # Pobranie wybranych cech
        selected_items = self.classification_features_list.selectedItems()

        if not selected_items:
            QMessageBox.warning(
                self, "Błąd", "Nie wybrano cech."
            )
            return

        features = [item.text() for item in selected_items]

        # Pobranie etykiety
        target = self.classification_target_combo.currentText()

        if not target:
            QMessageBox.warning(
                self, "Błąd", "Nie wybrano etykiety."
            )
            return

        # Sprawdzenie czy wybrane kolumny istnieją i czy target nie jest w features
        if target in features:
            QMessageBox.warning(
                self, "Błąd", "Etykieta nie może być jednocześnie cechą."
            )
            return

        try:
            # Proste sprawdzenie danych
            from sklearn.model_selection import train_test_split
            from sklearn.tree import DecisionTreeClassifier
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.svm import SVC
            from sklearn.neighbors import KNeighborsClassifier
            from sklearn.metrics import accuracy_score, classification_report

            # Przygotowanie danych
            X = self.current_data[features].dropna()
            y = self.current_data.loc[X.index, target].dropna()

            # Sprawdzenie czy mamy dane
            if len(X) == 0 or len(y) == 0:
                QMessageBox.warning(self, "Błąd", "Brak danych po usunięciu braków.")
                return

            # Podział na zbiór treningowy i testowy
            test_size = self.test_size_spin.value()
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )

            # Wybór klasyfikatora
            classifier_type_text = self.classifier_combo.currentText()

            if classifier_type_text == "Decision Tree":
                classifier = DecisionTreeClassifier(random_state=42)
            elif classifier_type_text == "Random Forest":
                classifier = RandomForestClassifier(random_state=42, n_estimators=100)
            elif classifier_type_text == "SVM":
                classifier = SVC(random_state=42)
            elif classifier_type_text == "KNN":
                classifier = KNeighborsClassifier()
            else:
                QMessageBox.warning(self, "Błąd", "Nieznany typ klasyfikatora.")
                return

            # Trenowanie i predykcja
            classifier.fit(X_train, y_train)
            y_pred = classifier.predict(X_test)

            # Obliczenie wyników
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

            # Aktualizacja wyników
            self.classification_results_text.clear()
            self.classification_results_text.append(f"Klasyfikator: {classifier_type_text}")
            self.classification_results_text.append(f"Cechy: {', '.join(features)}")
            self.classification_results_text.append(f"Etykieta: {target}")
            self.classification_results_text.append(f"Rozmiar zbioru testowego: {test_size}")
            self.classification_results_text.append(f"Rozmiar danych: {len(X)} próbek")
            self.classification_results_text.append(f"\nDokładność: {accuracy:.4f}")

            self.classification_results_text.append("\nRaport klasyfikacji:")
            for label, metrics in report.items():
                if isinstance(metrics, dict):
                    self.classification_results_text.append(f"\nKlasa: {label}")
                    for metric, value in metrics.items():
                        if isinstance(value, (int, float)):
                            self.classification_results_text.append(f"  {metric}: {value:.4f}")

            self.status_bar.showMessage(f"Dokonano klasyfikacji: {classifier_type_text}, dokładność: {accuracy:.4f}")

        except ImportError:
            QMessageBox.warning(
                self, "Błąd", "Brak biblioteki scikit-learn. Zainstaluj: pip install scikit-learn"
            )
        except Exception as error:
            print(f"Błąd przy klasyfikacji: {error}")
            QMessageBox.critical(
                self, "Błąd", f"Wystąpił błąd: {str(error)}"
            )

    def cluster_data(self):
        """Grupowanie danych - uproszczona implementacja."""
        if self.current_data is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do grupowania."
            )
            return

        import matplotlib.pyplot as plt

        # Pobranie wybranych cech
        selected_items = self.clustering_features_list.selectedItems()

        if not selected_items:
            QMessageBox.warning(
                self, "Błąd", "Nie wybrano cech."
            )
            return

        features = [item.text() for item in selected_items]

        # Pobranie parametrów
        n_clusters = self.n_clusters_spin.value()
        method_text = self.clustering_method_combo.currentText()

        try:
            from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
            from sklearn.preprocessing import StandardScaler

            # Przygotowanie danych - konwersja na numeryczne
            data_for_clustering = self.current_data[features].copy()

            # Konwertujemy każdą kolumnę na numeryczną
            numeric_columns = []
            for feature in features:
                try:
                    numeric_series = pd.to_numeric(data_for_clustering[feature], errors='coerce')
                    if not numeric_series.isna().all():
                        data_for_clustering[feature] = numeric_series
                        numeric_columns.append(feature)
                    else:
                        print(f"Kolumna {feature} nie zawiera danych numerycznych")
                except:
                    print(f"Nie można przekonwertować kolumny {feature}")

            if not numeric_columns:
                QMessageBox.warning(self, "Błąd", "Żadna z wybranych cech nie zawiera danych numerycznych.")
                return

            # Bierzemy tylko kolumny numeryczne i usuwamy braki
            numeric_data = data_for_clustering[numeric_columns].dropna()

            if len(numeric_data) == 0:
                QMessageBox.warning(self, "Błąd", "Brak danych po usunieciu braków.")
                return

            print(f"Grupowanie dla {len(numeric_data)} wierszy i {len(numeric_columns)} cech")

            # Skalowanie danych
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(numeric_data)

            # Wybór metody grupowania
            if method_text == "K-means":
                clustering = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            elif method_text == "Hierarchical":
                clustering = AgglomerativeClustering(n_clusters=n_clusters)
            elif method_text == "DBSCAN":
                clustering = DBSCAN(eps=0.5, min_samples=5)
            else:
                QMessageBox.warning(self, "Błąd", "Nieznana metoda grupowania.")
                return

            # Grupowanie
            labels = clustering.fit_predict(scaled_data)

            # Sprawdzenie czy znaleziono klastry
            unique_labels = np.unique(labels)
            n_clusters_found = len(unique_labels)

            if n_clusters_found <= 1:
                QMessageBox.warning(self, "Błąd",
                                    f"Znaleziono tylko {n_clusters_found} klastrów. Spróbuj innych parametrów.")
                return

            print(f"Znaleziono {n_clusters_found} klastrów")

            # Tworzenie wykresu
            self.clustering_canvas.fig.clear()

            if len(numeric_columns) >= 2:
                # Wykres 2D - używamy pierwszych dwóch cech
                ax = self.clustering_canvas.fig.add_subplot(111)

                # Tworzenie wykresu punktowego z kolorami klastrów
                scatter = ax.scatter(
                    numeric_data.iloc[:, 0],
                    numeric_data.iloc[:, 1],
                    c=labels,
                    cmap='viridis',
                    alpha=0.7,
                    s=50
                )

                ax.set_title(f"Grupowanie: {method_text} ({n_clusters_found} klastrów)")
                ax.set_xlabel(numeric_columns[0])
                ax.set_ylabel(numeric_columns[1])
                ax.grid(True, alpha=0.3)

                # Dodanie kolorowej legendy
                import matplotlib.pyplot as plt
                cbar = plt.colorbar(scatter, ax=ax)
                cbar.set_label('Numer klastra')

            else:
                # Wykres słupkowy liczebności klastrów dla jednej cechy
                ax = self.clustering_canvas.fig.add_subplot(111)
                unique_labels, counts = np.unique(labels, return_counts=True)

                colors = plt.cm.viridis(np.linspace(0, 1, len(unique_labels)))
                bars = ax.bar(unique_labels, counts, color=colors, edgecolor='black', alpha=0.7)

                ax.set_title(f"Liczebność klastrów: {method_text}")
                ax.set_xlabel("Numer klastra")
                ax.set_ylabel("Liczba punktów")

                # Dodanie wartości na słupkach
                for bar, count in zip(bars, counts):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                            f'{count}', ha='center', va='bottom', fontweight='bold')

                ax.grid(True, alpha=0.3, axis='y')

            # Odświeżenie wykresu
            self.clustering_canvas.fig.tight_layout()
            self.clustering_canvas.draw()

            self.status_bar.showMessage(
                f"Grupowanie: {method_text}, {n_clusters_found} klastrów, {len(numeric_data)} punktów")
            print(f"Grupowanie zakończone pomyślnie")

        except ImportError:
            QMessageBox.warning(
                self, "Błąd", "Brak biblioteki scikit-learn. Zainstaluj: pip install scikit-learn"
            )
        except Exception as error:
            print(f"Błąd przy grupowaniu: {error}")
            QMessageBox.critical(
                self, "Błąd", f"Wystąpił błąd: {str(error)}"
            )