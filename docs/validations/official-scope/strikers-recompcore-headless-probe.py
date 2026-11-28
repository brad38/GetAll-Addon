import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_module(host, dol, module, case, out):
    root = out / case
    config = root / "User/Config"
    logs = root / "User/Logs"
    config.mkdir(parents=True)
    logs.mkdir()
    (config / "Logger.ini").write_text(
        "[Options]\nVerbosity = 2\nWriteToFile = True\n[Logs]\nPowerPC = True\n", encoding="utf-8")
    fixture = root / "QA01.dol"
    shutil.copyfile(dol, fixture)
    env = {key: value for key, value in os.environ.items() if not key.startswith("STATICRECOMP_")}
    env["STATICRECOMP_MODULE"] = str(module)
    args = [host, "--platform", "headless", "-u", config.parent, "-e", fixture, "-v", "Null",
            "-C", "Dolphin.Core.CPUCore=6", "-C", "Dolphin.Analytics.Enabled=False",
            "-C", "Dolphin.General.UseDiscordPresence=False"]
    with (root / "host.log").open("wb") as log:
        child = subprocess.Popen(args, cwd=host.parent, env=env, stdout=log,
                                 stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            child.wait(timeout=3)
            stopped_by_probe = False
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait(timeout=8)
            stopped_by_probe = True
    output = (root / "host.log").read_text(encoding="utf-8", errors="replace")
    for log in logs.glob("*.log"):
        with log.open(encoding="utf-8", errors="replace") as stream:
            output += "\n" + "".join(line for line in stream if "staticrecomp" in line.casefold())
    checks = {
        "case": case, "module_sha256": sha(module), "stopped_by_probe": stopped_by_probe,
        "static_core_started": "[staticrecomp] core init" in output,
        "title_rejected": "module game_id 'G4QE01' != running game 'ID-QA01'" in output,
        "module_loaded": "[staticrecomp] module loaded:" in output,
    }
    if not checks["static_core_started"] or checks["title_rejected"] != (case == "mismatch") or checks["module_loaded"] != (case == "match"):
        raise RuntimeError(f"Unexpected RecompCore result: {checks}")
    return checks

def main():
    parser = argparse.ArgumentParser()
    for name in ("host", "dol", "strikers_module", "qa_module", "output"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    paths = {key: path.resolve() for key, path in vars(args).items()}
    out = paths["output"]
    out.mkdir()
    host, dol = paths["host"], paths["dol"]
    version = subprocess.run([host, "--version"], cwd=host.parent, capture_output=True,
                             text=True, timeout=15, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    result = {"scope": "Authored DOL and synthetic DLLs only. No retail disc or gameplay.",
              "host_version": version.stdout.strip(), "host_sha256": sha(host), "dol_sha256": sha(dol),
              "checks": [check_module(host, dol, paths["strikers_module"], "mismatch", out),
                         check_module(host, dol, paths["qa_module"], "match", out)]}
    print(json.dumps(result, indent=2))
    (out / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
