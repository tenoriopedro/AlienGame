
#################### MODULO ONDE A CALCULADORA É EXECUTADA

import sys
from components_main_window import (MainWindow, set_up_theme,
                                    InfoLabel, ButtonsGrid, Display)
from backend_components import BackEnd
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from variables import IMAGE_ICON
from PySide6.QtCore import Qt



if __name__ == '__main__':
    # Criar app
    app = QApplication(sys.argv)
    window = MainWindow()

    # Define ícone
    icon = QIcon(str(IMAGE_ICON))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)


    # Definindo Tema
    set_up_theme()

    # Info
    info_label = InfoLabel()
    window.add_widget_to_layout(info_label)

    # Display
    display = Display()
    window.add_widget_to_layout(display)

    # Grid de Botões
    back_end = BackEnd(display=display, info=info_label, window=window)
    buttons_grid = ButtonsGrid(display, back_end)
    window.v_layout.addLayout(buttons_grid)

    # ultima coisa a ser feita
    window.adjust_fixed_size()
    window.show()
    app.exec()
