"""
Modul do przetwarzania i analizy danych.
Proste funkcje matematyczne i statystyczne - bez kombinowania.

Tutaj robimy wszelkie obliczenia, czyszczenie i przygotowywanie danych.
Każda funkcja robi jedna konkretna rzecz i ma jasne zadanie.

Autor: Student, który chce żeby wszystko było proste
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer


def calculate_basic_statistics(data, column_name):
    """
    liczy podstawowe statystyki dla jednej kolumny
    średnia, mediana, minimum, maksimum - takie rzeczy

    co bierze:
    - data: ramka pandas
    - column_name: ktora kolumne analizowac

    co zwraca:
    - slownik ze statystykami albo pusty slownik jak cos nie gra
    """

    if data is None or column_name not in data.columns:
        print(f"nie ma kolumny {column_name} w danych")
        return {}

    # bierzemy tylko jedna kolumne i usuwamy braki
    column_data = data[column_name].dropna()

    if len(column_data) == 0:
        print(f"kolumna {column_name} jest pusta")
        return {}

    # sprawdzamy czy to sa liczby czy tekst
    if not np.issubdtype(column_data.dtype, np.number):
        # dla tekstu liczymy inne rzeczy
        stats = {
            'type': 'text',
            'count': len(column_data),
            'unique_values': column_data.nunique(),
            'most_frequent': column_data.value_counts().index[0] if len(column_data) > 0 else None,
            'frequency': column_data.value_counts().iloc[0] if len(column_data) > 0 else 0
        }
    else:
        # dla liczb liczymy wszystko co mozna
        stats = {
            'type': 'numeric',
            'count': len(column_data),
            'min': column_data.min(),
            'max': column_data.max(),
            'mean': column_data.mean(),
            'median': column_data.median(),
            'std': column_data.std(),
            'variance': column_data.var(),
            'skewness': column_data.skew(),  # czy dane sa przesunięte w lewo/prawo
            'q1': column_data.quantile(0.25),
            'q3': column_data.quantile(0.75),
            'iqr': column_data.quantile(0.75) - column_data.quantile(0.25),
            'missing_count': data[column_name].isnull().sum(),
            'missing_percent': (data[column_name].isnull().sum() / len(data)) * 100
        }

    print(f"obliczono statystyki dla kolumny: {column_name}")
    return stats


def calculate_correlation(data, method='pearson'):
    """
    liczy korelacje miedzy wszystkimi kolumnami liczbowymi
    korelacja pokazuje jak bardzo jedna rzecz wplywa na druga

    co bierze:
    - data: ramka pandas
    - method: jaka metoda korelacji (pearson, spearman, kendall)

    co zwraca:
    - macierz korelacji albo None jak cos nie gra
    """

    if data is None:
        print("brak danych do analizy korelacji")
        return None

    # bierzemy tylko kolumny z liczbami
    numeric_data = data.select_dtypes(include=[np.number])
    # usuwamy kolumny które są całkowicie puste lub mają mniej niż 2 wartości
    numeric_data = numeric_data.dropna(axis=1, how='all')
    for col in numeric_data.columns:
        if numeric_data[col].count() < 2:
            numeric_data = numeric_data.drop(col, axis=1)

    if numeric_data.empty:
        print("nie ma kolumn liczbowych - nie mozna liczyc korelacji")
        return None

    try:
        correlation_matrix = numeric_data.corr(method=method)
        print(f"obliczono korelacje metoda {method} dla {len(numeric_data.columns)} kolumn")
        return correlation_matrix

    except Exception as error:
        print(f"nie udalo sie obliczyc korelacji: {error}")
        return None


def extract_subset(data, columns=None, rows=None):
    """
    wycina kawałek z naszych danych - wybrane kolumny i/lub wiersze
    przydatne jak chcemy analizowac tylko część danych

    co bierze:
    - data: ramka pandas
    - columns: lista nazw kolumn (None = wszystkie)
    - rows: lista numerów wierszy (None = wszystkie)

    co zwraca:
    - nowa ramka z wybranymi danymi
    """

    if data is None:
        print("nie ma danych do wyciagania")
        return None

    # jesli nie wybrano kolumn, bierzemy wszystkie
    if columns is None:
        columns = data.columns

    # sprawdzamy czy wybrane kolumny istnieja
    missing_columns = [c for c in columns if c not in data.columns]
    if missing_columns:
        print(f"nie ma takich kolumn: {missing_columns}")
        return None

    try:
        if rows is None:
            # bierzemy wszystkie wiersze, wybrane kolumny
            result = data[columns].copy()
        else:
            # sprawdzamy czy wybrane wiersze istnieja
            valid_rows = [r for r in rows if r in data.index]
            if not valid_rows:
                print("nie ma zadnych prawidlowych wierszy")
                return None

            result = data.loc[valid_rows, columns].copy()

        print(f"wyciagnieto dane: {len(result)} wierszy x {len(result.columns)} kolumn")
        return result

    except Exception as error:
        print(f"nie udalo sie wyciagnac danych: {error}")
        return None


def replace_values(data, column_name, old_value, new_value):
    """
    zamienia jedna wartosc na inna w wybranej kolumnie
    np. zamienia wszystkie "tak" na 1 albo "nie" na 0

    co bierze:
    - data: ramka pandas
    - column_name: w ktorej kolumnie zamienic
    - old_value: co zamienic
    - new_value: na co zamienic

    co zwraca:
    - dane z zamienionymi wartosciami albo None jak cos nie gra
    """

    if data is None or column_name not in data.columns:
        print(f"nie ma kolumny {column_name}")
        return None

    try:
        # robimy kopie zeby nie zepsuc oryginalnych danych
        new_data = data.copy()

        # liczymy ile wartosci zamienimy
        count_to_replace = (new_data[column_name] == old_value).sum()

        # zamieniamy
        new_data[column_name] = new_data[column_name].replace(old_value, new_value)

        print(f"zamieniono {count_to_replace} wartosci '{old_value}' na '{new_value}' w kolumnie {column_name}")
        return new_data

    except Exception as error:
        print(f"nie udalo sie zamienic wartosci: {error}")
        return None


def scale_data(data, column_names, method='minmax'):
    """
    skaluje dane zeby wszystkie mialy podobny zakres wartosci
    przydatne przed analiza bo jedna kolumna moze miec wartosci 0-1 a inna 0-1000

    co bierze:
    - data: ramka pandas
    - column_names: ktore kolumny skalowac
    - method: 'minmax' (0-1) albo 'standard' (srednia=0, odchylenie=1)

    co zwraca:
    - dane z przeskalowanymi kolumnami
    """

    if data is None:
        print("brak danych do skalowania")
        return None

    # sprawdzamy czy wszystkie kolumny istnieja i sa liczbowe
    for column in column_names:
        if column not in data.columns:
            print(f"nie ma kolumny {column}")
            return None
        if not np.issubdtype(data[column].dtype, np.number):
            print(f"kolumna {column} nie zawiera liczb")
            return None

    try:
        new_data = data.copy()

        # Sprawdzamy i przygotowujemy dane do skalowania
        columns_to_scale = []
        for column in column_names:
            if column not in data.columns:
                print(f"nie ma kolumny {column}")
                continue

            # Próbujemy przekonwertować na liczby
            try:
                numeric_series = pd.to_numeric(data[column], errors='coerce')
                if not numeric_series.isna().all():
                    columns_to_scale.append(column)
                else:
                    print(f"kolumna {column} nie zawiera liczb")
            except:
                print(f"nie można przekonwertować kolumny {column}")

        if not columns_to_scale:
            print("nie ma kolumn do skalowania")
            return None

        # Przygotowujemy dane - konwertujemy na liczby i usuwamy braki
        data_for_scaling = new_data[columns_to_scale].copy()
        for col in columns_to_scale:
            data_for_scaling[col] = pd.to_numeric(data_for_scaling[col], errors='coerce')

        # Wybieramy tylko wiersze bez braków w skalowanych kolumnach
        complete_rows = data_for_scaling.dropna()

        if len(complete_rows) == 0:
            print("nie ma danych do skalowania po usunieciu brakow")
            return None

        # Wybieramy metode skalowania
        if method == 'minmax':
            scaler = MinMaxScaler()
            description = "0-1"
        elif method == 'standard':
            scaler = StandardScaler()
            description = "srednia=0, odchylenie=1"
        else:
            print(f"nieznana metoda skalowania: {method}")
            return None

        # Skalujemy dane
        scaled_values = scaler.fit_transform(complete_rows)

        # Dodajemy przeskalowane kolumny do danych
        for i, column in enumerate(columns_to_scale):
            new_column_name = f"{column}_scaled"
            # Tworzymy nową kolumnę wypełnioną NaN
            new_data[new_column_name] = np.nan
            # Wstawiamy przeskalowane wartości tam gdzie były oryginalne (bez braków)
            new_data.loc[complete_rows.index, new_column_name] = scaled_values[:, i]

        print(f"przeskalowano {len(columns_to_scale)} kolumn metoda {method} ({description})")
        return new_data

    except Exception as error:
        print(f"nie udalo sie przeskalowac danych: {error}")
        return None


def handle_missing_values(data, method='drop', fill_value=None, column_names=None):
    """
    radzi sobie z brakujacymi wartosciami - albo je usuwa albo wypelnia

    co bierze:
    - data: ramka pandas
    - method: 'drop', 'mean', 'median', 'mode', 'value'
    - fill_value: czym wypelnic jesli method='value'
    - column_names: ktore kolumny sprawdzac (None = wszystkie)

    co zwraca:
    - dane bez brakow albo z wypelnionymi brakami
    """

    if data is None:
        print("brak danych do obrobki")
        return None

    if column_names is None:
        column_names = data.columns

    try:
        new_data = data.copy()

        if method == 'drop':
            # usuwamy wiersze gdzie sa braki w wybranych kolumnach
            before = len(new_data)
            new_data = new_data.dropna(subset=column_names)
            after = len(new_data)
            print(f"usunieto {before - after} wierszy z brakami")

        else:
            # wypelniamy braki
            for column in column_names:
                if column not in new_data.columns:
                    continue

                missing_before = new_data[column].isnull().sum()

                if method == 'value' and fill_value is not None:
                    new_data[column].fillna(fill_value, inplace=True)
                    fill_method_desc = f"wartoscia {fill_value}"

                elif np.issubdtype(new_data[column].dtype, np.number):
                    # dla liczb
                    if method == 'mean':
                        fill_val = new_data[column].mean()
                        fill_method_desc = f"srednia ({fill_val:.2f})"
                    elif method == 'median':
                        fill_val = new_data[column].median()
                        fill_method_desc = f"mediana ({fill_val:.2f})"
                    else:  # mode
                        fill_val = new_data[column].mode().iloc[0] if not new_data[column].mode().empty else 0
                        fill_method_desc = f"moda ({fill_val})"

                    new_data[column].fillna(fill_val, inplace=True)
                else:
                    # dla tekstu - tylko moda ma sens
                    if len(new_data[column].mode()) > 0:
                        fill_val = new_data[column].mode().iloc[0]
                        new_data[column].fillna(fill_val, inplace=True)
                        fill_method_desc = f"moda ({fill_val})"
                    else:
                        fill_method_desc = "nie udalo sie - brak mody"

                missing_after = new_data[column].isnull().sum()
                print(f"kolumna {column}: wypelniono {missing_before - missing_after} brakow {fill_method_desc}")

        return new_data

    except Exception as error:
        print(f"nie udalo sie obsluzyc brakow: {error}")
        return None


def remove_duplicates(data, column_names=None):
    """
    usuwa powtarzajace sie wiersze z danych

    co bierze:
    - data: ramka pandas
    - column_names: na podstawie ktorych kolumn szukac duplikatow (None = wszystkie)

    co zwraca:
    - dane bez duplikatow
    """

    if data is None:
        print("brak danych do czyszczenia")
        return None

    try:
        before = len(data)

        if column_names is None:
            # sprawdzamy duplikaty we wszystkich kolumnach
            new_data = data.drop_duplicates().reset_index(drop=True)
            description = "wszystkich kolumn"
        else:
            # sprawdzamy duplikaty tylko w wybranych kolumnach
            new_data = data.drop_duplicates(subset=column_names).reset_index(drop=True)
            description = f"kolumn: {', '.join(column_names)}"

        after = len(new_data)
        removed = before - after

        print(f"usunieto {removed} duplikatow na podstawie {description}")
        return new_data

    except Exception as error:
        print(f"nie udalo sie usunac duplikatow: {error}")
        return None


# przykladowe uzycie
if __name__ == "__main__":
    print("testujemy przetwarzanie danych...")

    # tworzymy przykladowe dane
    test_data = pd.DataFrame({
        'numbers': [1, 2, 3, np.nan, 5, 5],
        'text': ['a', 'b', 'c', 'a', 'b', 'b'],
        'more_numbers': [10, 20, 30, 40, 50, 50]
    })

    print("dane testowe:")
    print(test_data)

    # testujemy funkcje
    print("\n=== TESTOWANIE FUNKCJI ===")

    # statystyki
    stats = calculate_basic_statistics(test_data, 'numbers')
    print(f"statystyki: {stats}")

    # korelacje
    corr = calculate_correlation(test_data)
    print(f"korelacje:\n{corr}")

    # usuwanie duplikatow
    no_duplicates = remove_duplicates(test_data)
    print(f"bez duplikatow:\n{no_duplicates}")

    print("\nwszystko dziala!")