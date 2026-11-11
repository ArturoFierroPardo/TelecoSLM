"""Utilidades compartidas por la suite de tests.

El repositorio es un conjunto de scripts independientes y no un paquete
instalable, así que los módulos se cargan por ruta de fichero en lugar de por
nombre de import.
"""

import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

# Alias en inglés por compatibilidad con el nombre habitual en pytest.
ROOT = RAIZ


def load_module(ruta_relativa, nombre=None):
    """Carga un módulo a partir de una ruta relativa a la raíz del repositorio."""
    ruta = RAIZ / ruta_relativa
    nombre_modulo = nombre or ruta.stem
    spec = importlib.util.spec_from_file_location(nombre_modulo, ruta)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre_modulo] = modulo
    spec.loader.exec_module(modulo)
    return modulo


# Alias en español, por si se prefiere en los tests.
cargar_modulo = load_module
