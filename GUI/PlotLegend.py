import tkinter


class PlotLegend:
    width = 100
    height = 100

    def __init__(self, master, list_of_colours):
        self._canvas = tkinter.Canvas(master, height=PlotLegend.height, width=PlotLegend.width)
        self._list_of_colours = list_of_colours
        self._number_of_entries = 0

    def clear_legend(self):
        """
        Czyści legendę.
        """
        self._canvas.delete('all')
        self._number_of_entries = 0

    def add_entries(self, entries):
        """
        Dodaje oznaczenie do legendy.
        """
        for entry in entries:
            self._canvas.create_rectangle(5, 5 + self._number_of_entries * 15, 10, 10 + self._number_of_entries * 15,
                                          fill=self._list_of_colours[self._number_of_entries],
                                          outline=self._list_of_colours[self._number_of_entries])
            self._canvas.create_text(PlotLegend.width / 2 + 10, 6 + self._number_of_entries * 15, text=entry)
            self._number_of_entries += 1

    @property
    def canvas(self):
        """
        Zwraca refernecję do wewnętrznego obiektu Canvas.
        """
        return self._canvas
