"""
Moduł wczytywania danych do projektu hurtowni danych o jakości powietrza.
"""
import pandas as pd
import numpy as np


class DataLoader:
    """
    Klasa odpowiedzialna za wczytywanie i podstawową obróbkę danych.
    """

    def __init__(self):
        """Inicjalizacja obiektu DataLoader."""
        self.data = None
        self.file_path = None

    def load_data(self, file_path, delimiter=';', encoding='ISO-8859-1'):
        """
        Wczytuje dane z pliku CSV.

        Args:
            file_path (str): Ścieżka do pliku CSV.
            delimiter (str, optional): Separator pól. Domyślnie ';'.
            encoding (str, optional): Kodowanie pliku. Domyślnie 'ISO-8859-1'.

        Returns:
            bool: True jeśli wczytywanie zakończyło się sukcesem, False w przeciwnym przypadku.
        """
        try:
            self.file_path = file_path

            # Dodanie parametru decimal=',' do obsługi europejskiego formatu liczb
            self.data = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding, decimal=',')

            # Zastępowanie wartości -200 (brakujące wartości) na NaN
            self.data.replace(-200, np.nan, inplace=True)

            return True
        except Exception as e:
            print(f"Błąd podczas wczytywania danych: {e}")
            return False
    def get_data(self):
        """
        Zwraca wczytane dane.

        Returns:
            pandas.DataFrame: Wczytane dane.
        """
        return self.data

    def get_column_names(self):
        """
        Zwraca nazwy kolumn.

        Returns:
            list: Lista nazw kolumn.
        """
        if self.data is not None:
            return list(self.data.columns)
        return []

    def get_data_shape(self):
        """
        Zwraca kształt danych (liczbę wierszy i kolumn).

        Returns:
            tuple: Krotka (liczba_wierszy, liczba_kolumn).
        """
        if self.data is not None:
            return self.data.shape
        return (0, 0)

    def get_data_types(self):
        """
        Zwraca typy danych dla każdej kolumny.

        Returns:
            dict: Słownik {nazwa_kolumny: typ_danych}.
        """
        if self.data is not None:
            return dict(self.data.dtypes)
        return {}

    def get_data_info(self):
        """
        Zwraca podstawowe informacje o danych.

        Returns:
            str: Informacje o danych.
        """
        if self.data is not None:
            # Użyj StringIO zamiast listy
            import io
            buffer = io.StringIO()
            self.data.info(buf=buffer)
            return buffer.getvalue()
        return "Brak wczytanych danych."

    def get_data_head(self, n=5):
        """
        Zwraca pierwsze n wierszy danych.

        Args:
            n (int, optional): Liczba wierszy. Domyślnie 5.

        Returns:
            pandas.DataFrame: Pierwsze n wierszy danych.
        """
        if self.data is not None:
            return self.data.head(n)
        return None

    def get_data_tail(self, n=5):
        """
        Zwraca ostatnie n wierszy danych.

        Args:
            n (int, optional): Liczba wierszy. Domyślnie 5.

        Returns:
            pandas.DataFrame: Ostatnie n wierszy danych.
        """
        if self.data is not None:
            return self.data.tail(n)
        return None