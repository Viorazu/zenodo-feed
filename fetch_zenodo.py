import json
import urllib.request
import os

ZENODO_API = "https://zenodo.org/api/records/"
QUERY = "Viorazu"
PAGE_SIZE = 50
OUTPUT = "docs/data.json"

def fetch_all():
    records = []
    page = 1
    while True:
        url = f"{ZENODO_API}?q=metadata.creators.person_or_org.name%3A%22Viorazu%22&sort=mostrecent&size={PAGE_SIZE}&page={page}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
        hits = data.get("hits", {}).get("hits", [])
        if not hits:
            break
        for h in hits:
            meta = h.get("metadata", {})
            # 著者名にViorazuが含まれるものだけ抽出
            creators = meta.get("creators", [])
            is_viorazu = False
            for c in creators:
                name = c.get("name", "") or ""
                person = c.get("person_or_org", {})
                if person:
                    name = person.get("name", "") or ""
                    given = person.get("given_name", "") or ""
                    family = person.get("family_name", "") or ""
                    name = name or f"{family} {given}"
                if "viorazu" in name.lower():
                    is_viorazu = True
                    break
            if not is_viorazu:
                continue
            records.append({
                "id": h.get("id"),
                "title": meta.get("title", ""),
                "doi": h.get("doi", ""),
                "date": meta.get("publication_date", ""),
                "url": f"https://zenodo.org/records/{h.get('id', '')}"
            })
        total = data.get("hits", {}).get("total", 0)
        if page * PAGE_SIZE >= total:
            break
        page += 1
    return records

def main():
    os.makedirs("docs", exist_ok=True)
    records = fetch_all()
    output = {
        "count": len(records),
        "records": records
    }
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(records)} records to {OUTPUT}")

if __name__ == "__main__":
    main()
