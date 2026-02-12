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
        print("Fetching: " + url)
        req = Request(url, headers={"Accept": "application/json"})
        with urlopen(req) as res:
            raw = res.read().decode("utf-8")
            data = json.loads(raw)
        hits = data.get("hits", {}).get("hits", [])
        total = data.get("hits", {}).get("total", 0)
        if isinstance(total, dict):
            total = total.get("value", 0)
        print("Page " + str(page) + ": " + str(len(hits)) + " hits, total: " + str(total))
        if not hits:
            break
        for i, h in enumerate(hits):
            meta = h.get("metadata", {})
            creators = meta.get("creators", [])
            creator_names = []
            for c in creators:
                name = c.get("name", "") or ""
                creator_names.append(name)
            print("  [" + str(i) + "] creators: " + str(creator_names))
            is_viorazu = False
            for name in creator_names:
                if "viorazu" in name.lower():
                    is_viorazu = True
                    break
            if not is_viorazu:
                print("  -> SKIP (no Viorazu in creators)")
                continue
            print("  -> MATCH")
            records.append({
                "id": h.get("id"),
                "title": meta.get("title", ""),
                "doi": h.get("doi", ""),
                "date": meta.get("publication_date", ""),
                "url": "https://zenodo.org/records/" + str(h.get("id", ""))
            })
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
