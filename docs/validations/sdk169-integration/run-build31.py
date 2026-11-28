"""Build and validate the transferred SDK169 sources; never transfer into the repo.

No native C++ build, NativeStage rerun, restore, package update or publish occurs.
All outputs are new. Run only in the coordinator's exclusive build window.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

BASE_HEAD = "8ba34eb51ee0ab93accef3da5e1689c68825977d"
SOURCE_SHA = "e130131a1a41e8599541d8ab3dd2f31c6d8abaa9af03411f8bba25c3f5b63f21"
PASS_LINE = re.compile(r"^[ \t]*PASS(?:[ \t].*)?$")
FAIL_LINE = re.compile(r"^[ \t]*FAIL(?:[ \t].*)?$")


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def file_info(path):
    path = Path(path)
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": digest(path)}


def write_json(path, payload):
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(payload, stream, indent=2, ensure_ascii=True)
        stream.write("\n")


def git(args, *command):
    return subprocess.check_output([str(args.git), "-C", str(args.desktop), *command],
                                   stderr=subprocess.PIPE).decode("utf-8", "strict")


def git_state(args):
    return {"head": git(args, "rev-parse", "HEAD").strip(),
            "branch": git(args, "branch", "--show-current").strip(),
            "status_porcelain_z": git(args, "status", "--porcelain=v1", "-z").split("\0")[:-1],
            "unstaged_name_status_z": git(args, "diff", "--name-status", "-z").split("\0")[:-1],
            "staged_name_status_z": git(args, "diff", "--cached", "--name-status", "-z").split("\0")[:-1]}


def source_manifest(args):
    # Includes transferred, not-yet-committed inputs. Ignored bin/obj directories
    # are not source inputs and are never mistaken for a source modification.
    names = set(git(args, "ls-files", "--cached", "--others", "--exclude-standard", "-z").split("\0")) - {""}
    rows = []
    for name in sorted(names):
        relative = Path(name)
        require(not relative.is_absolute() and ".." not in relative.parts, "Invalid Git path")
        path = args.desktop / relative
        if not path.exists():
            rows.append({"path": name, "missing": True})
            continue
        value = path.lstat()
        require(stat.S_ISREG(value.st_mode) and not value.st_file_attributes & 0x400,
                "Non-ordinary source input: " + name)
        rows.append({"path": name, "bytes": value.st_size, "sha256": digest(path)})
    return {"files": rows}


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-root", type=Path, default=Path(r"C:\Users\bradg\Downloads\GetAll-R18"))
    parser.add_argument("--desktop", type=Path)
    parser.add_argument("--getall", type=Path, required=True, help="Transferred final 145-recipe snapshot")
    parser.add_argument("--expected-index-sha256", required=True)
    parser.add_argument("--expected-head", default=BASE_HEAD)
    parser.add_argument("--run-id", default="31", help="31, or a new suffix such as 31b after a failed run")
    parser.add_argument("--dotnet", type=Path, default=Path(r"C:\Program Files\dotnet\dotnet.exe"))
    parser.add_argument("--git", type=Path, default=Path(r"C:\Program Files\Git\cmd\git.exe"))
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    require(re.fullmatch(r"31[a-z]?", args.run_id), "Use 31 or a new 31-letter suffix")
    require(re.fullmatch(r"[0-9a-f]{64}", args.expected_index_sha256), "Expected index SHA256 must be lower-case hex")
    require(re.fullmatch(r"[0-9a-f]{40}", args.expected_head), "Expected HEAD must be a full commit")
    args.desktop = args.desktop or args.task_root / "desktop-continuation-20261127"
    return args


def main():
    args = parse_args()
    evidence = args.task_root / "evidence-r18" / "flow-completion-20261127"
    prefix = "build" + args.run_id
    output = evidence / ("harness-" + prefix)
    result_path = evidence / (prefix + "-result.json")
    parser_path = evidence / ("parser" + args.run_id + ".json")
    policy_work = args.task_root / "evidence-r18" / "three-upstreams-20261127" / ("metaforce-policy-" + prefix)
    archive = args.task_root / "console-cache" / "metaforce-de8fc69-source.zip"
    labels = ["dotnet-version" + args.run_id, "harness-" + prefix,
              "regression" + args.run_id, "parser" + args.run_id, "metaforce-" + prefix]
    new_files = [result_path, parser_path]
    new_files += [evidence / (prefix + suffix + ".json") for suffix in
                  ("-request", "-git-before", "-git-after", "-sources-before", "-sources-after")]
    new_files += [evidence / (label + extension) for label in labels for extension in (".log", "-result.json")]
    plan = {"status": "PREPARED_ONLY", "desktop": str(args.desktop), "getall": str(args.getall),
            "expected_index_sha256": args.expected_index_sha256, "expected_head": args.expected_head,
            "output": str(output), "metaforce_work": str(policy_work), "result": str(result_path),
            "new_files": [str(path) for path in new_files], "native_stage_repeated": False}
    if not args.execute:
        print(json.dumps(plan), flush=True)
        return 0

    require(os.name == "nt", "This runner must execute on the authorized Windows device")
    for path in [args.desktop, args.getall, evidence, args.dotnet, args.git, archive]:
        require(path.is_absolute(), "Use an absolute input path: " + str(path))
        require(path.exists(), "Missing existing input: " + str(path))
    require(not output.exists() and not policy_work.exists(), "A fresh build output and Metaforce work path are required")
    require(len(new_files) == len(set(new_files)), "Internal output collision")
    for path in new_files:
        require(not path.exists(), "Refusing to overwrite evidence: " + str(path))
    index = args.getall / "index.json"
    require(digest(index) == args.expected_index_sha256, "GetAll index differs from the transferred final snapshot")
    require(archive.stat().st_size == 21536851 and digest(archive) == SOURCE_SHA, "Pinned Metaforce source cache is unavailable or changed")
    sdk_version = ET.parse(args.desktop / "AddonSdk" / "AllFix.Addons.Sdk.csproj").findtext(".//Version")
    require(sdk_version == "1.5.69", "Transferred SDK project must declare 1.5.69")
    initial_git = git_state(args)
    require(initial_git["head"] == args.expected_head, "Desktop HEAD changed before this run")
    initial_sources = source_manifest(args)
    environment = dict(os.environ)
    overrides = {"DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_NOLOGO": "1", "DOTNET_CLI_UI_LANGUAGE": "en"}
    environment.update(overrides)
    request = dict(plan, status="STARTED", started_utc=utc(), runner=file_info(__file__),
                   sdk_declared_version=sdk_version, dotnet=file_info(args.dotnet),
                   git_version=git(args, "--version").strip(), getall_index=file_info(index),
                   source_archive=file_info(archive), environment_overrides=overrides,
                   counts_regex={"pass": PASS_LINE.pattern, "fail": FAIL_LINE.pattern})
    write_json(evidence / (prefix + "-request.json"), request)
    write_json(evidence / (prefix + "-git-before.json"), initial_git)
    write_json(evidence / (prefix + "-sources-before.json"), initial_sources)
    output.mkdir()
    phases = []
    result = {"schema": 1, "status": "RUNNING", "run_id": args.run_id, "started_utc": request["started_utc"],
              "phases": phases, "source_inputs_unchanged": False, "git_state_unchanged": False,
              "getall_index_unchanged": False, "source_cache_unchanged": False,
              "native_stage_repeated": False, "native_cpp_built": False, "errors": []}

    def run(label, arguments, timeout, verify):
        log = evidence / (label + ".log")
        started = time.monotonic()
        row = {"mode": label, "command": [str(args.dotnet), *map(str, arguments)],
               "cwd": str(args.desktop), "started_utc": utc(), "status": "FAILED", "exit_code": None}
        phases.append(row)
        failure = None
        try:
            with log.open("xb") as stream:
                child = subprocess.run(row["command"], cwd=args.desktop, env=environment,
                                       stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
            row["exit_code"] = child.returncode
        except BaseException as error:
            failure = error
        text = log.read_text(encoding="utf-8-sig", errors="replace") if log.exists() else ""
        lines = text.splitlines()
        row.update(seconds=round(time.monotonic() - started, 3), finished_utc=utc(),
                   passes=sum(PASS_LINE.fullmatch(line) is not None for line in lines),
                   failures=sum(FAIL_LINE.fullmatch(line) is not None for line in lines),
                   log=file_info(log) if log.exists() else None)
        try:
            if failure is not None:
                raise failure
            require(row["exit_code"] == 0, label + " exited unsuccessfully")
            require(row["failures"] == 0, label + " emitted FAIL lines despite its exit code")
            verify(text, row)
            row["status"] = "PASS"
        except BaseException as error:
            row["error"] = str(error)
            failure = error
        write_json(evidence / (label + "-result.json"), row)
        print(json.dumps(row), flush=True)
        print(json.dumps({"mode": label, "tail": [line[:300] for line in lines[-8:]]}), flush=True)
        if failure is not None:
            raise failure

    def verify_version(text, row):
        require(text.strip() == "8.0.425", "Unexpected .NET SDK; use the existing verified 8.0.425")
        row["sdk_version"] = text.strip()

    def verify_build(text, row):
        summaries = {}
        for label in ("Warning", "Error"):
            found = re.findall(r"(?m)^\s*(\d+) " + label + r"\(s\)\s*$", text)
            require(len(found) == 1, "Missing or ambiguous MSBuild " + label + " summary")
            summaries[label.lower() + "s"] = int(found[0])
        row.update(summaries)
        require("Build succeeded." in text and summaries["errors"] == 0, "MSBuild success was not confirmed")
        row["assemblies"] = [file_info(output / name) for name in ("AddonInfrastructure.dll", "AllFix.Addons.Sdk.dll")]

    def verify_regression(text, row):
        require(row["passes"] >= 1866, "Regression passed fewer checks than the preserved BUILD30 baseline")
        for marker in ("METAFORCE_MEDIA_PASS checks=44", "MKW_CLI_POLICY_PASS"):
            require(text.splitlines().count(marker) == 1, "Missing or duplicate regression marker: " + marker)
        release = re.findall(r"(?m)^MKW_CLI_RELEASE_PASS checks=(\d+)\r?$", text)
        require(len(release) == 1 and int(release[0]) > 0, "MKW release policy did not finish")
        row["metaforce_media_checks"] = 44
        row["mkw_release_checks"] = int(release[0])

    def verify_parser(text, row):
        report = json.loads(parser_path.read_text(encoding="utf-8-sig"))
        require(report.get("passed") == 145 and report.get("failed") == 0, "Expected exactly 145 successful recipes and zero failures")
        row.update(recipes_passed=report["passed"], recipes_failed=report["failed"], report=file_info(parser_path))

    def verify_policy(text, row):
        require(row["passes"] == 52 and text.splitlines().count("METAFORCE_BUILD_POLICY_PASS checks=52") == 1,
                "Metaforce build policy did not finish all 52 checks")
        path = policy_work / "result.json"
        receipt = json.loads(path.read_text(encoding="utf-8-sig"))
        require(receipt.get("passed") == 52 and receipt.get("authoredDiscBytes") == 8192 and
                all(receipt.get(name) is False for name in ("commercialMediaAccepted", "nativeBuilderExecuted", "gameExecuted")) and
                receipt.get("sourceArchiveSha256") == SOURCE_SHA, "Metaforce authored-only receipt differs")
        row["receipt"] = file_info(path)

    try:
        run(labels[0], ["--version"], 30, verify_version)
        run(labels[1], ["build", str(args.desktop / "Tests" / "AddonInfrastructure" / "AddonInfrastructure.csproj"),
                       "-c", "Release", "--nologo", "--no-restore", "-o", str(output)], 300, verify_build)
        dll = output / "AddonInfrastructure.dll"
        run(labels[2], [str(dll)], 600, verify_regression)
        run(labels[3], [str(dll), "--parse-getall", str(args.getall), str(parser_path)], 180, verify_parser)
        run(labels[4], [str(dll), "--metaforce-build-policy", str(archive), str(policy_work)], 180, verify_policy)
    except BaseException as error:
        result["errors"].append(type(error).__name__ + ": " + str(error))
    finally:
        try:
            final_git = git_state(args)
            final_sources = source_manifest(args)
            write_json(evidence / (prefix + "-git-after.json"), final_git)
            write_json(evidence / (prefix + "-sources-after.json"), final_sources)
            result["git_state_unchanged"] = final_git == initial_git
            result["source_inputs_unchanged"] = final_sources == initial_sources
            result["getall_index_unchanged"] = digest(index) == args.expected_index_sha256
            result["source_cache_unchanged"] = archive.stat().st_size == 21536851 and digest(archive) == SOURCE_SHA
            require(all(result[key] for key in ("git_state_unchanged", "source_inputs_unchanged",
                                                "getall_index_unchanged", "source_cache_unchanged")),
                    "A source, Git state, index or preserved cache changed during validation")
        except BaseException as error:
            result["errors"].append("Final verification: " + type(error).__name__ + ": " + str(error))
        result["status"] = "PASS" if not result["errors"] and len(phases) == 5 and all(
            row["status"] == "PASS" and row["failures"] == 0 for row in phases) else "FAILED"
        result["finished_utc"] = utc()
        result["input_manifest"] = file_info(evidence / (prefix + "-sources-before.json"))
        result["sources_checked"] = len(initial_sources["files"])
        write_json(result_path, result)
        print(json.dumps({"final": result, "result": file_info(result_path)}), flush=True)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(json.dumps({"status": "FAILED_BEFORE_RUN", "error": type(error).__name__ + ": " + str(error)}), flush=True)
        raise SystemExit(1)
