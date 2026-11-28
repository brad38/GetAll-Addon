"""Verify the small, commit-pinned upstream contracts without binary downloads."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent


def verify(item):
    url = "https://raw.githubusercontent.com/{repository}/{commit}/{path}".format(**item)
    try:
        with urlopen(Request(url, headers={"User-Agent": "GetAll-source-contract-audit/1.0"}), timeout=20) as response:
            content = response.read(262145)
            status = response.status
        if len(content) > 262144:
            raise ValueError("Source-contract response exceeds 256 KiB")
        actual = hashlib.sha256(content).hexdigest()
        return {"project_id": item["project_id"], "path": item["path"], "url": url,
                "http_status": status, "bytes": len(content), "sha256": actual,
                "passed": actual == item["sha256"] and len(content) == item["utf8_bytes"]}
    except Exception as error:
        return {"project_id": item["project_id"], "path": item["path"], "url": url,
                "passed": False, "error": str(error)}


if __name__ == "__main__":
    sources = json.loads((ROOT / "source-manifest.json").read_text())["sources"]
    records = list(ThreadPoolExecutor(max_workers=4).map(verify, sources))
    report = {"verified_utc": datetime.now(timezone.utc).isoformat(),
              "passed": all(row["passed"] for row in records),
              "binary_bytes_downloaded": 0, "sources": records}
    (ROOT / "source-recheck-result.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["passed"] else 1)
