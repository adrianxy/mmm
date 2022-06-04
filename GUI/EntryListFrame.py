import tkinter


class EntryListFrame:
    """
    Ramka z tytułem oraz napisami, możliwością aktualizowania liczby oraz treści napisów oraz pobierania wszystkich
    wartości z pól tekstowych jednocześnie.
    """

    def __init__(self, master=None, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        self._frame = tkinter.Frame(master, cnf, **kw)
        self._entries = list()  # Format: (Label, Entry, str)

    def update_contents(self, text_field_names: tuple):
        """
        Aktualizuje wartości pól tekstowych. Tworzy tyle pól, ile jest elementów w podanej krotce. Czyści poprzednią
        zawartość ramki.
        """
        # Czyszczenie obecnej zawartości ramki:
        for entry_tuple in self._entries:
            for object_ in entry_tuple:
                if type(object_) != str:
                    object_.grid_forget()
        self._entries = list()

        # Dodawanie krotki z wszystkimi przekazanymi nazwami parametrów
        number_of_iteration = -1
        for name in text_field_names:
            number_of_iteration += 1
            label = tkinter.Label(self._frame, text=name + ':')
            label.grid(column=0, row=number_of_iteration)
            entry = tkinter.Entry(self._frame)
            entry.grid(column=1, row=number_of_iteration)
            self._entries.append((label, entry, name))

    @property
    def frame(self):
        """
        Zwraca wewnętrzny atrybut ramki
        """
        return self._frame

    @property
    def entry_values(self):
        """
        Zwraca wartości atrybutów wejściowych
        """
        return self._entries
