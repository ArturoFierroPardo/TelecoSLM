"""Tests de las funciones auxiliares de graficas_y_tests/calcula_metricas.py."""

import pytest

from conftest import cargar_modulo

cm = cargar_modulo("graficas_y_tests/calcula_metricas.py")


class TestDetectarDataset:
    """El dataset se deduce del nombre del fichero de métricas."""

    @pytest.mark.parametrize(
        "nombre, esperado",
        [
            ("metricas_por_fila_teleco_Qwen3_1.7B", "Teleco"),
            ("metricas_por_fila_Qwen3_1.7B_FT_valtest", "Teleco"),
            ("metricas_por_fila_GAN_valtest", "Teleco"),
            ("metricas_por_fila_webNLG_Gemma_3_1B", "WebNLG"),
            ("metricas_por_fila_totto_Llama_1B", "ToTTo"),
            ("metricas_por_fila_kelm_stem_Qwen3_1.7B", "KELM"),
        ],
    )
    def test_reconoce_cada_dataset(self, nombre, esperado):
        assert cm.detectar_dataset(nombre) == esperado

    def test_es_insensible_a_mayusculas(self):
        assert cm.detectar_dataset("METRICAS_WEBNLG_X") == "WebNLG"

    def test_nombre_no_reconocido_devuelve_unknown(self):
        assert cm.detectar_dataset("metricas_por_fila_otracosa") == "unknown"


class TestBertConfig:
    """BERTScore usa un modelo en español para Teleco y en inglés para el resto."""

    def test_teleco_usa_modelo_multilingue_en_espanol(self):
        assert cm.bert_config("Teleco") == {
            "lang": "es",
            "model_type": "xlm-roberta-base",
        }

    @pytest.mark.parametrize("dataset", ["WebNLG", "ToTTo", "KELM", "unknown"])
    def test_resto_de_datasets_usan_ingles(self, dataset):
        config = cm.bert_config(dataset)
        assert config["lang"] == "en"
        assert config["model_type"] == "distilbert-base-uncased"


class TestParsearResults:
    """Los nombres results_*.csv se traducen a nombre de métricas y clave de precio."""

    def test_mapa_directo(self):
        nombre, precio = cm.parsear_results("results_GAN_valtest.csv")
        assert (nombre, precio) == ("GAN_valtest", "gan")

    def test_mini_slm_sobre_teleco(self):
        nombre, precio = cm.parsear_results("results_teleco_Qwen3_1.7B.csv")
        assert (nombre, precio) == ("teleco_Qwen3_1.7B", "mini-qwen")

    def test_modelo_de_api_combina_modelo_y_dataset(self):
        nombre, precio = cm.parsear_results("results_webNLG_deepseek-chat.csv")
        assert (nombre, precio) == ("DeepSeek_WebNLG", "deepseek")

    def test_acepta_ruta_completa(self):
        nombre, _ = cm.parsear_results(
            "/tmp/resultados/results_totto_llama-3.3-70b-instruct.csv"
        )
        assert nombre == "Llama_70B_ToTTo"

    def test_fichero_desconocido_devuelve_none(self):
        assert cm.parsear_results("results_inventado.csv") == (None, None)


class TestPrecios:
    """Toda clave de precio referenciada en los mapas debe existir en PRECIOS."""

    def test_todas_las_claves_de_precio_estan_definidas(self):
        claves = {precio for _, precio in cm.MAPA_DIRECTO.values()}
        claves |= {precio for _, precio in cm.MODELO_API.values()}
        faltantes = claves - set(cm.PRECIOS)
        assert not faltantes, f"Claves sin precio definido: {faltantes}"

    def test_todas_las_claves_tienen_consumo_energetico(self):
        faltantes = set(cm.PRECIOS) - set(cm.KWH_POR_TOKEN)
        assert not faltantes, f"Claves sin kWh por token: {faltantes}"

    def test_la_gan_no_tiene_coste_de_api(self):
        assert cm.PRECIOS["gan"] == {"input": 0.0, "output": 0.0}


class TestLeerResults:
    """Las filas con error o mal formadas se descartan al leer los resultados."""

    def _escribir(self, tmp_path, lineas):
        archivo = tmp_path / "results_demo.csv"
        archivo.write_text("\n".join(lineas), encoding="utf-8")
        return str(archivo)

    def test_lee_filas_validas(self, tmp_path):
        archivo = self._escribir(
            tmp_path,
            [
                "input,reference,generated,time",
                "pregunta,referencia,respuesta,1.5",
                "otra,otra ref,otra resp,2.0",
            ],
        )
        filas = cm.leer_results(archivo)
        assert len(filas) == 2
        assert filas[0][0] == "pregunta"

    def test_descarta_filas_con_error_en_la_generacion(self, tmp_path):
        archivo = self._escribir(
            tmp_path,
            [
                "input,reference,generated,time",
                "pregunta,referencia,Error: timeout,0.0",
                "buena,referencia,respuesta,1.0",
            ],
        )
        filas = cm.leer_results(archivo)
        assert len(filas) == 1
        assert filas[0][0] == "buena"

    def test_descarta_separadores_y_filas_incompletas(self, tmp_path):
        archivo = self._escribir(
            tmp_path,
            [
                "input,reference,generated,time",
                "--- corte,x,y,z",
                "incompleta,solo dos",
                "buena,referencia,respuesta,1.0",
            ],
        )
        filas = cm.leer_results(archivo)
        assert len(filas) == 1


class TestContarTokens:
    """El conteo de tokens debe ser determinista y crecer con el texto."""

    def test_devuelve_entero_positivo(self):
        assert cm.contar_tokens("una frase de prueba") > 0

    def test_es_determinista(self):
        texto = "modelo de lenguaje de dominio especifico"
        assert cm.contar_tokens(texto) == cm.contar_tokens(texto)

    def test_texto_mas_largo_no_cuenta_menos(self):
        corto = cm.contar_tokens("hola")
        largo = cm.contar_tokens("hola " * 50)
        assert largo > corto

    def test_acepta_entradas_no_textuales(self):
        assert cm.contar_tokens(12345) > 0
