from sleep_app.metrics import (horas_por_cronotipo, latencia_por_filtro_luz_azul, reparto_deuda_sueno,
                               sueno_por_app, sueno_por_tramo_movil)


def test_sueno_por_tramo_movil(registros_validos):
    resultado = sueno_por_tramo_movil(registros_validos)

    # cada persona cae en un tramo distinto (20, 45, 90 y 150 minutos)
    assert list(resultado.index) == ["0-30", "31-60", "61-120", "mas de 120"]
    assert resultado["personas"].tolist() == [1, 1, 1, 1]
    assert resultado.loc["mas de 120", "horas_sueno_media"] == 4.0
    assert resultado.loc["mas de 120", "fatiga_media"] == 9.0


def test_sueno_por_app_ordena_por_fatiga(registros_validos):
    resultado = sueno_por_app(registros_validos)

    assert resultado.index[0] == "TikTok / Reels"
    assert resultado.loc["TikTok / Reels", "fatiga_media"] == 7.5
    assert resultado.loc["TikTok / Reels", "horas_sueno_media"] == 4.5


def test_horas_por_cronotipo(registros_validos):
    resultado = horas_por_cronotipo(registros_validos)
    assert resultado.to_dict() == {"Night Owl": 4.5, "Intermediate": 7.0, "Morning Lark": 8.0}


def test_reparto_deuda_sueno_suma_100(registros_validos):
    resultado = reparto_deuda_sueno(registros_validos)

    assert resultado["Moderate Debt"] == 50.0
    assert resultado.sum() == 100.0


def test_latencia_por_filtro_luz_azul(registros_validos):
    resultado = latencia_por_filtro_luz_azul(registros_validos)
    assert resultado.to_dict() == {"con filtro": 20.0, "sin filtro": 60.0}
