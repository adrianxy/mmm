import logging
import tkinter

from GUI.EntryListFrame import EntryListFrame
from GUI.ExceptionGUIDisplayer import ExceptionGUIDisplayer
from GUI.PlotManager import PlotManager

logging.basicConfig(level=logging.DEBUG)


class MainWindow(tkinter.Tk):
    """
    Główna klasa okna
    """

    def __init__(self, simulator):
        super().__init__()
        self._exception_displayer = ExceptionGUIDisplayer()
        self._simulator = simulator

    def create_window(self):
        """
        Tworzy wszystkie komponenty głównego okna programu i inwokuje uruchomienie programu.
        """

        signal_parameters = {  # Parametry sygnału
            'impulse': ('Amplituda', 'Offset', 'Czas włączenia', 'Czas wyłączenia'),
            'triangle': ('Amplituda', 'Offset', 'Okres', 'Faza początkowa'),
            'sine': ('Amplituda', 'Składowa stała', 'Okres', 'Faza początkowa')
        }

        model_parameters = ('Stała sprężyny (k)', 'Tłumienie (b)', 'Masa (m)')

        simulation_parameters = (
            'Położenie początkowe (x0)', 'Prędkość początkowa (v0)', 'Krok symulacji (h)', 'Czas symulacji (ts)')

        def run_simulation(*args):
            """
            Pobiera wpisane wartości parametrów i uruchamia symulację.
            """
            exceptions_caught = False
            parameters = dict()
            if euler_enabled.get() is False and runge_kutta_enabled.get() is False:
                self._exception_displayer.add_message("Należy wybrać rodzaj symulacji.")
                exceptions_caught = True
            parameters['euler'] = euler_enabled.get()
            parameters['runge_kutta'] = runge_kutta_enabled.get()
            parameters['signal_type'] = selected_signal.get()

            # TODO: Zmodyfikować, gdy kod symulujący będzie gotowy
            for frame, description in zip((signal_param_frame, model_param_frame, sim_param_frame),
                                          ('signal_parameters', 'model_parameters', 'simulation_parameters')):
                parameters[description] = dict()
                for entry_value in frame.entry_values:
                    value_to_insert = entry_value[1].get()
                    if value_to_insert == '':
                        self._exception_displayer.add_message('Pole [' + entry_value[2] + '] nie może pozostać puste.')
                        exceptions_caught = True
                    else:
                        try:
                            parameters[description][entry_value[2]] = float(value_to_insert)
                        except ValueError:
                            exceptions_caught = True
                            self._exception_displayer.add_message('Pole [' + entry_value[2] + '] zawiera '
                                                                                              'nieprawidłową wartość.')
            # Koniec bloku do zmodyfikowania
            if exceptions_caught:
                self._exception_displayer.display_error_message()
                logging.debug('Zgłoszono wyjątek; nie pobrano wartości parametrów.')
            else:
                logging.debug('Parametry: ' + parameters.__str__())
                reset_plots_button_action()
                self._simulator.send_information(lower_plot, upper_plot, parameters)
                self._simulator.run_simulation()

        def reset_plots_button_action(*args):
            """
            Funkcja wywoływana, gdy zostanie wciśnięty przycisk czyszczenia wykresów.
            Wysyła żądanie wyczyszczenia wykresów z sygnałem wejściowym i wyjściowym.
            """
            upper_plot.create_new_plot_area()
            lower_plot.create_new_plot_area()
            upper_plot.legend.clear_legend()
            lower_plot.legend.clear_legend()

        # Konfigurowanie parametrów głównego okna
        self.wm_title('Symulator układu z wózkiem')
        self.wm_resizable(False, False)
        self.wm_geometry("=1200x900+50+50")

        # Tworzenie obiektów potomnych
        plot_frame = tkinter.Frame(self)
        input_frame = tkinter.Frame(self)
        plot_frame.pack(side="right", padx=5, pady=5)
        input_frame.pack(side="left", padx=5, pady=5)

        euler_enabled = tkinter.BooleanVar()
        runge_kutta_enabled = tkinter.BooleanVar()

        # Pole wyboru, która metoda symulacji ma być wyświetlana
        simmethod_frame = tkinter.Frame(input_frame)
        simmethod_frame.grid(column=0, row=0, padx=5, pady=5)
        tkinter.Label(simmethod_frame, text="Metoda symulacji").grid(column=0, columnspan=2, row=0, sticky="n")
        tkinter.Label(simmethod_frame, text="Metoda Eulera").grid(column=0, row=1, sticky="e")
        euler_method_checkbox = tkinter.Checkbutton(simmethod_frame, variable=euler_enabled)
        euler_method_checkbox.grid(column=1, row=1, sticky="w")
        tkinter.Label(simmethod_frame, text="Metoda Rungego-Kutty").grid(column=0, row=2, sticky="e")
        rk_method_checkbox = tkinter.Checkbutton(simmethod_frame, variable=runge_kutta_enabled)
        rk_method_checkbox.grid(column=1, row=2, sticky="w")

        # Zmienna przechowująca rodzaj aktualnie wybranego wymuszenia
        selected_signal = tkinter.StringVar()
        selected_signal.set('impulse')

        # Pole wyboru rodzaju wymuszenia
        signal_type_frame = tkinter.Frame(input_frame)
        signal_type_frame.grid(column=0, row=2, padx=5, pady=5)
        tkinter.Label(signal_type_frame, text="Metoda symulacji").grid(column=0, columnspan=2, row=0, sticky="n")
        tkinter.Label(signal_type_frame, text="Sygnał prostokątny").grid(column=0, row=1)
        rectangle_singal_radio = tkinter.Radiobutton(signal_type_frame, variable=selected_signal, value='impulse')
        rectangle_singal_radio.grid(column=1, row=1)
        tkinter.Label(signal_type_frame, text="Sygnał trójkątny").grid(column=0, row=2)
        triangle_singal_radio = tkinter.Radiobutton(signal_type_frame, variable=selected_signal, value='triangle')
        triangle_singal_radio.grid(column=1, row=2)
        tkinter.Label(signal_type_frame, text="Sygnał sinusoidalny").grid(column=0, row=3)
        harmonic_singal_radio = tkinter.Radiobutton(signal_type_frame, variable=selected_signal, value='sine')
        harmonic_singal_radio.grid(column=1, row=3)

        # Pole wpisu wartości parametrów sygnału
        signal_param_frame = EntryListFrame(input_frame)

        def signal_type_selected(*args):
            """
            Funkcja wywołaywana, gdy zostanie dokonany zapis do zmiennej odpowiadającej za typ wymuszenia
            Wysyła żądanie modyfikacji typów parametrów do obiektu Frame odpowiedzialnego za ich wyświetlanie
            """
            selected_signal_type = selected_signal.get()
            signal_param_frame.update_contents(signal_parameters[selected_signal_type])

        selected_signal.trace_add('write', signal_type_selected)
        signal_param_frame.frame.grid(column=0, row=3, padx=5, pady=5)
        signal_type_selected()

        # Pole wpisu wartości parametrów symulowanego układu
        model_param_frame = EntryListFrame(input_frame)
        model_param_frame.frame.grid(column=0, row=4, padx=5, pady=5)
        model_param_frame.update_contents(model_parameters)

        # Pole wpisu wartości parametrów symulacji
        sim_param_frame = EntryListFrame(input_frame)
        sim_param_frame.frame.grid(column=0, row=5, padx=5, pady=5)
        sim_param_frame.update_contents(simulation_parameters)

        # Pole z przyciskami do aktywowania symulacji
        button_frame = tkinter.Frame(input_frame)
        button_frame.grid(column=0, row=6, padx=5, pady=5)
        run_simulation_button = tkinter.Button(button_frame, text='Uruchom symulację', command=run_simulation)
        run_simulation_button.grid(row=0, column=0)
        reset_button = tkinter.Button(button_frame, text='Resetuj wykresy', command=reset_plots_button_action)
        reset_button.grid(column=1, row=0)

        # Górny wykres
        upper_plot_frame = tkinter.Frame(plot_frame)
        upper_plot_frame.grid(row=0, column=0, padx=5, pady=5)
        tkinter.Label(upper_plot_frame, text="Wykres sygnałów wyjściowych").grid(row=0, column=0)
        upper_plot = PlotManager(upper_plot_frame)
        upper_plot.canvas.grid(column=0, row=1)
        upper_plot.configure(ydesc="y", xdesc="t")
        upper_plot.create_new_plot_area()

        lower_plot_frame = tkinter.Frame(plot_frame)
        lower_plot_frame.grid(row=1, column=0, padx=5, pady=5)
        tkinter.Label(lower_plot_frame, text="Wykres sygnału wejściowego").grid(row=0, column=0)
        lower_plot = PlotManager(lower_plot_frame)
        lower_plot.canvas.grid(column=0, row=1)
        lower_plot.configure(ydesc="u", xdesc="t")
        lower_plot.create_new_plot_area()

        self.mainloop()
