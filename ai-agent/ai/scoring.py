import json
from .gemini import call_gemini


def score_job(cv_text: str, job: dict) -> dict:
    prompt = f"""Tu es un assistant de recrutement technique. Compare ce CV et cette offre d'emploi DevOps.

CV :
{cv_text[:6000]}

Offre ({job['title']} chez {job['company']}) :
{job['description']}

Réponds UNIQUEMENT avec un objet JSON valide, sans texte autour, au format :
{{"score": <entier 0-100>, "competences_manquantes": ["...", "..."], "points_forts": ["...", "..."]}}
"""
    raw = call_gemini(prompt)
    try:
        cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(cleaned)
    except Exception:
        return {"score": 0, "competences_manquantes": [], "points_forts": []}
