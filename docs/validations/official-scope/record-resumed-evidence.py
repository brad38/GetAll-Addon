"""Transfer text-only review evidence and bind it to the exact active recipes.

Run from this worktree after the Desktop integration tests finish. Does not run
a game, download anything, change other repositories or infer original-media
success. Original encodings/hashes are retained in the transfer inventory.
"""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT.parent
DESKTOP = BASE / "desktop-scope-20261127"
OUT = ROOT / "docs/validations/official-scope"
TRANSFER = OUT / "resumed-evidence"
DATE = "2026-11-28"
def sha(data): return hashlib.sha256(data).hexdigest()
def load(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def save(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n",encoding="utf-8",newline="\n")
def relative(p): return p.relative_to(ROOT).as_posix()
inventory = []
seen_sources = set()
def transfer(src, rel):
    if not src.is_file(): return None
    if src in seen_sources: return TRANSFER / rel
    seen_sources.add(src)
    raw = src.read_bytes()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")): encoding = "utf-16"
    elif raw.startswith(b"\xef\xbb\xbf"): encoding = "utf-8-sig"
    else: encoding = "utf-8"
    try: text = raw.decode(encoding)
    except UnicodeDecodeError:
        if src.name not in {"scope-desktop-suite-final.log","scope-desktop-parser-final.log"}: raise
        encoding = "cp850"
        text = raw.decode(encoding)
    text = text.replace("\r\n","\n").replace("\r","\n")
    target = TRANSFER / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text,encoding="utf-8",newline="\n")
    record = dict(origin=src.relative_to(BASE).as_posix(),origin_bytes=len(raw),
        origin_sha256=sha(raw),origin_encoding=encoding,path=relative(target),
        bytes=target.stat().st_size,sha256=sha(target.read_bytes()))
    if src.suffix == ".log":
        record["pass_lines"] = sum(line.startswith("PASS ") for line in text.splitlines())
    inventory.append(record)
    return target
logs = [
 "scope-desktop-sm64plus-official-kit.log", "scope-desktop-sm64ex-official-kit.log",
 "scope-desktop-render96ex-official-kit.log", "scope-desktop-sm64rt-official-kit.log",
 "scope-desktop-sm-official-kit.log", "scope-desktop-sm-rewrite-official-kit.log",
 "scope-desktop-ssx-official-kit.log", "scope-desktop-fh1-official-kit.log",
 "scope-desktop-gt5-official-kit-final.log", "scope-desktop-kiexster-official-kit-final.log",
 "scope-desktop-kiexster-official-extractor-final.log", "scope-desktop-msvc-official-installed-final.log",
 "scope-desktop-shadow-rome-defaults.log", "scope-desktop-soh-official-kit-final.log",
 "scope-desktop-mkdd-official-kit-final.log", "scope-desktop-suite-final.log",
 "scope-desktop-source-parser-latest.log",
]
for name in logs: transfer(BASE/name, "desktop/"+name)
for final_log in sorted(BASE.glob("scope-desktop-*-final.log")):
    transfer(final_log,"desktop/"+final_log.name)
for name in ["scope-desktop-source-kits-results.json","scope-desktop-source-regression-results.json","scope-desktop-source-parser.json","scope-desktop-final-parser.json","scope-desktop-final-validation-results.json"]:
    transfer(BASE/name,"desktop/"+name)
for name, filenames in {
 "sm-official":["build-result.json","build.log","source-before.json","native-no-rom-result.json"],
 "sm-rewrite-official":["build-result.json","build.log","source-before.json","native-no-rom-result.json"],
 "mkdd-official":["build-result.json","build-official.log","combined-source-manifest.json","negative-extraction.log","source-receipt.json","gcn-receipt.json"],
 "kiexster-official-extractor":["result.json","extractor.log"],
}.items():
    for filename in filenames:
        transfer(BASE/"evidence-r18/official-scope-20261127"/name/filename,"native/"+name+"/"+filename)
transfer(BASE/"evidence-r18/official-scope-20261127/msvc-official/dotnet-smoke/msvc-smoke-result.json","native/msvc-official/msvc-smoke-result.json")
for filename in ["build-evidence.json","native-probe-evidence.json","recipe-validation.json","source-files.sha256.json","upstream.json","wrapper-compile-evidence.json","README.md","LICENSE-Torch.txt"]:
    transfer(DESKTOP/"Tools/NativeExtractors/SoH"/filename,"torch/"+filename)
transfer(DESKTOP/"docs/audits/official-installation-20261127/shadow-rome-firststart.json","contracts/shadow-rome-firststart.json")
transfer(DESKTOP/"docs/audits/official-installation-20261127/GOW-PINYON-OFFICIAL-CONTRACTS.md","contracts/GOW-PINYON-OFFICIAL-CONTRACTS.md")
save(OUT/"transferred-evidence.json",dict(reviewed_at=DATE,method="Text-only snapshots; originals are unchanged. UTF-16/Windows OEM CP850/CRLF logs normalized to UTF-8 LF with both hashes recorded.",files=inventory))

index = load(ROOT/"index.json")
active = {e["project_id"]:e for e in index["recipes"] if e["status"] in ("experimental","validated")}
profiles = {
 "ssx-recomp":"GameInstallationSsxOfficial.cs",
 "fh1-reimagined":"GameInstallationForzaOfficial.cs",
 "god-of-war-native-pc-port-gow-pc-port":"GameInstallationGowOfficial.cs",
 "pinyon-shift":"GameInstallationPinyonOfficial.cs",
 "ship-of-harkinian-soh":"GameInstallationSoh.cs",
 "sm64plus":"GameInstallationSm64PlusOfficial.cs",
 "sm64ex":"GameInstallationSm64PlusOfficial.cs",
 "render96ex":"GameInstallationSm64PlusOfficial.cs",
 "sm64rt":"GameInstallationSm64PlusOfficial.cs",
 "sm":"GameInstallationSmOfficialBuild.cs",
 "sm-rewrite":"GameInstallationSmOfficialBuild.cs",
 "gt5-recomp":"GameInstallationGt5Official.cs",
 "god-of-war-recomp":"GameInstallationGowKiexsterOfficial.cs",
 "mariokartdd-recomp":"GameInstallationMkddOfficialBuild.cs",
 "shadow-of-rome-recompiled":"GameInstallationShadowOfRome.cs",
 "crash-team-racing-turbocharged":"GameInstallationService.cs",
}
# Additional dispatch/profile files are captured by name, not treated as runtime proof.
source_paths = {DESKTOP/"Services"/name for name in profiles.values()}
source_paths.update(DESKTOP.glob("**/PreparedToolProfiles.cs"))
source_paths.update([DESKTOP/"Services/GameInstallationFidelity.cs",DESKTOP/"Services/GameInstallationOfficialMsvc.cs",DESKTOP/"Services/GameInstallationOfficialSourceKit.cs"])
for name in ["OfficialLauncherKitIntegration.cs","MarioOfficialIntegration.cs"]:
    source_paths.add(DESKTOP/"Tests/AddonInfrastructure"/name)
sources = []
for path in sorted(source_paths):
    assert path.is_file(), path
    raw = path.read_bytes()
    sources.append(dict(path=path.relative_to(DESKTOP).as_posix(),sha256=sha(raw),bytes=len(raw)))
contracts = []
for project, file in profiles.items():
    entry = active[project]
    recipe = load(ROOT/entry["path"])
    contracts.append(dict(project_id=project,tag=entry["tag"],recipe_sha256=entry["sha256"],recipe_path=entry["path"],
        build_profile=recipe.get("build_profile"),handler="Services/"+file,
        observation="Official source/payload, preparation, media validation and play dispatch reviewed by the implementation owners. This is implementation evidence only, not a completed original-media installation."))
save(OUT/"official-handler-review.json",dict(reviewed_at=DATE,
    repository="brad38/Allfix",branch="work/official-install-scope-20261127",
    state="Reviewed working-tree files; immutable commit is recorded separately by the final integration receipt.",
    source_files=sources,contracts=contracts,
    limits=["No original game media used for these review claims.","Synthetic and native tool results have separate receipts.","Retired profiles remain blocked; replacements require exact identity, profile and digest."]))

ledger = load(ROOT/"docs/installation-evidence.json")
ledger["reviewed_at"]=DATE
ledger["method"]="Reviewed official contracts and exact source/recipe bindings, with individually attributed current synthetic/native-tool results and separate historical reports. No original-media install, boot or gameplay occurred in this resumed review."
def proof(path, observed, data_kind="code_review"):
    path = ROOT/path if isinstance(path,str) else path
    assert path.is_file(), path
    return dict(path=relative(path),sha256=sha(path.read_bytes()),observed=observed,data_kind=data_kind,scope="getall")
for project in profiles:
    entry=active[project]
    row=ledger["projects"][project]
    row["reviewed_at"]=DATE
    row["recipe_revisions"]=[dict(tag=entry["tag"],sha256=entry["sha256"])]
    row["dimensions"]["automated_installation_implemented"]=dict(status="implemented",reason="Official preparation and play contract implemented in the SDK; this dimension does not assert full installation success.",
        evidence=[proof(OUT/"official-handler-review.json","Reviewed closed profile/generic import, source integrity, required original-media validation, official options, output registration and launch dispatch for "+project+"."),
                  proof(ROOT/"docs/OFFICIAL-CONTRACT-RESTORATION-20261128.md","Official route, preserved defaults and per-project execution limits documented.")])
    row["limits"]=["Implemented route, separate from a completed installation with original media.",
        "External upstream gameplay belongs only to upstream_functional.",
        "Current synthetic evidence covers only the explicitly observed operation; earlier evidence remains historical."]
synthetic_logs = {
 "ssx-recomp":"scope-desktop-ssx-official-kit.log",
 "fh1-reimagined":"scope-desktop-fh1-official-kit.log",
 "god-of-war-native-pc-port-gow-pc-port":"scope-desktop-gow-official-kit-final.log",
 "pinyon-shift":"scope-desktop-pinyon-official-kit-final.log",
 "sm64plus":"scope-desktop-sm64plus-official-kit.log",
 "sm64ex":"scope-desktop-sm64ex-official-kit.log",
 "render96ex":"scope-desktop-render96ex-official-kit.log",
 "sm64rt":"scope-desktop-sm64rt-official-kit.log",
 "sm":"scope-desktop-sm-official-kit.log",
 "sm-rewrite":"scope-desktop-sm-rewrite-official-kit.log",
 "gt5-recomp":"scope-desktop-gt5-official-kit-final.log",
 "god-of-war-recomp":"scope-desktop-kiexster-official-kit-final.log",
 "mariokartdd-recomp":"scope-desktop-mkdd-official-kit-final.log",
 "ship-of-harkinian-soh":"scope-desktop-soh-official-kit-final.log",
 "shadow-of-rome-recompiled":"scope-desktop-shadow-rome-defaults.log",
}
for project, filename in synthetic_logs.items():
    path=TRANSFER/"desktop"/filename
    if not path.exists(): continue
    text=path.read_text(encoding="utf-8")
    assert "PASS " in text and not any(line.startswith("FAIL ") for line in text.splitlines()), path
    if project=="fh1-reimagined": observed="Actual official kit manifest matches; missing/modified files rejected. Kit integrity only, not the complete installer."
    elif project=="pinyon-shift": observed="Real official kit and embedded scripts verified; cancellation/unsupported extension and missing Microsoft license acceptance stop preparation. No official setup, compiler, original ISO validation, boot or gameplay executed."
    elif project=="shadow-of-rome-recompiled": observed="Seven checks of all 44 upstream FirstStartIni defaults, PAL/NTSC binding and byte-exact preservation of an existing INI; no original-disc extraction or boot."
    else: observed="Project-specific official kit/native integration checks shown in this log; synthetic invalid or absent media rejected. No completed original-media installation, boot or gameplay."
    ledger["projects"][project]["dimensions"]["synthetic_validation"]=dict(status="passed",evidence=[proof(path,observed,"synthetic")],reason="Current result limited to the named checks, not a full game installation.")
for project, filename, observed in [
 ("shadow-of-rome-recompiled","desktop/scope-desktop-shadow-rome-official-kit-final.log","Six actual release kit and authored launch-plan checks, including changed media rejection. No original-disc installation or game boot."),
 ("sm","native/sm-official/build-result.json","Unchanged official MSVC solution built sm.exe and SDL2.dll, with 124 original files unchanged; no ROM or game execution."),
 ("sm-rewrite","native/sm-rewrite-official/build-result.json","Official Windows CMake/vcpkg preset built sm.exe and SDL2.dll, with 193 source files unchanged; no ROM or game execution."),
 ("mariokartdd-recomp","native/mkdd-official/build-result.json","Official build.ps1 compiled 42 runtime_check objects, 165 original sources unchanged, OpenXR ON and benchmark-only OFF; synthetic wrong main.dol hash rejected. No final game link or OpenXR runtime build."),
 ("god-of-war-recomp","native/kiexster-official-extractor/result.json","Unchanged upstream extractor tested only with an authored synthetic ISO, preserving original script bytes."),
 ("ship-of-harkinian-soh","torch/build-evidence.json","Standalone official Torch built from intact sources; wrapper compile failure is separately preserved. No original ROM used."),
 ("ship-of-harkinian-soh","torch/native-probe-evidence.json","Native Torch metadata/negative-input probes; output and metadata are required independently of exit code."),
]:
    path=TRANSFER/filename
    if not path.exists(): continue
    state=ledger["projects"][project]["dimensions"]["synthetic_validation"]
    if state["status"] not in ("passed",): state=dict(status="passed",evidence=[],reason="Current native tool/build result only; no original-media install or gameplay.")
    state["evidence"].append(proof(path,observed,"synthetic"))
    ledger["projects"][project]["dimensions"]["synthetic_validation"]=state
for project, filename, observed in [
 ("sm64plus","sm64plus-official-script-result.json","Official source/tools and script behavior checked with absent media; source/HEAD intact. No complete game build."),
 ("sm64ex","mario-official-tools-all-result.json","Official make tools target compiled using private signed MSYS2 packages; no original ROM or game link."),
 ("render96ex","mario-official-tools-all-result.json","Official make tools target compiled using private signed MSYS2 packages; no original ROM or game link."),
 ("sm64rt","mario-official-tools-all-result.json","Official make tools target compiled; RT64 option preserved. No original ROM, game link or ray-tracing execution."),
]:
    state=ledger["projects"][project]["dimensions"]["synthetic_validation"]
    assert state["status"]=="passed"
    state["evidence"].append(proof(OUT/filename,observed,"synthetic"))
blockers=load(OUT/"remaining-official-blockers.json")
for blocker in blockers["projects"]:
    row=ledger["projects"][blocker["project_id"]]
    row["reviewed_at"]=DATE
    row["dimensions"]["automated_installation_implemented"]=dict(status="blocked",
        reason=blocker["reason"],evidence=[proof(OUT/"remaining-official-blockers.json",blocker["reason"]+" Restoration condition: "+blocker["restore_when"])])
    row["limits"]=[blocker["official_alternative"],blocker["restore_when"],"Upstream functionality remains distinct from the unavailable official Windows automation."]
ledger["projects"]["vandalhearts-pcport"]["dimensions"]["synthetic_validation"]=dict(
    status="failed",reason="The intact native Windows CMake configuration failed on required symlinks and OpenAL; no claim about overall game functionality.",
    evidence=[proof(OUT/"vandal-native-configure-result.json","Native configuration only: required symbolic links could not be created in this environment; sources remained unchanged and no original media was supplied.","synthetic")])
save(ROOT/"docs/installation-evidence.json",ledger)
print(json.dumps(dict(transferred_files=len(inventory),transferred_bytes=sum(x["bytes"] for x in inventory),reviewed_contracts=len(contracts),index_sha256=sha((ROOT/"index.json").read_bytes())),ensure_ascii=True))
