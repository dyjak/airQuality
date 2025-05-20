"""
Moduł wizualizacji danych dla projektu hurtowni danych o jakości powietrza.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from io import BytesIO


class DataVisualizer:
    """
    Klasa odpowiedzialna za wizualizację danych.
    """

    def __init__(self, data=None):
        """
        Inicjalizacja obiektu DataVisualizer.

        Args:
            data (pandas.DataFrame, optional): Dane do wizualizacji. Domyślnie None.
        """
        self.data = data
        # Ustawienie stylu dla wykresów
        sns.set(style="whitegrid")

    def set_data(self, data):
        """
        Ustawia dane do wizualizacji.

        Args:
            data (pandas.DataFrame): Dane do wizualizacji.
        """
        self.data = data

    def create_histogram(self, column, bins=10, figsize=(10, 6), title=None, xlabel=None, ylabel='Częstość',
                         color='skyblue', edgecolor='black'):
        """
        Tworzy histogram dla wybranej kolumny.

        Args:
            column (str): Nazwa kolumny.
            bins (int, optional): Liczba przedziałów. Domyślnie 10.
            figsize (tuple, optional): Rozmiar wykresu. Domyślnie (10, 6).
            title (str, optional): Tytuł wykresu. Domyślnie None.
            xlabel (str, optional): Etykieta osi X. Domyślnie None.
            ylabel (str, optional): Etykieta osi Y. Domyślnie 'Częstość'.
            color (str, optional): Kolor wypełnienia słupków. Domyślnie 'skyblue'.
            edgecolor (str, optional): Kolor krawędzi słupków. Domyślnie 'black'.

        Returns:
            matplotlib.figure.Figure: Obiekt figury Matplotlib.
        """
        if self.data is None or column not in self.data.columns:
            return None

        fig, ax = plt.subplots(figsize=figsize)

        # Usuwanie wartości NaN
        data = self.data[column].dropna()

        # Tworzenie histogramu
        ax.hist(data, bins=bins, color=color, edgecolor=edgecolor, alpha=0.7)

        # Dodawanie tytułu i etykiet osi
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title(f'Histogram dla {column}', fontsize=14)

        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
        else:
            ax.set_xlabel(column, fontsize=12)

        ax.set_ylabel(ylabel, fontsize=12)

        # Dodawanie siatki
        ax.grid(True, linestyle='--', alpha=0.7)

        # Dodanie podstawowych statystyk
        mean = data.mean()
        median = data.median()
        ax.axvline(mean, color='red', linestyle='dashed', linewidth=2, label=f'Średnia: {mean:.2f}')
        ax.axvline(median, color='green', linestyle='dashed', linewidth=2, label=f'Mediana: {median:.2f}')
        ax.legend()

        plt.tight_layout()

        return fig

    def create_boxplot(self, column, figsize=(10, 6), title=None, xlabel=None, ylabel=None, color='skyblue'):
        """
        Tworzy wykres pudełkowy dla wybranej kolumny.

        Args:
            column (str): Nazwa kolumny.
            figsize (tuple, optional): Rozmiar wykresu. Domyślnie (10, 6).
            title (str, optional): Tytuł wykresu. Domyślnie None.
            xlabel (str, optional): Etykieta osi X. Domyślnie None.
            ylabel (str, optional): Etykieta osi Y. Domyślnie None.
            color (str, optional): Kolor wykresu. Domyślnie 'skyblue'.

        Returns:
            matplotlib.figure.Figure: Obiekt figury Matplotlib.
        """
        if self.data is None or column not in self.data.columns:
            return None

        fig, ax = plt.subplots(figsize=figsize)

        # Usuwanie wartości NaN
        data = self.data[column].dropna()

        # Tworzenie wykresu pudełkowego
        sns.boxplot(x=data, ax=ax, color=color)

        # Dodawanie tytułu i etykiet osi
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title(f'Wykres pudełkowy dla {column}', fontsize=14)

        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
        else:
            ax.set_xlabel(column, fontsize=12)

        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)

        # Dodawanie siatki
        ax.grid(True, linestyle='--', alpha=0.7)

        plt.tight_layout()

        return fig

    def create_scatter_plot(self, x_column, y_column, figsize=(10, 6), title=None, xlabel=None, ylabel=None,
                            color='blue', alpha=0.7):
        """
        Tworzy wykres punktowy dla dwóch wybranych kolumn.

        Args:
            x_column (str): Nazwa kolumny dla osi X.
            y_column (str): Nazwa kolumny dla osi Y.
            figsize (tuple, optional): Rozmiar wykresu. Domyślnie (10, 6).
            title (str, optional): Tytuł wykresu. Domyślnie None.
            xlabel (str, optional): Etykieta osi X. Domyślnie None.
            ylabel (str, optional): Etykieta osi Y. Domyślnie None.
            color (str, optional): Kolor punktów. Domyślnie 'blue'.
            alpha (float, optional): Przezroczystość punktów. Domyślnie 0.7.

        Returns:
            matplotlib.figure.Figure: Obiekt figury Matplotlib.
        """
        if self.data is None or x_column not in self.data.columns or y_column not in self.data.columns:
            return None

        fig, ax = plt.subplots(figsize=figsize)

        # Usuwanie wierszy z wartościami NaN
        data = self.data[[x_column, y_column]].dropna()

        # Tworzenie wykresu punktowego
        ax.scatter(data[x_column], data[y_column], color=color, alpha=alpha)

        # Dodawanie tytułu i etykiet osi
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title(f'Wykres punktowy: {x_column} vs {y_column}', fontsize=14)

        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
        else:
            ax.set_xlabel(x_column, fontsize=12)

        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)
        else:
            ax.set_ylabel(y_column, fontsize=12)

        # Dodawanie siatki
        ax.grid(True, linestyle='--', alpha=0.7)

        # Dodanie linii trendu
        z = np.polyfit(data[x_column], data[y_column], 1)
        p = np.poly1d(z)
        ax.plot(data[x_column], p(data[x_column]), "r--", alpha=0.7,
                label=f'Trend: y={z[0]:.2f}x+{z[1]:.2f}')
        ax.legend()

        plt.tight_layout()

        return fig

    def create_correlation_heatmap(self, columns=None, figsize=(12, 10), title='Macierz korelacji', cmap='coolwarm',
                                   annot=True, fmt='.2f'):
        """
        Tworzy mapę ciepła korelacji dla wybranych kolumn.

        Args:
            columns (list, optional): Lista nazw kolumn. Domyślnie None (wszystkie kolumny numeryczne).
            figsize (tuple, optional): Rozmiar wykresu. Domyślnie (12, 10).
            title (str, optional): Tytuł wykresu. Domyślnie 'Macierz korelacji'.
            cmap (str, optional): Paleta kolorów. Domyślnie 'coolwarm'.
            annot (bool, optional): Czy wyświetlać wartości korelacji. Domyślnie True.
            fmt (str, optional): Format wartości korelacji. Domyślnie '.2f'.

        Returns:
            matplotlib.figure.Figure: Obiekt figury Matplotlib.
        """
        if self.data is None:
            return None

        # Wybierz tylko kolumny numeryczne
        if columns is None:
            numeric_data = self.data.select_dtypes(include=[np.number])
        else:
            # Sprawdź, czy wszystkie kolumny istnieją
            for col in columns:
                if col not in self.data.columns:
                    print(f"Kolumna {col} nie istnieje.")
                    return None

            numeric_data = self.data[columns].select_dtypes(include=[np.number])

        if numeric_data.empty:
            print("Brak kolumn numerycznych.")
            return None

        # Obliczanie macierzy korelacji
        corr_matrix = numeric_data.corr()

        # Tworzenie mapy ciepła
        fig, ax = plt.subplots(figsize=figsize)
        heatmap = sns.heatmap(corr_matrix, annot=annot, fmt=fmt, cmap=cmap,
                              linewidths=.5, ax=ax, vmin=-1, vmax=1)

        # Dodawanie tytułu
        ax.set_title(title, fontsize=16)

        plt.tight_layout()

        return fig

    def create_time_series_plot(self, date_column, value_column, figsize=(14, 8), title=None, xlabel='Data',
                                ylabel=None, color='blue', marker=None, grid=True):
        """
        Tworzy wykres szeregu czasowego.

        Args:
            date_column (str): Nazwa kolumny zawierającej daty.
            value_column (str): Nazwa kolumny zawierającej wartości.
            figsize (tuple, optional): Rozmiar wykresu. Domyślnie (14, 8).
            title (str, optional): Tytuł wykresu. Domyślnie None.
            xlabel (str, optional): Etykieta osi X. Domyślnie 'Data'.
            ylabel (str, optional): Etykieta osi Y. Domyślnie None.
            color (str, optional): Kolor linii. Domyślnie 'blue'.
            marker (str, optional): Marker punktów. Domyślnie None.
            grid (bool, optional): Czy wyświetlać siatkę. Domyślnie True.

        Returns:
            matplotlib.figure.Figure: Obiekt figury Matplotlib.
        """
        if self.data is None or date_column not in self.data.columns or value_column not in self.data.columns:
            return None

        # Przygotowanie danych
        data = self.data[[date_column, value_column]].dropna().copy()

        # Sprawdzenie, czy kolumna z datami jest w odpowiednim formacie
        if not pd.api.types.is_datetime64_any_dtype(data[date_column]):
            try:
                data[date_column] = pd.to_datetime(data[date_column])
            except:
                print(f"Nie można przekształcić kolumny {date_column} na format daty.")
                return None

        # Sortowanie danych według daty
        data = data.sort_values(by=date_column)

        # Tworzenie wykresu
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(data[date_column], data[value_column], color=color, marker=marker)

        # Dodawanie tytułu i etykiet osi
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title(f'Szereg czasowy: {value_column}', fontsize=14)

        ax.set_xlabel(xlabel, fontsize=12)

        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)
        else:
            ax.set_ylabel(value_column, fontsize=12)

        # Formatowanie osi X
        fig.autofmt_xdate()

        # Dodawanie siatki
        if grid:
            ax.grid(True, linestyle='--', alpha=0.7)

        plt.tight_layout()

        return fig

    def create_bar_chart(self, x_column, y_column=None, figsize=(10, 6), title=None, xlabel=None, ylabel='Liczba',
                         color='skyblue', edgecolor='black', horizontal=False):
        """
        Tworzy wykres słupkowy.

        Args:
            x_column (str): Nazwa kolumny dla kategorii.
            y_column (str, optional): Nazwa kolumny dla wartości. Domyślnie None (zliczanie).
            figsize (tuple, optional): Rozmiar wykresu. Domyślnie (10, 6).
            title (str, optional): Tytuł wykresu. Domyślnie None.
            xlabel (str, optional): Etykieta osi X. Domyślnie None.
            ylabel (str, optional): Etykieta osi Y. Domyślnie 'Liczba'.
            color (str, optional): Kolor słupków. Domyślnie 'skyblue'.
            edgecolor (str, optional): Kolor krawędzi słupków. Domyślnie 'black'.
            horizontal (bool, optional): Czy wykres ma być poziomy. Domyślnie False.

        Returns:
            matplotlib.figure.Figure: Obiekt figury Matplotlib.
        """
        if self.data is None or x_column not in self.data.columns:
            return None

        fig, ax = plt.subplots(figsize=figsize)

        if y_column is None:
            # Zliczanie wartości
            counts = self.data[x_column].value_counts().sort_index()
            x_values = counts.index
            y_values = counts.values
        else:
            if y_column not in self.data.columns:
                print(f"Kolumna {y_column} nie istnieje.")
                return None

            # Agregacja danych
            grouped = self.data.groupby(x_column)[y_column].mean().sort_index()
            x_values = grouped.index
            y_values = grouped.values

        # Tworzenie wykresu słupkowego
        if horizontal:
            ax.barh(x_values, y_values, color=color, edgecolor=edgecolor, alpha=0.7)
        else:
            ax.bar(x_values, y_values, color=color, edgecolor=edgecolor, alpha=0.7)

        # Dodawanie tytułu i etykiet osi
        if title:
            ax.set_title(title, fontsize=14)
        else:
            if y_column:
                ax.set_title(f'Wykres słupkowy: {y_column} według {x_column}', fontsize=14)
            else:
                ax.set_title(f'Wykres słupkowy: częstość {x_column}', fontsize=14)

        if xlabel:
            if horizontal:
                ax.set_ylabel(xlabel, fontsize=12)
            else:
                ax.set_xlabel(xlabel, fontsize=12)
        else:
            if horizontal:
                ax.set_ylabel(x_column, fontsize=12)
            else:
                ax.set_xlabel(x_column, fontsize=12)

        if ylabel:
            if horizontal:
                ax.set_xlabel(ylabel, fontsize=12)
            else:
                ax.set_ylabel(ylabel, fontsize=12)
        else:
            if y_column:
                label = y_column
            else:
                label = 'Liczba'

            if horizontal:
                ax.set_xlabel(label, fontsize=12)
            else:
                ax.set_ylabel(label, fontsize=12)

        # Dodawanie siatki
        ax.grid(True, linestyle='--', alpha=0.7)

        # Dodawanie etykiet wartości na słupkach
        for i, v in enumerate(y_values):
            if horizontal:
                ax.text(v + 0.1, i, f"{v:.2f}", va='center')
            else:
                ax.text(i, v + 0.1, f"{v:.2f}", ha='center')

        plt.tight_layout()

        return fig

    def create_pie_chart(self, column, figsize=(10, 8), title=None, colors=None, explode=None, startangle=90,
                         shadow=False, autopct='%1.1f%%'):
        """
        Tworzy wykres kołowy.

        Args:
            column (str): Nazwa kolumny.
            figsize (tuple, optional): Rozmiar wykresu. Domyślnie (10, 8).
            title (str, optional): Tytuł wykresu. Domyślnie None.
            colors (list, optional): Lista kolorów. Domyślnie None.
            explode (list, optional): Lista wartości odsunięcia wycinków. Domyślnie None.
            startangle (int, optional): Kąt początkowy. Domyślnie 90.
            shadow (bool, optional): Czy dodać cień. Domyślnie False.
            autopct (str, optional): Format etykiet procentowych. Domyślnie '%1.1f%%'.

        Returns:
            matplotlib.figure.Figure: Obiekt figury Matplotlib.
        """
        if self.data is None or column not in self.data.columns:
            return None

        # Zliczanie wartości
        counts = self.data[column].value_counts()

        # Ograniczenie liczby kategorii (jeśli jest ich zbyt wiele)
        max_categories = 8
        if len(counts) > max_categories:
            others = counts.iloc[max_categories:].sum()
            counts = counts.iloc[:max_categories]
            counts['Inne'] = others

        fig, ax = plt.subplots(figsize=figsize)

        # Tworzenie wykresu kołowego
        wedges, texts, autotexts = ax.pie(
            counts.values,
            explode=explode,
            labels=counts.index,
            colors=colors,
            autopct=autopct,
            shadow=shadow,
            startangle=startangle
        )

        # Ustawienie stylu etykiet
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_color('white')

        # Dodawanie tytułu
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title(f'Wykres kołowy dla {column}', fontsize=14)

        # Równe proporcje, aby koło było okrągłe
        ax.axis('equal')

        plt.tight_layout()

        return fig

    def create_heatmap(self, x_column, y_column, z_column, figsize=(12, 10), title=None, cmap='viridis', annot=True,
                       fmt='.2f'):
        """
        Tworzy mapę ciepła dla trzech wybranych kolumn.

        Args:
            x_column (str): Nazwa kolumny dla osi X.
            y_column (str): Nazwa kolumny dla osi Y.
            z_column (str): Nazwa kolumny dla wartości.
            figsize (tuple, optional): Rozmiar wykresu. Domyślnie (12, 10).
            title (str, optional): Tytuł wykresu. Domyślnie None.
            cmap (str, optional): Paleta kolorów. Domyślnie 'viridis'.
            annot (bool, optional): Czy wyświetlać wartości. Domyślnie True.
            fmt (str, optional): Format wartości. Domyślnie '.2f'.

        Returns:
            matplotlib.figure.Figure: Obiekt figury Matplotlib.
        """
        if self.data is None or x_column not in self.data.columns or y_column not in self.data.columns or z_column not in self.data.columns:
            return None

        # Przygotowanie danych
        pivot_data = self.data.pivot_table(index=y_column, columns=x_column, values=z_column, aggfunc='mean')

        # Tworzenie mapy ciepła
        fig, ax = plt.subplots(figsize=figsize)
        heatmap = sns.heatmap(pivot_data, annot=annot, fmt=fmt, cmap=cmap, linewidths=.5, ax=ax)

        # Dodawanie tytułu
        if title:
            ax.set_title(title, fontsize=14)
        else:
            ax.set_title(f'Mapa ciepła: {z_column} według {x_column} i {y_column}', fontsize=14)

        plt.tight_layout()

        return fig

    def create_pair_plot(self, columns=None, hue=None, figsize=(12, 12), title='Wykres par', palette=None,
                         diag_kind='kde'):
        """
        Tworzy wykres par dla wybranych kolumn.

        Args:
            columns (list, optional): Lista nazw kolumn. Domyślnie None (wszystkie kolumny numeryczne).
            hue (str, optional): Nazwa kolumny do kolorowania punktów. Domyślnie None.
            figsize (tuple, optional): Rozmiar wykresu. Domyślnie (12, 12).
            title (str, optional): Tytuł wykresu. Domyślnie 'Wykres par'.
            palette (str, optional): Paleta kolorów. Domyślnie None.
            diag_kind (str, optional): Rodzaj wykresu na przekątnej ('hist', 'kde'). Domyślnie 'kde'.

        Returns:
            matplotlib.figure.Figure: Obiekt figury Matplotlib.
        """
        if self.data is None:
            return None

        # Wybierz tylko kolumny numeryczne
        if columns is None:
            numeric_data = self.data.select_dtypes(include=[np.number])
        else:
            # Sprawdź, czy wszystkie kolumny istnieją
            for col in columns:
                if col not in self.data.columns:
                    print(f"Kolumna {col} nie istnieje.")
                    return None

            numeric_data = self.data[columns].select_dtypes(include=[np.number])

        if numeric_data.empty:
            print("Brak kolumn numerycznych.")
            return None

        # Dodanie kolumny hue, jeśli została podana
        if hue is not None:
            if hue not in self.data.columns:
                print(f"Kolumna {hue} nie istnieje.")
                return None

            numeric_data = pd.concat([numeric_data, self.data[hue]], axis=1)

        # Ograniczenie liczby kolumn, jeśli jest ich zbyt wiele
        max_columns = 5
        if len(numeric_data.columns) > max_columns and columns is None:
            numeric_data = numeric_data.iloc[:, :max_columns]
            if hue is not None and hue not in numeric_data.columns:
                numeric_data = pd.concat([numeric_data, self.data[hue]], axis=1)

        # Tworzenie wykresu par
        g = sns.pairplot(numeric_data, hue=hue, palette=palette, diag_kind=diag_kind,
                         height=figsize[0] / len(numeric_data.columns))

        # Dodawanie tytułu
        g.fig.suptitle(title, fontsize=16)
        g.fig.subplots_adjust(top=0.95)

        return g.fig

    def save_figure(self, fig, filename, dpi=300, bbox_inches='tight'):
        """
        Zapisuje wykres do pliku.

        Args:
            fig (matplotlib.figure.Figure): Obiekt figury Matplotlib.
            filename (str): Nazwa pliku.
            dpi (int, optional): Rozdzielczość. Domyślnie 300.
            bbox_inches (str, optional): Sposób przycinania. Domyślnie 'tight'.

        Returns:
            bool: True jeśli zapisywanie zakończyło się sukcesem, False w przeciwnym przypadku.
        """
        if fig is None:
            return False

        try:
            fig.savefig(filename, dpi=dpi, bbox_inches=bbox_inches)
            return True
        except Exception as e:
            print(f"Błąd podczas zapisywania wykresu: {e}")
            return False

    def get_figure_as_bytesio(self, fig, format='png', dpi=300):
        """
        Zwraca wykres jako obiekt BytesIO.

        Args:
            fig (matplotlib.figure.Figure): Obiekt figury Matplotlib.
            format (str, optional): Format pliku ('png', 'jpg', 'pdf', 'svg'). Domyślnie 'png'.
            dpi (int, optional): Rozdzielczość. Domyślnie 300.

        Returns:
            BytesIO: Obiekt BytesIO zawierający dane wykresu.
        """
        if fig is None:
            return None

        try:
            buf = BytesIO()
            fig.savefig(buf, format=format, dpi=dpi, bbox_inches='tight')
            buf.seek(0)
            return buf
        except Exception as e:
            print(f"Błąd podczas konwersji wykresu: {e}")
            return None