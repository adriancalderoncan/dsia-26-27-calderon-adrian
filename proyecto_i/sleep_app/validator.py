"""Reglas de validación del dataset de sueño.

Cada fila inválida se guarda con una columna "motivo" que dice la primera
regla que no cumple, así se puede revisar después por qué se ha descartado.
"""

from dataclasses import dataclass

import pandas as pd

COLUMNAS_OBLIGATORIAS = [
    "user_id", "age", "gender", "occupation_type", "chronotype",
    "bedtime_phone_minutes", "primary_bedtime_app", "screen_brightness_pct",
    "blue_light_filter_active", "caffeine_post_5pm_mg", "physical_activity_min",
    "sleep_latency_min", "total_sleep_hours", "deep_sleep_pct", "rem_sleep_pct",
    "morning_alarm_snoozes", "next_day_fatigue_score", "sleep_debt_category",
]

FORMATO_USER_ID = r"USR-\d{5}"

VALORES_PERMITIDOS = {
    "gender": {"Female", "Male", "Non-Binary"},
    "occupation_type": {"Corporate 9-to-5", "Remote Tech", "Student",
                        "Healthcare / Shift Worker", "Freelance / Creative"},
    "chronotype": {"Intermediate", "Night Owl", "Morning Lark"},
    "primary_bedtime_app": {"TikTok / Reels", "YouTube", "Instagram / Reddit",
                            "Streaming (Netflix/Hulu)", "Messaging / Chat", "News / Reading"},
    "sleep_debt_category": {"Optimal Recovery", "Mild Deficit", "Moderate Debt", "Severe Sleep Debt"},
    "blue_light_filter_active": {0, 1},
}


@dataclass(frozen=True)
class Rango:
    """Intervalo cerrado [minimo, maximo] de valores aceptados para una columna."""

    minimo: float
    maximo: float

    def contiene(self, valores: pd.Series) -> pd.Series:
        """True para cada valor dentro del rango (los extremos cuentan). Los NaN dan False."""
        return valores.between(self.minimo, self.maximo)


# limites que sean posibles en la realidad, no los min/max que trae el dataset
RANGOS = {
    "age": Rango(18, 100),
    "bedtime_phone_minutes": Rango(0, 600),
    "screen_brightness_pct": Rango(0, 100),
    "caffeine_post_5pm_mg": Rango(0, 1000),
    "physical_activity_min": Rango(0, 600),
    "sleep_latency_min": Rango(0, 300),
    "total_sleep_hours": Rango(0, 24),
    "deep_sleep_pct": Rango(0, 100),
    "rem_sleep_pct": Rango(0, 100),
    "morning_alarm_snoozes": Rango(0, 50),
    "next_day_fatigue_score": Rango(1, 10),
}

COLUMNAS_NUMERICAS = list(RANGOS) + ["blue_light_filter_active"]


class ValidationError(Exception):
    """El fichero no tiene las columnas que se esperan."""


def validar_registros(registros: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separa los registros en (validos, errores).

    Reglas, en este orden:
      1. sin valores nulos (un texto en una columna numerica cuenta como nulo)
      2. user_id con formato USR-00000
      3. user_id sin repetir (se queda el primero)
      4. columnas categoricas con un valor conocido
      5. columnas numericas dentro de su rango
      6. deep_sleep_pct + rem_sleep_pct no puede pasar de 100

    Lanza ValidationError si falta alguna columna obligatoria.
    """
    faltan = [col for col in COLUMNAS_OBLIGATORIAS if col not in registros.columns]
    if faltan:
        raise ValidationError(f"Faltan columnas: {faltan}")

    df = registros.copy()
    for col in COLUMNAS_NUMERICAS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    comprobaciones = [
        (df[COLUMNAS_OBLIGATORIAS].isna().any(axis=1), "valores nulos"),
        (~df["user_id"].astype(str).str.fullmatch(FORMATO_USER_ID), "user_id con formato incorrecto"),
        (df["user_id"].duplicated(keep="first"), "user_id duplicado"),
    ]
    for col, permitidos in VALORES_PERMITIDOS.items():
        comprobaciones.append((~df[col].isin(permitidos), f"{col} con valor desconocido"))
    for col, rango in RANGOS.items():
        comprobaciones.append((~rango.contiene(df[col]), f"{col} fuera de rango"))
    comprobaciones.append((df["deep_sleep_pct"] + df["rem_sleep_pct"] > 100,
                           "deep_sleep_pct + rem_sleep_pct mayor que 100"))

    motivo = pd.Series("", index=df.index)
    for es_mala, texto in comprobaciones:
        motivo[es_mala & (motivo == "")] = texto

    validos = df[motivo == ""].copy()
    errores = df[motivo != ""].copy()
    errores["motivo"] = motivo[motivo != ""]
    return validos, errores
