"""
E5 - Cliente unificado de IA (basado en el demo ai_api_client.py del curso).

Lo que he añadido para el E5:
  --batch prompts.txt --output respuestas.jsonl  -> una linea json por prompt
  --fail-once                                     -> simula un fallo transitorio y reintenta

Uso (desde la carpeta del repo):
    python -m ejercicios.ai_api_client --provider mock --prompt "Hola"
    python -m ejercicios.ai_api_client --provider mock --batch ejercicios/prompts.txt --output ejercicios/respuestas.jsonl --fail-once
"""

import argparse
import json
import logging
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

MAX_REINTENTOS = 2
ESPERA_SEGUNDOS = 0.2

logger = logging.getLogger(__name__)


@dataclass
class AIResponse:
    provider: str
    text: str


class AIClientError(RuntimeError):
    pass


class ErrorTransitorio(AIClientError):
    """Fallos que si merece la pena reintentar (429, 5xx, timeout)."""


def complete(provider: str, prompt: str, model: str | None = None) -> AIResponse:
    provider = provider.lower().strip()
    if provider == "mock":
        return AIResponse(provider="mock", text=f"[mock] Recibido: {prompt[:200]}")

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise AIClientError("Falta OPENAI_API_KEY en el entorno")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise AIClientError("Instala el SDK: pip install openai") from exc
        client = OpenAI(api_key=api_key)
        chosen = model or "gpt-4o-mini"
        result = client.chat.completions.create(
            model=chosen,
            messages=[{"role": "user", "content": prompt}],
        )
        return AIResponse(provider="openai", text=result.choices[0].message.content or "")

    if provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise AIClientError("Falta ANTHROPIC_API_KEY en el entorno")
        try:
            import anthropic
        except ImportError as exc:
            raise AIClientError("Instala el SDK: pip install anthropic") from exc
        client = anthropic.Anthropic(api_key=api_key)
        chosen = model or "claude-sonnet-4-20250514"
        result = client.messages.create(
            model=chosen,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(block.text for block in result.content if hasattr(block, "text"))
        return AIResponse(provider="anthropic", text=text)

    if provider in {"hf", "huggingface"}:
        token = os.getenv("HF_TOKEN")
        if not token:
            raise AIClientError("Falta HF_TOKEN en el entorno")
        try:
            from huggingface_hub import InferenceClient
        except ImportError as exc:
            raise AIClientError("Instala: pip install huggingface_hub") from exc
        client = InferenceClient(token=token)
        chosen = model or "mistralai/Mistral-7B-Instruct-v0.3"
        text = client.text_generation(prompt, model=chosen, max_new_tokens=256)
        return AIResponse(provider="huggingface", text=text)

    raise AIClientError(f"Proveedor no soportado: {provider}")


def complete_con_reintentos(provider: str, prompt: str, model: str | None = None,
                            fail_once: bool = False) -> AIResponse:
    # solo se reintentan los ErrorTransitorio, los de configuracion (falta clave,
    # proveedor raro...) salen a la primera porque reintentar no los arregla
    for intento in range(1, MAX_REINTENTOS + 2):
        try:
            if fail_once and intento == 1:
                raise ErrorTransitorio("fallo simulado con --fail-once")
            return complete(provider, prompt, model)
        except ErrorTransitorio as e:
            if intento > MAX_REINTENTOS:
                raise AIClientError(f"Agotados {MAX_REINTENTOS} reintentos: {e}") from e
            logger.warning("Intento %d fallido (%s), reintento en %.1fs", intento, e, ESPERA_SEGUNDOS)
            time.sleep(ESPERA_SEGUNDOS)


def procesar_batch(provider: str, ruta_prompts: Path, ruta_salida: Path,
                   model: str | None = None, fail_once: bool = False) -> int:
    prompts = [linea.strip() for linea in ruta_prompts.read_text(encoding="utf-8").splitlines() if linea.strip()]
    with open(ruta_salida, "w", encoding="utf-8") as f:
        for i, prompt in enumerate(prompts):
            # el fallo simulado solo en la primera peticion
            respuesta = complete_con_reintentos(provider, prompt, model, fail_once and i == 0)
            linea = {"prompt": prompt, **asdict(respuesta)}
            f.write(json.dumps(linea, ensure_ascii=False) + "\n")
    return len(prompts)


def main(argv: list[str] | None = None) -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", default="mock", choices=["mock", "openai", "anthropic", "hf"])
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--prompt")
    grupo.add_argument("--batch", type=Path, help="fichero de texto con un prompt por linea")
    parser.add_argument("--output", type=Path, help="jsonl de salida (con --batch)")
    parser.add_argument("--model", default=None)
    parser.add_argument("--fail-once", action="store_true", help="simula un fallo transitorio en la primera llamada")
    args = parser.parse_args(argv)

    if args.batch:
        if not args.output:
            parser.error("--batch necesita --output")
        n = procesar_batch(args.provider, args.batch, args.output, args.model, args.fail_once)
        print(f"{n} respuestas guardadas en {args.output}")
    else:
        response = complete_con_reintentos(args.provider, args.prompt, args.model, args.fail_once)
        print(f"[{response.provider}]\n{response.text}")


if __name__ == "__main__":
    main()
