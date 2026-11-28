#!/usr/bin/env python3
"""Verify preserved Unleashed source ZIP against audit hashes.

The six upstream comparisons were fetched through GitHub at immutable revisions.
--fetch-upstream optionally repeats those downloads; default is fully offline.
No helper/game binaries are built or executed.
"""
import argparse
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path

OUT = Path(__file__).resolve().parent
DESKTOP = OUT.parents[3] / 'audit-desktop-source'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch-upstream', action='store_true')
    args = parser.parse_args()
    report = json.loads((OUT / 'unleashed-helper-review.json').read_text())
    bundle = DESKTOP / report['bundle']
    assert hashlib.sha256(bundle.read_bytes()).hexdigest() == report['bundle_sha256']
    with zipfile.ZipFile(bundle) as archive:
        for item in report['bundle_manifest']:
            data = archive.read(item['path'])
            assert len(data) == item['bytes']
            assert hashlib.sha256(data).hexdigest() == item['sha256']
        for item in report['upstream_comparisons']:
            data = archive.read(item['path'])
            assert hashlib.sha256(data).hexdigest() == item['upstream_sha256']
            if args.fetch_upstream:
                url = item['upstream_url'].replace('https://github.com/', 'https://raw.githubusercontent.com/').replace('/blob/', '/')
                with urllib.request.urlopen(url, timeout=30) as response:
                    upstream = response.read(2_000_000)
                assert data == upstream, item['path']
    print(json.dumps({'bundle_files_verified': len(report['bundle_manifest']),
                      'upstream_hash_anchors_verified': len(report['upstream_comparisons']),
                      'upstream_refetched': args.fetch_upstream, 'binary_rebuild': False}))

if __name__ == '__main__':
    main()
