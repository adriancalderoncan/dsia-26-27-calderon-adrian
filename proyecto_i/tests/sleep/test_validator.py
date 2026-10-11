import pandas as pd
import pytest

from sleep_app.validator import Rango, ValidationError, validar_registros


def test_todos_validos(registros_validos):
    validos, errores = validar_registros(registros_validos)
    assert len(validos) == 4
    assert len(errores) == 0


@pytest.mark.parametrize("cambio, motivo", [
    ({"age": None}, "valores nulos"),
    ({"total_sleep_hours": "mucho"}, "valores nulos"),
    ({"user_id": "USER-1"}, "user_id con formato incorrecto"),
    ({"gender": "Otro"}, "gender con valor desconocido"),
    ({"primary_bedtime_app": "Twitch"}, "primary_bedtime_app con valor desconocido"),
    ({"blue_light_filter_active": 2}, "blue_light_filter_active con valor desconocido"),
    ({"age": 10}, "age fuera de rango"),
    ({"bedtime_phone_minutes": -1}, "bedtime_phone_minutes fuera de rango"),
    ({"screen_brightness_pct": 101}, "screen_brightness_pct fuera de rango"),
    ({"total_sleep_hours": 25}, "total_sleep_hours fuera de rango"),
    ({"next_day_fatigue_score": 0}, "next_day_fatigue_score fuera de rango"),
    ({"deep_sleep_pct": 60.0, "rem_sleep_pct": 50.0}, "deep_sleep_pct + rem_sleep_pct mayor que 100"),
])
def test_registro_invalido_va_a_errores_con_su_motivo(crear_registro, cambio, motivo):
    df = pd.DataFrame([crear_registro("USR-00001"), crear_registro(**{"user_id": "USR-00002", **cambio})])

    validos, errores = validar_registros(df)

    assert len(validos) == 1
    assert len(errores) == 1
    assert errores["motivo"].iloc[0] == motivo


@pytest.mark.parametrize("fatiga, es_valido", [(1, True), (10, True), (0.9, False), (10.1, False)])
def test_bordes_de_la_fatiga(crear_registro, fatiga, es_valido):
    df = pd.DataFrame([crear_registro(next_day_fatigue_score=fatiga)])
    validos, _ = validar_registros(df)
    assert len(validos) == int(es_valido)


def test_user_id_duplicado_se_queda_el_primero(crear_registro):
    df = pd.DataFrame([crear_registro("USR-00001", age=30), crear_registro("USR-00001", age=40)])

    validos, errores = validar_registros(df)

    assert validos["age"].tolist() == [30]
    assert errores["motivo"].tolist() == ["user_id duplicado"]


def test_no_modifica_el_original(crear_registro):
    df = pd.DataFrame([crear_registro(age="treinta")])

    validos, errores = validar_registros(df)

    assert df.loc[0, "age"] == "treinta"
    assert errores["motivo"].tolist() == ["valores nulos"]


def test_sin_columnas_obligatorias_lanza_error(registros_validos):
    with pytest.raises(ValidationError, match="total_sleep_hours"):
        validar_registros(registros_validos.drop(columns=["total_sleep_hours"]))


def test_rango_contiene_los_extremos():
    rango = Rango(0, 10)
    assert rango.contiene(pd.Series([0, 5, 10, 11])).tolist() == [True, True, True, False]
