"""Apply the reviewed, fixed SDK169 disposable-output manifest after coordinator release."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat

PLAN_SHA = '7e9298276b3c2fdfdda238e5e33f3862c24c2e36079691cbb95ab62bfa3ecfcb'
B = Path(r'C:\Users\bradg\Downloads\GetAll-R18')
F = B / 'evidence-r18/flow-completion-20261127'
ALLOWED = [B / 'publish-desktop-final-sdk169-20261127', *(F / ('harness-build'+x) for x in ('31','31b','31c'))]
KEEP = [B / 'publish-getall-complete-flows-20261127', B / 'publish-getall-sdk168-20261127',
        B / 'publish-getall-sdk169-20261127', F / 'harness-build30', F / 'harness-build31d']


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def safe(path):
    for item in [path, *path.parents]:
        value = item.lstat()
        require(not stat.S_ISLNK(value.st_mode) and not getattr(value, 'st_file_attributes', 0) & 1024,
                'Linked path: ' + str(item))


def child(root, relative):
    value = PurePosixPath(relative)
    require(relative and not value.is_absolute() and '\\' not in relative and
            all(x not in ('.', '..') and ':' not in x for x in value.parts), 'Invalid recorded path')
    path = root.joinpath(*value.parts)
    safe(path)
    return path


def info(path, relative):
    return {'path': relative, 'bytes': path.stat().st_size, 'sha256': digest(path)}


def inventory(root):
    safe(root)
    rows = []
    for path in root.rglob('*'):
        safe(path)
        if path.is_file():
            rows.append(info(path, path.relative_to(root).as_posix()))
    return sorted(rows, key=lambda x: x['path'])


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    require(digest(args.plan) == PLAN_SHA, 'The approved plan changed')
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    require([Path(x['root']) for x in plan['groups']] == ALLOWED, 'Unexpected deletion roots')
    require([Path(x['root']) for x in plan['preserved_roots']] == KEEP, 'Unexpected preserved roots')
    require(args.evidence == F / 'cleanup-final-sdk169' and args.evidence.is_dir(), 'Unexpected evidence directory')
    require(plan['candidate_receipts_to_archive'] == ['ARTIFACT-MANIFEST.json', 'SHA256SUMS.txt', 'RESOURCE-AUDIT.json'],
            'Unexpected candidate receipts')
    require(not (args.evidence / 'result.json').exists(), 'Cleanup receipt already exists')
    for group in plan['groups'] + plan['preserved_roots']:
        require(inventory(Path(group['root'])) == group['files'], 'Inventory changed: ' + group['root'])
    for row in plan['preserved_failed_gate_results']:
        path = Path(row['path']); safe(path)
        require(info(path, row['path']) == row and json.loads(path.read_text())['status'] == 'FAILED',
                'Failed build receipt changed')
    candidate = ALLOWED[0]
    complete = KEEP[2]
    cm = json.loads((candidate / 'ARTIFACT-MANIFEST.json').read_text())
    require(digest(candidate / 'ARTIFACT-MANIFEST.json') == plan['candidate_manifest_sha256'] and
            digest(complete / 'ARTIFACT-MANIFEST.json') == plan['complete_preview_manifest_sha256'],
            'Publication manifest changed')
    for row in cm['artifacts']:
        require(info(child(complete, row['name']), row['name']) ==
                {'path': row['name'], 'bytes': row['bytes'], 'sha256': row['sha256']},
                'Candidate payload is not retained identically: ' + row['name'])
    if not args.execute:
        print('PREPARED_ONLY: all fixed inventories verified; no files removed')
        return
    archive = args.evidence / 'candidate-receipts'
    require(not archive.exists(), 'Candidate receipt archive already exists')
    started = datetime.now(timezone.utc).isoformat()
    free_before = shutil.disk_usage(B).free
    archive.mkdir()
    archived = []
    for name in plan['candidate_receipts_to_archive']:
        src = child(candidate, name); dst = archive / name
        with src.open('rb') as source, dst.open('xb') as target:
            shutil.copyfileobj(source, target, length=1024*1024)
        require(digest(src) == digest(dst) and src.stat().st_size == dst.stat().st_size, 'Receipt archive differs')
        archived.append(info(dst, str(dst)))
    deleted = []
    removed_directories = []
    errors = []
    preserved = []
    failed_gate_receipts_verified = False
    try:
        for group in plan['groups']:
            root = Path(group['root'])
            for row in group['files']:
                path = child(root, row['path'])
                require(info(path, row['path']) == row, 'Disposable changed immediately before removal')
                path.unlink()
                deleted.append(dict(row, group=group['name']))
            directories = sorted((p for p in root.rglob('*') if p.is_dir()), key=lambda p: len(p.parts), reverse=True)
            for path in directories:
                safe(path); path.rmdir(); removed_directories.append(str(path))
            safe(root); root.rmdir(); removed_directories.append(str(root))
    except Exception as error:
        errors.append(type(error).__name__ + ': ' + str(error))
    finally:
        try:
            for group in plan['preserved_roots']:
                current = inventory(Path(group['root']))
                require(current == group['files'], 'Protected output changed: ' + group['root'])
                preserved.append({'root': group['root'], 'files': len(current), 'bytes': sum(x['bytes'] for x in current),
                                  'inventory_sha256': hashlib.sha256(encode(current)).hexdigest(), 'unchanged': True})
            for row in plan['preserved_failed_gate_results']:
                require(info(Path(row['path']), row['path']) == row, 'Failed gate result changed')
            failed_gate_receipts_verified = True
            for row in archived:
                require(info(Path(row['path']), row['path']) == row, 'Archived receipt changed')
        except Exception as error:
            errors.append('Preservation: ' + type(error).__name__ + ': ' + str(error))
        expected_files = sum(len(x['files']) for x in plan['groups'])
        result = {'status': 'PASS' if not errors and len(deleted) == expected_files and all(not x.exists() for x in ALLOWED) else 'FAILED',
                  'started_utc': started, 'completed_utc': datetime.now(timezone.utc).isoformat(),
                  'plan_sha256': PLAN_SHA, 'script_sha256': digest(Path(__file__)),
                  'removed_files': len(deleted), 'removed_bytes': sum(x['bytes'] for x in deleted),
                  'removed': deleted, 'removed_directories': removed_directories,
                  'candidate_receipts_archived': archived, 'preserved_roots': preserved,
                  'failed_gate_receipts_preserved': failed_gate_receipts_verified,
                  'complete_preview_manifest_sha256': digest(complete / 'ARTIFACT-MANIFEST.json'),
                  'free_before': free_before, 'free_after': shutil.disk_usage(B).free, 'errors': errors,
                  'limits': 'Only the duplicate Desktop candidate and failed harness31/31b/31c output trees were removed. Complete previews167/168/169 and harness30/31d were verified unchanged. Repository bin/obj, source, caches, shared tools, originals and personal files are outside all deletion roots.'}
        with (args.evidence / 'result.json').open('xb') as stream:
            stream.write(encode(result))
        print(json.dumps({k: result[k] for k in ('status','removed_files','removed_bytes','free_before','free_after','errors')}))
        print('RESULT_SHA256=' + digest(args.evidence / 'result.json'))
    if result['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
