"""Tests de integridad del split train/val/test versionado en el repositorio.

La afirmación científica del Grupo 2 depende de que ningún subtema aparezca en
más de un split. Estos tests vigilan esa propiedad sobre el artefacto que
realmente se distribuye con el proyecto.
"""

import json

import pytest

from conftest import RAIZ

RUTA_SPLITS = RAIZ / "splits" / "splits_por_subtema.json"


@pytest.fixture(scope="module")
def splits():
    with open(RUTA_SPLITS, encoding="utf-8") as f:
        return json.load(f)


class TestEstructura:
    """El fichero existe y trae los metadatos que documentan el método."""

    def test_el_fichero_existe(self):
        assert RUTA_SPLITS.exists()

    @pytest.mark.parametrize(
        "clave",
        [
            "seed",
            "train_ratio",
            "val_ratio",
            "test_ratio",
            "train_ids",
            "val_ids",
            "test_ids",
            "n_filas_total",
        ],
    )
    def test_contiene_las_claves_necesarias(self, splits, clave):
        assert clave in splits

    def test_la_semilla_queda_registrada(self, splits):
        assert splits["seed"] == 42


class TestSinFugaDeDatos:
    """Ningún id puede aparecer en más de un split."""

    def test_train_y_val_son_disjuntos(self, splits):
        assert not set(splits["train_ids"]) & set(splits["val_ids"])

    def test_train_y_test_son_disjuntos(self, splits):
        assert not set(splits["train_ids"]) & set(splits["test_ids"])

    def test_val_y_test_son_disjuntos(self, splits):
        assert not set(splits["val_ids"]) & set(splits["test_ids"])

    def test_no_hay_ids_repetidos_dentro_de_un_split(self, splits):
        for nombre in ("train_ids", "val_ids", "test_ids"):
            ids = splits[nombre]
            assert len(ids) == len(set(ids)), f"Ids duplicados en {nombre}"


class TestCoherencia:
    """Los recuentos declarados deben cuadrar con las listas reales de ids."""

    @pytest.mark.parametrize(
        "clave_ids, clave_n",
        [
            ("train_ids", "n_filas_train"),
            ("val_ids", "n_filas_val"),
            ("test_ids", "n_filas_test"),
        ],
    )
    def test_los_recuentos_declarados_cuadran(self, splits, clave_ids, clave_n):
        assert len(splits[clave_ids]) == splits[clave_n]

    def test_las_particiones_suman_el_total(self, splits):
        total = (
            len(splits["train_ids"])
            + len(splits["val_ids"])
            + len(splits["test_ids"])
        )
        assert total == splits["n_filas_total"]

    def test_las_ratios_suman_uno(self, splits):
        suma = splits["train_ratio"] + splits["val_ratio"] + splits["test_ratio"]
        assert suma == pytest.approx(1.0)

    def test_ningun_split_esta_vacio(self, splits):
        for nombre in ("train_ids", "val_ids", "test_ids"):
            assert splits[nombre], f"{nombre} está vacío"

    def test_train_es_la_particion_mayoritaria(self, splits):
        assert len(splits["train_ids"]) > len(splits["val_ids"])
        assert len(splits["train_ids"]) > len(splits["test_ids"])

    def test_la_proporcion_real_se_acerca_a_la_declarada(self, splits):
        total = splits["n_filas_total"]
        real = len(splits["train_ids"]) / total
        assert real == pytest.approx(splits["train_ratio"], abs=0.05)
