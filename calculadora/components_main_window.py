from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget,
                               QPushButton, QLabel, QLineEdit,
                               QGridLayout, QMessageBox)
from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtGui import QKeyEvent
import qdarktheme
from variables import (PRIMARY_COLOR, DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR,
                       MEDIUM_FONT_SIZE, SMALL_FONT_SIZE,BIG_FONT_SIZE,
                       TEXT_MARGIN,is_empty, MINIMUM_WIDTH,
                       is_valid_number, is_num_or_dot)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend_components import BackEnd, BackDisplay

############ MODULO PARA DEFINIÇÕES VISUAIS DA CALCULADORA


### CRIANDO JANELA PRINCIPAL
class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        # Configurando o layout
        self.cw = QWidget()
        self.v_layout = QVBoxLayout()
        self.cw.setLayout(self.v_layout)
        self.setCentralWidget(self.cw)

        # Titulo da janela
        self.setWindowTitle('Calculadora')

    def add_widget_to_layout(self, widget: QWidget):
        self.v_layout.addWidget(widget)
        #self.adjust_fixed_size()


    def adjust_fixed_size(self):
        # Ultima coisa a ser feita
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def make_message_box(self):
        return QMessageBox(self)


### DEFININDO TEMA DA JANELA PRINCIPAL

# Definindo cores do botão
qss = f'''
    QPushButton[cssClass="specialButton"] {{
    color: #fff;
    background: "{PRIMARY_COLOR}";
    }}
    QPushButton[cssClass="specialButton"]:hover {{
    color: #fff;
    background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
    color: #fff;
    background: {DARKEST_PRIMARY_COLOR};
    }}
'''

# Definindo o tema da calculadora
def set_up_theme():
    qdarktheme.setup_theme(additional_qss=qss)




### COLOCANDO O INPUT DA CALCULADORA(DISPLAY)

class Display(QLineEdit):
    eq_pressed = Signal()
    del_pressed = Signal()
    clear_pressed = Signal()
    input_pressed = Signal(str)
    operator_pressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_style_display()

        # self.setReadOnly(True) # -> Isto é para não permitir entrada de teclas a partir do teclado


    def config_style_display(self):
        margins = [TEXT_MARGIN for _ in range(4)]
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)


    # Função para permitir a entrada de teclas do teclado
    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        is_enter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        is_delete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        is_esc = key in [KEYS.Key_Escape, KEYS.Key_C]
        is_operator = key in [
            KEYS.Key_Plus, KEYS.Key_Minus,
            KEYS.Key_Slash, KEYS.Key_Asterisk, KEYS.Key_P]


        if is_enter :
            self.eq_pressed.emit()
            return event.ignore()

        if is_delete or text == '«':
            self.del_pressed.emit()
            return event.ignore()

        if is_esc:
            self.clear_pressed.emit()
            return event.ignore()

        if is_operator or text == '%':
            if text.lower() == 'p':
                text = '^'
            self.operator_pressed.emit(text)
            return event.ignore()

        # Não passar daqui se não tiver texto
        if is_empty(text):
            return event.ignore()

        if is_num_or_dot(text):
            self.input_pressed.emit(text)
            return event.ignore()

### DEFININDO INFORMAÇÃO DA ATUAL CONTA NA CALCULADORA(ACIMA DO INPUT)

class InfoLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_style_info()

    def config_style_info(self):

        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)




### DEFININDO BOTÕES DA CALCULADORA

class Button(QPushButton):
    def __init__(self, *args, ** kwargs):
        super().__init__(*args, **kwargs)
        self.config_style_button()

    def config_style_button(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(50, 50)

# DEFININDO A POSIÇÃO DAS TECLAS NA CALCULADORA

class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', back_end: 'BackEnd' ,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ['C', '<<<', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['-N', '0', '.', '=']
        ]
        self.back_end = back_end # Back End faz parte de outro modulo(backend_components)
                                 # onde é tratado as ações da Calculadora
        self.display = display
        self._make_grid()


    def _make_grid(self):
        self.display.eq_pressed.connect(self.back_end._eq)
        self.display.del_pressed.connect(self.back_end._backspace)
        self.display.clear_pressed.connect(self.back_end._clear)
        self.display.input_pressed.connect(self.back_end._insert_to_display)
        self.display.operator_pressed.connect(self.back_end._config_left_op)

        for row_number, row_data in enumerate(self._grid_mask):
            for column_number, button_text in enumerate(row_data):
                button = Button(button_text)


                if button_text not in '0123456789.':
                    button.setProperty('cssClass', 'specialButton')
                    self.back_end.config_special_button(button)


                # DEFININDO O QUE É ESCRITO NA CALCULADORA
                self.addWidget(button, row_number, column_number)
                slot = self.back_end.make_slot(
                    self.back_end._insert_to_display, button_text)
                self.back_end.connect_button_clicked(button, slot)

