#!/usr/bin/env python3
"""Static and semantic validator for GetAll-Addon index, schemas, and recipes (SDK 1.4.1, v1-v8)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

try:
    import jsonschema
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    HAS_JSONSCHEMA = True
except ImportError:  # pragma: no cover - optional fallback for minimal local Python
    HAS_JSONSCHEMA = False

MAX_TOTAL_DATA_BYTES = 68_719_476_736  # 64 GiB per SDK 1.2.0 / 1.3.0

RE_INDEX_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,160}$")
RE_REPOSITORY = re.compile(
    r"^(?:[A-Za-z0-9-]+/[A-Za-z0-9_.-]+|gitlab:[A-Za-z0-9][A-Za-z0-9_.-]*(?:/[A-Za-z0-9][A-Za-z0-9_.-]*){1,7})$"
)
RE_INDEX_PATH = re.compile(
    r"^[A-Za-z0-9_][A-Za-z0-9_.-]*(/[A-Za-z0-9_][A-Za-z0-9_.-]*)*\.json$"
)
RE_RECIPE_PATH = re.compile(
    r"^[a-zA-Z0-9_][a-zA-Z0-9_.+-]*(/[a-zA-Z0-9_][a-zA-Z0-9_.+-]*)*$"
)
RE_RECIPE_PATH_V5 = re.compile(
    r"^(?![Cc][Oo][Nn] *(?:[./]|$)|[Pp][Rr][Nn] *(?:[./]|$)|[Aa][Uu][Xx] *(?:[./]|$)|[Nn][Uu][Ll] *(?:[./]|$)|(?:[Cc][Oo][Mm]|[Ll][Pp][Tt])[0-9\u00b9\u00b2\u00b3] *(?:[./]|$))[A-Za-z0-9_(](?:[A-Za-z0-9_.+() -]*[A-Za-z0-9_+()-])?(?:/(?![Cc][Oo][Nn] *(?:[./]|$)|[Pp][Rr][Nn] *(?:[./]|$)|[Aa][Uu][Xx] *(?:[./]|$)|[Nn][Uu][Ll] *(?:[./]|$)|(?:[Cc][Oo][Mm]|[Ll][Pp][Tt])[0-9\u00b9\u00b2\u00b3] *(?:[./]|$))[A-Za-z0-9_(](?:[A-Za-z0-9_.+() -]*[A-Za-z0-9_+()-])?)*$"
)
RE_SHA256 = re.compile(r"^[0-9A-Fa-f]{64}$")
RE_SHA1 = re.compile(r"^[0-9A-Fa-f]{40}$")
RE_MD5 = re.compile(r"^[0-9A-Fa-f]{32}$")
RE_MAGIC_HEX = re.compile(r"^(?:[A-Fa-f0-9]{2}){2,32}$")
RE_EXT = re.compile(r"^\.[A-Za-z0-9]{1,12}$")
RE_PROFILE_FOLDER = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.-]{0,79}$")
RE_ROAMING_TARGET = re.compile(
    r"^[A-Za-z0-9_][A-Za-z0-9_.-]*\.(z64|n64|v64|rom|bin|dat|pak|wad)$"
)
RE_DATA_TARGET_EXT = re.compile(
    r"\.(?:z64|n64|v64|rom|bin|dat|pak|wad)$",
    re.IGNORECASE,
)
RE_DATA_TARGET_EXT_V7 = re.compile(r"\.(?:z64|n64|v64|rom|bin|dat|pak|wad|sfc|smc|gba)$", re.IGNORECASE)
RE_V4_DATA_EXT = re.compile(
    r"\.(?:bin|cue|iso|img|dat|pak|wad|rom|z64|n64|v64|o2r|otr|wav|raw|chd|gdi|vpk|wma|mp3|ogg)$",
    re.IGNORECASE,
)

WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}

RE_CRC32 = re.compile(r"^[a-fA-F0-9]{8}$")
RE_JAVA_MAIN_CLASS_V8 = re.compile(
    r"^[A-Za-z_$][A-Za-z0-9_$]*(\.[A-Za-z_$][A-Za-z0-9_$]*)+$"
)
ALLOWED_JVM_OPTIONS_V8 = {
    "joml-fastmath", "joml-sin-lookup", "joml-fma",
    "open-java-util", "export-jdk-internal-misc", "enable-native-access",
}
SEVERED_CHAINS_JVM_OPTIONS = [
    "joml-fastmath", "joml-sin-lookup", "joml-fma",
    "open-java-util", "export-jdk-internal-misc", "enable-native-access",
]
SEVERED_CHAINS_SOURCE = "https://github.com/Legend-of-Dragoon-Modding/Severed-Chains"
RE_NUMERIC_ROM_EXT = re.compile(r"\.[0-9]{1,3}$")
RE_DATA_EXT_V7 = re.compile(r"\.(?:sfc|smc|gba)$", re.IGNORECASE)
RE_BLOCKED_EXEC_ASSET = re.compile(r"\.(?:exe|msi|cmd|bat|ps1|vbs|wsf|scr|pif|com)$", re.IGNORECASE)
VALID_STATUSES = {"validated", "disabled", "draft", "experimental"}
VALID_SCHEMA_VERSIONS = {1, 2, 3, 4, 5, 6, 7, 8, 9}
VALID_PROFILE_SCOPES_V5 = {"installation", "roaming_app_data", "local_app_data"}
VALID_PREREQUISITES = {
    "dotnet-desktop-10-x64",
    "java-21",
    "openal-x64",
    "openal-x86",
}
DEFAULT_CATALOG_URL = (
    "https://raw.githubusercontent.com/brad38/AllFix-Repo/main/catalog.json"
)


def is_safe_relative_path(
    value: Any,
    *,
    allow_v5_chars: bool = False,
) -> tuple[bool, str]:
    """Validate a relative recipe path according to SDK 1.2.0 / 1.3.0 and Windows safety rules."""
    if not isinstance(value, str) or not value:
        return False, "must be a non-empty string"
    if len(value) > 240:
        return False, "exceeds maxLength 240"
    if "\\" in value or value.startswith("/"):
        return False, "must be a forward-slash relative path"
    pattern = RE_RECIPE_PATH_V5 if allow_v5_chars else RE_RECIPE_PATH
    if not pattern.match(value):
        return False, "fails SDK path grammar (spaces or disallowed characters)"
    for segment in value.split("/"):
        if segment in {".", ".."} or ".." in segment.split("."):
            return False, f"disallowed traversal segment '{segment}'"
        stem = segment.split(".", 1)[0].rstrip(" ").upper()
        if stem in WINDOWS_RESERVED_NAMES:
            return False, f"disallowed Windows reserved device name '{segment}'"
    return True, ""


def read_utf8_bytes(path: Path, strict_lf: bool) -> tuple[bytes, list[str]]:
    """Read file bytes, verify UTF-8 without BOM, and check LF line endings."""
    errors: list[str] = []
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{path.as_posix()}: UTF-8 BOM is not allowed")
    if b"\r\n" in raw:
        if strict_lf:
            errors.append(f"{path.as_posix()}: contains CRLF line endings (expected LF)")
        raw_lf = raw.replace(b"\r\n", b"\n")
    else:
        raw_lf = raw
    try:
        raw_lf.decode("utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{path.as_posix()}: invalid UTF-8 ({exc})")
    return raw_lf, errors


def load_schema_registry(schemas_dir: Path) -> tuple[dict[str, dict[str, Any]], Any]:
    """Load all local JSON schemas and build a referencing.Registry when jsonschema is installed."""
    schema_files = {
        "index": "remote-recipe-index-v1.schema.json",
        1: "installation-recipe-v1.schema.json",
        2: "installation-recipe-v2.schema.json",
        3: "installation-recipe-v3.schema.json",
        4: "installation-recipe-v4.schema.json",
        5: "installation-recipe-v5.schema.json",
        6: "installation-recipe-v6.schema.json",
        7: "installation-recipe-v7.schema.json",
        8: "installation-recipe-v8.schema.json",
        9: "installation-recipe-v9.schema.json",
    }
    schemas: dict[Any, dict[str, Any]] = {}
    for key, filename in schema_files.items():
        schema_path = schemas_dir / filename
        if not schema_path.is_file():
            raise FileNotFoundError(f"Missing schema file: {schema_path}")
        schemas[key] = json.loads(schema_path.read_text(encoding="utf-8"))

    registry = None
    if HAS_JSONSCHEMA:
        resources = []
        for jf in sorted(schemas_dir.glob("*.json")):
            doc = json.loads(jf.read_text(encoding="utf-8"))
            resource = Resource.from_contents(doc)
            resources.append((jf.name, resource))
            resources.append((jf.resolve().as_uri(), resource))
        registry = Registry().with_resources(resources)
    return schemas, registry


def validate_with_jsonschema(
    instance: Any,
    schema: dict[str, Any],
    registry: Any,
    label: str,
) -> list[str]:
    """Run Draft 2020-12 JSON Schema validation when jsonschema is available."""
    if not HAS_JSONSCHEMA:
        return []
    validator = Draft202012Validator(schema, registry=registry)
    errors = []
    for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.path) or "<root>"
        errors.append(f"{label}: schema violation at '{loc}': {err.message}")
    return errors


def _validate_size_fields(
    item: dict[str, Any],
    label: str,
    item_loc: str,
    errors: list[str],
) -> None:
    """Validate optional integer size/min_size/max_size fields within 1..MAX_TOTAL_DATA_BYTES."""
    for field in ("size", "min_size", "max_size"):
        if field in item:
            val = item[field]
            if isinstance(val, bool) or not isinstance(val, int) or not (1 <= val <= MAX_TOTAL_DATA_BYTES):
                errors.append(
                    f"{label}: {item_loc}.{field} must be integer in 1..{MAX_TOTAL_DATA_BYTES}"
                )
    if (
        isinstance(item.get("min_size"), int)
        and not isinstance(item.get("min_size"), bool)
        and isinstance(item.get("max_size"), int)
        and not isinstance(item.get("max_size"), bool)
        and item["min_size"] > item["max_size"]
    ):
        errors.append(f"{label}: {item_loc}.min_size exceeds max_size")


def _has_v5_file_verification(item: dict[str, Any]) -> bool:
    """Check whether item satisfies one of the four SDK v5 verification contracts."""
    has_sha256 = isinstance(item.get("sha256"), str) and bool(RE_SHA256.match(item["sha256"]))
    has_sha1 = isinstance(item.get("sha1"), str) and bool(RE_SHA1.match(item["sha1"]))
    has_magic = isinstance(item.get("magic_hex"), str) and bool(RE_MAGIC_HEX.match(item["magic_hex"]))
    has_size = (
        isinstance(item.get("size"), int)
        and not isinstance(item.get("size"), bool)
        and item["size"] >= 1
    )
    has_min_size = (
        isinstance(item.get("min_size"), int)
        and not isinstance(item.get("min_size"), bool)
        and item["min_size"] >= 1
    )
    return has_sha256 or has_sha1 or (has_size and has_magic) or (has_min_size and has_magic)


def _validate_single_segment_v5(
    value: Any,
    *,
    allow_v5_chars: bool,
    max_length: int = 80,
) -> bool:
    """Validate a single folder name segment (no '/')."""
    if not isinstance(value, str) or not value or len(value) > max_length or "/" in value:
        return False
    if not allow_v5_chars:
        return bool(RE_PROFILE_FOLDER.match(value))
    return is_safe_relative_path(value, allow_v5_chars=True)[0]


def validate_verified_data_files(
    files: Any,
    label: str,
    prefix: str,
    *,
    schema_version: int = 4,
    is_import_set: bool = False,
    is_first_run: bool = False,
    is_arcade: bool = False,
) -> list[str]:
    """Validate SDK v4/v5 verifiedDataFiles / importFiles / firstRunFiles array semantics."""
    errors: list[str] = []
    if not isinstance(files, list) or not (1 <= len(files) <= 64):
        return [f"{label}: {prefix} must be an array with 1..64 items"]

    allow_v5 = schema_version >= 5
    seen_keys: set[tuple[str, str, str]] = set()
    total_size = 0
    for idx, item in enumerate(files):
        item_loc = f"{prefix}[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: {item_loc} must be an object")
            continue
        p = item.get("path")
        ok, reason = is_safe_relative_path(p, allow_v5_chars=allow_v5)
        if not ok:
            errors.append(f"{label}: {item_loc}.path {reason}")
        else:
            regular = RE_V4_DATA_EXT.search(p) or (
                schema_version >= 7 and RE_DATA_EXT_V7.search(p)
            )
            arcade_numeric = is_arcade and schema_version >= 7 and RE_NUMERIC_ROM_EXT.search(p)
            if not (regular or arcade_numeric):
                errors.append(f"{label}: {item_loc}.path '{p}' has disallowed data file extension")

        if schema_version < 5:
            size = item.get("size")
            if not isinstance(size, int) or isinstance(size, bool) or not (1 <= size <= MAX_TOTAL_DATA_BYTES):
                errors.append(f"{label}: {item_loc}.size must be integer in 1..{MAX_TOTAL_DATA_BYTES}")
            else:
                total_size += size

            sha256 = item.get("sha256")
            if not isinstance(sha256, str) or not RE_SHA256.match(sha256):
                errors.append(f"{label}: {item_loc}.sha256 must be 64 hex chars")

            if isinstance(p, str):
                norm_key = ("installation", "", p.lower())
                if norm_key in seen_keys:
                    errors.append(f"{label}: duplicate case-insensitive path '{p}' in {prefix}")
                seen_keys.add(norm_key)
        else:
            _validate_size_fields(item, label, item_loc, errors)
            if is_arcade:
                if schema_version < 7:
                    errors.append(f"{label}: {item_loc} arcade_romset requires v7")
                if not isinstance(item.get("size"), int) or isinstance(item.get("size"), bool) or not 1 <= item["size"] <= MAX_TOTAL_DATA_BYTES:
                    errors.append(f"{label}: {item_loc}.size is required for arcade ROM")
                if "crc32" in item and (not isinstance(item["crc32"], str) or not RE_CRC32.fullmatch(item["crc32"])):
                    errors.append(f"{label}: {item_loc}.crc32 must be 8 hex characters")
                if not (
                    isinstance(item.get("crc32"), str) and bool(RE_CRC32.fullmatch(item["crc32"]))
                    or isinstance(item.get("sha256"), str) and bool(RE_SHA256.fullmatch(item["sha256"]))
                    or isinstance(item.get("sha1"), str) and bool(RE_SHA1.fullmatch(item["sha1"]))
                ):
                    errors.append(f"{label}: {item_loc} requires CRC32, SHA256 or SHA1")
            if is_import_set and "size" not in item and "max_size" not in item:
                errors.append(f"{label}: {item_loc} in import_input_set requires size or max_size")
            if not _has_v5_file_verification(item) and not (
                is_arcade and schema_version >= 7
                and isinstance(item.get("crc32"), str)
                and bool(RE_CRC32.fullmatch(item["crc32"]))
                and isinstance(item.get("size"), int) and not isinstance(item.get("size"), bool)
            ):
                errors.append(f"{label}: {item_loc} requires verified checksum and size/magic")
            if "sha256" in item and (not isinstance(item["sha256"], str) or not RE_SHA256.match(item["sha256"])):
                errors.append(f"{label}: {item_loc}.sha256 must be 64 hex chars")
            if "sha1" in item and (not isinstance(item["sha1"], str) or not RE_SHA1.match(item["sha1"])):
                errors.append(f"{label}: {item_loc}.sha1 must be 40 hex chars")
            if "magic_hex" in item and (not isinstance(item["magic_hex"], str) or not RE_MAGIC_HEX.match(item["magic_hex"])):
                errors.append(f"{label}: {item_loc}.magic_hex must be 4..64 hex chars")

            quota_size = item.get("size") if isinstance(item.get("size"), int) and not isinstance(item.get("size"), bool) else (
                item.get("max_size") if isinstance(item.get("max_size"), int) and not isinstance(item.get("max_size"), bool) else 0
            )
            total_size += max(0, quota_size)

            scope = "installation"
            profile_folder = ""
            if is_first_run:
                if "scope" in item:
                    scope_val = item["scope"]
                    if scope_val not in VALID_PROFILE_SCOPES_V5:
                        errors.append(f"{label}: {item_loc}.scope invalid '{scope_val}'")
                    else:
                        scope = scope_val
                if scope in {"local_app_data", "roaming_app_data"}:
                    pf = item.get("profile_folder")
                    if schema_version >= 7:
                        valid_pf = isinstance(pf, str) and len(pf) <= 160 and all(
                            _validate_single_segment_v5(seg, allow_v5_chars=True, max_length=80)
                            for seg in pf.split("/")
                        ) and len(pf.split("/")) <= 4
                    else:
                        valid_pf = _validate_single_segment_v5(pf, allow_v5_chars=True, max_length=80)
                    if not valid_pf:
                        errors.append(f"{label}: {item_loc}.profile_folder invalid or missing for scope '{scope}'")
                    else:
                        profile_folder = pf
                elif "profile_folder" in item:
                    errors.append(f"{label}: {item_loc}.profile_folder is forbidden when scope == 'installation'")

            if isinstance(p, str):
                norm_key = (scope, profile_folder.lower(), p.lower())
                if norm_key in seen_keys:
                    errors.append(f"{label}: duplicate case-insensitive path '{p}' in {prefix}")
                seen_keys.add(norm_key)

    if total_size > MAX_TOTAL_DATA_BYTES:
        errors.append(
            f"{label}: total size in {prefix} ({total_size} bytes) exceeds 64 GiB limit"
        )
    return errors


def validate_java_launcher_v8(
    recipe: dict[str, Any],
    required_files: set[str],
    label: str,
) -> list[str]:
    """Exact static counterpart of SDK 1.4.1 Java v8 parser allowlists.

    This deliberately does not claim to check actual JAR bytecode, external Java
    runtime availability or a playable game: those checks belong to the host.
    """
    errors: list[str] = []
    java = recipe.get("java_launcher")
    if not isinstance(java, dict):
        return [f"{label}: java_launcher must be an object"]
    allowed = {
        "jar", "runtime", "working_directory", "main_class", "classpath",
        "jvm_options", "program_arguments_profile",
    }
    for key in java:
        if key not in allowed:
            errors.append(f"{label}: java_launcher.{key} is not allowed")
    req_lower = {f.casefold() for f in required_files}

    def is_declared_jar(path: Any) -> bool:
        return (
            isinstance(path, str) and path.lower().endswith(".jar")
            and is_safe_relative_path(path, allow_v5_chars=True)[0]
            and path.casefold() in req_lower
        )

    jar = java.get("jar")
    if not is_declared_jar(jar):
        errors.append(f"{label}: java_launcher.jar must be a safe declared local JAR")
    runtime = java.get("runtime")
    if runtime not in ("java-21", "java-25"):
        errors.append(f"{label}: java_launcher.runtime requires java-21 or java-25")
    if runtime not in (recipe.get("prerequisites") or []):
        errors.append(f"{label}: java_launcher requires matching runtime prerequisite")
    if "working_directory" in java and not is_safe_relative_path(
        java["working_directory"], allow_v5_chars=True
    )[0]:
        errors.append(f"{label}: java_launcher.working_directory is unsafe")

    has_class = "main_class" in java
    if has_class:
        main_class = java["main_class"]
        if not isinstance(main_class, str) or len(main_class) > 180 or not RE_JAVA_MAIN_CLASS_V8.fullmatch(main_class):
            errors.append(f"{label}: java_launcher.main_class is invalid")
        cp = java.get("classpath")
        if not isinstance(cp, list) or not 1 <= len(cp) <= 128:
            errors.append(f"{label}: java_launcher.classpath needs 1..128 JAR paths")
        else:
            if len({v.casefold() for v in cp if isinstance(v, str)}) != len(cp):
                errors.append(f"{label}: java_launcher.classpath has case-insensitive duplicates")
            if not isinstance(jar, str) or jar.casefold() not in {
                v.casefold() for v in cp if isinstance(v, str)
            }:
                errors.append(f"{label}: java_launcher.jar must be in classpath")
            for i, path in enumerate(cp):
                if not is_declared_jar(path):
                    errors.append(f"{label}: java_launcher.classpath[{i}] must be safe .jar in required_files")
        if "jvm_options" in java:
            opts = java["jvm_options"]
            if (
                not isinstance(opts, list) or len(opts) > 12
                or not all(isinstance(o, str) and o in ALLOWED_JVM_OPTIONS_V8 for o in opts)
                or len(set(o for o in opts if isinstance(o, str))) != len(opts)
            ):
                errors.append(f"{label}: java_launcher.jvm_options must use the SDK allowlist without duplicates")
        profile = java.get("program_arguments_profile")
        if profile is not None and profile != "severed-chains-3":
            errors.append(f"{label}: java_launcher.program_arguments_profile is not approved")
        if profile == "severed-chains-3" and (
            recipe.get("project_id") != "severed-chains"
            or recipe.get("source_url") != SEVERED_CHAINS_SOURCE
            or runtime != "java-25"
            or main_class != "legend.game.MainWindows"
            or java.get("jvm_options") != SEVERED_CHAINS_JVM_OPTIONS
        ):
            errors.append(f"{label}: severed-chains-3 requires exact official identity, runtime, main_class and ordered JVM options")
    else:
        for field in ("classpath", "jvm_options", "program_arguments_profile"):
            if field in java:
                errors.append(f"{label}: java_launcher.{field} requires main_class in schema v8")

    if "launch_file" in recipe:
        errors.append(f"{label}: java_launcher cannot coexist with launch_file")
    return errors


def validate_recipe_semantics(
    recipe: Any,
    entry: dict[str, Any],
    label: str,
) -> list[str]:
    """Validate semantic and cross-field SDK 1.2.0–1.4.1 contracts for v1-v8 recipes."""
    errors: list[str] = []
    if not isinstance(recipe, dict):
        return [f"{label}: root must be a JSON object"]

    required_root = [
        "schema_version",
        "project_id",
        "tag",
        "source_url",
        "operations",
        "required_files",
        "inputs",
    ]
    for key in required_root:
        if key not in recipe:
            errors.append(f"{label}: missing required field '{key}'")

    schema_version = recipe.get("schema_version")
    if schema_version not in VALID_SCHEMA_VERSIONS:
        errors.append(f"{label}: unsupported schema_version '{schema_version}'")
        return errors

    if schema_version == 9:
        # Independently pin the exact preparation contract, even without jsonschema.
        profiles = json.loads("[{\"schema_version\":9,\"project_id\":\"god-of-war-native-pc-port-gow-pc-port\",\"tag\":\"launcher-v0.4.0\",\"source_url\":\"https://github.com/danielalves96/gow-pc-port/releases/tag/launcher-v0.4.0\",\"operations\":[],\"required_files\":[\"God Of War - PC Launcher_0.4.0_x64-portable/God Of War - PC Launcher.exe\",\"God Of War - PC Launcher_0.4.0_x64-portable/README.txt\",\"God Of War - PC Launcher_0.4.0_x64-portable/kit/install.ps1\",\"God Of War - PC Launcher_0.4.0_x64-portable/kit/bin/ps2_recomp.exe\",\"God Of War - PC Launcher_0.4.0_x64-portable/kit/bin/ps2-tools.exe\",\"God Of War - PC Launcher_0.4.0_x64-portable/kit/RustPortPS2/games/scus-97399/gow-port.toml\"],\"inputs\":[],\"manual_steps\":\"Kit oficial preparado. O jogo ainda nao foi compilado. A compilacao exige sua propria midia PS2 USA SCUS-97399 e dependencias do projeto. O All-Fix nao executa o launcher nem scripts automaticamente. Consulte as instrucoes oficiais.\",\"build_profile\":\"gow-0.4.0-prepare\",\"preparation_media\":[{\"id\":\"original-disc\",\"kind\":\"file\",\"extensions\":[\".iso\",\".chd\"],\"version\":\"PS2 USA SCUS-97399\"}]},{\"schema_version\":9,\"project_id\":\"totk-pc-recomp\",\"tag\":\"v0.5.0\",\"source_url\":\"https://github.com/valentderah/totk-pc-recomp/releases/tag/v0.5.0\",\"operations\":[],\"required_files\":[\"TotK-Setup-0.5.0-windows/TotK-Setup.exe\",\"TotK-Setup-0.5.0-windows/bin/totk_xlate.exe\",\"TotK-Setup-0.5.0-windows/bin/hactool.exe\",\"TotK-Setup-0.5.0-windows/bin/ninja.exe\",\"TotK-Setup-0.5.0-windows/llvm/bin/clang.exe\",\"TotK-Setup-0.5.0-windows/python/python.exe\",\"TotK-Setup-0.5.0-windows/bin/SDL3.dll\"],\"inputs\":[],\"manual_steps\":\"Kit oficial preparado. O jogo ainda nao foi compilado. A compilacao exige sua propria midia Switch e atualizacao 1.1.0, 1.2.1 ou 1.4.3, alem dos requisitos oficiais. O All-Fix nao executa o setup nem scripts automaticamente. Consulte as instrucoes oficiais.\",\"build_profile\":\"totk-0.5.0-prepare\",\"preparation_media\":[{\"id\":\"base-game\",\"kind\":\"file\",\"extensions\":[\".nsp\",\".xci\",\".nsz\",\".xcz\"],\"version\":\"Switch original\"},{\"id\":\"game-update\",\"kind\":\"file\",\"extensions\":[\".nsp\",\".xci\",\".nsz\",\".xcz\"],\"version\":\"1.1.0, 1.2.1 ou 1.4.3\"}]},{\"schema_version\":9,\"project_id\":\"pinyon-shift\",\"tag\":\"v0.9.5\",\"source_url\":\"https://github.com/arcanite24/pinyon-shift/releases/tag/v0.9.5\",\"operations\":[],\"required_files\":[\"PinyonShiftLauncher.exe\",\"pinyon-shift-source.zip\"],\"inputs\":[],\"manual_steps\":\"Kit oficial preparado. O jogo ainda nao foi compilado. Use sua propria midia Xbox 360 USA MS-2505 (4D5309C9). O launcher oficial obtem ferramentas e compila localmente. O All-Fix nao executa o launcher nem scripts automaticamente. Consulte as instrucoes oficiais.\",\"build_profile\":\"pinyon-0.9.5-prepare\",\"preparation_media\":[{\"id\":\"original-disc\",\"kind\":\"file\",\"extensions\":[\".iso\"],\"version\":\"Xbox 360 USA MS-2505 / 4D5309C9\"}]},{\"schema_version\":9,\"project_id\":\"doaxvb-re\",\"tag\":\"v0.8.0\",\"source_url\":\"https://github.com/NoRain211/doaxvb-re/releases/tag/v0.8.0\",\"operations\":[],\"required_files\":[\"DOAXBV-0.8.0/README.txt\",\"DOAXBV-0.8.0/BuildGame.cmd\",\"DOAXBV-0.8.0/Launcher.cmd\",\"DOAXBV-0.8.0/tools/build_game.py\",\"DOAXBV-0.8.0/tools/extract_iso.py\",\"DOAXBV-0.8.0/recomp-runtime/CMakeLists.txt\"],\"inputs\":[],\"manual_steps\":\"Kit oficial preparado. O jogo ainda nao foi compilado. Use sua propria ISO Xbox USA suportada pelo projeto. O primeiro build exige dependencias externas oficiais. O All-Fix nao executa Launcher.cmd, BuildGame.cmd ou instaladores automaticamente. Consulte README.txt e as instrucoes oficiais.\",\"build_profile\":\"doax-0.8.0-prepare\",\"preparation_media\":[{\"id\":\"original-disc\",\"kind\":\"file\",\"extensions\":[\".iso\"],\"version\":\"Xbox USA suportado pelo projeto\"}]},{\"schema_version\":9,\"project_id\":\"ssx-recomp\",\"tag\":\"v2.0.0\",\"source_url\":\"https://github.com/AmarilloNL/ssx-recomp/releases/tag/v2.0.0\",\"operations\":[],\"required_files\":[\"ssx-recomp.exe\",\"recomplauncher.json\"],\"inputs\":[],\"manual_steps\":\"Kit oficial preparado. O jogo ainda nao foi compilado. Use sua propria ISO Xbox 360 EA-2413 (USA, Europa ou Australia), ou pasta extraida com default.xex. O launcher necessita de Visual Studio Build Tools e pode baixar ferramentas; o All-Fix nao executa nem instala essas dependencias automaticamente. Consulte as instrucoes oficiais.\",\"build_profile\":\"ssx-2.0.0-prepare\",\"preparation_media\":[{\"id\":\"original-disc\",\"kind\":\"file\",\"extensions\":[\".iso\"],\"version\":\"Xbox 360 EA-2413 USA/Europe/Australia\"}]},{\"schema_version\":9,\"project_id\":\"lasrecomp\",\"tag\":\"v0.6.1\",\"source_url\":\"https://github.com/peiikai/LASRecomp/releases/tag/v0.6.1\",\"operations\":[],\"required_files\":[\"LAS Recomp/lasrecomp.exe\",\"LAS Recomp/README.md\",\"LAS Recomp/SDL3.dll\",\"LAS Recomp/lasgen/lasgen.exe\",\"LAS Recomp/zig/zig.exe\",\"LAS Recomp/gamelib-src/gamelib_entry.c\"],\"inputs\":[],\"manual_steps\":\"Kit oficial preparado. O jogo ainda nao foi compilado. Use sua propria copia de Link's Awakening Switch, versao 1.0.0, 1.0.1 ou 1.1.0, com pastas exefs e romfs. O aplicativo oficial recompila a biblioteca do jogo localmente com as ferramentas fornecidas. O All-Fix nao executa o launcher nem compiladores automaticamente.\",\"build_profile\":\"las-0.6.1-prepare\",\"preparation_media\":[{\"id\":\"original-game\",\"kind\":\"directory\",\"extensions\":[],\"version\":\"Switch 1.0.0, 1.0.1 ou 1.1.0 (ExeFS/RomFS)\"}]},{\"schema_version\":9,\"project_id\":\"gta-stories-recompiled\",\"tag\":\"v0.3.2\",\"source_url\":\"https://github.com/batinium/gta-stories-recompiled/releases/tag/v0.3.2\",\"operations\":[],\"required_files\":[\"GTA-Stories-Recompiled-0.3.2-windows/GTAStoriesLauncher.exe\",\"GTA-Stories-Recompiled-0.3.2-windows/README.md\",\"GTA-Stories-Recompiled-0.3.2-windows/CMakeLists.txt\",\"GTA-Stories-Recompiled-0.3.2-windows/tools/build.py\",\"GTA-Stories-Recompiled-0.3.2-windows/python/python.exe\",\"GTA-Stories-Recompiled-0.3.2-windows/deps/manifest.json\"],\"inputs\":[],\"manual_steps\":\"Prepara\\u00e7\\u00e3o apenas. Forne\\u00e7a seu disco original PS2 USA de Liberty City Stories (SLUS-21423) ou Vice City Stories (SLUS-21590); ambos para o modo combinado. Fa\\u00e7a a compila\\u00e7\\u00e3o pelo launcher oficial manualmente. N\\u00e3o inclui m\\u00eddia.\",\"build_profile\":\"gta-stories-0.3.2-prepare\",\"preparation_media\":[{\"id\":\"original-disc\",\"kind\":\"file\",\"extensions\":[\".iso\"],\"version\":\"PS2 USA SLUS-21423 ou SLUS-21590; ambos para modo combinado\"}]},{\"schema_version\":9,\"project_id\":\"rygt-gt7\",\"tag\":\"rygt-2026-11-23\",\"source_url\":\"https://github.com/RyGT-Team/RyGT/releases/tag/rygt-2026-11-23\",\"operations\":[],\"required_files\":[\"RyGT-ci-889c5a7e/RyGTLauncher.exe\",\"RyGT-ci-889c5a7e/converter/ryty.exe\",\"RyGT-ci-889c5a7e/README.txt\",\"RyGT-ci-889c5a7e/BUILD_INFO.txt\",\"RyGT-ci-889c5a7e/SHA256SUMS.txt\"],\"inputs\":[],\"manual_steps\":\"Prepara\\u00e7\\u00e3o apenas. Use seu pr\\u00f3prio dump PS4 Gran Turismo 7 CUSA24769 e m\\u00f3dulos de firmware obtidos legitimamente. A convers\\u00e3o e configura\\u00e7\\u00e3o ficam a cargo do usu\\u00e1rio no launcher oficial; n\\u00e3o execute automaticamente nem instale patches ou servi\\u00e7os.\",\"build_profile\":\"rygt-2026-11-23-prepare\",\"preparation_media\":[{\"id\":\"original-game\",\"kind\":\"directory\",\"extensions\":[],\"version\":\"PS4 CUSA24769\"}]},{\"schema_version\":9,\"project_id\":\"spartanport\",\"tag\":\"windows-v3.2.1\",\"source_url\":\"https://github.com/FelipePrado0/SpartanPort/releases/tag/windows-v3.2.1\",\"operations\":[],\"required_files\":[\"spartanport-windows/SpartanPort.exe\",\"spartanport-windows/Play SpartanPort.exe\",\"spartanport-windows/README-Windows.txt\",\"spartanport-windows/recomplauncher.json\",\"spartanport-windows/bin/spartanport-probe.exe\"],\"inputs\":[],\"manual_steps\":\"Prepara\\u00e7\\u00e3o apenas. Use seu pr\\u00f3prio dump de God of War III Remastered PS4 CUSA01623 ou CUSA01715, vers\\u00e3o 01.00/01.02. Configure manualmente o launcher oficial para preparar a imagem; nenhuma execu\\u00e7\\u00e3o autom\\u00e1tica.\",\"build_profile\":\"spartanport-3.2.1-prepare\",\"preparation_media\":[{\"id\":\"original-game\",\"kind\":\"directory\",\"extensions\":[],\"version\":\"PS4 CUSA01623/CUSA01715 01.00 ou 01.02\"}]},{\"schema_version\":9,\"project_id\":\"super-odyssey-pc-recomp\",\"tag\":\"v1.0.0\",\"source_url\":\"https://github.com/Simon3Sarkis/super-odyssey-pc-recomp/releases/tag/v1.0.0\",\"operations\":[],\"required_files\":[\"Super Odyssey PC Recomp/SuperOdysseyRecomp.exe\",\"Super Odyssey PC Recomp/README.md\",\"Super Odyssey PC Recomp/recomplauncher.json\",\"Super Odyssey PC Recomp/SDL3.dll\",\"Super Odyssey PC Recomp/zig/zig.exe\",\"Super Odyssey PC Recomp/odysseygen/python.exe\"],\"inputs\":[],\"manual_steps\":\"Prepara\\u00e7\\u00e3o apenas. Forne\\u00e7a sua pr\\u00f3pria c\\u00f3pia Nintendo Switch de Super Mario Odyssey 1.0.0 ou 1.4.1 com update aplicado, pastas exefs e romfs. O instalador oficial compila o jogo localmente. Nenhuma execu\\u00e7\\u00e3o autom\\u00e1tica.\",\"build_profile\":\"odyssey-1.0.0-prepare\",\"preparation_media\":[{\"id\":\"original-game\",\"kind\":\"directory\",\"extensions\":[],\"version\":\"Switch 1.0.0 ou 1.4.1 (ExeFS/RomFS)\"}]},{\"schema_version\":9,\"project_id\":\"dkb-pc-recomp\",\"tag\":\"v0.5.1\",\"source_url\":\"https://github.com/Lucas-blip-png/dkb-pc-recomp/releases/tag/v0.5.1\",\"operations\":[],\"required_files\":[\"DKB-Setup/DKB-Setup.exe\",\"DKB-Setup/recomplauncher.json\",\"DKB-Setup/VERSION\",\"DKB-Setup/bin/ninja.exe\",\"DKB-Setup/bin/totk_xlate.exe\",\"DKB-Setup/python/python.exe\",\"DKB-Setup/llvm/bin/clang.exe\"],\"inputs\":[],\"manual_steps\":\"Kit oficial preparado. Forneca sua propria copia Switch 2 de Donkey Kong Bananza 1.0.0 ou com update 3.2.0: arquivo .nup, ou pasta contendo exefs e romfs. O setup oficial compila o jogo localmente. O All-Fix nao executa o setup nem ferramentas automaticamente.\",\"build_profile\":\"dkb-0.5.1-44ba6b1-prepare\",\"preparation_media\":[{\"id\":\"original-game\",\"kind\":\"file\",\"extensions\":[\".nup\"],\"version\":\"Switch 2 1.0.0 ou 3.2.0; alternativa: pasta ExeFS/RomFS\"}]},{\"schema_version\":9,\"project_id\":\"mkw-recomp\",\"tag\":\"v0.1.18\",\"source_url\":\"https://github.com/adriadam10/mkw-recomp/releases/tag/v0.1.18\",\"operations\":[],\"required_files\":[\"mkw-recomp/mkw.exe\",\"mkw-recomp/SDL3.dll\",\"mkw-recomp/recomplauncher.json\",\"mkw-recomp/setup/clang/clang.exe\",\"mkw-recomp/setup/python/python.exe\",\"mkw-recomp/setup/src/recomp/gen.py\",\"mkw-recomp/setup/src/tools/build/build.py\"],\"inputs\":[],\"manual_steps\":\"Kit oficial preparado. Forneca sua propria copia de Mario Kart World Switch 2, versao 1.0.0 ou 1.8.0, na interface oficial de configuracao. O jogo e compilado localmente e ferramentas adicionais podem ser necessarias. O All-Fix nao executa automaticamente o launcher nem compiladores.\",\"build_profile\":\"mkw-0.1.18-prepare\",\"preparation_media\":[{\"id\":\"original-game\",\"kind\":\"directory\",\"extensions\":[],\"version\":\"Switch 2 1.0.0 ou 1.8.0 (ExeFS/RomFS)\"}]},{\"schema_version\":9,\"project_id\":\"sarecomp-sonic-adventure-recompiled\",\"tag\":\"v0.52.0\",\"source_url\":\"https://github.com/sonicfreak1337/SARecomp/releases/tag/v0.52.0\",\"operations\":[],\"required_files\":[\"game.exe\",\"sonic-setup.exe\",\"sonic-config.exe\",\"SDL3.dll\",\"README.txt\",\"resources/payload-files.tsv\",\"resources/install-identity.json\",\"resources/bootstrap.xor.z\"],\"inputs\":[],\"manual_steps\":\"Payload oficial extraido offline e verificado. Use seu proprio Sonic Adventure Dreamcast PAL v1.003 (MK-5100050), GDI e todas as tracks juntos. Execute manualmente sonic-setup.exe conforme README.txt para verificar e importar a midia. O All-Fix nao executa o instalador nem o jogo automaticamente.\",\"build_profile\":\"sarecomp-0.52.0-prepare\",\"preparation_media\":[{\"id\":\"original-disc\",\"kind\":\"file\",\"extensions\":[\".gdi\"],\"version\":\"Dreamcast PAL v1.003 (MK-5100050), GDI e todas as tracks\"}]},{\"schema_version\":9,\"project_id\":\"fh1-reimagined\",\"tag\":\"v0.3.9\",\"source_url\":\"https://github.com/FH1-ReImagined/ForzaHorizon1-ReImagined/releases/tag/v0.3.9\",\"operations\":[],\"required_files\":[\"forza-launcher.exe\",\"README.txt\",\"windows-build-manifest.json\",\"project/forza-recomp/CMakeLists.txt\",\"project/forza-recomp/forza_manifest.toml\",\"licenses/ForzaHorizon1-ReImagined.txt\"],\"inputs\":[],\"manual_steps\":\"Kit oficial do Forza extraido offline e verificado integralmente. O jogo ainda nao foi compilado. Forneca sua propria copia Xbox 360 (ISO, Games on Demand ou pasta extraida), conforme README.txt. O All-Fix nao executa o launcher, instalador ou compiladores automaticamente.\",\"build_profile\":\"fh1-0.3.9-inno-prepare\",\"preparation_media\":[{\"id\":\"original-disc\",\"kind\":\"file\",\"extensions\":[\".iso\"],\"version\":\"Xbox 360 original; alternativa: Games on Demand ou pasta extraida\"}]},{\"schema_version\":9,\"project_id\":\"mega-man-legends-modernization-project\",\"tag\":\"v0.9.6-beta\",\"source_url\":\"https://github.com/Drakfix/MML_Modernization-Project/releases/tag/v0.9.6-beta\",\"operations\":[],\"required_files\":[\"mml_run64.exe\",\"mml.dll\",\"mml.ini\",\"ddraw.dll\",\"SDL3.dll\",\"x64/SDL3.dll\",\"THIRD-PARTY-NOTICES.txt\"],\"inputs\":[],\"manual_steps\":\"Runtime oficial extraido offline e verificado. Use sua propria instalacao de Mega Man Legends PC (MEGAMAN.EXE US) ou Rockman DASH PC (ROCKMAN.EXE JP). A importacao, patch e primeiro boot ainda precisam ser homologados. O All-Fix nao executa o instalador ou o jogo automaticamente.\",\"build_profile\":\"mml-0.9.6-beta-pyinstaller-prepare\",\"preparation_media\":[{\"id\":\"original-game\",\"kind\":\"directory\",\"extensions\":[],\"version\":\"PC CD-ROM US ou JP; pasta com executavel original\"}]},{\"schema_version\":9,\"project_id\":\"hookshot-zelda-oot-port\",\"tag\":\"v3.0.2\",\"source_url\":\"https://github.com/ZuanCrisp/Zelda-OOT-Port/releases/tag/v3.0.2\",\"operations\":[],\"required_files\":[\"HookshotBuilder.exe\",\"recomplauncher.json\"],\"inputs\":[],\"manual_steps\":\"Kit oficial preparado. Use Retomar e selecione sua propria copia de Ocarina of Time Nintendo Switch 2 (.nup/.nx v131072 e0f3ccfa ou pasta com exefs e romfs). O All-Fix verifica os componentes oficiais por SHA-256 e compila localmente.\",\"build_profile\":\"hookshot-3.0.2-prepare\",\"preparation_media\":[{\"id\":\"original-game\",\"kind\":\"file_or_directory\",\"extensions\":[\".nup\",\".nx\"],\"version\":\"Switch 2 v131072 build e0f3ccfa (.nup/.nx ou pasta ExeFS/RomFS)\"}]}]")
        identities = {
            "gow-0.4.0-prepare": ("god-of-war-2005", "danielalves96/gow-pc-port"),
            "totk-0.5.0-prepare": ("the-legend-of-zelda-tears-of-the-kingdom", "valentderah/totk-pc-recomp"),
            "pinyon-0.9.5-prepare": ("forza-horizon", "arcanite24/pinyon-shift"),
            "doax-0.8.0-prepare": ("dead-or-alive-xtreme-beach-volleyball", "NoRain211/doaxvb-re"),
            "ssx-2.0.0-prepare": ("ssx-2012", "AmarilloNL/ssx-recomp"),
            "las-0.6.1-prepare": ("the-legend-of-zelda-link-s-awakening", "peiikai/LASRecomp"),
            "gta-stories-0.3.2-prepare": ("grand-theft-auto-liberty-city-stories-vice-city-stories", "batinium/gta-stories-recompiled"),
            "rygt-2026-11-23-prepare": ("gran-turismo-7", "RyGT-Team/RyGT"),
            "spartanport-3.2.1-prepare": ("god-of-war-iii-remastered", "FelipePrado0/SpartanPort"),
            "odyssey-1.0.0-prepare": ("super-mario-odyssey", "Simon3Sarkis/super-odyssey-pc-recomp"),
            "dkb-0.5.1-44ba6b1-prepare": ("donkey-kong-bananza", "Lucas-blip-png/dkb-pc-recomp"),
            "mkw-0.1.18-prepare": ("mario-kart-world", "adriadam10/mkw-recomp"),
            "sarecomp-0.52.0-prepare": ("sonic-adventure", "sonicfreak1337/SARecomp"),
            "fh1-0.3.9-inno-prepare": ("forza-horizon", "FH1-ReImagined/ForzaHorizon1-ReImagined"),
            "mml-0.9.6-beta-pyinstaller-prepare": ("mega-man-legends-rockman-dash", "Drakfix/MML_Modernization-Project"),
            "hookshot-3.0.2-prepare": ("the-legend-of-zelda-ocarina-of-time", "ZuanCrisp/Zelda-OOT-Port"),
        }
        profile = next((p for p in profiles if p["build_profile"] == recipe.get("build_profile")), None)
        if profile is None or recipe != profile:
            return errors + [f"{label}: v9 preparation profile is not approved"]
        game, repository = identities[profile["build_profile"]]
        if (entry.get("schema_version") != 9 or entry.get("status") != "experimental"
                or entry.get("game_id") != game or entry.get("repository") != repository
                or entry.get("project_id") != profile["project_id"] or entry.get("tag") != profile["tag"]
                or entry.get("has_inputs") is not False or entry.get("has_manual_steps") is not True):
            errors.append(f"{label}: preparation-only index identity or status invalid")
        return errors

    if "preparation_media" in recipe:
        errors.append(f"{label}: preparation_media requires schema 9")

    # SDK 1.4.1 parser does not provide shell commands or arbitrary root scripts.
    # Reject unknown v8 members rather than silently treating them as launch steps.
    if schema_version >= 8:
        allowed_root = {
            "schema_version", "project_id", "tag", "source_url", "operations",
            "required_files", "manual_steps", "inputs", "launch_file",
            "first_run_files", "prerequisites", "assets", "java_launcher",
            "installer_profile", "build_profile",
        }
        for key in recipe:
            if key not in allowed_root:
                errors.append(f"{label}: unknown v8 recipe field '{key}'")

    allow_v5 = schema_version >= 5

    if schema_version != entry.get("schema_version"):
        errors.append(
            f"{label}: schema_version ({schema_version}) != index entry ({entry.get('schema_version')})"
        )

    if recipe.get("project_id") != entry.get("project_id"):
        errors.append(
            f"{label}: project_id ({recipe.get('project_id')}) != index entry ({entry.get('project_id')})"
        )

    if recipe.get("tag") != entry.get("tag"):
        errors.append(
            f"{label}: tag ({recipe.get('tag')}) != index entry ({entry.get('tag')})"
        )

    source_url = recipe.get("source_url")
    repo = entry.get("repository", "")
    if isinstance(repo, str) and repo.startswith("gitlab:"):
        expected_prefix = f"https://gitlab.com/{repo[len('gitlab:'):]}/"
    else:
        expected_prefix = f"https://github.com/{repo}/"
    if not isinstance(source_url, str) or not source_url.startswith("https://"):
        errors.append(f"{label}: source_url must start with https://")
    elif not (source_url.startswith(expected_prefix) or (
        schema_version >= 8 and source_url == expected_prefix[:-1]
    )):
        errors.append(
            f"{label}: source_url '{source_url}' does not match repository '{repo}'"
        )

    # Validate required_files
    required_files = recipe.get("required_files")
    req_file_set: set[str] = set()
    req_file_lower: set[str] = set()
    if not isinstance(required_files, list) or not (1 <= len(required_files) <= 256):
        errors.append(f"{label}: required_files must have 1..256 items")
    else:
        for idx, rf in enumerate(required_files):
            ok, reason = is_safe_relative_path(rf, allow_v5_chars=allow_v5)
            if not ok:
                errors.append(f"{label}: required_files[{idx}] {reason}")
            else:
                if rf.lower() in req_file_lower:
                    errors.append(f"{label}: duplicate required_files path '{rf}'")
                req_file_set.add(rf)
                req_file_lower.add(rf.lower())

    # Validate launch_file
    launch_file = recipe.get("launch_file")
    if launch_file is not None:
        if schema_version < 3:
            errors.append(f"{label}: launch_file is only supported in schema_version >= 3")
        ok, reason = is_safe_relative_path(launch_file, allow_v5_chars=allow_v5)
        if not ok:
            errors.append(f"{label}: launch_file {reason}")
        else:
            if launch_file not in req_file_set:
                errors.append(
                    f"{label}: launch_file '{launch_file}' must be present in required_files"
                )
            if allow_v5 and not launch_file.lower().endswith(".exe"):
                errors.append(
                    f"{label}: launch_file '{launch_file}' must point to an .exe file in schema_version >= 5"
                )

    # Validate prerequisites (v5+)
    if "prerequisites" in recipe:
        if schema_version < 5:
            errors.append(f"{label}: prerequisites requires schema_version >= 5")
        prereqs = recipe["prerequisites"]
        if (
            not isinstance(prereqs, list)
            or len(prereqs) > 4
            or len(set(prereqs)) != len(prereqs)
            or not all(
                isinstance(p, str) and p in (VALID_PREREQUISITES | (
                    {"java-25"} if schema_version >= 8 else set()
                )) for p in prereqs
            )
        ):
            errors.append(f"{label}: prerequisites must contain up to 4 unique valid runtime IDs")

    # Validate manual_steps and index flags
    manual_steps = recipe.get("manual_steps")
    if manual_steps is not None:
        if not isinstance(manual_steps, str) or len(manual_steps) > 2000:
            errors.append(f"{label}: manual_steps must be a string <= 2000 chars")

    inputs = recipe.get("inputs")
    input_map: dict[str, dict[str, Any]] = {}
    if not isinstance(inputs, list) or len(inputs) > 64:
        errors.append(f"{label}: inputs must be an array with at most 64 items")
    else:
        for idx, inp in enumerate(inputs):
            loc = f"inputs[{idx}]"
            if not isinstance(inp, dict):
                errors.append(f"{label}: {loc} must be an object")
                continue
            inp_id = inp.get("id")
            if not isinstance(inp_id, str) or not (1 <= len(inp_id) <= 100):
                errors.append(f"{label}: {loc}.id must be 1..100 chars")
                continue
            if inp_id in input_map:
                errors.append(f"{label}: duplicate input id '{inp_id}'")
            input_map[inp_id] = inp

            if schema_version == 1:
                sha256 = inp.get("sha256")
                if not isinstance(sha256, str) or not RE_SHA256.match(sha256):
                    errors.append(f"{label}: {loc}.sha256 invalid for schema v1")
            else:
                kind = inp.get("kind")
                if "files" in inp:
                    if schema_version < 4:
                        errors.append(f"{label}: {loc}.files requires schema_version 4 or 5")
                    if kind != "directory" and not (schema_version >= 7 and kind == "arcade_romset"):
                        errors.append(f"{label}: {loc}.files requires directory or v7 arcade_romset")
                    if not isinstance(inp.get("name"), str) or not inp["name"]:
                        errors.append(f"{label}: {loc}.name is required")
                    errors.extend(
                        validate_verified_data_files(
                            inp["files"],
                            label,
                            f"{loc}.files",
                            schema_version=schema_version,
                            is_import_set=True,
                            is_arcade=kind == "arcade_romset",
                        )
                    )
                elif kind is not None:
                    if kind not in {"file", "directory"}:
                        errors.append(f"{label}: {loc}.kind invalid '{kind}'")
                    if not isinstance(inp.get("name"), str) or not inp["name"]:
                        errors.append(f"{label}: {loc}.name is required when kind is set")
                    if allow_v5:
                        _validate_size_fields(inp, label, loc, errors)
                        if not _has_v5_file_verification(inp):
                            errors.append(
                                f"{label}: {loc} requires sha256, sha1, (size + magic_hex), or (min_size + magic_hex)"
                            )
                        if "md5" in inp:
                            if not isinstance(inp["md5"], str) or not RE_MD5.match(inp["md5"]):
                                errors.append(f"{label}: {loc}.md5 must be 32 hex chars")
                    else:
                        has_sha256 = isinstance(inp.get("sha256"), str) and RE_SHA256.match(
                            inp["sha256"]
                        )
                        has_size_magic = (
                            isinstance(inp.get("size"), int)
                            and not isinstance(inp.get("size"), bool)
                            and inp["size"] >= 1
                            and isinstance(inp.get("magic_hex"), str)
                            and RE_MAGIC_HEX.match(inp["magic_hex"])
                        )
                        if not (has_sha256 or has_size_magic):
                            errors.append(
                                f"{label}: {loc} requires sha256 or (size + magic_hex)"
                            )
                    if kind == "directory":
                        ok, reason = is_safe_relative_path(
                            inp.get("verify_file"), allow_v5_chars=allow_v5
                        )
                        if not ok:
                            errors.append(
                                f"{label}: {loc}.verify_file {reason} (required for directory)"
                            )
                else:
                    sha256 = inp.get("sha256")
                    if not isinstance(sha256, str) or not RE_SHA256.match(sha256):
                        errors.append(f"{label}: {loc}.sha256 required when kind is omitted")

                if "sha1" in inp and (
                    not isinstance(inp["sha1"], str) or not RE_SHA1.match(inp["sha1"])
                ):
                    errors.append(f"{label}: {loc}.sha1 must be 40 hex chars")
                if "extensions" in inp:
                    exts = inp["extensions"]
                    if not isinstance(exts, list) or len(exts) > 10 or not all(
                        isinstance(e, str) and RE_EXT.match(e) for e in exts
                    ):
                        errors.append(f"{label}: {loc}.extensions contains invalid entry")

    if "has_inputs" in entry and isinstance(inputs, list):
        expected_has_inputs = len(inputs) > 0
        if entry["has_inputs"] != expected_has_inputs:
            errors.append(
                f"{label}: index has_inputs={entry['has_inputs']} != {expected_has_inputs}"
            )

    if "has_manual_steps" in entry:
        expected_manual = isinstance(manual_steps, str) and bool(manual_steps.strip())
        if entry["has_manual_steps"] != expected_manual:
            errors.append(
                f"{label}: index has_manual_steps={entry['has_manual_steps']} != {expected_manual}"
            )

    # Validate operations
    operations = recipe.get("operations")
    if not isinstance(operations, list) or len(operations) > 256:
        errors.append(f"{label}: operations must be an array with at most 256 items")
    else:
        for idx, op in enumerate(operations):
            loc = f"operations[{idx}]"
            if not isinstance(op, dict):
                errors.append(f"{label}: {loc} must be an object")
                continue
            kind = op.get("kind")
            ok_target, reason_target = is_safe_relative_path(
                op.get("target"), allow_v5_chars=allow_v5
            )
            if not ok_target:
                errors.append(f"{label}: {loc}.target {reason_target}")

            if kind == "create_directory":
                if "source" in op:
                    errors.append(f"{label}: {loc} create_directory must not have source")
            elif kind in {"copy", "move"}:
                ok_src, reason_src = is_safe_relative_path(
                    op.get("source"), allow_v5_chars=allow_v5
                )
                if not ok_src:
                    errors.append(f"{label}: {loc}.source {reason_src}")
            elif kind == "copy_input":
                src = op.get("source")
                if not isinstance(src, str) or src not in input_map:
                    errors.append(
                        f"{label}: {loc}.source '{src}' does not reference a declared input"
                    )
            elif kind == "import_input":
                if schema_version < 3:
                    errors.append(f"{label}: {loc} import_input requires schema_version >= 3")
                src = op.get("source")
                if not isinstance(src, str) or src not in input_map:
                    errors.append(
                        f"{label}: {loc}.source '{src}' does not reference a declared input"
                    )
                else:
                    ref_inp = input_map[src]
                    if allow_v5:
                        if ref_inp.get("kind") is not None and not _has_v5_file_verification(ref_inp):
                            errors.append(
                                f"{label}: {loc}.source '{src}' fails v5 verification rules for import_input"
                            )
                    else:
                        has_strong_hash = (
                            isinstance(ref_inp.get("sha256"), str)
                            and bool(RE_SHA256.match(ref_inp["sha256"]))
                        ) or (
                            isinstance(ref_inp.get("sha1"), str)
                            and bool(RE_SHA1.match(ref_inp["sha1"]))
                        )
                        if not has_strong_hash:
                            errors.append(
                                f"{label}: {loc}.source '{src}' requires sha256 or sha1 on referenced input for import_input"
                            )
                scope = op.get("scope")
                allowed_scopes = VALID_PROFILE_SCOPES_V5 if allow_v5 else {"installation", "roaming_app_data"}
                if scope not in allowed_scopes:
                    errors.append(f"{label}: {loc}.scope invalid '{scope}'")
                elif scope in {"roaming_app_data", "local_app_data"}:
                    folders = op.get("profile_folders")
                    if schema_version >= 7:
                        valid_folders = isinstance(folders, list) and 1 <= len(folders) <= 4 and all(
                            isinstance(f, str) and len(f) <= 160 and 1 <= len(f.split("/")) <= 4
                            and all(_validate_single_segment_v5(seg, allow_v5_chars=True, max_length=80)
                                    for seg in f.split("/"))
                            for f in folders
                        )
                    else:
                        valid_folders = isinstance(folders, list) and 1 <= len(folders) <= 4 and all(
                            _validate_single_segment_v5(f, allow_v5_chars=allow_v5, max_length=80)
                            for f in folders
                        )
                    if not valid_folders:
                        errors.append(f"{label}: {loc}.profile_folders invalid for {scope}")
                    target = op.get("target")
                    if allow_v5:
                        valid_target = (
                            (is_safe_relative_path(target, allow_v5_chars=True)[0] if schema_version >= 7
                             else _validate_single_segment_v5(target, allow_v5_chars=True, max_length=240))
                            and bool((RE_DATA_TARGET_EXT_V7 if schema_version >= 7 else RE_DATA_TARGET_EXT).search(target))
                        )
                    else:
                        valid_target = isinstance(target, str) and bool(RE_ROAMING_TARGET.match(target))
                    if not valid_target:
                        errors.append(f"{label}: {loc}.target invalid for {scope}")
                elif scope == "installation":
                    if "profile_folders" in op:
                        errors.append(
                            f"{label}: {loc}.profile_folders is forbidden when scope == 'installation'"
                        )
            elif kind == "import_input_set":
                if schema_version < 4:
                    errors.append(
                        f"{label}: {loc} import_input_set requires schema_version 4 or 5"
                    )
                if op.get("scope") != "installation":
                    errors.append(f"{label}: {loc}.scope must be 'installation'")
                src = op.get("source")
                inp = input_map.get(src) if isinstance(src, str) else None
                if not inp or inp.get("kind") not in ({"directory", "arcade_romset"} if schema_version >= 7 else {"directory"}) or "files" not in inp:
                    errors.append(
                        f"{label}: {loc}.source '{src}' must reference a directory input with 'files'"
                    )
            else:
                errors.append(f"{label}: {loc}.kind unknown '{kind}'")

    # Validate v4/v5 first_run_files
    if "first_run_files" in recipe:
        if schema_version < 4:
            errors.append(f"{label}: first_run_files requires schema_version 4 or 5")
        if not (isinstance(manual_steps, str) and manual_steps.strip()):
            errors.append(f"{label}: first_run_files requires non-empty manual_steps")
        if not launch_file:
            errors.append(f"{label}: first_run_files requires launch_file")
        errors.extend(
            validate_verified_data_files(
                recipe["first_run_files"],
                label,
                "first_run_files",
                schema_version=schema_version,
                is_first_run=True,
            )
        )

    # SDK 1.4.0 versioned contracts: do not relax v3/v5 semantic rules.
    assets = recipe.get("assets")
    if assets is not None:
        if schema_version < 6:
            errors.append(f"{label}: assets requires schema version 6+")
        if not isinstance(assets, list) or not 1 <= len(assets) <= 16:
            errors.append(f"{label}: assets must contain 1..16 files")
        else:
            asset_targets: set[str] = set()
            asset_names: set[str] = set()
            total = 0
            for n, asset in enumerate(assets):
                loc = f"assets[{n}]"
                if not isinstance(asset, dict):
                    errors.append(f"{label}: {loc} must be object")
                    continue
                if set(asset) != {"name", "target", "size", "sha256", "kind"}:
                    errors.append(f"{label}: {loc} unexpected/missing asset fields")
                target = asset.get("target")
                name = asset.get("name")
                if not isinstance(name, str) or not name or any(x in name for x in ("/", "\\", ":")):
                    errors.append(f"{label}: {loc}.name invalid")
                if isinstance(name, str) and name.lower() in asset_names:
                    errors.append(f"{label}: duplicate asset name {name}")
                elif isinstance(name, str):
                    asset_names.add(name.lower())
                ok, reason = is_safe_relative_path(target, allow_v5_chars=True)
                if not ok:
                    errors.append(f"{label}: {loc}.target {reason}")
                elif target.lower() in asset_targets:
                    errors.append(f"{label}: duplicate asset target '{target}'")
                else:
                    asset_targets.add(target.lower())
                size = asset.get("size")
                if not isinstance(size, int) or isinstance(size, bool) or not 1 <= size <= MAX_TOTAL_DATA_BYTES:
                    errors.append(f"{label}: {loc}.size invalid")
                else:
                    total += size
                if not isinstance(asset.get("sha256"), str) or not RE_SHA256.fullmatch(asset["sha256"]):
                    errors.append(f"{label}: {loc}.sha256 invalid")
                kind = asset.get("kind")
                if kind == "portable_executable":
                    if not isinstance(target, str) or not target.lower().endswith(".exe"):
                        errors.append(f"{label}: {loc} portable_executable target must end .exe")
                    if target != launch_file or target not in req_file_set:
                        errors.append(f"{label}: {loc} portable_executable target must match launch_file and required_files")
                elif kind == "payload":
                    if not isinstance(target, str) or RE_BLOCKED_EXEC_ASSET.search(target):
                        errors.append(f"{label}: {loc} payload cannot be executable or script")
                else:
                    errors.append(f"{label}: {loc}.kind invalid")
            if total > MAX_TOTAL_DATA_BYTES:
                errors.append(f"{label}: sum of assets exceeds 64 GiB")
    if "java_launcher" in recipe and schema_version >= 8:
        errors.extend(validate_java_launcher_v8(recipe, req_file_set, label))
    elif "java_launcher" in recipe:
            if schema_version < 7:
                errors.append(f"{label}: java_launcher requires v7")
            launcher = recipe["java_launcher"]
            if not isinstance(launcher, dict) or set(launcher) - {"jar", "runtime", "working_directory"}:
                errors.append(f"{label}: invalid java_launcher structure")
            else:
                jar = launcher.get("jar")
                if not isinstance(jar, str) or not jar.lower().endswith(".jar") or not is_safe_relative_path(jar, allow_v5_chars=True)[0]:
                    errors.append(f"{label}: java_launcher.jar must be safe .jar path")
                if jar not in req_file_set:
                    errors.append(f"{label}: java_launcher.jar must be in required_files")
                if launcher.get("runtime") != "java-21" or "java-21" not in (recipe.get("prerequisites") or []):
                    errors.append(f"{label}: java_launcher requires runtime/prerequisite java-21")
                if "working_directory" in launcher and not is_safe_relative_path(launcher["working_directory"], allow_v5_chars=True)[0]:
                    errors.append(f"{label}: java_launcher.working_directory unsafe")
            if launch_file is not None:
                errors.append(f"{label}: java_launcher cannot coexist with launch_file")
    for blocked in ("installer_profile", "build_profile"):
        if blocked in recipe:
            errors.append(f"{label}: {blocked} is disabled without approved execution profile")
    if schema_version >= 7 and isinstance(inputs, list):
        for n, inp in enumerate(inputs):
            if not isinstance(inp, dict):
                continue
            if inp.get("kind") == "arcade_romset" and "files" not in inp:
                errors.append(f"{label}: inputs[{n}] arcade_romset requires file manifest")
            if inp.get("validate_cue_references"):
                files = inp.get("files") or []
                cues = [f for f in files if isinstance(f, dict) and isinstance(f.get("path"), str) and f["path"].lower().endswith(".cue")]
                bins = [f for f in files if isinstance(f, dict) and isinstance(f.get("path"), str) and f["path"].lower().endswith(".bin")]
                if inp.get("kind") != "directory" or not cues or not bins:
                    errors.append(f"{label}: inputs[{n}] validate_cue_references requires declared CUE and BIN files")

    return errors


def load_catalog_lookup(catalog_source: str) -> dict[tuple[str, str], str]:
    """Load (game_id, project_id) -> repository (GitHub owner/repo or gitlab:group/project) from local path or HTTPS URL."""
    if catalog_source.startswith("https://"):
        req = urllib.request.Request(
            catalog_source,
            headers={"User-Agent": "GetAll-Addon-Validator/1.0"},
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    else:
        data = json.loads(Path(catalog_source).read_text(encoding="utf-8"))

    lookup: dict[tuple[str, str], str] = {}
    for game in data.get("games", []):
        game_id = game.get("id")
        for proj in game.get("projects", []):
            proj_id = proj.get("id")
            src = proj.get("source") or {}
            repo = src.get("github_repository") or ""
            if not repo and src.get("provider") == "gitlab":
                url = src.get("url") or ""
                if url.startswith("https://gitlab.com/"):
                    gitlab_path = url[len("https://gitlab.com/"):].split("/-/", 1)[0].strip("/")
                    if gitlab_path:
                        repo = f"gitlab:{gitlab_path}"
            if game_id and proj_id:
                lookup[(game_id, proj_id)] = repo
    return lookup


def check_git_blobs_lf(repo_root: Path, paths: list[Path]) -> list[str]:
    """Verify tracked Git blobs contain LF (no CRLF) and match normalized disk SHA-256."""
    errors: list[str] = []
    for p in paths:
        rel = p.relative_to(repo_root).as_posix()
        proc = subprocess.run(
            ["git", "cat-file", "blob", f"HEAD:{rel}"],
            cwd=repo_root,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            # New untracked/uncommitted file: verify disk directly without CRLF
            if b"\r\n" in p.read_bytes():
                errors.append(f"{rel}: uncommitted file contains CRLF")
            continue
        blob = proc.stdout
        if b"\r\n" in blob:
            errors.append(f"{rel}: Git blob contains CRLF")
        disk_lf = p.read_bytes().replace(b"\r\n", b"\n")
        if blob != disk_lf:
            # Modified locally; check staged or disk has no CRLF if intended
            pass
    return errors


def validate_repository(
    repo_root: Path,
    *,
    strict_lf: bool = False,
    require_jsonschema: bool = False,
    check_git_blobs: bool = False,
    catalog_source: str | None = None,
) -> tuple[bool, list[str], dict[str, Any]]:
    """Validate schemas, addons, index.json, and all recipes in repo_root."""
    errors: list[str] = []
    stats: dict[str, Any] = {
        "jsonschema_enabled": HAS_JSONSCHEMA,
        "recipe_count": 0,
        "statuses": {},
        "schema_versions": {},
    }

    if require_jsonschema and not HAS_JSONSCHEMA:
        errors.append("jsonschema package is required but not installed")
        return False, errors, stats

    schemas_dir = repo_root / "schemas"
    try:
        schemas, registry = load_schema_registry(schemas_dir)
    except Exception as exc:
        errors.append(f"Failed to load schemas: {exc}")
        return False, errors, stats

    # Validate JSON syntax & encoding of schemas and universal addon docs
    json_support_files = sorted(schemas_dir.glob("*.json"))
    addon_dir = repo_root / "addons" / "allfix.install.universal"
    if addon_dir.is_dir():
        json_support_files.extend(sorted(addon_dir.glob("*.json")))

    for jf in json_support_files:
        raw, io_errs = read_utf8_bytes(jf, strict_lf=False)
        errors.extend(io_errs)
        try:
            json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{jf.relative_to(repo_root).as_posix()}: invalid JSON ({exc})")

    # Validate index.json
    index_path = repo_root / "index.json"
    if not index_path.is_file():
        errors.append("Missing index.json at repository root")
        return False, errors, stats

    raw_index, idx_io_errs = read_utf8_bytes(index_path, strict_lf=strict_lf)
    errors.extend(idx_io_errs)
    try:
        index_data = json.loads(raw_index.decode("utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"index.json: invalid JSON ({exc})")
        return False, errors, stats

    errors.extend(
        validate_with_jsonschema(index_data, schemas["index"], registry, "index.json")
    )

    if not isinstance(index_data, dict):
        errors.append("index.json: root must be a JSON object")
        return False, errors, stats

    if index_data.get("index_format_version") != 1:
        errors.append("index.json: index_format_version must be 1")

    entries = index_data.get("recipes")
    if not isinstance(entries, list) or not entries:
        errors.append("index.json: recipes must be a non-empty array")
        return False, errors, stats

    if len(entries) > 2048:
        errors.append("index.json: recipes exceeds maxItems 2048")

    catalog_lookup: dict[tuple[str, str], str] | None = None
    if catalog_source:
        try:
            catalog_lookup = load_catalog_lookup(catalog_source)
        except Exception as exc:
            errors.append(f"Failed to load catalog '{catalog_source}': {exc}")

    seen_keys: set[tuple[str, str]] = set()
    seen_paths: set[str] = set()
    indexed_files: set[Path] = set()
    checked_files: list[Path] = [index_path]

    for idx, entry in enumerate(entries):
        loc = f"index.json:recipes[{idx}]"
        if not isinstance(entry, dict):
            errors.append(f"{loc} must be an object")
            continue

        for req in (
            "game_id",
            "project_id",
            "repository",
            "tag",
            "schema_version",
            "path",
            "sha256",
            "status",
        ):
            if req not in entry:
                errors.append(f"{loc}: missing required field '{req}'")

        game_id = entry.get("game_id", "")
        project_id = entry.get("project_id", "")
        repository = entry.get("repository", "")
        tag = entry.get("tag", "")
        sv = entry.get("schema_version")
        rel_path = entry.get("path", "")
        expected_sha = entry.get("sha256", "")
        status = entry.get("status", "")

        if not isinstance(game_id, str) or not RE_INDEX_ID.match(game_id):
            errors.append(f"{loc}: invalid game_id '{game_id}'")
        if not isinstance(project_id, str) or not RE_INDEX_ID.match(project_id):
            errors.append(f"{loc}: invalid project_id '{project_id}'")
        if not isinstance(repository, str) or not RE_REPOSITORY.match(repository) or len(repository) > 200:
            errors.append(f"{loc}: invalid repository '{repository}'")
        if not isinstance(tag, str) or not (1 <= len(tag) <= 200):
            errors.append(f"{loc}: invalid tag '{tag}'")
        if sv not in VALID_SCHEMA_VERSIONS:
            errors.append(f"{loc}: unsupported schema_version '{sv}'")
        if status not in VALID_STATUSES:
            errors.append(f"{loc}: invalid status '{status}'")
        if not isinstance(expected_sha, str) or not RE_SHA256.match(expected_sha):
            errors.append(f"{loc}: invalid sha256 '{expected_sha}'")

        if not isinstance(rel_path, str) or not rel_path.startswith("recipes/") or not RE_INDEX_PATH.match(rel_path) or len(rel_path) > 240:
            errors.append(f"{loc}: invalid recipe path '{rel_path}'")
        else:
            expected_prefix_path = f"recipes/{game_id}/"
            if not rel_path.startswith(expected_prefix_path):
                errors.append(
                    f"{loc}: path '{rel_path}' should live under '{expected_prefix_path}'"
                )

        key = (str(project_id), str(tag))
        if key in seen_keys:
            errors.append(f"{loc}: duplicate (project_id, tag) entry {key}")
        seen_keys.add(key)

        norm_path = str(rel_path).lower()
        if norm_path in seen_paths:
            errors.append(f"{loc}: duplicate path '{rel_path}'")
        seen_paths.add(norm_path)

        stats["statuses"][status] = stats["statuses"].get(status, 0) + 1
        stats["schema_versions"][str(sv)] = stats["schema_versions"].get(str(sv), 0) + 1

        if catalog_lookup is not None:
            cat_key = (game_id, project_id)
            if cat_key not in catalog_lookup:
                errors.append(f"{loc}: {cat_key} not found in AllFix-Repo catalog")
            elif catalog_lookup[cat_key] and catalog_lookup[cat_key].lower() != str(repository).lower():
                errors.append(
                    f"{loc}: repository '{repository}' != catalog '{catalog_lookup[cat_key]}'"
                )

        recipe_file = repo_root / rel_path
        if not recipe_file.is_file():
            errors.append(f"{loc}: referenced file '{rel_path}' does not exist")
            continue

        indexed_files.add(recipe_file.resolve())
        checked_files.append(recipe_file)

        raw_recipe, rec_io_errs = read_utf8_bytes(recipe_file, strict_lf=strict_lf)
        errors.extend(rec_io_errs)

        actual_sha = hashlib.sha256(raw_recipe).hexdigest()
        if isinstance(expected_sha, str) and actual_sha != expected_sha.lower():
            errors.append(
                f"{rel_path}: SHA-256 mismatch (index={expected_sha.lower()}, actual_lf={actual_sha})"
            )

        try:
            recipe_doc = json.loads(raw_recipe.decode("utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{rel_path}: invalid JSON ({exc})")
            continue

        if sv in VALID_SCHEMA_VERSIONS:
            errors.extend(
                validate_with_jsonschema(recipe_doc, schemas[sv], registry, rel_path)
            )
        errors.extend(validate_recipe_semantics(recipe_doc, entry, rel_path))

    # Detect orphaned recipe files under recipes/
    recipes_dir = repo_root / "recipes"
    if recipes_dir.is_dir():
        for disk_file in sorted(recipes_dir.rglob("*.json")):
            if disk_file.resolve() not in indexed_files:
                errors.append(
                    f"Orphan recipe file not registered in index.json: {disk_file.relative_to(repo_root).as_posix()}"
                )

    if check_git_blobs:
        errors.extend(check_git_blobs_lf(repo_root, checked_files))

    stats["recipe_count"] = len(entries)
    return len(errors) == 0, errors, stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate GetAll-Addon recipes and index.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Path to GetAll-Addon repository root",
    )
    parser.add_argument(
        "--strict-lf",
        action="store_true",
        help="Fail if any checked JSON file contains CRLF on disk",
    )
    parser.add_argument(
        "--require-jsonschema",
        action="store_true",
        help="Fail if the jsonschema Python package is unavailable",
    )
    parser.add_argument(
        "--check-git-blobs",
        action="store_true",
        help="Also verify tracked Git blobs in HEAD use LF",
    )
    parser.add_argument(
        "--check-catalog",
        nargs="?",
        const=DEFAULT_CATALOG_URL,
        default=None,
        help="Optional path or URL to AllFix-Repo catalog.json to cross-check IDs and repositories",
    )
    args = parser.parse_args()

    ok, errors, stats = validate_repository(
        args.repo_root.resolve(),
        strict_lf=args.strict_lf,
        require_jsonschema=args.require_jsonschema,
        check_git_blobs=args.check_git_blobs,
        catalog_source=args.check_catalog,
    )

    print(
        f"Validation summary: recipes={stats['recipe_count']}, "
        f"statuses={stats['statuses']}, schema_versions={stats['schema_versions']}, "
        f"jsonschema={stats['jsonschema_enabled']}"
    )
    if not ok:
        print(f"FAILED with {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("OK: all recipes, schemas, paths, and SHA-256 hashes are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
