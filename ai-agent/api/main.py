"""
API du radar emploi. Lancement :
    uvicorn api.main:app --host 0.0.0.0 --port 8000
"""
import os
import uuid
from fastapi import BackgroundTasks, Depends, FastAPI, File, Form, Header, HTTPException, UploadFile

from cv.extractor import extract_cv_text
from sources import fetch_all_jobs
from ai.scoring import score_job
from ai.cover_letter import generate_cover_letter


def verify_key(x_api_key: str = Header(default="")):
    """Protège l'API : Spring Boot doit envoyer l'en-tête X-API-Key."""
    expected = os.environ.get("AGENT_API_KEY")
    if expected and x_api_key != expected:
        raise HTTPException(401, "Clé API invalide")


app = FastAPI(title="Radar Emploi - AI Agent")

# Stockage en mémoire (perdu au redémarrage : Spring Boot doit persister les résultats)
JOBS: dict[str, dict] = {}


def run_analysis(job_id: str, cv_text: str, keyword: str, min_score: int, limit: int):
    state = JOBS[job_id]
    try:
        offers = fetch_all_jobs(keyword)[:limit]
        state.update(total=len(offers), status="running")
        for offer in offers:
            result = score_job(cv_text, offer)
            score = int(result.get("score", 0) or 0)
            letter = generate_cover_letter(cv_text, offer) if score >= min_score else ""
            state["results"].append({
                "source": offer["source"],
                "titre": offer["title"],
                "entreprise": offer["company"],
                "url": offer["url"],
                "score": score,
                "competences_manquantes": result.get("competences_manquantes", []),
                "points_forts": result.get("points_forts", []),
                "lettre_motivation": letter,
            })
            state["done"] += 1
        state["results"].sort(key=lambda r: r["score"], reverse=True)
        state["status"] = "finished"
    except Exception as e:
        state.update(status="error", error=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", dependencies=[Depends(verify_key)])
async def analyze(
    background: BackgroundTasks,
    cv: UploadFile = File(...),
    keyword: str = Form("devops"),
    min_score: int = Form(70),
    limit: int = Form(30),
):
    try:
        cv_text = extract_cv_text(cv.filename, await cv.read())
    except ValueError as e:
        raise HTTPException(400, str(e))
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "pending", "total": 0, "done": 0, "results": [], "error": None}
    background.add_task(run_analysis, job_id, cv_text, keyword, min_score, limit)
    return {"job_id": job_id}


@app.get("/analyze/{job_id}", dependencies=[Depends(verify_key)])
def get_status(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(404, "job_id inconnu")
    return JOBS[job_id]
