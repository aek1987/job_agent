from .gemini import call_gemini


def generate_cover_letter(cv_text: str, job: dict) -> str:
    prompt = f"""Rédige une lettre de motivation courte (150-200 mots), en français, professionnelle
et personnalisée pour cette offre précise. Référence des éléments concrets de l'annonce et du profil.

CV :
{cv_text[:6000]}

Offre ({job['title']} chez {job['company']}) :
{job['description']}
"""
    return call_gemini(prompt)
