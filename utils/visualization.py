"""
Modul do tworzenia wykresow i wizualizacji danych.
Proste funkcje do robienia ladnych wykresow bez kombinowania.

Każda funkcja robi jeden typ wykresu i zwraca gotowa figure.
Mozna je potem pokazac, zapisac albo wstawic do GUI.

Autor: Student, który lubi ladne wykresy
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def setup_plot_style():
    """
    ustawia ladny styl dla wszystkich wykresow
    wywolaj to na poczatku zeby wykresy wygladaly profesjonalnie
    """
    sns.set_style("whitegrid")  # bialy styl z siatka
    plt.rcParams['figure.figsize'] = (10, 6)  # domyslny rozmiar
    plt.rcParams['font.size'] = 12  # rozmiar czcionki
    print("ustawiono ladny styl wykresow")


def create_histogram(data, column_name, bins=20, title=None):
    """
    rysuje histogram - pokazuje jak czesto wystepuja rozne wartosci

    co bierze:
    - data: ramka pandas
    - column_name: ktora kolumne narysowac
    - bins: na ile części podzielic wartosci
    - title: tytul wykresu (None = automatyczny)

    co zwraca:
    - obiekt figure do pokazania/zapisania
    """

    if data is None or column_name not in data.columns:
        print(f"nie ma kolumny {column_name}")
        return None

    # bierzemy dane bez brakow
    values = data[column_name].dropna()

    if len(values) == 0:
        print("nie ma danych do narysowania")
        return None

    # sprawdzamy czy to sa liczby
    if not np.issubdtype(values.dtype, np.number):
        print("histogram dziala tylko dla liczb")
        return None

    try:
        fig, ax = plt.subplots(figsize=(10, 6))

        # rysujemy histogram
        ax.hist(values, bins=bins, color='skyblue', edgecolor='black', alpha=0.7)

        # dodajemy linie ze srednia i mediana
        mean_val = values.mean()
        median_val = values.median()

        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'srednia: {mean_val:.2f}')
        ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'mediana: {median_val:.2f}')

        # ustawiamy tytuly i etykiety
        if title is None:
            title = f'Histogram dla {column_name}'

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(column_name, fontsize=12)
        ax.set_ylabel('czestotliwosc', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        print(f"narysowano histogram dla {column_name}")
        return fig

    except Exception as error:
        print(f"nie udalo sie narysowac histogramu: {error}")
        return None


def create_boxplot(data, column_name, title=None):
    """
    rysuje boxplot (wykres pudelkowy) - pokazuje rozklad danych
    widac mediane, kwartyle i wartosci odstajace

    co bierze:
    - data: ramka pandas
    - column_name: ktora kolumne narysowac
    - title: tytul wykresu

    co zwraca:
    - obiekt figure
    """

    if data is None or column_name not in data.columns:
        print(f"nie ma kolumny {column_name}")
        return None

    values = data[column_name].dropna()

    if len(values) == 0 or not np.issubdtype(values.dtype, np.number):
        print("boxplot dziala tylko dla liczb")
        return None

    try:
        fig, ax = plt.subplots(figsize=(10, 6))

        # rysujemy boxplot
        box_plot = ax.boxplot(values, patch_artist=True)
        box_plot['boxes'][0].set_facecolor('lightblue')

        # ustawiamy tytuly
        if title is None:
            title = f'Boxplot dla {column_name}'

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel(column_name, fontsize=12)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        print(f"narysowano boxplot dla {column_name}")
        return fig

    except Exception as error:
        print(f"nie udalo sie narysowac boxplot: {error}")
        return None


def create_scatter_plot(data, x_column, y_column, title=None):
    """
    rysuje wykres punktowy - pokazuje zaleznosc miedzy dwoma zmiennymi

    co bierze:
    - data: ramka pandas
    - x_column: kolumna na osi x
    - y_column: kolumna na osi y
    - title: tytul wykresu

    co zwraca:
    - obiekt figure
    """

    if data is None or x_column not in data.columns or y_column not in data.columns:
        print(f"nie ma kolumn {x_column} lub {y_column}")
        return None

    # bierzemy dane bez brakow
    clean_data = data[[x_column, y_column]].dropna()

    if len(clean_data) == 0:
        print("nie ma danych do narysowania po usunieciu brakow")
        return None

    try:
        fig, ax = plt.subplots(figsize=(10, 6))

        # rysujemy punkty
        ax.scatter(clean_data[x_column], clean_data[y_column], alpha=0.7, color='blue')

        # dodajemy linie trendu
        z = np.polyfit(clean_data[x_column], clean_data[y_column], 1)
        p = np.poly1d(z)
        ax.plot(clean_data[x_column], p(clean_data[x_column]), "r--", alpha=0.8,
                label=f'trend: y={z[0]:.2f}x+{z[1]:.2f}')

        # ustawiamy tytuly
        if title is None:
            title = f'{x_column} vs {y_column}'

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(x_column, fontsize=12)
        ax.set_ylabel(y_column, fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        print(f"narysowano scatter plot: {x_column} vs {y_column}")
        return fig

    except Exception as error:
        print(f"nie udalo sie narysowac scatter plot: {error}")
        return None


def create_correlation_heatmap(data, title='Mapa korelacji'):
    """
    rysuje mape ciepla korelacji - pokazuje jak zmienne sa ze soba powiazane
    czerwone = silna korelacja, niebieskie = slaba korelacja

    co bierze:
    - data: ramka pandas
    - title: tytul wykresu

    co zwraca:
    - obiekt figure
    """

    if data is None:
        print("brak danych do analizy korelacji")
        return None

    # bierzemy tylko kolumny liczbowe
    numeric_data = data.select_dtypes(include=[np.number])

    if numeric_data.empty:
        print("nie ma kolumn liczbowych - nie mozna narysowac mapy korelacji")
        return None

    try:
        # liczymy korelacje
        correlation_matrix = numeric_data.corr()

        fig, ax = plt.subplots(figsize=(12, 10))

        # rysujemy mape ciepla
        heatmap = sns.heatmap(
            correlation_matrix,
            annot=True,  # pokazuj wartosci
            fmt='.2f',   # format liczb
            cmap='coolwarm',  # kolory od niebieskiego do czerwonego
            center=0,    # wyśrodkuj na 0
            square=True, # kwadratowe komorki
            ax=ax
        )

        ax.set_title(title, fontsize=16, fontweight='bold')
        plt.tight_layout()

        print("narysowano mape korelacji")
        return fig

    except Exception as error:
        print(f"nie udalo sie narysowac mapy korelacji: {error}")
        return None


def create_bar_chart(data, x_column, y_column=None, title=None):
    """
    rysuje wykres slupkowy - pokazuje wartosci dla roznych kategorii

    co bierze:
    - data: ramka pandas
    - x_column: kolumna z kategoriami
    - y_column: kolumna z wartosciami (None = liczy wystapienia)
    - title: tytul wykresu

    co zwraca:
    - obiekt figure
    """

    if data is None or x_column not in data.columns:
        print(f"nie ma kolumny {x_column}")
        return None

    try:
        fig, ax = plt.subplots(figsize=(10, 6))

        if y_column is None:
            # liczymy wystapienia kategorii
            value_counts = data[x_column].value_counts()
            x_values = value_counts.index
            y_values = value_counts.values
            ylabel = 'liczba wystapien'
        else:
            if y_column not in data.columns:
                print(f"nie ma kolumny {y_column}")
                return None
            # grupujemy i liczymy srednia
            grouped = data.groupby(x_column)[y_column].mean()
            x_values = grouped.index
            y_values = grouped.values
            ylabel = f'srednia {y_column}'

        # rysujemy slupki
        bars = ax.bar(x_values, y_values, color='lightblue', edgecolor='black')

        # dodajemy wartosci na slupkach
        for bar, value in zip(bars, y_values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(y_values),
                   f'{value:.1f}', ha='center', va='bottom')

        # ustawiamy tytuly
        if title is None:
            title = f'Wykres slupkowy: {x_column}'

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(x_column, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')

        # obracamy etykiety jak jest ich duzo
        if len(x_values) > 5:
            plt.xticks(rotation=45)

        plt.tight_layout()
        print(f"narysowano wykres slupkowy dla {x_column}")
        return fig

    except Exception as error:
        print(f"nie udalo sie narysowac wykresu slupkowego: {error}")
        return None


def create_pie_chart(data, column_name, title=None, max_categories=8):
    """
    rysuje wykres kolowy - pokazuje udzialy procentowe kategorii

    co bierze:
    - data: ramka pandas
    - column_name: ktora kolumne narysowac
    - title: tytul wykresu
    - max_categories: maksymalna liczba kategorii (reszta w "inne")

    co zwraca:
    - obiekt figure
    """

    if data is None or column_name not in data.columns:
        print(f"nie ma kolumny {column_name}")
        return None

    try:
        # liczymy wystapienia
        value_counts = data[column_name].value_counts()

        # ograniczamy liczbe kategorii
        if len(value_counts) > max_categories:
            top_categories = value_counts.head(max_categories)
            others_sum = value_counts.tail(len(value_counts) - max_categories).sum()
            value_counts = top_categories
            value_counts['Inne'] = others_sum

        fig, ax = plt.subplots(figsize=(10, 8))

        # rysujemy wykres kolowy
        wedges, texts, autotexts = ax.pie(
            value_counts.values,
            labels=value_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Set3.colors  # ladne kolory
        )

        # ustawiamy styl tekstu
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        # ustawiamy tytul
        if title is None:
            title = f'Wykres kolowy: {column_name}'

        ax.set_title(title, fontsize=14, fontweight='bold')

        plt.tight_layout()
        print(f"narysowano wykres kolowy dla {column_name}")
        return fig

    except Exception as error:
        print(f"nie udalo sie narysowac wykresu kolowego: {error}")
        return None


def create_line_plot(data, x_column, y_column, title=None):
    """
    rysuje wykres liniowy - dobry dla szeregów czasowych

    co bierze:
    - data: ramka pandas
    - x_column: kolumna na osi x (czesto data/czas)
    - y_column: kolumna na osi y (wartosci)
    - title: tytul wykresu

    co zwraca:
    - obiekt figure
    """

    if data is None or x_column not in data.columns or y_column not in data.columns:
        print(f"nie ma kolumn {x_column} lub {y_column}")
        return None

    # bierzemy dane bez brakow i sortujemy po x
    clean_data = data[[x_column, y_column]].dropna().sort_values(x_column)

    if len(clean_data) == 0:
        print("nie ma danych do narysowania")
        return None

    try:
        fig, ax = plt.subplots(figsize=(12, 6))

        # rysujemy linie
        ax.plot(clean_data[x_column], clean_data[y_column],
                color='blue', linewidth=2, marker='o', markersize=4)

        # ustawiamy tytuly
        if title is None:
            title = f'{y_column} w czasie'

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(x_column, fontsize=12)
        ax.set_ylabel(y_column, fontsize=12)
        ax.grid(True, alpha=0.3)

        # obracamy etykiety dat
        plt.xticks(rotation=45)
        plt.tight_layout()

        print(f"narysowano wykres liniowy: {x_column} vs {y_column}")
        return fig

    except Exception as error:
        print(f"nie udalo sie narysowac wykresu liniowego: {error}")
        return None


def save_plot(figure, filename, dpi=300):
    """
    zapisuje wykres do pliku

    co bierze:
    - figure: obiekt figure z matplotlib
    - filename: nazwa pliku (z rozszerzeniem)
    - dpi: jakosc obrazu (wiecej = lepsze)

    co zwraca:
    - True jak sie udało, False jak nie
    """

    if figure is None:
        print("nie ma wykresu do zapisania")
        return False

    try:
        figure.savefig(filename, dpi=dpi, bbox_inches='tight')
        print(f"zapisano wykres do pliku: {filename}")
        return True
    except Exception as error:
        print(f"nie udalo sie zapisac wykresu: {error}")
        return False


# przykladowe uzycie
if __name__ == "__main__":
    print("testujemy rysowanie wykresow...")

    # ustawiamy ladny styl
    setup_plot_style()

    # tworzymy przykladowe dane
    test_data = pd.DataFrame({
        'kategorie': ['A', 'B', 'C', 'A', 'B', 'C', 'A'],
        'wartosci': [10, 15, 12, 8, 20, 18, 14],
        'liczby': [1, 2, 3, 4, 5, 6, 7]
    })

    print("dane testowe:")
    print(test_data)

    # testujemy wykresy
    print("\n=== TESTOWANIE WYKRESOW ===")

    # histogram
    hist_fig = create_histogram(test_data, 'wartosci')
    if hist_fig:
        save_plot(hist_fig, 'test_histogram.png')

    # wykres slupkowy
    bar_fig = create_bar_chart(test_data, 'kategorie', 'wartosci')
    if bar_fig:
        save_plot(bar_fig, 'test_bar_chart.png')

    # scatter plot
    scatter_fig = create_scatter_plot(test_data, 'liczby', 'wartosci')
    if scatter_fig:
        save_plot(scatter_fig, 'test_scatter.png')

    print("\nwszystko dziala! sprawdz zapisane pliki png :)")