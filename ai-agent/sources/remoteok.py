import re
import requests


def fetch(keyword: str) -> list[dict]:
    try:
        r = requests.get("https://remoteok.com/api",
                         headers={"User-Agent": "Mozilla/5.0 (radar-emploi)"}, timeout=15)
        r.raise_for_status()
        kw = keyword.lower()
        out = []
        for j in r.json():
            if not isinstance(j, dict) or "position" not in j:
                continue
            tags = j.get("tags", [])
            if kw in j["position"].lower() or kw in " ".join(tags).lower():
                out.append({
                    "source": "RemoteOK",
                    "title": j["position"],
                    "company": j.get("company", ""),
                    "url": j.get("url", ""),
                    "description": re.sub("<[^<]+?>", " ", j.get("description", ""))[:4000],
                    "tags": ", ".join(tags),
                })
        return out
    except Exception as e:
        print(f"[RemoteOK] Erreur : {e}")
        return []
