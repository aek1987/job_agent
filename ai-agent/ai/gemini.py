import os
import time
import google.generativeai as genai

SECONDS_BETWEEN_CALLS = 13   # plan gratuit : ~5 requêtes/minute
MAX_RETRIES = 5

_model = None


def get_model():
    global _model
    if _model is None:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("Variable d'environnement GOOGLE_API_KEY manquante")
        genai.configure(api_key=api_key)
        # Nom du modèle configurable sans toucher au code
        _model = genai.GenerativeModel(os.environ.get("GEMINI_MODEL", "gemini-3.8-flash"))
    return _model


def call_gemini(prompt: str) -> str:
    model = get_model()
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = model.generate_content(prompt)
            time.sleep(SECONDS_BETWEEN_CALLS)
            return resp.text or ""
        except Exception as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                time.sleep(20 * attempt)
            else:
                raise
    raise RuntimeError("Limite de requêtes Gemini atteinte trop souvent")
