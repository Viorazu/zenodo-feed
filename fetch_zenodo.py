import json
import os
from urllib.request import urlopen, Request
from urllib.parse import urlencode

ZENODO_API = "https://zenodo.org/api/records/"
OUTPUT = "docs/data.json"

def fetch_all():
    records = []
    page = 1
    while True:
        params = urlencode({
            "q": "Viorazu",
            "sort": "mostrecent",
            "size": 50,
            "page": page
        })
        url = ZENODO_API + "?" + params
        req = Request(url, headers={"Accept": "application/json"})
        with urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
        hits = data.get("hits", {}).get("hits", [])
        if not hits:
            break
        for h in hits:
            meta = h.get("metadata", {})
            creators = meta.get("creators", [])
            is_viorazu = False
            for c in creators:
                name = c.get("name", "") or ""
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
                "url": "https://zenodo.org/records/" + str(h.get("id", ""))
            })
        total = data.get("hits", {}).get("total", 0)
        if isinstance(total, dict):
            total = total.get("value", 0)
        if page * 50 >= total:
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
    print("Saved " + str(len(records)) + " records to " + OUTPUT)

if __name__ == "__main__":
    main()
