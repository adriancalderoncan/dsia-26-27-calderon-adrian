import pandas as pd
import pytest


def registro(user_id="USR-00001", **cambios):
    """Un registro valido del dataset de sueño. Con cambios se modifica lo que haga falta."""
    fila = {
        "user_id": user_id,
        "age": 30,
        "gender": "Female",
        "occupation_type": "Student",
        "chronotype": "Intermediate",
        "bedtime_phone_minutes": 20,
        "primary_bedtime_app": "YouTube",
        "screen_brightness_pct": 50,
        "blue_light_filter_active": 1,
        "caffeine_post_5pm_mg": 0,
        "physical_activity_min": 30,
        "sleep_latency_min": 20.0,
        "total_sleep_hours": 8.0,
        "deep_sleep_pct": 20.0,
        "rem_sleep_pct": 20.0,
        "morning_alarm_snoozes": 1,
        "next_day_fatigue_score": 2.0,
        "sleep_debt_category": "Optimal Recovery",
    }
    fila.update(cambios)
    return fila


@pytest.fixture
def crear_registro():
    """Devuelve la funcion registro para crear filas dentro de los tests."""
    return registro


@pytest.fixture
def registros_validos():
    """4 personas validas con valores pensados para saber el resultado de las metricas."""
    return pd.DataFrame([
        registro("USR-00001", bedtime_phone_minutes=20, total_sleep_hours=8.0, next_day_fatigue_score=2.0,
                 chronotype="Morning Lark", primary_bedtime_app="News / Reading",
                 blue_light_filter_active=1, sleep_latency_min=10.0, sleep_debt_category="Optimal Recovery"),
        registro("USR-00002", bedtime_phone_minutes=45, total_sleep_hours=7.0, next_day_fatigue_score=3.0,
                 chronotype="Intermediate", primary_bedtime_app="YouTube",
                 blue_light_filter_active=1, sleep_latency_min=30.0, sleep_debt_category="Mild Deficit"),
        registro("USR-00003", bedtime_phone_minutes=90, total_sleep_hours=5.0, next_day_fatigue_score=6.0,
                 chronotype="Night Owl", primary_bedtime_app="TikTok / Reels",
                 blue_light_filter_active=0, sleep_latency_min=50.0, sleep_debt_category="Moderate Debt"),
        registro("USR-00004", bedtime_phone_minutes=150, total_sleep_hours=4.0, next_day_fatigue_score=9.0,
                 chronotype="Night Owl", primary_bedtime_app="TikTok / Reels",
                 blue_light_filter_active=0, sleep_latency_min=70.0, sleep_debt_category="Moderate Debt"),
    ])
