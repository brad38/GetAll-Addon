"""Exercise the real SDK169 Desktop Store services without launching the app."""
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--desktop-commit', required=True)
    parser.add_argument('--candidate-manifest-sha256', required=True)
    parser.add_argument('--candidate-executable-sha256', required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    root = args.task_root.absolute()
    desktop = root/'desktop-continuation-20261127'
    candidate = root/'publish-desktop-final-sdk169-20261127'
    assembly_root = desktop/'bin/Release/net8.0-windows/win-x64'
    assembly = assembly_root/'AllFix.dll'
    dotnet = r'C:\Program Files\dotnet\dotnet.exe'
    git = r'C:\Program Files\Git\cmd\git.exe'
    require(not args.output.exists(), 'Use a fresh proof output directory')
    require(digest(candidate/'ARTIFACT-MANIFEST.json') == args.candidate_manifest_sha256 and
            digest(candidate/'AllFix.exe') == args.candidate_executable_sha256,
            'Published candidate pins differ')
    manifest = json.loads((candidate/'ARTIFACT-MANIFEST.json').read_text(encoding='utf-8-sig'))
    require(manifest['desktop_commit'] == args.desktop_commit and manifest['sdk_version'] == '1.5.69',
            'Wrong Desktop candidate')
    audit = json.loads((candidate/'RESOURCE-AUDIT.json').read_text(encoding='utf-8-sig'))
    assembly_sha = digest(assembly)
    require(assembly_sha == audit['desktop']['sha256'], 'Build output differs from the audited bundle')
    def git_state():
        return {name: subprocess.check_output([git, '-C', str(desktop), *command],
                    text=True, encoding='utf-8').strip()
                for name, command in [('head', ['rev-parse', 'HEAD']),
                                      ('status', ['status', '--porcelain', '--untracked-files=all'])]}
    before = git_state()
    require(before == {'head': args.desktop_commit, 'status': ''}, 'Desktop checkout must be clean and fixed')
    args.output.mkdir(parents=True)
    result = {'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(),
              'desktop_commit': args.desktop_commit, 'desktop_assembly': str(assembly),
              'desktop_assembly_sha256': assembly_sha,
              'candidate_manifest_sha256': args.candidate_manifest_sha256,
              'candidate_executable_sha256': args.candidate_executable_sha256,
              'source_files': [{'path': p.name, 'bytes': p.stat().st_size, 'sha256': digest(p)}
                               for p in sorted(source.iterdir()) if p.is_file()],
              'host': 'Runner framework-dependent runtimeconfig; real Desktop AssemblyDependencyResolver',
              'commands': [], 'errors': []}
    def run(label, command, timeout):
        started = time.monotonic()
        complete = subprocess.run(command, cwd=source, capture_output=True, timeout=timeout)
        log = args.output/(label+'.log')
        log.write_bytes(complete.stdout + complete.stderr)
        row = {'label': label, 'command': command, 'exit_code': complete.returncode,
               'seconds': round(time.monotonic()-started, 3), 'log': log.name,
               'bytes': log.stat().st_size, 'sha256': digest(log)}
        result['commands'].append(row)
        require(complete.returncode == 0, label+' failed; see '+str(log))
        return log.read_text(encoding='utf-8-sig', errors='replace')
    try:
        require(run('dotnet-version', [dotnet, '--version'], 30).strip() == '8.0.425', 'Wrong shared .NET SDK')
        output = args.output/'bin'
        run('build', [dotnet, 'build', str(source/'StoreAssemblyProof.csproj'), '-c', 'Release',
                     '--nologo', '--configfile', str(source/'NuGet.Config'),
                     '-p:UseAppHost=false', '-o', str(output)], 180)
        text = run('store-services', [dotnet, 'exec', '--runtimeconfig',
                   str(output/'StoreAssemblyProof.runtimeconfig.json'),
                   str(output/'StoreAssemblyProof.dll'), str(assembly)], 45)
        require(text.splitlines().count('MKW_CLI_STORE_ASSEMBLY_PASS checks=20') == 1 and
                len(re.findall(r'^PASS MKW store assembly:', text, re.M)) == 20 and
                not re.search(r'^FAIL', text, re.M), 'Real Store service checks did not all pass')
        require('DESKTOP_ASSEMBLY_SHA256='+assembly_sha in text, 'Tested Desktop hash differs')
        result['checks'] = 20
    except Exception as error:
        result['errors'].append(type(error).__name__+': '+str(error))
    finally:
        result['git_state_unchanged'] = git_state() == before
        result['desktop_assembly_unchanged'] = digest(assembly) == assembly_sha
        result['candidate_unchanged'] = digest(candidate/'ARTIFACT-MANIFEST.json') == args.candidate_manifest_sha256 and digest(candidate/'AllFix.exe') == args.candidate_executable_sha256
        if not all(result[k] for k in ('git_state_unchanged', 'desktop_assembly_unchanged', 'candidate_unchanged')):
            result['errors'].append('Inputs changed during the Store service proof')
        result['status'] = 'PASS' if not result['errors'] else 'FAILED'
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (args.output/'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
