import re
import requests


def fetch(keyword: str) -> list[dict]:
    try:
        r = requests.get("https://remotive.com/api/remote-jobs",
                         params={"search": keyword}, timeout=15)
        r.raise_for_status()
        return [{
            "source": "Remotive",
            "title": j.get("title", ""),
            "company": j.get("company_name", ""),
            "url": j.get("url", ""),
            "description": re.sub("<[^<]+?>", " ", j.get("description", ""))[:4000],
            "tags": ", ".join(j.get("tags", [])),
        } for j in r.json().get("jobs", [])]
    except Exception as e:
        print(f"[Remotive] Erreur : {e}")
        return []
