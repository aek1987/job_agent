# ai-agent

    pip install -r requirements.txt
    export GOOGLE_API_KEY="ta_clé"      # Windows : set GOOGLE_API_KEY=ta_clé
    export AGENT_API_KEY="un_secret"    # optionnel en local
    uvicorn api.main:app --reload --port 8000

Docs : http://localhost:8000/docs

## Endpoints (en-tête X-API-Key requis si AGENT_API_KEY est défini)
- POST /analyze  (multipart : cv, keyword, min_score, limit) -> {"job_id": "..."}
- GET  /analyze/{job_id} -> status: pending | running | finished | error, done, total, results
- GET  /health  (sans clé)
