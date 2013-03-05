import models
from utils import KOMENCA_DATO, FINIGHA_DATO, PLEJFRUA_DATO, PLEJMALFRUA_DATO

DATE_JAVASCRIPT = ((
    'window.KOMENCA_DATO = new Date({}, {}, {});\n'
    'window.FINIGHA_DATO = new Date({}, {}, {});\n'
    'window.PLEJFRUA_DATO = new Date({}, {}, {});\n'
    'window.PLEJMALFRUA_DATO = new Date({}, {}, {});\n').format(
    KOMENCA_DATO.year, KOMENCA_DATO.month-1, KOMENCA_DATO.day,
    FINIGHA_DATO.year, FINIGHA_DATO.month - 1, FINIGHA_DATO.day,
    PLEJFRUA_DATO.year, PLEJFRUA_DATO.month - 1, PLEJFRUA_DATO.day,
    PLEJMALFRUA_DATO.year, PLEJMALFRUA_DATO.month - 1, PLEJMALFRUA_DATO.day) +
    'window.KOMENCJARO = window.KOMENCA_DATO.getFullYear();\n')

def all_javascript():
    result = []
    for name in dir(models):
        cls = getattr(models, name)
        if hasattr(cls, 'javascript'):
            result.append(cls.javascript())
    return DATE_JAVASCRIPT + '\n'.join(result)

