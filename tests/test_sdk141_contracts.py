"""SDK 1.4.1 JSON Schema v8 and semantic contract tests, with synthetic inputs only."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_recipes as val  # noqa: E402


class Sdk141V8ContractsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas, cls.registry = val.load_schema_registry(ROOT / "schemas")

    @staticmethod
    def load(path: str) -> dict:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))

    def synthetic(self) -> dict:
        return self.load("examples/sdk141-synthetic/v8-java-classpath.synthetic.json")

    def official_candidate(self) -> dict:
        return self.load("recipes/the-legend-of-dragoon/severed-chains/release-3.0.0.json")

    def errors(self, recipe: dict, repository: str | None = None) -> list[str]:
        # The index and manifest require the real repo owner/name, not just the URL.
        url = urlsplit(recipe.get("source_url", ""))
        path = url.path.strip("/").split("/")
        repo = repository or "/".join(path[:2])
        entry = {
            "schema_version": recipe.get("schema_version"),
            "project_id": recipe.get("project_id"),
            "tag": recipe.get("tag"),
            "repository": repo,
            "has_inputs": bool(recipe.get("inputs")),
            "has_manual_steps": bool(recipe.get("manual_steps")),
        }
        # v7 handoff synthetic examples use a GitHub root URL, while the
        # pre-v8 GetAll validator expects a slash after the owner/repository.
        # Normalize only the fixture adapter, never the production recipe.
        semantic = copy.deepcopy(recipe)
        if recipe.get("schema_version", 0) < 8 and (
            semantic.get("source_url") == "https://github.com/" + repo
        ):
            semantic["source_url"] += "/"
        errors = val.validate_recipe_semantics(semantic, entry, "sdk141-test")
        version = recipe.get("schema_version")
        if val.HAS_JSONSCHEMA and version in self.schemas:
            validator = val.Draft202012Validator(
                self.schemas[version], registry=self.registry
            )
            errors.extend("jsonschema: " + err.message for err in validator.iter_errors(recipe))
        return errors

    def rejects(self, document: dict, mutations) -> None:
        for name, edit in mutations:
            with self.subTest(name=name):
                obj = copy.deepcopy(document)
                edit(obj)
                self.assertTrue(self.errors(obj), name)

    def test_v8_synthetic_classpath_accepted(self) -> None:
        self.assertEqual(self.errors(self.synthetic()), [])

    def test_real_severed_chains_96_jars_accepted_as_experimental(self) -> None:
        doc = self.official_candidate()
        self.assertEqual(self.errors(doc), [])
        java = doc["java_launcher"]
        self.assertEqual(java["runtime"], "java-25")
        self.assertEqual(java["main_class"], "legend.game.MainWindows")
        self.assertEqual(len(java["classpath"]), 96)
        self.assertEqual(java["classpath"], doc["required_files"])
        self.assertEqual(java["classpath"][0], java["jar"])
        self.assertEqual(java["program_arguments_profile"], "severed-chains-3")
        self.assertEqual(java["jvm_options"], val.SEVERED_CHAINS_JVM_OPTIONS)
        self.assertTrue(doc["manual_steps"])
        self.assertFalse(doc["inputs"])
        index = self.load("index.json")
        entry = next(e for e in index["recipes"] if e["project_id"] == "severed-chains")
        self.assertEqual(entry["status"], "experimental")
        self.assertEqual(entry["schema_version"], 8)
        self.assertEqual(entry["repository"], "Legend-of-Dragoon-Modding/Severed-Chains")
        self.assertGreaterEqual(len(index["recipes"]), 94)

    def test_classpath_paths_are_safe_declared_jars(self) -> None:
        original = self.synthetic()
        self.rejects(original, [
            ("missing-classpath", lambda d: d["java_launcher"].pop("classpath")),
            ("empty-classpath", lambda d: d["java_launcher"].update(classpath=[])),
            ("string-classpath", lambda d: d["java_launcher"].update(classpath="app/game.jar")),
            ("too-many", lambda d: d["java_launcher"].update(classpath=["app/game.jar"] + [f"libs/lib{i}.jar" for i in range(128)])),
            ("duplicate", lambda d: d["java_launcher"]["classpath"].append("app/libs/core.jar")),
            ("duplicate-casefold", lambda d: d["java_launcher"]["classpath"].append("APP/LIBS/CORE.JAR")),
            ("not-declared", lambda d: d["java_launcher"]["classpath"].append("app/unknown.jar")),
            ("primary-missing", lambda d: d["java_launcher"].update(classpath=["app/libs/core.jar"])),
            ("traversal", lambda d: d["java_launcher"]["classpath"].append("../outside.jar")),
            ("absolute", lambda d: d["java_launcher"]["classpath"].append("C:/outside.jar")),
            ("uri", lambda d: d["java_launcher"]["classpath"].append("https://evil.org/x.jar")),
            ("wildcard", lambda d: d["java_launcher"]["classpath"].append("libs/*.jar")),
            ("not-jar", lambda d: d["java_launcher"]["classpath"].append("app/readme.exe")),
            ("command-injection", lambda d: d["java_launcher"]["classpath"].append("app/test.jar;cmd")),
            ("jar-unknown", lambda d: d["java_launcher"].update(jar="app/unknown.jar")),
            ("jar-script", lambda d: d["java_launcher"].update(jar="launch.bat")),
            ("working-dir-traversal", lambda d: d["java_launcher"].update(working_directory="../..")),
        ])

    def test_jvm_options_and_class_injection_rejected(self) -> None:
        self.rejects(self.synthetic(), [
            ("main-simple", lambda d: d["java_launcher"].update(main_class="Main")),
            ("main-injection", lambda d: d["java_launcher"].update(main_class="test.Main;cmd")),
            ("main-spaces", lambda d: d["java_launcher"].update(main_class="test. Main")),
            ("main-too-long", lambda d: d["java_launcher"].update(main_class="test." + "A"*181)),
            ("main-empty", lambda d: d["java_launcher"].update(main_class="")),
            ("arbitrary-jvm", lambda d: d["java_launcher"].update(jvm_options=["-javaagent:x.jar"])),
            ("java-options", lambda d: d["java_launcher"].update(jvm_options=["@evil"])),
            ("duplicate-options", lambda d: d["java_launcher"].update(jvm_options=["joml-fma","joml-fma"])),
            ("unknown-launch-arguments", lambda d: d["java_launcher"].update(arguments=["-jar","bad.jar"])),
            ("script-field", lambda d: d.update(command="powershell -c Invoke-WebRequest ...")),
            ("extra-shell", lambda d: d["java_launcher"].update(shell="cmd.exe")),
            ("profile-arbitrary", lambda d: d["java_launcher"].update(program_arguments_profile="--debug")),
        ])

    def test_severed_chains_approved_profile_must_match_all_constraints(self) -> None:
        original = self.official_candidate()
        self.rejects(original, [
            ("foreign-project", lambda d: d.update(project_id="other-java-game")),
            ("wrong-source", lambda d: d.update(source_url="https://github.com/Legend-of-Dragoon-Modding/Severed-Chains/releases/tag/release-3.0.0")),
            ("wrong-class", lambda d: d["java_launcher"].update(main_class="legend.game.Main")),
            ("wrong-runtime", lambda d: d["java_launcher"].update(runtime="java-21")),
            ("wrong-prerequisite", lambda d: d.update(prerequisites=["java-21"])),
            ("omitted-options", lambda d: d["java_launcher"].pop("jvm_options")),
            ("missing-required-option", lambda d: d["java_launcher"].update(jvm_options=d["java_launcher"]["jvm_options"][:-1])),
            ("reordered-options", lambda d: d["java_launcher"].update(jvm_options=list(reversed(d["java_launcher"]["jvm_options"])))),
            ("extra-proprietary-arg", lambda d: d["java_launcher"].update(program_arguments_profile="-Xmx999G")),
        ])

    def test_classpath_mode_requires_main_class(self) -> None:
        original = self.synthetic()
        self.rejects(original, [
            ("missing-main", lambda d: d["java_launcher"].pop("main_class")),
            ("null-main", lambda d: d["java_launcher"].update(main_class=None)),
            ("missing-runtime", lambda d: d["java_launcher"].pop("runtime")),
            ("unknown-runtime", lambda d: d["java_launcher"].update(runtime="java-26")),
            ("missing-prerequisites", lambda d: d.update(prerequisites=[])),
            ("with-exe", lambda d: d.update(launch_file="game.exe")),
        ])

    def test_v7_keeps_old_java21_contract_and_rejects_v8_fields(self) -> None:
        old = self.load("examples/sdk14-synthetic/v7-java.synthetic.json")
        self.assertEqual(self.errors(old), [])
        mutations = [
            ("java25-v7", lambda d: d["java_launcher"].update(runtime="java-25")),
            ("java25-prereq-v7", lambda d: d.update(prerequisites=["java-25"])),
            ("main-class-v7", lambda d: d["java_launcher"].update(main_class="synthetic.game.Main")),
            ("classpath-v7", lambda d: d["java_launcher"].update(classpath=["app/game.jar"])),
            ("flags-v7", lambda d: d["java_launcher"].update(jvm_options=["joml-fastmath"])),
        ]
        self.rejects(old, mutations)

    def test_v8_legacy_jar_launch_mode_accepts_java21_or_25(self) -> None:
        doc = self.synthetic()
        for runtime in ("java-21", "java-25"):
            with self.subTest(runtime=runtime):
                java = doc["java_launcher"]
                doc["java_launcher"] = {
                    "jar": java["jar"], "runtime": runtime,
                    "working_directory": java["working_directory"],
                }
                doc["prerequisites"] = [runtime]
                self.assertEqual(self.errors(doc), [])

    def test_v8_disallows_unapproved_installer_or_build_profiles(self) -> None:
        self.rejects(self.synthetic(), [
            ("installer", lambda d: d.update(installer_profile="native-exe")),
            ("build", lambda d: d.update(build_profile="powershell")),
        ])


if __name__ == "__main__":
    unittest.main()
