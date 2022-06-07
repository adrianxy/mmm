class Symulator:

    def __init__(self):
        # Deklaracja pól w __init__ jest dobrą praktyką programistyczną nawet jeżeli nic jeszcze nie ma być do nich
        # przypisane w momencie tworzenia obiektu, można wtedy sprawdzić łatwiej, że nic nie zostało przypisane,
        # inaczej próba odczytu z nieistniejącego pola zakończy się wywaleniem błędu
        self._wykres_wejscia = None
        self._wykres_wyjscia = None
        self._parametry = None

    def send_information(self, wykres_wejscia, wykres_wyjscia, parametry):
        """
        To jest wywoływane przez obiekt w menu głównym, aby przekazać referencje do obiektów wykresów oraz parametry
        symulacji.
        """
        if (wykres_wejscia is None) or (wykres_wyjscia is None) or (parametry is None):
            raise ValueError('Podano nieprawidłowe parametry symulacji.')

        self._wykres_wejscia = wykres_wejscia  # Referencja do wykresu wejścia
        self._wykres_wyjscia = wykres_wyjscia  # Referencja do wykresu wyjścia
        self._parametry = parametry  # Ten atrybut jest dosyć rozbudowany, jest klasy dict: nie chce mi się pisać
        # dokładnie, jak wygląda jego struktura, po wpisaniu jakichś danych do tego mojego GUI i kliknięciu "URUCHOM
        # SYMULACJĘ" do konsoli będzie wywalać jak ten obiekt wygląda w środku, zasadniczo zawiera informacje o tym,
        # jakie opcje wybrał użytkownik

    def run_simulation(self):
        """
        To jest wywoływane, gdy użytkownik wciśnie przycisk "uruchom symulację".
        Ta metoda nie musi się nazywać run_simulation, ale wtedy musiałbym zrobić modyfikację kodu z GUI, który
        uruchamia symulator.
        Wykres jest wcześniej czyszczony z czegokolwiek, co się tam wcześniej znajdowało.
        """

        # Jakiś przykładowy kod dodający rzeczy na wykresach
        # Wykresy są czyszczone automatycznie przed wywołaniem, zadaniem symulatora jest tylko wysyłać żądania
        # zmiany kolorów, dodawania punktów na wykres i upload informacji dotyczącej opisu wykresu

        self._wykres_wejscia.configure(xscale=2, yscale=5, xdiv_number=5, ydiv_number=5, xdesc='t', ydesc='y')
        # Ustawienie parametrów wykresu
        # xscale <- skala podziałki (jeden div - xscale jednostek)
        # yscale <- to samo, tylko że podziałka pionowa
        # xdiv_number, ydiv_number <- ile podziałek ma być, włącznie z działką na zerze (2 oznacza działkę na zerze
        # i jedną działkę jeszcze gdzieś w środku wykresu)
        # xdesc, ydesc <- opis osi, dobrze tu będzie dodać jednostki później
        # powinno się tę metodę wywołać zanim wywoła się create_new_plot_area (poniżej)
        self._wykres_wejscia.create_new_plot_area()  # odświeżenie wykresu

        self._wykres_wejscia.active_plot = 0  # ustaw aktywny wykres, numeracja od zera
        self._wykres_wejscia.add_data_point((0.5, 5))  # dodawanie punktów na wykres
        self._wykres_wejscia.add_data_point((0.2, 5))  # te liczby to (współrzędna pozioma, współrzędna pionowa)
        self._wykres_wejscia.add_data_point((0.11, 5))  # i one mają być wynikami symulacji, obliczaniem gdzie dokładnie
        self._wykres_wejscia.add_data_point((0.1, 5))  # ma się znajdować punkt na ekranie zajmuje się moje GUI
        self._wykres_wejscia.add_data_point((1E-3, 5))

        self._wykres_wejscia.active_plot = 1  # zmiana koloru wykresu (zdefiniowałem 6, więcej sie raczej nie przyda
        self._wykres_wejscia.add_data_point((4, 5))  # bo i tak 2 sygnały wyjściowe mamy tylko kreślić, a dla każdej
        self._wykres_wejscia.add_data_point((3, 2))  # z dwóch metod daje i tak max 4 sygnały
        self._wykres_wejscia.add_data_point((1, 6))
        self._wykres_wejscia.legend.add_entries(('Wejscie 1', 'Wejscie 2'))
        # Dodawanie opisu legendy, kolejne napisy to będą opisy: wykresu 0, wykresu 1, wykresu 2 (zgodnie z numeracją
        # podaną na atrybut active_plot. Dobrze, żeby nie były zbyt długie, bo nie chciało mi się już implementować
        # zawijania tekstu w legendzie i część opisu się utnie. Uwaga: ta metoda przyjmuje krotki (tuple) i jeżeli
        # będziesz chciał przesłać tylko jednego stringa:
        # self._wykres_wejscia.legend.add_entries(('Wejscie 1'))
        # to python będzie iterować po literach, i zostanie utworzonych 9 wpisów do legendy: "W", "e", "j", itd., a po
        # dojściu do "i" program wywali się, bo zrobiłem tylko 6 kolorów. Powinno się to wtedy zrobić tak:
        # self._wykres_wejscia.legend.add_entries(('Wejscie 1', ))
        # z przecinkiem i zamkniętym nawiasem, to mówi Pythonowi: "to jest krotka, ale tylko z jednym elementem, którym
        # jest cały string (a nie każda litera z osobna), potraktuj cały napis "Wejscie 1' jako jedną całość
