"""
Moduł przetwarzania danych dla projektu hurtowni danych o jakości powietrza.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder


class DataProcessor:
    """
    Klasa odpowiedzialna za przetwarzanie i analizę danych.
    """

    def __init__(self, data=None):
        """
        Inicjalizacja obiektu DataProcessor.

        Args:
            data (pandas.DataFrame, optional): Dane do przetwarzania. Domyślnie None.
        """
        self.data = data
        self.original_data = None
        if data is not None:
            self.original_data = data.copy()

    def set_data(self, data):
        """
        Ustawia dane do przetwarzania.

        Args:
            data (pandas.DataFrame): Dane do przetwarzania.
        """
        self.data = data
        self.original_data = data.copy()

    def get_data(self):
        """
        Zwraca aktualnie przetwarzane dane.

        Returns:
            pandas.DataFrame: Aktualnie przetwarzane dane.
        """
        return self.data

    def reset_data(self):
        """
        Przywraca oryginalne dane.

        Returns:
            bool: True jeśli przywrócenie danych zakończyło się sukcesem, False w przeciwnym przypadku.
        """
        if self.original_data is not None:
            self.data = self.original_data.copy()
            return True
        return False

    def calculate_statistics(self, column_name):
        """
        Oblicza podstawowe statystyki dla wybranej kolumny.

        Args:
            column_name (str): Nazwa kolumny.

        Returns:
            dict: Słownik ze statystykami.
        """
        if self.data is None or column_name not in self.data.columns:
            return {}

        column_data = self.data[column_name].dropna()

        if column_data.empty:
            return {}

        # Sprawdzenie, czy dane są numeryczne
        if not np.issubdtype(column_data.dtype, np.number):
            return {
                'count': len(column_data),
                'unique': column_data.nunique(),
                'top': column_data.value_counts().index[0] if not column_data.value_counts().empty else None,
                'freq': column_data.value_counts().iloc[0] if not column_data.value_counts().empty else 0
            }

        # Statystyki dla danych numerycznych
        stats = {
            'count': len(column_data),
            'min': column_data.min(),
            'max': column_data.max(),
            'mean': column_data.mean(),
            'median': column_data.median(),
            'std': column_data.std(),
            'var': column_data.var(),
            'skewness': column_data.skew(),
            'kurtosis': column_data.kurtosis(),
            'q1': column_data.quantile(0.25),
            'q3': column_data.quantile(0.75),
            'iqr': column_data.quantile(0.75) - column_data.quantile(0.25),
            'mode': column_data.mode().iloc[0] if not column_data.mode().empty else None,
            'missing': self.data[column_name].isna().sum(),
            'missing_percentage': (self.data[column_name].isna().sum() / len(self.data)) * 100
        }

        return stats

    def calculate_correlation(self, method='pearson'):
        """
        Oblicza macierz korelacji dla wszystkich kolumn numerycznych.

        Args:
            method (str, optional): Metoda obliczania korelacji ('pearson', 'kendall', 'spearman').
                                    Domyślnie 'pearson'.

        Returns:
            pandas.DataFrame: Macierz korelacji.
        """
        if self.data is None:
            return None

        # Wybierz tylko kolumny numeryczne
        numeric_data = self.data.select_dtypes(include=[np.number])

        if numeric_data.empty:
            return None

        return numeric_data.corr(method=method)

    def extract_subset(self, columns=None, rows=None):
        """
        Ekstrahuje podzbiór danych na podstawie określonych kolumn i wierszy.

        Args:
            columns (list, optional): Lista nazw kolumn do ekstrakcji. Domyślnie None (wszystkie kolumny).
            rows (list, optional): Lista indeksów wierszy do ekstrakcji. Domyślnie None (wszystkie wiersze).

        Returns:
            pandas.DataFrame: Podzbiór danych.
        """
        if self.data is None:
            return None

        if columns is None:
            columns = self.data.columns

        if rows is None:
            return self.data[columns].copy()

        # Sprawdzenie, czy indeksy wierszy są poprawne
        valid_rows = [idx for idx in rows if idx in self.data.index]

        return self.data.loc[valid_rows, columns].copy()

    def replace_values(self, column_name, old_value, new_value):
        """
        Zastępuje wartości w określonej kolumnie.

        Args:
            column_name (str): Nazwa kolumny.
            old_value (any): Wartość do zastąpienia.
            new_value (any): Nowa wartość.

        Returns:
            bool: True jeśli zastąpienie wartości zakończyło się sukcesem, False w przeciwnym przypadku.
        """
        if self.data is None or column_name not in self.data.columns:
            return False

        try:
            self.data[column_name].replace(old_value, new_value, inplace=True)
            return True
        except Exception as e:
            print(f"Błąd podczas zastępowania wartości: {e}")
            return False

    def scale_data(self, columns, method='minmax', feature_range=(0, 1)):
        """
        Skaluje dane w wybranych kolumnach.

        Args:
            columns (list): Lista nazw kolumn do skalowania.
            method (str, optional): Metoda skalowania ('minmax', 'standard'). Domyślnie 'minmax'.
            feature_range (tuple, optional): Zakres wartości dla MinMaxScaler. Domyślnie (0, 1).

        Returns:
            bool: True jeśli skalowanie zakończyło się sukcesem, False w przeciwnym przypadku.
        """
        if self.data is None:
            return False

        # Sprawdzenie, czy wszystkie kolumny istnieją i są numeryczne
        for col in columns:
            if col not in self.data.columns:
                print(f"Kolumna {col} nie istnieje.")
                return False
            if not np.issubdtype(self.data[col].dtype, np.number):
                print(f"Kolumna {col} nie jest numeryczna.")
                return False

        try:
            # Tworzenie kopii danych
            data_to_scale = self.data[columns].copy()

            # Usuwanie wierszy z wartościami NaN
            data_to_scale = data_to_scale.dropna()

            if data_to_scale.empty:
                print("Brak danych do skalowania po usunięciu wartości NaN.")
                return False

            # Wybór metody skalowania
            if method == 'minmax':
                scaler = MinMaxScaler(feature_range=feature_range)
            elif method == 'standard':
                scaler = StandardScaler()
            else:
                print(f"Nieznana metoda skalowania: {method}")
                return False

            # Skalowanie danych
            scaled_data = scaler.fit_transform(data_to_scale)

            # Aktualizacja danych
            for i, col in enumerate(columns):
                # Tworzenie nowej kolumny z przeskalowanymi danymi
                new_col_name = f"{col}_scaled"
                self.data.loc[data_to_scale.index, new_col_name] = scaled_data[:, i]

            return True
        except Exception as e:
            print(f"Błąd podczas skalowania danych: {e}")
            return False

    def standardize_data(self, columns):
        """
        Standaryzuje dane w wybranych kolumnach.

        Args:
            columns (list): Lista nazw kolumn do standaryzacji.

        Returns:
            bool: True jeśli standaryzacja zakończyła się sukcesem, False w przeciwnym przypadku.
        """
        return self.scale_data(columns, method='standard')

    def remove_missing_values(self, method='drop', threshold=None, columns=None, fill_value=None):
        """
        Usuwa wiersze z brakującymi wartościami lub wypełnia je.

        Args:
            method (str, optional): Metoda obsługi brakujących wartości ('drop', 'fill').
                                    Domyślnie 'drop'.
            threshold (float, optional): Próg brakujących wartości (0.0-1.0) powyżej którego
                                         wiersz jest usuwany. Domyślnie None (usuwane są wszystkie
                                         wiersze z brakującymi wartościami).
            columns (list, optional): Lista kolumn do sprawdzenia. Domyślnie None (wszystkie kolumny).
            fill_value (any, optional): Wartość do wypełnienia brakujących danych.
                                      Domyślnie None (używana jest średnia dla danych numerycznych
                                      i najczęstsza wartość dla danych kategorycznych).

        Returns:
            bool: True jeśli operacja zakończyła się sukcesem, False w przeciwnym przypadku.
        """
        if self.data is None:
            return False

        try:
            if columns is None:
                columns = self.data.columns

            # Wybierz tylko określone kolumny
            data_subset = self.data[columns]

            if method == 'drop':
                if threshold is not None:
                    # Oblicz procent brakujących wartości dla każdego wiersza
                    missing_percentage = data_subset.isna().mean(axis=1)
                    # Wybierz wiersze, gdzie procent brakujących wartości jest mniejszy lub równy progowi
                    mask = missing_percentage <= threshold
                    self.data = self.data[mask].copy()
                else:
                    # Usuń wiersze z brakującymi wartościami
                    self.data = self.data.dropna(subset=columns).copy()
            elif method == 'fill':
                for col in columns:
                    if col not in self.data.columns:
                        continue

                    # Wybierz metodę wypełniania
                    if fill_value is not None:
                        self.data[col].fillna(fill_value, inplace=True)
                    else:
                        if np.issubdtype(self.data[col].dtype, np.number):
                            # Dla danych numerycznych użyj średniej
                            imputer = SimpleImputer(strategy='mean')
                            self.data[col] = imputer.fit_transform(self.data[[col]])
                        else:
                            # Dla danych kategorycznych użyj najczęstszej wartości
                            imputer = SimpleImputer(strategy='most_frequent')
                            self.data[col] = imputer.fit_transform(self.data[[col]])
            else:
                print(f"Nieznana metoda obsługi brakujących wartości: {method}")
                return False

            return True
        except Exception as e:
            print(f"Błąd podczas obsługi brakujących wartości: {e}")
            return False

    def remove_duplicates(self, columns=None):
        """
        Usuwa duplikaty wierszy.

        Args:
            columns (list, optional): Lista kolumn do sprawdzenia duplikatów.
                                    Domyślnie None (wszystkie kolumny).

        Returns:
            bool: True jeśli usunięcie duplikatów zakończyło się sukcesem, False w przeciwnym przypadku.
        """
        if self.data is None:
            return False

        try:
            if columns is None:
                # Usuń duplikaty na podstawie wszystkich kolumn
                self.data = self.data.drop_duplicates().copy()
            else:
                # Usuń duplikaty na podstawie określonych kolumn
                self.data = self.data.drop_duplicates(subset=columns).copy()

            # Zresetuj indeksy
            self.data.reset_index(drop=True, inplace=True)

            return True
        except Exception as e:
            print(f"Błąd podczas usuwania duplikatów: {e}")
            return False

    def encode_categorical(self, columns, method='onehot'):
        """
        Koduje zmienne kategoryczne na binarne.

        Args:
            columns (list): Lista nazw kolumn do kodowania.
            method (str, optional): Metoda kodowania ('onehot', 'label'). Domyślnie 'onehot'.

        Returns:
            bool: True jeśli kodowanie zakończyło się sukcesem, False w przeciwnym przypadku.
        """
        if self.data is None:
            return False

        try:
            for col in columns:
                if col not in self.data.columns:
                    print(f"Kolumna {col} nie istnieje.")
                    continue

                if method == 'onehot':
                    # Kodowanie One-Hot
                    encoder = OneHotEncoder(sparse=False, drop='first')
                    encoded = encoder.fit_transform(self.data[[col]])

                    # Tworzenie nazw nowych kolumn
                    categories = encoder.categories_[0][1:]  # drop='first' pomija pierwszą kategorię
                    encoded_cols = [f"{col}_{cat}" for cat in categories]

                    # Dodawanie zakodowanych kolumn do danych
                    encoded_df = pd.DataFrame(encoded, columns=encoded_cols, index=self.data.index)
                    self.data = pd.concat([self.data, encoded_df], axis=1)

                elif method == 'label':
                    # Kodowanie Label
                    self.data[f"{col}_encoded"] = self.data[col].astype('category').cat.codes
                else:
                    print(f"Nieznana metoda kodowania: {method}")
                    return False

            return True
        except Exception as e:
            print(f"Błąd podczas kodowania zmiennych kategorycznych: {e}")
            return False