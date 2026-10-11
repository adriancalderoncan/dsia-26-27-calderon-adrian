"""Métricas sobre los registros válidos del dataset de sueño."""

import pandas as pd

# tramos de minutos con el movil en la cama antes de dormir
TRAMOS_MINUTOS = [0, 30, 60, 120, float("inf")]
NOMBRES_TRAMOS = ["0-30", "31-60", "61-120", "mas de 120"]
DECIMALES = 2


def sueno_por_tramo_movil(validos: pd.DataFrame) -> pd.DataFrame:
    """Horas de sueño y fatiga media según los minutos de móvil antes de dormir."""
    tramo = pd.cut(validos["bedtime_phone_minutes"], bins=TRAMOS_MINUTOS,
                   labels=NOMBRES_TRAMOS, include_lowest=True).rename("minutos_movil")
    resumen = validos.groupby(tramo, observed=True).agg(
        personas=("user_id", "count"),
        horas_sueno_media=("total_sleep_hours", "mean"),
        fatiga_media=("next_day_fatigue_score", "mean"),
    )
    return resumen.round(DECIMALES)


def sueno_por_app(validos: pd.DataFrame) -> pd.DataFrame:
    """Horas de sueño y fatiga media por app usada antes de dormir (más fatiga primero)."""
    resumen = validos.groupby("primary_bedtime_app").agg(
        horas_sueno_media=("total_sleep_hours", "mean"),
        fatiga_media=("next_day_fatigue_score", "mean"),
    )
    return resumen.sort_values("fatiga_media", ascending=False).round(DECIMALES)


def horas_por_cronotipo(validos: pd.DataFrame) -> pd.Series:
    """Horas de sueño medias de cada cronotipo, de menos a más."""
    return validos.groupby("chronotype")["total_sleep_hours"].mean().sort_values().round(DECIMALES)


def reparto_deuda_sueno(validos: pd.DataFrame) -> pd.Series:
    """Porcentaje de personas en cada categoría de deuda de sueño."""
    return (validos["sleep_debt_category"].value_counts(normalize=True) * 100).round(1)


def latencia_por_filtro_luz_azul(validos: pd.DataFrame) -> pd.Series:
    """Minutos medios que se tarda en dormir con y sin filtro de luz azul."""
    con_filtro = validos["blue_light_filter_active"].map({1: "con filtro", 0: "sin filtro"})
    return validos.groupby(con_filtro)["sleep_latency_min"].mean().round(DECIMALES)
