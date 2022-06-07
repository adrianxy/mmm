from GUI.MainWindow import MainWindow
from Symulator import Symulator

if __name__ == '__main__':
    simulator = Symulator()
    main_window = MainWindow(simulator)
    main_window.create_window()
