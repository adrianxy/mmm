import tkinter.messagebox


class ExceptionGUIDisplayer:
    """
    Klasa umożliwiająca wyświetlanie komunikatów błędu w postaci wyskakujących okienek.
    Kumuluje wywoływane komunikaty błędu (aby użytkownik nie musiał zamykać wielu okien, tylko dostał pełną informację
    o błędach w programie). Zamraża okno nadrzędne podczas działania.
    """

    def __init__(self):
        self._error_strings = list()

    def add_message(self, message: str):
        """
        Dodaje komunikat o błędzie do listy błędów.
        """
        self._error_strings.append(message)

    def display_error_message(self):
        """
        Bierze wszystkie komunikaty błędów z obecnej listy błędów, wyświetla komunikat o błędach w wyskakującym
        okienku, a następnie czyści kolejkę komunikatów o błędach. Zamraża okno nadrzędne.
        """
        error_message = str()
        for string in self._error_strings:
            error_message += string + '\n'
        tkinter.messagebox.showerror('Błąd', error_message)
        self._error_strings = list()
