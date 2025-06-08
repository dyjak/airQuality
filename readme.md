# AirQuality

Aplikacja służy do kompleksowej analizy danych o jakości powietrza zebranych przez czujniki chemiczne. Wykorzystuje zestaw danych **Air Quality** z UCI Machine Learning Repository, który zawiera pomiary zanieczyszczeń powietrza zebrane w włoskim mieście przez okres od marca 2004 do lutego 2005.

## Dane

Dane pochodzą z wielosensorowej sieci pomiarowej i zawierają następujące atrybuty:

**Informacje czasowe:**
- `Date` - Data pomiaru (DD# Analiza Danych o Jakości Powietrza - Aplikacja GUI

## O projekcie

Aplikacja służy do kompleksowej analizy danych o jakości powietrza zebranych przez czujniki chemiczne. Wykorzystuje zestaw danych **Air Quality** z UCI Machine Learning Repository, który zawiera pomiary zanieczyszczeń powietrza zebrane w włoskim mieście przez okres od marca 2004 do lutego 2005.

## Dane - co analizujemy?

### Struktura zestawu danych
Dane pochodzą z wielosensorowej sieci pomiarowej i zawierają następujące atrybuty:

**Informacje czasowe:**
- `Date` - Data pomiaru (DD/MM/YYYY)
- `Time` - Czas pomiaru (HH.MM.SS)

**Główne zanieczyszczenia:**
- `CO(GT)` - Tlenek węgla (mg/m³) - gaz powstający przy niepełnym spalaniu, niebezpieczny dla zdrowia
- `NOx(GT)` - Tlenki azotu (ppb) - powstają w silnikach i elektrowniach, powodują smog
- `NO2(GT)` - Dwutlenek azotu (µg/m³) - jeden z głównych składników smogu miejskiego

**Pomiary sensorów:**
- `PT08.S1(CO)` - Odpowiedź sensora tlenku węgla (nieznormalizowana)
- `PT08.S2(NMHC)` - Odpowiedź sensora niemetanowych węglowodorów
- `PT08.S3(NOx)` - Odpowiedź sensora tlenków azotu
- `PT08.S4(NO2)` - Odpowiedź sensora dwutlenku azotu
- `PT08.S5(O3)` - Odpowiedź sensora ozonu

**Dodatkowe parametry:**
- `NMHC(GT)` - Niemetanowe węglowodory (µg/m³) - składniki benzyny i rozpuszczalników
- `C6H6(GT)` - Benzen (µg/m³) - rakotwórczy związek organiczny
- `T` - Temperatura (°C)
- `RH` - Wilgotność względna (%)
- `AH` - Wilgotność bezwzględna

**Specjalne wartości:**
- `-200` - oznacza brakujące pomiary (automatycznie zamieniane na NaN)

## Architektura aplikacji

### 1. Struktura modułów

```
airQuality/
├── main.py                    # Punkt wejścia aplikacji
├── gui/                       # Interfejs użytkownika (PyQt5)
│   ├── main_window.py        # Główne okno aplikacji
│   ├── matplotlib_canvas.py   # Integracja wykresów z GUI
│   └── tabs/                 # Poszczególne zakładki
└── utils/                    # Funkcje przetwarzania danych
    ├── data_loader.py        # Wczytywanie CSV
    ├── data_processor.py     # Obliczenia i transformacje
    └── visualization.py      # Tworzenie wykresów
```

### 2. Główne komponenty

**main.py**
- Inicjalizuje aplikację PyQt5
- Tworzy główne okno (`MainWindow`)
- Uruchamia pętlę wydarzeń

**gui/main_window.py**
- Klasa `MainWindow` - główne okno aplikacji
- Zarządza wczytywaniem i zapisywaniem danych
- Koordynuje komunikację między zakładkami
- Funkcje: `load_data_from_csv()`, `save_data_to_csv()`, `reset_data()`

## Funkcjonalności aplikacji

### 1. Wczytywanie i podgląd danych

**Lokalizacja:** `utils/data_loader.py`, `gui/tabs/data_previews.py`

**Funkcje kluczowe:**
- `load_csv_data()` - wczytuje CSV z automatyczną obsługą kodowania i separatorów
- `check_basic_info()` - analizuje podstawowe właściwości zbioru
- `check_missing_data()` - identyfikuje braki w danych

**Co robi:**
1. Automatycznie wykrywa separator (`;`, `,`, `\t`)
2. Obsługuje europejskie kodowanie (ISO-8859-1)
3. Zamienia wartości `-200` na `NaN`
4. Wyświetla statystyki: rozmiar, typy danych, braki, duplikaty
5. Pokazuje pierwsze 100 wierszy w tabeli

### 2. Analiza statystyczna

**Lokalizacja:** `utils/data_processor.py`, `gui/tabs/stats_tab.py`

**Funkcja kluczowa:** `calculate_basic_statistics()`

**Dla danych numerycznych oblicza:**
- Podstawowe: minimum, maksimum, średnia, mediana
- Rozrzut: odchylenie standardowe, wariancja, rozstęp międzykwartylowy
- Kształt rozkładu: skośność (czy dane są przesunięte w lewo/prawo)
- Kwantyle: Q1 (25%), Q3 (75%)
- Braki: liczba i procent brakujących wartości

**Dla danych tekstowych:**
- Liczba unikalnych wartości
- Najczęściej występująca wartość i jej częstość

### 3. Analiza korelacji

**Lokalizacja:** `utils/data_processor.py`, `gui/tabs/correlation_tab.py`

**Funkcja kluczowa:** `calculate_correlation()`

**Dostępne metody:**
- **Pearson** - mierzy liniową zależność (standardowa korelacja)
- **Spearman** - mierzy monotoniczną zależność (odporna na wartości odstające)
- **Kendall** - alternatywa dla Spearman, lepsza dla małych zbiorów

**Wizualizacja:**
- Tabela z kolorowaniem komórek (czerwone = silna korelacja)
- Mapa ciepła (heatmap) z gradientem kolorów
- Wartości od -1 (korelacja ujemna) do +1 (korelacja dodatnia)

### 4. Wizualizacja danych

**Lokalizacja:** `utils/visualization.py`, `gui/tabs/visualization_tab.py`

**Dostępne wykresy:**

#### Histogram (`create_histogram()`)
- Pokazuje rozkład wartości w kolumnie
- Dodaje linie ze średnią (czerwona) i medianą (zielona)
- Parametr: liczba przedziałów (bins)

#### Wykres pudełkowy (`create_boxplot()`)
- Wizualizuje kwartyle, medianę i wartości odstające
- Ideal do identyfikacji outlierów w danych o zanieczyszczeniach

#### Wykres punktowy (`create_scatter_plot()`)
- Pokazuje zależność między dwoma zmiennymi
- Dodaje linię trendu z równaniem
- Przydatny do analizy korelacji (np. temperatura vs wilgotność)

#### Wykres liniowy (`create_line_plot()`)
- Idealny dla szeregów czasowych
- Pokazuje zmiany zanieczyszczeń w czasie
- Automatycznie sortuje dane po osi X

#### Wykres słupkowy (`create_bar_chart()`)
- Porównuje kategorie lub średnie wartości
- Dodaje wartości na słupkach
- Obsługuje długie etykiety (obraca o 45°)

#### Wykres kołowy (`create_pie_chart()`)
- Pokazuje proporcje kategorii
- Ogranicza do 8 głównych kategorii (reszta w "Inne")
- Wyświetla procentowe udziały

#### Mapa korelacji (`create_correlation_heatmap()`)
- Zaawansowana wizualizacja macierzy korelacji
- Używa biblioteki Seaborn dla profesjonalnego wyglądu
- Skala kolorów od niebieskiego (ujemna) do czerwonego (dodatnia)

**Wspólne funkcje:**
- `setup_plot_style()` - ustawia jednolity styl wykresów
- `save_plot()` - zapisuje wykresy w formatach PNG, JPG, SVG, PDF

### 5. Przetwarzanie danych

**Lokalizacja:** `utils/data_processor.py`, `gui/tabs/data_processing_tab.py`

#### Obsługa brakujących wartości (`handle_missing_values()`)
**Strategie:**
- **Usuń wiersze** - eliminuje rekordy z brakami
- **Wypełnij średnią** - dla danych numerycznych
- **Wypełnij medianą** - odporna na wartości odstające
- **Wypełnij modą** - najczęstsza wartość (dla wszystkich typów)
- **Wypełnij wartością** - użytkownik podaje własną wartość

#### Skalowanie danych (`scale_data()`)
**Metody:**
- **MinMax (0-1)** - przekształca wszystkie wartości do zakresu 0-1
- **Standard (z-score)** - średnia=0, odchylenie standardowe=1
- Tworzy nowe kolumny z sufiksem `_scaled`

#### Usuwanie duplikatów (`remove_duplicates()`)
- Może sprawdzać wszystkie kolumny lub wybrane
- Zachowuje pierwszy wystąpienie duplikatu
- Resetuje indeksy po usunięciu

#### Zamiana wartości (`replace_values()`)
- Zamienia konkretne wartości w wybranej kolumnie
- Przydatne do standaryzacji danych (np. "tak"→1, "nie"→0)
- Automatycznie wykrywa typ danych

#### Ekstrakcja podzbiorów (`extract_subset()`)
- Wybiera konkretne kolumny i/lub wiersze
- Tworzy nową ramkę danych
- Waliduje istnienie wybranych elementów

### 6. Klasyfikacja i grupowanie

**Lokalizacja:** `gui/tabs/classification_tab.py`

#### Klasyfikacja (nadzorowana)
**Dostępne algorytmy:**
- **Decision Tree** - drzewo decyzyjne, interpretowalne reguły
- **Random Forest** - zespół drzew, wyższa dokładność
- **SVM** - maszyna wektorów nośnych, dobra dla nieliniowych danych
- **KNN** - k-najbliższych sąsiadów, prosty ale skuteczny

**Proces:**
1. Wybór cech (zmiennych niezależnych)
2. Wybór etykiety (zmienna zależna)
3. Podział na zbiór treningowy/testowy
4. Trenowanie modelu
5. Ewaluacja: dokładność, raport klasyfikacji

#### Grupowanie (nienadzorowane)
**Algorytmy:**
- **K-means** - dzieli dane na k okrągłych grup
- **Hierarchical** - tworzy hierarchię grup (dendrogram)
- **DBSCAN** - znajduje grupy o różnych kształtach, ignoruje outliers

**Wizualizacja:**
- Wykres 2D z kolorowaniem klastrów (dla 2 cech)
- Wykres słupkowy liczebności klastrów

### 7. Integracja z GUI

**matplotlib_canvas.py**
- Klasa `MatplotlibCanvas` integruje wykresy Matplotlib z PyQt5
- Umożliwia interaktywną nawigację (zoom, pan)
- Toolbar z narzędziami do zapisywania i edycji wykresów

**Komunikacja między modułami:**
1. `MainWindow` wczytuje dane funkcją z `utils/data_loader.py`
2. Dane przekazywane są do wszystkich zakładek przez `update_data()`
3. Każda zakładka używa funkcji z `utils/` do przetwarzania
4. Wyniki wyświetlane są w tabelach lub na wykresach

## Przykładowe zastosowania

### Analiza zanieczyszczeń miejskich
1. **Wczytaj dane** AirQualityUCI.csv
2. **Podgląd** - sprawdź braki w danych (szczególnie w sensorach PT08)
3. **Statystyki** - przeanalizuj rozkład CO(GT) i NO2(GT)
4. **Korelacja** - znajdź zależności między temperaturą a zanieczyszczeniami
5. **Wizualizacja** - stwórz szeregi czasowe pokazujące zmiany w czasie
6. **Przetwarzanie** - wypełnij braki medianą, przeskaluj dane
7. **Grupowanie** - znajdź dni o podobnych wzorcach zanieczyszczeń

### Identyfikacja wzorców sezonowych
1. Utwórz wykres liniowy CO(GT) w funkcji czasu
2. Przeanalizuj korelację temperatury z poziomem zanieczyszczeń
3. Pogrupuj dni według podobieństwa profili zanieczyszczeń
4. Zidentyfikuj anomalie (dni o nietypowo wysokich wartościach)

### Porównanie czujników
1. Oblicz korelacje między pomiarami referencyjnymi (GT) a czujnikami (PT08)
2. Sprawdź które czujniki są najbardziej wiarygodne
3. Znajdź czujniki z największą liczbą braków danych

## Technologie i biblioteki

- **PyQt5** - interfejs graficzny
- **pandas** - manipulacja danych
- **numpy** - obliczenia numeryczne  
- **matplotlib** - podstawowe wykresy
- **seaborn** - zaawansowane wizualizacje
- **scikit-learn** - uczenie maszynowe
- **functools** - podejście funkcyjne zamiast obiektowego

Aplikacja została zaprojektowana z myślą o prostocie użytkowania i modularności kodu. Każda funkcja ma jedno, jasno zdefiniowane zadanie, co ułatwia rozwijanie i debugowanie./MM/YYYY)
- `Time` - Czas pomiaru (HH.MM.SS)

**Główne zanieczyszczenia:**
- `CO(GT)` - Tlenek węgla (mg/m³) - gaz powstający przy niepełnym spalaniu, niebezpieczny dla zdrowia
- `NOx(GT)` - Tlenki azotu (ppb) - powstają w silnikach i elektrowniach, powodują smog
- `NO2(GT)` - Dwutlenek azotu (µg/m³) - jeden z głównych składników smogu miejskiego

**Pomiary sensorów:**
- `PT08.S1(CO)` - Odpowiedź sensora tlenku węgla (nieznormalizowana)
- `PT08.S2(NMHC)` - Odpowiedź sensora niemetanowych węglowodorów
- `PT08.S3(NOx)` - Odpowiedź sensora tlenków azotu
- `PT08.S4(NO2)` - Odpowiedź sensora dwutlenku azotu
- `PT08.S5(O3)` - Odpowiedź sensora ozonu

**Dodatkowe parametry:**
- `NMHC(GT)` - Niemetanowe węglowodory (µg/m³) - składniki benzyny i rozpuszczalników
- `C6H6(GT)` - Benzen (µg/m³) - rakotwórczy związek organiczny
- `T` - Temperatura (°C)
- `RH` - Wilgotność względna (%)
- `AH` - Wilgotność bezwzględna

**Specjalne wartości:**
- `-200` - oznacza brakujące pomiary (automatycznie zamieniane na NaN)

## Architektura aplikacji

### 1. Struktura modułów

```
airQuality/
├── main.py                    # Punkt wejścia aplikacji
├── gui/                       # Interfejs użytkownika (PyQt5)
│   ├── main_window.py        # Główne okno aplikacji
│   ├── matplotlib_canvas.py   # Integracja wykresów z GUI
│   └── tabs/                 # Poszczególne zakładki
└── utils/                    # Funkcje przetwarzania danych
    ├── data_loader.py        # Wczytywanie CSV
    ├── data_processor.py     # Obliczenia i transformacje
    └── visualization.py      # Tworzenie wykresów
```

### 2. Główne komponenty

**main.py**
- Inicjalizuje aplikację PyQt5
- Tworzy główne okno (`MainWindow`)
- Uruchamia pętlę wydarzeń

**gui/main_window.py**
- Klasa `MainWindow` - główne okno aplikacji
- Zarządza wczytywaniem i zapisywaniem danych
- Koordynuje komunikację między zakładkami
- Funkcje: `load_data_from_csv()`, `save_data_to_csv()`, `reset_data()`

## Funkcjonalności aplikacji

### 1. Wczytywanie i podgląd danych

**Lokalizacja:** `utils/data_loader.py`, `gui/tabs/data_previews.py`

**Funkcje kluczowe:**
- `load_csv_data()` - wczytuje CSV z automatyczną obsługą kodowania i separatorów
- `check_basic_info()` - analizuje podstawowe właściwości zbioru
- `check_missing_data()` - identyfikuje braki w danych

**Co robi:**
1. Automatycznie wykrywa separator (`;`, `,`, `\t`)
2. Obsługuje europejskie kodowanie (ISO-8859-1)
3. Zamienia wartości `-200` na `NaN`
4. Wyświetla statystyki: rozmiar, typy danych, braki, duplikaty
5. Pokazuje pierwsze 100 wierszy w tabeli

### 2. Analiza statystyczna

**Lokalizacja:** `utils/data_processor.py`, `gui/tabs/stats_tab.py`

**Funkcja kluczowa:** `calculate_basic_statistics()`

**Dla danych numerycznych oblicza:**
- Podstawowe: minimum, maksimum, średnia, mediana
- Rozrzut: odchylenie standardowe, wariancja, rozstęp międzykwartylowy
- Kształt rozkładu: skośność (czy dane są przesunięte w lewo/prawo)
- Kwantyle: Q1 (25%), Q3 (75%)
- Braki: liczba i procent brakujących wartości

**Dla danych tekstowych:**
- Liczba unikalnych wartości
- Najczęściej występująca wartość i jej częstość

### 3. Analiza korelacji

**Lokalizacja:** `utils/data_processor.py`, `gui/tabs/correlation_tab.py`

**Funkcja kluczowa:** `calculate_correlation()`

**Dostępne metody:**
- **Pearson** - mierzy liniową zależność (standardowa korelacja)
- **Spearman** - mierzy monotoniczną zależność (odporna na wartości odstające)
- **Kendall** - alternatywa dla Spearman, lepsza dla małych zbiorów

**Wizualizacja:**
- Tabela z kolorowaniem komórek (czerwone = silna korelacja)
- Mapa ciepła (heatmap) z gradientem kolorów
- Wartości od -1 (korelacja ujemna) do +1 (korelacja dodatnia)

### 4. Wizualizacja danych

**Lokalizacja:** `utils/visualization.py`, `gui/tabs/visualization_tab.py`

**Dostępne wykresy:**

#### Histogram (`create_histogram()`)
- Pokazuje rozkład wartości w kolumnie
- Dodaje linie ze średnią (czerwona) i medianą (zielona)
- Parametr: liczba przedziałów (bins)

#### Wykres pudełkowy (`create_boxplot()`)
- Wizualizuje kwartyle, medianę i wartości odstające
- Ideal do identyfikacji outlierów w danych o zanieczyszczeniach

#### Wykres punktowy (`create_scatter_plot()`)
- Pokazuje zależność między dwoma zmiennymi
- Dodaje linię trendu z równaniem
- Przydatny do analizy korelacji (np. temperatura vs wilgotność)

#### Wykres liniowy (`create_line_plot()`)
- Idealny dla szeregów czasowych
- Pokazuje zmiany zanieczyszczeń w czasie
- Automatycznie sortuje dane po osi X

#### Wykres słupkowy (`create_bar_chart()`)
- Porównuje kategorie lub średnie wartości
- Dodaje wartości na słupkach
- Obsługuje długie etykiety (obraca o 45°)

#### Wykres kołowy (`create_pie_chart()`)
- Pokazuje proporcje kategorii
- Ogranicza do 8 głównych kategorii (reszta w "Inne")
- Wyświetla procentowe udziały

#### Mapa korelacji (`create_correlation_heatmap()`)
- Zaawansowana wizualizacja macierzy korelacji
- Używa biblioteki Seaborn dla profesjonalnego wyglądu
- Skala kolorów od niebieskiego (ujemna) do czerwonego (dodatnia)

**Wspólne funkcje:**
- `setup_plot_style()` - ustawia jednolity styl wykresów
- `save_plot()` - zapisuje wykresy w formatach PNG, JPG, SVG, PDF

### 5. Przetwarzanie danych

**Lokalizacja:** `utils/data_processor.py`, `gui/tabs/data_processing_tab.py`

#### Obsługa brakujących wartości (`handle_missing_values()`)
**Strategie:**
- **Usuń wiersze** - eliminuje rekordy z brakami
- **Wypełnij średnią** - dla danych numerycznych
- **Wypełnij medianą** - odporna na wartości odstające
- **Wypełnij modą** - najczęstsza wartość (dla wszystkich typów)
- **Wypełnij wartością** - użytkownik podaje własną wartość

#### Skalowanie danych (`scale_data()`)
**Metody:**
- **MinMax (0-1)** - przekształca wszystkie wartości do zakresu 0-1
- **Standard (z-score)** - średnia=0, odchylenie standardowe=1
- Tworzy nowe kolumny z sufiksem `_scaled`

#### Usuwanie duplikatów (`remove_duplicates()`)
- Może sprawdzać wszystkie kolumny lub wybrane
- Zachowuje pierwszy wystąpienie duplikatu
- Resetuje indeksy po usunięciu

#### Zamiana wartości (`replace_values()`)
- Zamienia konkretne wartości w wybranej kolumnie
- Przydatne do standaryzacji danych (np. "tak"→1, "nie"→0)
- Automatycznie wykrywa typ danych

#### Ekstrakcja podzbiorów (`extract_subset()`)
- Wybiera konkretne kolumny i/lub wiersze
- Tworzy nową ramkę danych
- Waliduje istnienie wybranych elementów

### 6. Klasyfikacja i grupowanie

**Lokalizacja:** `gui/tabs/classification_tab.py`

#### Klasyfikacja (nadzorowana)
**Dostępne algorytmy:**
- **Decision Tree** - drzewo decyzyjne, interpretowalne reguły
- **Random Forest** - zespół drzew, wyższa dokładność
- **SVM** - maszyna wektorów nośnych, dobra dla nieliniowych danych
- **KNN** - k-najbliższych sąsiadów, prosty ale skuteczny

**Proces:**
1. Wybór cech (zmiennych niezależnych)
2. Wybór etykiety (zmienna zależna)
3. Podział na zbiór treningowy/testowy
4. Trenowanie modelu
5. Ewaluacja: dokładność, raport klasyfikacji

#### Grupowanie (nienadzorowane)
**Algorytmy:**
- **K-means** - dzieli dane na k okrągłych grup
- **Hierarchical** - tworzy hierarchię grup (dendrogram)
- **DBSCAN** - znajduje grupy o różnych kształtach, ignoruje outliers

**Wizualizacja:**
- Wykres 2D z kolorowaniem klastrów (dla 2 cech)
- Wykres słupkowy liczebności klastrów

### 7. Integracja z GUI

**matplotlib_canvas.py**
- Klasa `MatplotlibCanvas` integruje wykresy Matplotlib z PyQt5
- Umożliwia interaktywną nawigację (zoom, pan)
- Toolbar z narzędziami do zapisywania i edycji wykresów

**Komunikacja między modułami:**
1. `MainWindow` wczytuje dane funkcją z `utils/data_loader.py`
2. Dane przekazywane są do wszystkich zakładek przez `update_data()`
3. Każda zakładka używa funkcji z `utils/` do przetwarzania
4. Wyniki wyświetlane są w tabelach lub na wykresach

## Przykładowe zastosowania

### Analiza zanieczyszczeń miejskich
1. **Wczytaj dane** AirQualityUCI.csv
2. **Podgląd** - sprawdź braki w danych (szczególnie w sensorach PT08)
3. **Statystyki** - przeanalizuj rozkład CO(GT) i NO2(GT)
4. **Korelacja** - znajdź zależności między temperaturą a zanieczyszczeniami
5. **Wizualizacja** - stwórz szeregi czasowe pokazujące zmiany w czasie
6. **Przetwarzanie** - wypełnij braki medianą, przeskaluj dane
7. **Grupowanie** - znajdź dni o podobnych wzorcach zanieczyszczeń

### Identyfikacja wzorców sezonowych
1. Utwórz wykres liniowy CO(GT) w funkcji czasu
2. Przeanalizuj korelację temperatury z poziomem zanieczyszczeń
3. Pogrupuj dni według podobieństwa profili zanieczyszczeń
4. Zidentyfikuj anomalie (dni o nietypowo wysokich wartościach)

### Porównanie czujników
1. Oblicz korelacje między pomiarami referencyjnymi (GT) a czujnikami (PT08)
2. Sprawdź które czujniki są najbardziej wiarygodne
3. Znajdź czujniki z największą liczbą braków danych

## Technologie i biblioteki

- **PyQt5** - interfejs graficzny
- **pandas** - manipulacja danych
- **numpy** - obliczenia numeryczne  
- **matplotlib** - podstawowe wykresy
- **seaborn** - zaawansowane wizualizacje
- **scikit-learn** - uczenie maszynowe
- **functools** - podejście funkcyjne zamiast obiektowego

Aplikacja została zaprojektowana z myślą o prostocie użytkowania i modularności kodu. Każda funkcja ma jedno, jasno zdefiniowane zadanie, co ułatwia rozwijanie i debugowanie.