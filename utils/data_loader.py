"""
Modul do wczytywania danych z plikow CSV.
Proste funkcje, które każdy zrozumie - nawet babcia :)

Autor: Student hurtowni danych
Data: 2025
"""

import pandas as pd
import numpy as np
import os


def load_csv_data(file_path, separator=';', encoding='ISO-8859-1'):
    """
    wczytuje dane z pliku csv i robi podstawowe czyszczenie

    co bierze:
    - file_path: gdzie jest nasz plik (string)
    - separator: czym sa oddzielone kolumny (domyslnie ; bo europejski format)
    - encoding: jakie kodowanie ma plik (domyslnie ISO-8859-1 bo stare pliki)

    co zwraca:
    - ramke danych pandas albo None jak cos sie zepsuje
    """

    try:
        print(f"probuje wczytac plik: {file_path}")

        # sprawdzamy czy plik w ogole istnieje
        if not os.path.exists(file_path):
            print("plik nie istnieje, sprawdz sciezke!")
            return None

        # wczytujemy dane - decimal=',' bo europejski format liczb
        data = pd.read_csv(
            file_path,
            delimiter=separator,
            encoding=encoding,
            decimal=','
        )

        # usuwamy puste kolumny które powstają przez ;; na końcu wierszy
        data = data.dropna(axis=1, how='all')
        print("usunieto puste kolumny")

        print(f"udalo sie! wczytano {len(data)} wierszy i {len(data.columns)} kolumn")

        # czyścimy dane - zamieniamy -200 na NaN bo to oznacza brakujace wartosci
        data = data.replace(-200, np.nan)
        print("posprzatano dane - zamienilem -200 na NaN")

        return data

    except Exception as error:
        print(f"ups, cos sie zepsulo przy wczytywaniu: {error}")
        return None


def check_basic_info(data):
    """
    pokazuje podstawowe informacje o naszych danych
    przydatne zeby wiedziec z czym mamy do czynienia

    co bierze:
    - data: ramka pandas

    co zwraca:
    - slownik z podstawowymi informacjami
    """

    if data is None:
        return {"error": "brak danych do sprawdzenia"}

    info = {
        "row_count": len(data),
        "column_count": len(data.columns),
        "column_names": list(data.columns),
        "data_types": dict(data.dtypes),
        "missing_values": dict(data.isnull().sum())
    }

    print("=== PODSTAWOWE INFORMACJE ===")
    print(f"wiersze: {info['row_count']}")
    print(f"kolumny: {info['column_count']}")
    print(f"nazwy kolumn: {info['column_names']}")
    print("===============================")

    return info


def show_sample_data(data, num_rows=5):
    """
    pokazuje kilka pierwszych wierszy zeby zobaczyc jak wygladaja dane

    co bierze:
    - data: ramka pandas
    - num_rows: ile wierszy pokazac (domyslnie 5)

    co zwraca:
    - przykladowe wiersze albo None
    """

    if data is None:
        print("nie ma danych do pokazania")
        return None

    print(f"\n=== PIERWSZE {num_rows} WIERSZY ===")
    sample = data.head(num_rows)
    print(sample)
    print("=====================================\n")

    return sample


def check_missing_data(data):
    """
    sprawdza gdzie sa brakujace wartosci w naszych danych
    bardzo wazne bo braki moga zepsuc analize

    co bierze:
    - data: ramka pandas

    co zwraca:
    - slownik z informacjami o brakach
    """

    if data is None:
        return {"error": "brak danych"}

    missing = data.isnull().sum()
    missing_percent = (missing / len(data)) * 100

    missing_info = {}
    for column in data.columns:
        missing_info[column] = {
            "missing_count": missing[column],
            "missing_percent": round(missing_percent[column], 2)
        }

    print("=== ANALIZA BRAKUJACYCH WARTOSCI ===")
    for column, info in missing_info.items():
        if info["missing_count"] > 0:
            print(f"{column}: {info['missing_count']} brakow ({info['missing_percent']}%)")
    print("====================================")

    return missing_info


def save_data_to_csv(data, save_path, separator=';'):
    """
    zapisuje nasze przetworzone dane do nowego pliku csv

    co bierze:
    - data: ramka pandas do zapisania
    - save_path: gdzie zapisac plik
    - separator: jakim znakiem oddzielic kolumny

    co zwraca:
    - True jak sie udalo, False jak nie
    """

    if data is None:
        print("nie ma co zapisywac - dane sa puste")
        return False

    try:
        data.to_csv(save_path, sep=separator, index=False, encoding='utf-8')
        print(f"zapisano dane do pliku: {save_path}")
        return True

    except Exception as error:
        print(f"nie udalo sie zapisac pliku: {error}")
        return False


# przykladowe uzycie - jak ktos chce przetestowac
if __name__ == "__main__":
    print("testujemy wczytywanie danych...")

    # probujemy wczytac plik
    test_data = load_csv_data("../data/AirQualityUCI.csv")

    if test_data is not None:
        # sprawdzamy podstawowe info
        info = check_basic_info(test_data)

        # pokazujemy przyklad
        show_sample_data(test_data, 3)

        # sprawdzamy braki
        missing = check_missing_data(test_data)

        print("wszystko dziala! mozna isc dalej :)")
    else:
        print("cos nie gra z danymi...")