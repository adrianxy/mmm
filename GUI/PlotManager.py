import tkinter

from GUI.PlotLegend import PlotLegend


class PlotManager:
    """
    Klasa zarządzająca wykresami.
    """

    height = 400
    width = 900
    colours = ["#0000FF", "#00FF00", "#FF0000", "#FFFF00", '#FF00FF', '#FFFF00']
    # W razie potrzeby kolorów można dopisać więcej

    def __init__(self, master=None, cnf=None, **kw):
        self._x_step = None
        self._y_step = None
        if cnf is None:
            cnf = {}
        self._canvas = tkinter.Canvas(master, cnf, **kw)
        self._canvas.configure(bg='white', width=PlotManager.width, height=PlotManager.height)
        self._active_plot = 0
        self._legend = PlotLegend(self._canvas, PlotManager.colours)
        self._configuration = {'xdesc': 'x', 'ydesc': 'y', 'xdiv_number': 20, 'ydiv_number': 8, 'xscale': 1,
                               'yscale': 1}

    def add_data_point(self, data_point: tuple):
        """
        Dodaje pojedynczy punkt na wykresie. Punkt danych podawany w formacie:
        (współrzędna pozioma, współrzędna pionowa). Przeskalowanie na "współrzędne ekranowe" dokonywana jest
        wewnętrznie.
        """
        x_coordinate = 30 + data_point[0] * self._x_step / self._configuration['xscale']
        y_coordinate = PlotManager.height / 2 - data_point[1] * self._y_step / self._configuration['yscale']
        self._canvas.create_rectangle(x_coordinate - 1, y_coordinate - 1, x_coordinate + 1, y_coordinate + 1,
                                      fill=PlotManager.colours[self.active_plot],
                                      outline=PlotManager.colours[self.active_plot])

    def create_new_plot_area(self):
        """
        Tworzy nowe pole wykresowe, usuwając to, które znajdowało się poprzednio.
        """

        self._canvas.delete('all')

        # Oś pionowa
        self._canvas.create_line(30, 10, 30, PlotManager.height - 10)
        self._canvas.create_line(30, 10, 40, 20)
        self._canvas.create_line(30, 10, 20, 20)
        self._canvas.create_text(50, 20, text=self._configuration['ydesc'])

        # Oś pozioma
        self._canvas.create_line(25, int(PlotManager.height / 2), PlotManager.width - 30, int(PlotManager.height / 2))
        self._canvas.create_line(PlotManager.width - 40, PlotManager.height / 2 - 10, PlotManager.width - 30,
                                 PlotManager.height / 2)
        self._canvas.create_line(PlotManager.width - 40, PlotManager.height / 2 + 10, PlotManager.width - 30,
                                 PlotManager.height / 2)
        self._canvas.create_text(PlotManager.width - 30, PlotManager.height / 2 + 20, text=self._configuration['xdesc'])

        # Podziałka pionowa
        self._y_step = int((PlotManager.height / 2 - 20) / self._configuration['ydiv_number'])
        for k in range(self._configuration['ydiv_number']):
            y_offset = self._y_step * k
            self._canvas.create_line(20, PlotManager.height / 2 + y_offset, 40, PlotManager.height / 2 + y_offset)
            self._canvas.create_line(20, PlotManager.height / 2 - y_offset, 40, PlotManager.height / 2 - y_offset)
            self._canvas.create_text(45, PlotManager.height / 2 - y_offset, text=k * self._configuration["yscale"])
            self._canvas.create_text(45, PlotManager.height / 2 + y_offset, text=-k * self._configuration["yscale"])

        # Podziałka pozioma
        self._x_step = int((PlotManager.width - 40) / self._configuration['xdiv_number'])
        for k in range(self._configuration['xdiv_number']):
            x_offset = self._x_step * k
            self._canvas.create_line(30 + x_offset, PlotManager.height / 2 - 10, 30 + x_offset,
                                     PlotManager.height / 2 + 10)
            self._canvas.create_text(30 + x_offset, PlotManager.height / 2 + 15, text=k * self._configuration["xscale"])

        self._canvas.create_window(PlotManager.width - PlotLegend.width / 2, PlotManager.height - PlotLegend.height / 2,
                                   window=self._legend.canvas)

    def configure(self, **kw):
        """
        Zmienia parametry konfiguracyjne do rysowania wykresów.
        Argumenty podawane przez słowa kluczowe:
            xscale <-- skalowanie osi poziomej [wartości/div]
            yscale <-- skalowanie osi pionowej [wartości/div]
            xdiv_number <-- liczba podziałek osi poziomej
            ydiv_number <-- liczba podziałek osi pionowej
            ydesc <-- opis osi pionowej
            xdesc <-- opis osi poziomej
        """

        for key in kw:
            if key in self._configuration.keys():
                self._configuration[key] = kw[key]
            else:
                raise AttributeError()

    @property
    def active_plot(self):
        """
        Zwraca wartość liczbową odpowiadającą obecnie rysowanemu numerowi wykresu.
        Numeracja zaczyna się od zera.
        """
        return self._active_plot

    @active_plot.setter
    def active_plot(self, new_active_plot):
        if type(new_active_plot) != int:
            raise TypeError("nieprawidłowy typ danych" + new_active_plot + "; powinien być: int")
        self._active_plot = new_active_plot

    @property
    def canvas(self):
        """
        Zwraca bezpośrednio referencję do obiektu Canvas, odpowiadającego za obsługę wykresu.
        """
        return self._canvas

    @property
    def legend(self):
        """
        Zwraca referencję do obiektu PlotLegend skojarzonego z danym obiektem PlotManager.
        """
        return self._legend
