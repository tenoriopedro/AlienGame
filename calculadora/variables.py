
##### MODULO SOMENTE PARA GUARDAR VARIAVEIS CONSTANTES

from pathlib import Path
import re


ROOT_FOLDER = Path(__file__).parent
ROOT_FILES = ROOT_FOLDER / 'Files'
IMAGE_ICON = ROOT_FILES / 'calculadora.png'

# Colors
PRIMARY_COLOR = '#1e81b0'
DARKER_PRIMARY_COLOR = '#16658a'
DARKEST_PRIMARY_COLOR = '#115270'


# Sizing
BIG_FONT_SIZE = 23
MEDIUM_FONT_SIZE = 15
SMALL_FONT_SIZE = 13
TEXT_MARGIN = 5
MINIMUM_WIDTH = 350

# Validações

import re
NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')
def is_num_or_dot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))


def convert_to_number(string: str):
    number = float(string)

    if number.is_integer():
        number = int(number)

    return number


def is_valid_number(string: str):
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        valid = False
    return valid

def is_empty(string: str):
    return len(string) == 0