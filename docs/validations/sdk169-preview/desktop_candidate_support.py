"""Desktop-only SDK169 preflight/final receipts; reuse the audited static tooling.

No GetAll package is created and no application/native helper is executed.
"""
import argparse
from collections import Counter
import contextlib
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
BASE_INPUTS = 'run-20261127T190214Z-0467ae01/effective-inputs.json'
OLD_MANIFEST = '0f2db05e027d27732451a4d1f29fffb0fb7b868f82c1c9fd23c00c9b329c8e96'
SDK168_MANIFEST = '0220e843125b9223435d671fcbb834df1d13ce653fb770e6599989f7efd1c95a'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def audited_tools(task_root):
    pins = json.loads((HERE/'reuse-pins.json').read_text(encoding='utf-8-sig'))
    history = task_root.joinpath(*Path(pins['historical_root']).parts)
    for item in pins['inputs']:
        path = history.joinpath(*item['path'].replace('\\', '/').split('/'))
        require(path.is_file() and path.stat().st_size == item['bytes'] and digest(path) == item['sha256'],
                'Historical audit input changed: ' + str(path))
    spec = importlib.util.spec_from_file_location('verified_preview138_support', history/'preview_support.py')
    support = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(support)
    base = support.read_json(history/BASE_INPUTS)
    require(base['desktop_version'] == '3.0.0' and base['sdk_version'] == '1.5.67' and
            base['preview_version'] == '1.5.72', 'Unexpected predecessor version')
    require((len(base['properties']), len(base['resources']), len(base['notices'])) == (12, 34, 66),
            'Expected the complete audited 12/34/66 input set')
    return support, base, history


def preserve_previous(support, base, task_root):
    old = task_root/'publish-getall-complete-flows-20261127'
    require(digest(old/'ARTIFACT-MANIFEST.json') == OLD_MANIFEST, 'Preview138 manifest changed')
    with contextlib.redirect_stdout(io.StringIO()):
        support.verify_final(old, {key: base[key] for key in ('desktop_commit', 'getall_commit')})
    print('PRESERVED_PREVIEW_138_PASS (SDK167 and addon1.5.72 unchanged)')
    previous = task_root/'publish-getall-sdk168-20261127'
    require(digest(previous/'ARTIFACT-MANIFEST.json') == SDK168_MANIFEST, 'Preview140 manifest changed')
    manifest = support.read_json(previous/'ARTIFACT-MANIFEST.json')
    require(support.file_inventory(previous) == manifest['artifacts'], 'Preview140 files changed')
    sums = [(item['name'], item['sha256']) for item in manifest['artifacts']]
    sums.append(('ARTIFACT-MANIFEST.json', SDK168_MANIFEST))
    require((previous/'SHA256SUMS.txt').read_text(encoding='utf-8') ==
            ''.join(f'{value}  {name}\n' for name, value in sorted(sums)), 'Preview140 checksum receipt differs')
    print('PRESERVED_PREVIEW_140_PASS (SDK168 and addon1.5.73 unchanged)')


def preflight(args):
    support, base, history = audited_tools(args.task_root)
    support.check_checkout(args.git, args.desktop_root, args.desktop_commit)
    inputs = copy.deepcopy(base)
    inputs.update(task_root=str(args.task_root.absolute()), desktop_root=str(args.desktop_root.absolute()),
                  desktop_commit=args.desktop_commit, sdk_version='1.5.69', desktop_only=True,
                  predecessor_inputs_sha256=digest(history/BASE_INPUTS), predecessor_sdk_version='1.5.67')
    extra_path = HERE/'mkw-publish-inputs.json'
    extra = support.read_json(extra_path)
    require(extra.get('format') == 1 and len(extra.get('resources', [])) == 1 and
            extra['resources'][0]['name'] == 'MkwSm86.cli-support.zip' and extra.get('notices'),
            'Missing frozen MKW support/notice manifest')
    inputs['resources'] += extra['resources']
    inputs['notices'] += extra['notices']
    inputs['prefixes'] = sorted(set(inputs['prefixes'] + ['MkwSm86.']))
    inputs['mkw_inputs_sha256'] = digest(extra_path)
    audit_path = HERE/'audit-reuse.json'
    audit = support.read_json(audit_path)
    require(audit.get('format') == 1 and audit.get('target_sdk_version') == '1.5.69' and
            audit.get('required_runtime_files_present') is True and audit.get('source_pin_matches') is True,
            'Missing verified reusable auditor')
    for item in audit['files']:
        record = dict(item, source=item['path'])
        support.check_record(args.task_root, record)
    auditor = next(item for item in audit['files'] if item['role'] == 'audit_assembly')
    inputs['audit_reuse_sha256'] = digest(audit_path)
    inputs['audit_assembly'] = str(args.task_root.joinpath(*auditor['path'].split('/')))
    support.validate_inputs(inputs, history/'catalog.json')
    preserve_previous(support, base, args.task_root)
    support.write_json(args.output, inputs)
    print(f"DESKTOP_CANDIDATE_INPUTS_PASS sdk=1.5.69 properties={len(inputs['properties'])} resources={len(inputs['resources'])} notices={len(inputs['notices'])}")


def finish(args):
    support, base, history = audited_tools(args.task_root)
    inputs = support.read_json(args.inputs)
    require(inputs.get('desktop_only') is True and inputs['sdk_version'] == '1.5.69', 'Wrong candidate contract')
    support.check_checkout(args.git, Path(inputs['desktop_root']), inputs['desktop_commit'])
    support.validate_inputs(inputs, history/'catalog.json')
    preserve_previous(support, base, args.task_root)
    output = args.publish
    require(not (output/'GetAll-Preview.zip').exists(), 'Desktop-only output must not contain a new addon package')
    bundle = support.read_json(args.audit_dir/'bundle.json')
    audit = support.read_json(args.audit_dir/'resources.json')
    require(digest(output/'AllFix.exe') == bundle['executable_sha256'], 'Audited bundle changed')
    expected = sorted(({key: item[key] for key in ('name', 'bytes', 'sha256')} for item in inputs['resources']),
                      key=lambda item: item['name'])
    require(audit['resources'] == expected, 'Resource set/size/hash differs')
    for key, name, version in [('desktop', 'AllFix.dll', '3.0.0'), ('sdk', 'AllFix.Addons.Sdk.dll', '1.5.69')]:
        item = next(item for item in bundle['assemblies'] if item['name'] == name)
        require(audit[key]['sha256'] == item['sha256'] and audit[key]['version'] == version+'.0',
                'Assembly identity/hash differs: ' + name)
    require(audit['desktop']['informational_version'].endswith('+'+inputs['desktop_commit']), 'Wrong source revision')
    for item in inputs['notices']:
        source_root = Path(inputs['desktop_root'] if item['source_root'] == 'desktop' else inputs['task_root'])
        source = support.check_record(source_root, item)
        target = support.confined(output, item['target'], existing=False)
        if target.exists():
            support.check_record(output, item, 'target')
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with source.open('rb') as src, target.open('xb') as dst:
                shutil.copyfileobj(src, dst)
            support.check_record(output, item, 'target')
    support.write_json(output/'RESOURCE-AUDIT.json', audit)
    manifest = {'format': 1, 'artifact_type': 'desktop-only-candidate',
        'created_utc': datetime.now(timezone.utc).isoformat(), 'desktop_commit': inputs['desktop_commit'],
        'desktop_version': '3.0.0', 'sdk_version': '1.5.69', 'addon_included': False,
        'remote_recipes_modified': False, 'native_resources_verified': len(inputs['resources']),
        'notices_verified': len(inputs['notices']), 'native_properties_verified': len(inputs['properties']),
        'source_inputs_sha256': digest(history/BASE_INPUTS), 'mkw_inputs_sha256': inputs['mkw_inputs_sha256'],
        'audit_reuse_sha256': inputs['audit_reuse_sha256'],
        'effective_inputs_sha256': digest(args.inputs), 'preserved_preview138_manifest_sha256': OLD_MANIFEST,
        'preserved_preview140_manifest_sha256': SDK168_MANIFEST,
        'resource_groups': dict(sorted(Counter(item['group'] for item in inputs['resources']).items())),
        'artifacts': support.file_inventory(output)}
    support.write_json(output/'ARTIFACT-MANIFEST.json', manifest)
    sums = [(item['name'], item['sha256']) for item in manifest['artifacts']]
    sums.append(('ARTIFACT-MANIFEST.json', digest(output/'ARTIFACT-MANIFEST.json')))
    with (output/'SHA256SUMS.txt').open('x', encoding='utf-8', newline='\n') as stream:
        stream.writelines(f'{value}  {name}\n' for name, value in sorted(sums))
    verify(args, inputs['desktop_commit'])


def verify(args, revision=None):
    support, base, _ = audited_tools(args.task_root)
    manifest = support.read_json(args.publish/'ARTIFACT-MANIFEST.json')
    revision = revision or args.desktop_commit
    require(manifest['artifact_type'] == 'desktop-only-candidate' and manifest['sdk_version'] == '1.5.69' and
            manifest['desktop_version'] == '3.0.0' and manifest['desktop_commit'] == revision and
            manifest['addon_included'] is False, 'Candidate identity differs')
    require(support.file_inventory(args.publish) == manifest['artifacts'], 'Candidate file set or hashes changed')
    expected = [(item['name'], item['sha256']) for item in manifest['artifacts']]
    expected.append(('ARTIFACT-MANIFEST.json', digest(args.publish/'ARTIFACT-MANIFEST.json')))
    require((args.publish/'SHA256SUMS.txt').read_text(encoding='utf-8') ==
            ''.join(f'{value}  {name}\n' for name, value in sorted(expected)), 'Candidate checksum receipt differs')
    preserve_previous(support, base, args.task_root)
    print(f"DESKTOP_CANDIDATE_VERIFIED sdk=1.5.69 resources={manifest['native_resources_verified']} notices={manifest['notices_verified']} addon_included=false")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['preflight', 'finish', 'verify'])
    parser.add_argument('--task-root', type=Path, required=True)
    parser.add_argument('--desktop-root', type=Path)
    parser.add_argument('--desktop-commit')
    parser.add_argument('--git')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--inputs', type=Path)
    parser.add_argument('--publish', type=Path)
    parser.add_argument('--audit-dir', type=Path)
    args = parser.parse_args()
    {'preflight': preflight, 'finish': finish, 'verify': verify}[args.mode](args)


if __name__ == '__main__':
    main()
