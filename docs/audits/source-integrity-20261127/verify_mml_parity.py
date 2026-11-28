#!/usr/bin/env python3
"""Compare the fixed upstream literal patch table with the Desktop resource.

Does not execute imported upstream code or modify a game executable.
"""
import ast
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
DESKTOP = OUT.parents[3] / 'audit-desktop-source'
SOURCE = OUT / 'mml-upstream-patch-manifest.py'
EXPECTED_BLOB = 'b300621c88e1573371f9c91c128981be7e36c55e'

def main():
    data = SOURCE.read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert blob == EXPECTED_BLOB, (blob, EXPECTED_BLOB)
    values = {}
    for node in ast.parse(data.decode()).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            values[node.targets[0].id] = ast.literal_eval(node.value)
    target = json.loads((DESKTOP / 'Tools/VerifiedPatches/mml-v0.9.6-beta.json').read_text())
    assert target['source_commit'] == '09b8dd326e009e895635e6516ac73e5709db0aec'
    assert target['source_blob'] == EXPECTED_BLOB
    reports = []
    for profile in target['profiles']:
        prefix = '' if profile['edition'] == 'US' else 'JP_'
        ranges = values[prefix + 'PATCHES']
        tail = values[prefix + 'EXE_TAIL']
        expected = {
            'input_size': values[prefix + 'EXE_SIZE'],
            'input_sha256': values[prefix + 'VANILLA_SHA256'],
            'output_size': values[prefix + 'EXE_SIZE'] + len(bytes.fromhex(tail)),
            'output_sha256': values[prefix + 'PATCHED_SHA256'],
            'ranges': [{'offset': offset, 'hex_bytes': encoded} for offset, encoded in ranges],
            'tail_hex': tail,
        }
        differences = [key for key in sorted(set(profile['plan']) | set(expected)) if profile['plan'].get(key) != expected.get(key)]
        reports.append({'edition': profile['edition'], 'ranges': len(ranges),
                        'changed_bytes': sum(len(bytes.fromhex(encoded)) for _, encoded in ranges),
                        'tail_bytes': len(bytes.fromhex(tail)), 'equal_to_upstream': not differences,
                        'different_fields': differences})
        assert not differences, differences
    report = {
        'source_url': 'https://github.com/Drakfix/MML_Modernization-Project/blob/09b8dd326e009e895635e6516ac73e5709db0aec/src/patch_manifest.py',
        'source_sha256': hashlib.sha256(data).hexdigest(),
        'source_git_blob': EXPECTED_BLOB, 'source_git_blob_computed': blob,
        'source_blob_verified': True, 'profiles': reports,
        'method': 'AST literal evaluation only; compare all plan fields; no upstream module execution or game/media processing',
    }
    (OUT / 'mml-parity-review.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
