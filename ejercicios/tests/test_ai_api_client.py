import json

import pytest

from ejercicios import ai_api_client
from ejercicios.ai_api_client import AIClientError, ErrorTransitorio, complete, complete_con_reintentos


@pytest.fixture(autouse=True)
def sin_esperas(monkeypatch):
    # para que los tests de reintentos no tarden
    monkeypatch.setattr(ai_api_client.time, "sleep", lambda segundos: None)


def test_complete_mock_devuelve_airesponse():
    respuesta = complete("mock", "Hola")
    assert respuesta.provider == "mock"
    assert "Hola" in respuesta.text


def test_complete_proveedor_desconocido_lanza_error():
    with pytest.raises(AIClientError):
        complete("otro", "Hola")


def test_complete_sin_clave_lanza_error(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(AIClientError):
        complete("openai", "Hola")


def test_fail_once_reintenta_y_funciona():
    respuesta = complete_con_reintentos("mock", "Hola", fail_once=True)
    assert respuesta.provider == "mock"


def test_agota_reintentos(monkeypatch):
    llamadas = []

    def siempre_falla(provider, prompt, model=None):
        llamadas.append(1)
        raise ErrorTransitorio("503")

    monkeypatch.setattr(ai_api_client, "complete", siempre_falla)
    with pytest.raises(AIClientError):
        complete_con_reintentos("mock", "Hola")
    assert len(llamadas) == 3  # 1 intento + 2 reintentos


def test_error_de_configuracion_no_se_reintenta(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(AIClientError, match="OPENAI_API_KEY"):
        complete_con_reintentos("openai", "Hola")


def test_batch_genera_una_linea_por_prompt(tmp_path):
    prompts = tmp_path / "prompts.txt"
    prompts.write_text("uno\ndos\n\ntres\ncuatro\ncinco\n", encoding="utf-8")
    salida = tmp_path / "respuestas.jsonl"

    ai_api_client.main(["--provider", "mock", "--batch", str(prompts), "--output", str(salida), "--fail-once"])

    lineas = salida.read_text(encoding="utf-8").splitlines()
    assert len(lineas) == 5
    primera = json.loads(lineas[0])
    assert primera == {"prompt": "uno", "provider": "mock", "text": "[mock] Recibido: uno"}
