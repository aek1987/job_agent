import re
import requests


def fetch(keyword: str) -> list[dict]:
    try:
        r = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=15)
        r.raise_for_status()
        kw = keyword.lower()
        out = []
        for j in r.json().get("data", []):
            title, desc = j.get("title", ""), j.get("description", "")
            if j.get("remote") and (kw in title.lower() or kw in desc.lower()):
                out.append({
                    "source": "Arbeitnow",
                    "title": title,
                    "company": j.get("company_name", ""),
                    "url": j.get("url", ""),
                    "description": re.sub("<[^<]+?>", " ", desc)[:4000],
                    "tags": ", ".join(j.get("tags", [])),
                })
        return out
    except Exception as e:
        print(f"[Arbeitnow] Erreur : {e}")
        return []
