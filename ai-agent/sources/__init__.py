from . import remotive, remoteok, arbeitnow


def fetch_all_jobs(keyword: str) -> list[dict]:
    jobs = remotive.fetch(keyword) + arbeitnow.fetch(keyword) + remoteok.fetch(keyword)
    seen, unique = set(), []
    for j in jobs:
        if j["url"] and j["url"] not in seen:
            seen.add(j["url"])
            unique.append(j)
    return unique
