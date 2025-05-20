"""
Moduł zawierający klasę zakładki klasyfikacji i grupowania.
"""
import numpy as np
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel,
                             QComboBox, QPushButton, QListWidget, QAbstractItemView,
                             QSpinBox, QDoubleSpinBox, QSplitter, QTableWidget,
                             QTableWidgetItem, QTabWidget, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt

from ..matplotlib_canvas import MatplotlibCanvas, NavigationToolbar


class ClassificationTab(QWidget):
    """Zakładka klasyfikacji i grupowania."""

    def __init__(self, data_processor, status_bar):
        """
        Inicjalizacja zakładki klasyfikacji i grupowania.

        Args:
            data_processor (DataProcessor): Obiekt przetwarzający dane.
            status_bar (QStatusBar): Pasek stanu głównego okna.
        """
        super(ClassificationTab, self).__init__()

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

        # Reguły asocjacyjne
        association_group = QGroupBox("Reguły asocjacyjne")
        association_layout = QVBoxLayout()

        # Minimalne wsparcie
        support_layout = QHBoxLayout()

        self.min_support_spin = QDoubleSpinBox()
        self.min_support_spin.setRange(0.01, 1.0)
        self.min_support_spin.setValue(0.1)
        self.min_support_spin.setSingleStep(0.01)

        support_layout.addWidget(QLabel("Minimalne wsparcie:"))
        support_layout.addWidget(self.min_support_spin)

        association_layout.addLayout(support_layout)

        # Minimalna pewność
        confidence_layout = QHBoxLayout()

        self.min_confidence_spin = QDoubleSpinBox()
        self.min_confidence_spin.setRange(0.01, 1.0)
        self.min_confidence_spin.setValue(0.5)
        self.min_confidence_spin.setSingleStep(0.01)

        confidence_layout.addWidget(QLabel("Minimalna pewność:"))
        confidence_layout.addWidget(self.min_confidence_spin)

        association_layout.addLayout(confidence_layout)

        # Minimalny współczynnik podniesienia
        lift_layout = QHBoxLayout()

        self.min_lift_spin = QDoubleSpinBox()
        self.min_lift_spin.setRange(0.01, 10.0)
        self.min_lift_spin.setValue(1.0)
        self.min_lift_spin.setSingleStep(0.01)

        lift_layout.addWidget(QLabel("Minimalny współczynnik podniesienia:"))
        lift_layout.addWidget(self.min_lift_spin)

        association_layout.addLayout(lift_layout)

        # Przycisk do znajdowania reguł
        find_rules_button = QPushButton("Znajdź reguły")
        find_rules_button.clicked.connect(self.find_association_rules)
        association_layout.addWidget(find_rules_button)

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

        # Zakładka wyników reguł asocjacyjnych
        self.association_results_tab = QWidget()
        association_results_layout = QVBoxLayout(self.association_results_tab)

        self.association_rules_table = QTableWidget()

        association_results_layout.addWidget(self.association_rules_table)

        # Dodanie zakładek do panelu wyników
        results_panel.addTab(self.classification_results_tab, "Klasyfikacja")
        results_panel.addTab(self.clustering_results_tab, "Grupowanie")
        results_panel.addTab(self.association_results_tab, "Reguły asocjacyjne")

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
        self.classification_features_list.clear()
        self.classification_features_list.addItems(columns)

        self.classification_target_combo.clear()
        self.classification_target_combo.addItems(columns)

        self.clustering_features_list.clear()
        self.clustering_features_list.addItems(columns)

    def classify_data(self):
        """Klasyfikacja danych."""
        if self.data_processor.get_data() is None:
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

        # Pobranie typu klasyfikatora
        classifier_type_text = self.classifier_combo.currentText()

        if classifier_type_text == "Decision Tree":
            classifier_type = 'decision_tree'
        elif classifier_type_text == "Random Forest":
            classifier_type = 'random_forest'
        elif classifier_type_text == "SVM":
            classifier_type = 'svm'
        elif classifier_type_text == "KNN":
            classifier_type = 'knn'
        else:
            QMessageBox.warning(
                self, "Błąd", "Nieznany typ klasyfikatora."
            )
            return

        # Pobranie rozmiaru zbioru testowego
        test_size = self.test_size_spin.value()

        # Klasyfikacja danych
        result = self.data_processor.classify_data(
            features, target, classifier_type=classifier_type, test_size=test_size
        )

        if result:
            # Aktualizacja pola tekstowego z wynikami
            self.classification_results_text.clear()
            self.classification_results_text.append(f"Klasyfikator: {classifier_type_text}")
            self.classification_results_text.append(f"Cechy: {', '.join(features)}")
            self.classification_results_text.append(f"Etykieta: {target}")
            self.classification_results_text.append(f"Rozmiar zbioru testowego: {test_size}")
            self.classification_results_text.append(f"\nDokładność: {result['accuracy']:.4f}")

            # Dodanie raportu klasyfikacji
            self.classification_results_text.append("\nRaport klasyfikacji:")
            for label, metrics in result['classification_report'].items():
                if isinstance(metrics, dict):
                    self.classification_results_text.append(f"\nKlasa: {label}")
                    for metric, value in metrics.items():
                        self.classification_results_text.append(f"  {metric}: {value:.4f}")

            self.status_bar.showMessage(f"Dokonano klasyfikacji danych: {classifier_type_text}")

            # Przełączenie na zakładkę z wynikami klasyfikacji
            self.parent().tabs.setCurrentIndex(self.parent().tabs.indexOf(self))
        else:
            QMessageBox.warning(
                self, "Błąd", "Nie udało się dokonać klasyfikacji danych."
            )

    def cluster_data(self):
        """Grupowanie danych."""
        if self.data_processor.get_data() is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do grupowania."
            )
            return

        # Pobranie wybranych cech
        selected_items = self.clustering_features_list.selectedItems()

        if not selected_items:
            QMessageBox.warning(
                self, "Błąd", "Nie wybrano cech."
            )
            return

        features = [item.text() for item in selected_items]

        # Pobranie liczby klastrów
        n_clusters = self.n_clusters_spin.value()

        # Pobranie metody grupowania
        method_text = self.clustering_method_combo.currentText()

        if method_text == "K-means":
            method = 'kmeans'
        elif method_text == "Hierarchical":
            method = 'hierarchical'
        elif method_text == "DBSCAN":
            method = 'dbscan'
        else:
            QMessageBox.warning(
                self, "Błąd", "Nieznana metoda grupowania."
            )
            return

        # Grupowanie danych
        result = self.data_processor.cluster_data(
            features, n_clusters=n_clusters, method=method
        )

        if result:
            # Aktualizacja wykresu grupowania
            self.clustering_canvas.fig.clear()

            # Jeśli mamy dokładnie 2 cechy, możemy narysować wykres punktowy
            if len(features) == 2:
                # Pobranie danych
                data = result['result_data']
                labels = result['labels']

                # Rysowanie wykresu
                ax = self.clustering_canvas.fig.add_subplot(111)
                scatter = ax.scatter(data[features[0]], data[features[1]], c=labels, cmap='viridis')

                # Dodanie legendy
                legend1 = ax.legend(*scatter.legend_elements(), title="Klastry")
                ax.add_artist(legend1)

                # Dodanie tytułu i etykiet osi
                ax.set_title(f"Grupowanie: {method_text}")
                ax.set_xlabel(features[0])
                ax.set_ylabel(features[1])

                # Dodanie siatki
                ax.grid(True, linestyle='--', alpha=0.7)
            else:
                # Jeśli mamy więcej niż 2 cechy, rysujemy wykres słupkowy liczebności klastrów
                ax = self.clustering_canvas.fig.add_subplot(111)

                # Zliczanie wystąpień każdego klastra
                unique_labels, counts = np.unique(result['labels'], return_counts=True)

                # Rysowanie wykresu słupkowego
                ax.bar(unique_labels, counts, color='skyblue', edgecolor='black')

                # Dodanie tytułu i etykiet osi
                ax.set_title(f"Liczebność klastrów: {method_text}")
                ax.set_xlabel("Klaster")
                ax.set_ylabel("Liczba punktów")

                # Dodanie etykiet wartości na słupkach
                for i, v in enumerate(counts):
                    ax.text(i, v + 0.1, str(v), ha='center')

                # Dodanie siatki
                ax.grid(True, linestyle='--', alpha=0.7, axis='y')

            # Aktualizacja wykresu
            self.clustering_canvas.draw()

            self.status_bar.showMessage(f"Dokonano grupowania danych: {method_text}, {n_clusters} klastrów")

            # Przełączenie na zakładkę z wynikami grupowania
            self.parent().tabs.setCurrentWidget(self)
        else:
            QMessageBox.warning(
                self, "Błąd", "Nie udało się dokonać grupowania danych."
            )

    def find_association_rules(self):
        """Znajdowanie reguł asocjacyjnych."""
        if self.data_processor.get_data() is None:
            QMessageBox.warning(
                self, "Błąd", "Brak danych do analizy."
            )
            return

        # Pobranie parametrów
        min_support = self.min_support_spin.value()
        min_confidence = self.min_confidence_spin.value()
        min_lift = self.min_lift_spin.value()

        # Znajdowanie reguł asocjacyjnych
        rules = self.data_processor.find_association_rules(
            min_support=min_support, min_confidence=min_confidence, min_lift=min_lift
        )

        if rules is not None and not rules.empty:
            # Aktualizacja tabeli reguł
            self.association_rules_table.setRowCount(len(rules))
            self.association_rules_table.setColumnCount(len(rules.columns))
            self.association_rules_table.setHorizontalHeaderLabels(list(rules.columns))

            for i in range(len(rules)):
                for j, col in enumerate(rules.columns):
                    value = rules.iloc[i, j]

                    # Formatowanie wartości w zależności od typu
                    if isinstance(value, float):
                        formatted_value = f"{value:.4f}"
                    else:
                        formatted_value = str(value)

                    self.association_rules_table.setItem(i, j, QTableWidgetItem(formatted_value))

            # Dopasowanie szerokości kolumn
            self.association_rules_table.resizeColumnsToContents()

            self.status_bar.showMessage(f"Znaleziono {len(rules)} reguł asocjacyjnych")

            # Przełączenie na zakładkę z wynikami reguł asocjacyjnych
            self.parent().tabs.setCurrentWidget(self)
        else:
            QMessageBox.warning(
                self, "Błąd", "Nie znaleziono reguł asocjacyjnych spełniających podane kryteria."
            )