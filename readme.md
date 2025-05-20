# Analiza Danych AirQuality

## Struktura projektu

- `main.py` - Główny plik aplikacji
- `data_loader.py` - Moduł wczytywania danych
- `data_processor.py` - Moduł przetwarzania danych
- `data_visualizer.py` - Moduł wizualizacji danych
- `gui/` - Katalog zawierający moduły interfejsu użytkownika
  - `__init__.py` - Plik inicjalizacyjny pakietu GUI
  - `main_window.py` - Implementacja głównego okna aplikacji
  - `matplotlib_canvas.py` - Klasa do osadzania wykresów Matplotlib w PyQt
  - `tabs/` - Katalog zawierający implementacje poszczególnych zakładek
    - `__init__.py` - Plik inicjalizacyjny pakietu zakładek
    - `data_preview_tab.py` - Zakładka podglądu danych
    - `stats_tab.py` - Zakładka analizy statystycznej
    - `correlation_tab.py` - Zakładka korelacji
    - `visualization_tab.py` - Zakładka wizualizacji
    - `data_processing_tab.py` - Zakładka przetwarzania danych
    - `classification_tab.py` - Zakładka klasyfikacji i grupowania

## Interfejs użytkownika

Interfejs użytkownika składa się z następujących zakładek:

1. **Podgląd danych** - Wyświetla podstawowe informacje o danych oraz ich podgląd w formie tabeli.
2. **Analiza statystyczna** - Umożliwia obliczanie różnych miar statystycznych dla wybranych kolumn.
3. **Korelacje** - Pozwala na obliczanie i wizualizację macierzy korelacji między kolumnami.
4. **Wizualizacja** - Umożliwia tworzenie różnych typów wykresów (histogramy, wykresy pudełkowe, wykresy punktowe, wykresy szeregów czasowych, wykresy słupkowe, wykresy kołowe, mapy ciepła, wykresy par).
5. **Przetwarzanie danych** - Zawiera narzędzia do przetwarzania danych (ekstrakcja podzbioru, zastępowanie wartości, skalowanie i standaryzacja, obsługa brakujących wartości, usuwanie duplikatów, kodowanie binarne).
6. **Klasyfikacja i grupowanie** - Umożliwia klasyfikację i grupowanie danych oraz znajdowanie reguł asocjacyjnych.
