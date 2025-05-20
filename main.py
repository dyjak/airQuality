"""
Główny plik aplikacji do analizy danych o jakości powietrza.

Program pozwala na wczytywanie, przetwarzanie i wizualizację danych o jakości powietrza.
Jest to projekt hurtowni danych, który implementuje różne funkcjonalności związane
z przetwarzaniem i analizą danych.

Funkcjonalności:
- Odczyt danych z pliku CSV
- Obliczanie miar statystycznych (min, max, odchylenie std., mediana, moda, inne)
- Wyznaczanie korelacji cech / atrybutów
- Ekstrakcja podzbioru poprzez podanie numerów/nazw wierszy/kolumn
- Zastępowanie wartości w tabelach danych (zamiana wartości z danej kolumny na inną)
- Skalowanie i standaryzacja kolumn w tabelach danych
- Usuwanie wierszy z brakującymi wartościami i wypełnianie pustych miejsc
- Usuwanie powtarzających się miejsc w tabelach danych
- Kodowanie binarne kolumn symbolicznych
- Proste wykresy dot. danych
- Klasyfikacja, grupowanie i reguły asocjacyjne

Zestaw danych użyty w projekcie:
Air Quality - https://archive.ics.uci.edu/dataset/360/air+quality
"""
import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow


def main():
    """
    Funkcja główna aplikacji.

    Tworzy i uruchamia główne okno aplikacji.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()