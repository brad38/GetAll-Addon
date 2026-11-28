"""Record public Software Heritage metadata for the documented Courage origin."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
API = "https://archive.softwareheritage.org/api/1/"
ORIGINS = [
    "https://github.com/linifadomra/Courage-Reborn.git",
    "https://github.com/Linifadomra/Courage-Reborn",
    "https://github.com/Linifadomra/Courage-Reborn.git",
    "https://github.com/linifadomra/Courage-Reborn",
]


def probe(origin):
    url = API + "origin/" + quote(origin, safe="") + "/visit/latest/?require_snapshot=true"
    try:
        with urlopen(Request(url, headers={"User-Agent": "GetAll-source-contract-audit/1.0"}), timeout=20) as response:
            payload = response.read(256001)
            status = response.status
        if len(payload) > 256000:
            raise ValueError("Metadata response exceeds 250 KiB")
        return {"origin": origin, "url": url, "http_status": status,
                "sha256": hashlib.sha256(payload).hexdigest(), "data": json.loads(payload)}
    except HTTPError as error:
        return {"origin": origin, "url": url, "http_status": error.code}
    except Exception as error:
        return {"origin": origin, "url": url, "error": str(error)}


if __name__ == "__main__":
    rows = list(ThreadPoolExecutor(max_workers=4).map(probe, ORIGINS))
    result = {"queried_utc": datetime.now(timezone.utc).isoformat(), "origins": rows}
    (ROOT / "courage-archive-origins.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
