import models
from utils import KOMENCA_DATO, FINIGHA_DATO

DATE_JAVASCRIPT = ('window.KOMENCA_DATO = new Date({}, {}, {});\n'
    'window.FINIGHA_DATO = new Date({}, {}, {});\n').format(
    KOMENCA_DATO.year, KOMENCA_DATO.month-1, KOMENCA_DATO.day,
    FINIGHA_DATO.year, FINIGHA_DATO.month-1, FINIGHA_DATO.day)

def all_javascript():
    result = []
    for name in dir(models):
        cls = getattr(models, name)
        if hasattr(cls, 'javascript'):
            result.append(cls.javascript())
    return DATE_JAVASCRIPT + '\n'.join(result)

