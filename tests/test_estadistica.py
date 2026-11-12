"""Tests de las funciones estadísticas usadas en los scripts de análisis."""

import numpy as np
import pytest

from conftest import cargar_modulo

bs = cargar_modulo("graficas_y_tests/bootstrap.py")
ap = cargar_modulo("graficas_y_tests/analisis_p.py")


class TestBootstrapCI:
    """El intervalo de confianza bootstrap debe ser reproducible y coherente."""

    @pytest.fixture
    def datos(self):
        rng = np.random.RandomState(0)
        return rng.normal(loc=0.5, scale=0.1, size=500)

    def test_el_intervalo_contiene_a_la_media(self, datos):
        media, ci_low, ci_high, _ = bs.bootstrap_ci(datos, n_boot=200, seed=42)
        assert ci_low <= media <= ci_high

    def test_el_ancho_es_la_diferencia_entre_extremos(self, datos):
        _, ci_low, ci_high, ancho = bs.bootstrap_ci(datos, n_boot=200, seed=42)
        assert ancho == pytest.approx(ci_high - ci_low)

    def test_la_misma_semilla_da_el_mismo_intervalo(self, datos):
        primero = bs.bootstrap_ci(datos, n_boot=200, seed=42)
        segundo = bs.bootstrap_ci(datos, n_boot=200, seed=42)
        assert primero == segundo

    def test_semillas_distintas_dan_intervalos_distintos(self, datos):
        _, low_a, high_a, _ = bs.bootstrap_ci(datos, n_boot=200, seed=1)
        _, low_b, high_b, _ = bs.bootstrap_ci(datos, n_boot=200, seed=2)
        assert (low_a, high_a) != (low_b, high_b)

    def test_la_media_devuelta_es_la_de_los_datos(self, datos):
        media, _, _, _ = bs.bootstrap_ci(datos, n_boot=200, seed=42)
        assert media == pytest.approx(np.mean(datos))

    def test_mas_remuestreos_no_desplazan_el_intervalo(self, datos):
        _, low_pocos, high_pocos, _ = bs.bootstrap_ci(datos, n_boot=200, seed=42)
        _, low_muchos, high_muchos, _ = bs.bootstrap_ci(datos, n_boot=2000, seed=42)
        assert low_muchos == pytest.approx(low_pocos, abs=0.01)
        assert high_muchos == pytest.approx(high_pocos, abs=0.01)


class TestFormatearP:
    """Los p-valores siempre deben mostrarse como algo legible."""

    def test_cero_se_muestra_como_cota(self):
        assert ap.formatear_p(0.0) == "< 1.0e-300"

    def test_valores_por_debajo_del_minimo_representable(self):
        assert ap.formatear_p(1e-310) == "< 1.0e-300"

    def test_valores_muy_pequenos_en_notacion_cientifica(self):
        assert ap.formatear_p(0.0005) == "5.00e-04"

    def test_valores_normales_con_cuatro_decimales(self):
        assert ap.formatear_p(0.05) == "0.0500"

    @pytest.mark.parametrize("p", [0.0, 1e-310, 1e-50, 0.0005, 0.05, 0.5, 1.0])
    def test_nunca_devuelve_cadena_vacia(self, p):
        assert ap.formatear_p(p).strip()
