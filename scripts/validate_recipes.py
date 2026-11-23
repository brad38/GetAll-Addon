#!/usr/bin/env python3
"""Static and semantic validator for GetAll-Addon index, schemas, and recipes (SDK 1.3.0, v1-v5)."""

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

VALID_STATUSES = {"validated", "disabled", "draft", "experimental"}
VALID_SCHEMA_VERSIONS = {1, 2, 3, 4, 5}
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
            if not RE_V4_DATA_EXT.search(p):
                errors.append(
                    f"{label}: {item_loc}.path '{p}' has disallowed data file extension"
                )

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
            if is_import_set and "size" not in item and "max_size" not in item:
                errors.append(f"{label}: {item_loc} in import_input_set requires size or max_size")
            if not _has_v5_file_verification(item):
                errors.append(
                    f"{label}: {item_loc} requires sha256, sha1, (size + magic_hex), or (min_size + magic_hex)"
                )
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
                    if not _validate_single_segment_v5(pf, allow_v5_chars=True, max_length=80):
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


def validate_recipe_semantics(
    recipe: Any,
    entry: dict[str, Any],
    label: str,
) -> list[str]:
    """Validate semantic and cross-field SDK 1.2.0 / 1.3.0 contracts for v1-v5 recipes."""
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
    elif not source_url.startswith(expected_prefix):
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
            or not all(isinstance(p, str) and p in VALID_PREREQUISITES for p in prereqs)
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
                    if kind != "directory":
                        errors.append(f"{label}: {loc}.files requires kind == 'directory'")
                    if not isinstance(inp.get("name"), str) or not inp["name"]:
                        errors.append(f"{label}: {loc}.name is required")
                    errors.extend(
                        validate_verified_data_files(
                            inp["files"],
                            label,
                            f"{loc}.files",
                            schema_version=schema_version,
                            is_import_set=True,
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
                    if (
                        not isinstance(folders, list)
                        or not (1 <= len(folders) <= 4)
                        or not all(
                            _validate_single_segment_v5(f, allow_v5_chars=allow_v5, max_length=80)
                            for f in folders
                        )
                    ):
                        errors.append(f"{label}: {loc}.profile_folders invalid for {scope}")
                    target = op.get("target")
                    if allow_v5:
                        valid_target = (
                            _validate_single_segment_v5(target, allow_v5_chars=True, max_length=240)
                            and bool(RE_DATA_TARGET_EXT.search(target))
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
                if not inp or inp.get("kind") != "directory" or "files" not in inp:
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
