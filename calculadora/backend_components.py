
################### MODULO PARA TRATAR DAS AÇÕES DA CALCULADORA

from components_main_window import Display, InfoLabel, MainWindow
from variables import is_valid_number, convert_to_number
from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtGui import QKeyEvent
import math




class BackEnd:


    def __init__(self, display: 'Display', info: 'InfoLabel', window: 'MainWindow', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equation_initial = 'Faça sua conta'
        self._left = None
        self._right = None
        self._operator = None
        self.equation = self._equation_initial

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)



    def connect_button_clicked(self, button, slot):
        button.clicked.connect(slot)
        self.display.setFocus()

    def config_special_button(self, button):

        text = button.text()

        # Limpa Display
        if text == 'C':
            self.connect_button_clicked(button, self._clear)

        # Numero Negativo
        if text == '-N':
            self.connect_button_clicked(button, self._invert_number)

        # Operadores
        if text in '+-/*^':
            self.connect_button_clicked(
                button, self.make_slot(self._config_left_op, text)
            )

        if text == '=':
            self.connect_button_clicked(
            button, self._eq)

        # Apaga caracteres
        if text == '<<<':
            self.connect_button_clicked(button, self._backspace)


    @Slot()
    def make_slot(self, func, *args, **kwargs):
        @Slot(bool)
        def real_slot(_):
            func(*args, **kwargs)

        return real_slot

    @Slot()
    def _invert_number(self):   # Numero negativo
        display_text = self.display.text()
        self.display.setFocus()

        if not is_valid_number(display_text):
            return

        number = convert_to_number(display_text) * -1
        self.display.setText(str(number))

    @Slot()
    def _insert_to_display(self, text):
        new_display_value = self.display.text() + text

        if not is_valid_number(new_display_value):
            return

        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._operator = None
        self.equation = self._equation_initial
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _config_left_op(self, text):
        display_text = self.display.text() # Numero da esquerda (_left)
        self.display.clear() # Limpa o display
        self.display.setFocus()

        # Se a pessoa clicou no operador sem
        # configurar qualquer numero
        if not is_valid_number(display_text) and self._left is None:
            self._show_error('Digite Algo')
            return


        # Se houver algo no numero da esquerda,
        # nao fazemos nada. Aguardando numero da direita

        if self._left is None:
            self._left = convert_to_number(display_text)

        self._operator = text
        self.equation = f'{self._left} {self._operator} ??'

    @Slot()
    def _eq(self):
        display_text = self.display.text()

        if not is_valid_number(display_text) or self._left is None:
            self._show_error('Conta incompleta')
            return


        self._right = convert_to_number(display_text)
        self.equation = f'{self._left} {self._operator} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, int | float):
                result = math.pow(self._left, self._right)
                result = convert_to_number(str(result))
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._show_error('Divisão por zero')
        except OverflowError:
            self._show_error('Essa conta não pode ser realizada')


        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None
        self.display.setFocus()

        if result == 'error':
            self._left = None

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    def _make_dialog(self, text):
        msg_box = self.window.make_message_box()
        msg_box.setText(text)
        return msg_box

    def _show_error(self, text):
        msg_box = self._make_dialog(text)
        msg_box.setIcon(msg_box.Icon.Critical)
        msg_box.exec()
        self.display.setFocus()

    def _show_info(self, text):
        msg_box = self._make_dialog(text)
        msg_box.setIcon(msg_box.Icon.Information)
        msg_box.exec()
        self.display.setFocus()
