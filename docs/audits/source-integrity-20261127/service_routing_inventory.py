#!/usr/bin/env python3
"""Reproduce the manually reviewed route ledger, checking every source locator.

Route decisions below were made by reading dispatch/handler bodies, not inferred
from a filename or the absence of .patch. This script checks coverage and links.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
DESKTOP = OUT.parents[3] / 'audit-desktop-source'
PIN = '921295de12349e726f7ca21a5edd8a8ecee123d8'
GROUPS = {}
PROJECTS = {}

def group(key, ids, file, methods, behavior, review='handler_body_and_shared_dispatch', changes='', helpers=()):
    assert key not in GROUPS
    GROUPS[key] = dict(id=key, service='Services/' + file, methods=methods.split(),
                       behavior=behavior, review_scope=review, local_changes_or_transform=changes,
                       helper_files=['Services/' + x for x in helpers])
    for pid in ids.split():
        assert pid not in PROJECTS, pid
        PROJECTS[pid] = key

# Each fixed profile array and its receipt/package constraints were inspected.
group('generic', 'sm64coopdx-super-mario-64-coop-deluxe perfect-dark-pc-port-perfect-dark project-midas goldeneye-007-pc-port zelda3 crash-team-racing-high-octane ctr-native sonic-3-a-i-r-oxygen-engine cannonball',
      'GameInstallationService.cs', 'Prepare ApplyRecipe PlayInstalled',
      'Unpack official package, execute declarative input/copy/mkdir contract, verify required files and select declared executable. No game boot occurs in this completion path.',
      changes='Only the declarative operations/launch contract in the recipe; see complete recipe payload in catalog-review.json. This is not a binary-origin audit.')
group('n64_portable', 'zelda-64-recompiled banjo-recompiled banjo-tooie-recompiled mariokart-64-recompiled wcwvsnwoworldtourrecomp wcwnworevengerecomp',
      'GameInstallationN64Portable.cs', 'ResumeN64Portable',
      'Hash-check supported original ROM and fixed official runtime kit; copy media into runtime-specific portable location; set marker/arguments/environment. No reconstruction of missing gameplay in this C# path.')
for pid in 'wwfwrestlemania2000recomp vpw64recomp wwfnomercyrecomp btgarecomp battletanx-global-assault-pc-port body-harvest-recomp quest64-recomp snowboardkids2-recomp sssv-recomp bm64recomp bmherorecomp chameleontwist1-jp-recomp dnzhrecomp donkey-kong-64-recompiled-dk64-rekongpiled drmario64-recomp-plus goemon64recomp gga64recomp megaman64recompiled snap64-recomp automobililamborghini-recomp dinosaur-planet-recompiled-dino-recomp ggarecomp rocket-r extremegrecomp'.split():
    PROJECTS[pid] = 'n64_portable'
group('xbox_portable', 'ng2recomp lost-odyssey-recomp king-kong-recompiled the-darkness-recomp gears-of-war-2-pc-port downpourrecomp project8recomp opence shadow-recompiled dprecomp thesimpsonsgamerecomp pgr4-recomp re-blue unleashedrecomp dead-rising-2-case-zero-xenon-recomp dead-rising-2-case-west-xenon-recomp earthworm-jim-hd-recompiled 3on3nhl-recomp',
      'GameInstallationXboxPortable.cs', 'ResumeXboxPortable LaunchXboxPortable',
      'Fixed release kit plus title-specific original Xbox media validation/import. ReBlue and Unleashed dispatch to their own Resume methods; other branches import data or invoke bundled official extraction/cache commands.',
      changes='Original title updates imported for NG2/Downpour/PGR4. Unleashed applies original TU through helper. ReBlue merges original language configuration. Dead Rising invokes upstream shader-cache/overlay generation. No blanket copy-only classification.',
      helpers=('GameInstallationReBlue.cs','GameInstallationUnleashed.cs','GameInstallationXboxRetail.cs','GameInstallationDeadRisingArcade.cs','GameInstallationRetailArcade.cs','GameInstallationPgr4.cs','GameInstallationOpenCe.cs','GameInstallationDeadlyPremonition.cs','GameInstallationSimpsons.cs'))
group('direct_gamecube', 'dusklight-ex-dusk foxhollow nookery-ex-acgc-pc-port strikers', 'GameInstallationDirectGameCube.cs', 'ResumeDirectGameCube LaunchDirectGameCube',
      'Verify exact kit manifest, original disc region/revision/size and SHA-1; copy original ISO/GCM unchanged; pass original disc argument/environment to official runtime.')
group('direct_media', 'recharged supermarioworldrecomp smw yu-gi-oh-forbidden-memories-recompiled god-hand-rearmed', 'GameInstallationDirectMedia.cs', 'ResumeDirectMedia PrepareGodHand LaunchDirectMedia',
      'Verify kit/media hash and size; copy original media (optional SNES copier header removed). God Hand additionally invokes official GHR.exe --prepare --iso and checks extracted boot ELF hash.',
      changes='Media-header normalization for supported SNES inputs; God Hand official preparation. No C# overwrite of runtime game code.')
group('torch_staged', 'ghostship battleship paperboat', 'GameInstallationPaperboat.cs', 'ResumeStagedTorch',
      'ROM import followed by fixed Torch asset-generation CLI; validate archive metadata/output; publish original runtime kit plus generated resources.',
      changes='Helper/source-origin verification is a separate NativeExtractors audit. Reading this caller does not establish that every helper is unmodified.')
for key, ids, file, methods, behavior, changes in [
 ('soh','ship-of-harkinian-soh','GameInstallationSoh.cs','ResumeSoh','Hash-check original ROM and official kit, run fixed Torch extraction for O2R resources, verify output.','Deletes temporary Torch hash cache; helper provenance reviewed separately.'),
 ('2ship','2-ship-2-harkinian-2s2h','GameInstallationTwoShip.cs','ResumeTwoShip','Validate original ROM, run fixed ZAPD resource extraction, validate generated O2R.','Official extractor arguments; no game source rewrite in caller.'),
 ('starship','starship','GameInstallationStarship.cs','ResumeStarship','Validate fixed ROM editions and official kit; call Torch for resource extraction and validate output.','Helper provenance reviewed separately.'),
 ('spaghetti','spaghettikart','GameInstallationSpaghetti.cs','ResumeSpaghetti','Validate original MK64 ROM and official kit; call fixed Torch resource generation and validate output.','Helper provenance reviewed separately.'),
 ('lighthouse','lighthouse','GameInstallationLighthouse.cs','ResumeLighthouse','Validate original Banjo ROM and official kit; call fixed Torch resource generation and validate output.','Helper provenance reviewed separately.'),
 ('adam','adam-s-ant-farm','GameInstallationAdamsAntFarm.cs','ResumeAdam LaunchAdam','Use already imported verified original ROM; stage fixed runtime dependencies and portable launch.','No game source generation in this method.'),
 ('bluewake','bluewake','GameInstallationBlueWake.cs','ResumeBlueWake','Validate original GZLE01 disc and official runtime kit; helper extracts original DOL/REL/resources and validates them.','Helper provenance reviewed separately.'),
 ('wwhd','zeldawwhdrecomp','GameInstallationWindWakerHd.cs','ResumeWindWakerHd LaunchWindWakerHd','Invoke bundled official setup.py for original Wii U data; require real Windows installation and reject placeholder_code.','Flags --no-decomp --code-mods 0 --skip-shader-prebuild select upstream options; not proof of game boot.'),
 ('nectar','open-nectar','GameInstallationNectar.cs','ResumeNectar','Validate Pikmin/Pikmin2 original discs, call fixed native image extractor, verify resulting files and selection.','Custom helper boundary, sources outside Git investigated separately.'),
 ('radz','zelda-3-launcher super-metroid-launcher','GameInstallationRadzLauncher.cs','ResumeRadzLauncher LaunchRadzLauncher','Use fixed official launcher/tool bundle and original ROM; compile pinned snesrev sources with bundled TCC and generate assets.','Compiler options STBI_NO_SIMD=1 and SYSTEM_VOLUME_MIXER_AVAILABLE=0 disable image SIMD and OS volume mixer integration. No source file overwrite found in caller.'),
 ('phase','phase-distorter','GameInstallationPhaseDistorter.cs','ResumePhase LaunchPhase','Validate EarthBound/Mother2 ROM, normalize optional copier header, invoke official importer, verify required generated resources.','Header normalization is media preparation, not new gameplay.'),
 ('picori','autotmc-auto-tmc project-picori-999sian-tmc','GameInstallationPicori.cs','ResumePicori LaunchPicori','Validate original GBA ROM, prepare Picori runtime and invoke extraction CLI; verify cache/pak/sound resources. AutoTMC route downloads the same Picori runtime.','Normalizes generated rom_mtime stamp to zero. AutoTMC and Picori are two catalog IDs for this shared engine path.'),
 ('goldensun','gsrecomp','GameInstallationGoldenSun.cs','ResumeGoldenSun LaunchGoldenSun','Call official gsr_builder.exe --rom --work to generate game library from original ROM; require completion marker and fixed build/engine/library identity.','Official source-generation boundary; not merely copying a launcher, not AllFix-authored gameplay.'),
 ('opengoal','opengoal','GameInstallationOpenGoal.cs','ResumeOpenGoal LaunchOpenGoal','Call official extractor.exe with --extract --validate --decompile --compile; validate serial/build-info and KERNEL.CGO/GAME.CGO.','Upstream decompilation/compilation workflow; no AllFix source patch in caller.'),
 ('shadowrome','shadow-of-rome-recompiled','GameInstallationShadowOfRome.cs','ResumeShadowRome LaunchShadowRome','Validate original PS2 ISO and extract required original executable/data; select official runtime and retain original image reference.','No gameplay implementation in C# handler.'),
 ('symphony','symphonyrecomp','GameInstallationSymphony.cs','ResumeSymphony LaunchSymphony','Validate original PSX disc tracks, extract original resources and convert original CD audio.','Data/media conversion; no runtime source write.'),
 ('wipeoutphantom','wipeout-phantom-edition','GameInstallationWipeoutPhantom.cs','ResumeWipeoutPhantom ExtractWipeoutResources LaunchWipeoutPhantom','Validate nine original track hashes; import 517 named resources, XA sector data and convert CDDA to WAV.','Custom data extractor; preserves official runtime kit. Not new levels/game logic.'),
 ('redriver','redriver2','GameInstallationRedriver.cs','ResumeRedriver MergeRedriverMedia LaunchRedriver','Validate two matching original discs; call bundled jpsxdec.jar to convert original videos/audio; verify RIFF and file plan; launch official runtime with original disc.','Media conversion only in handler; original discs retained as launch inputs.'),
 ('severed','severed-chains','GameInstallationSevered.cs','ResumeSevered','Validate original disc set and bundled Java JARs; run official legend.game.unpacker.Unpacker through generated Java launcher.','Writes temporary AllFixSeveredUnpack Java adapter calling official Unpacker; does not modify JAR game sources.'),
 ('silenthill','silent-hill-native-pc-port','GameInstallationSilentHill.cs','ResumeSilentHill LaunchSilentHill','Validate supported original BIN and stage media/launch configuration for fixed official runtime.','No game source write in handler.'),
 ('vandal','vandalhearts-pcport','GameInstallationVandal.cs','ResumeVandal LaunchVandal','Validate supported original BIN and stage media for fixed official runtime.','No game source write in handler.'),
 ('bloodyroar','bloodyroar2recomp','GameInstallationBloodyRoar.cs','ResumeBloodyRoar LaunchBloodyRoar','Validate original BIN, write CUE description, invoke official --headless --verify-disc.','CUE launch descriptor; verification command is not gameplay homologation.'),
 ('knowyourrole','knowyourrolerecomp','GameInstallationKnowYourRole.cs','ResumeKnowYourRole LaunchKnowYourRole','Validate original PSX BIN, invoke pinned official CLI generator with --cue --out; verify generated managed assemblies.','Bundled custom-published CLI/extractor boundary; build script uses official source. No game source edit observed in caller.'),
 ('kingsfield','kf1-enhanced','GameInstallationKingsField.cs','ResumeKingsField LaunchKingsField','Validate original Japanese PSX disc; invoke fixed extraction helper and verify Japanese data.','Helper adapter build includes conditional NOMINMAX edit in translation_ppf.cpp and optional empty English translation include. Do not classify as entirely unmodified.'),
 ('trx','trx-tomb-raider-i-iii-community-edition openlara','GameInstallationTrx.cs','ResumeTombRaiderPc PlanTrxMedia LaunchTrx','Validate original PC level formats and required files; map original level/media into TRX or OpenLara runtime layout.','Layout/copy and game-selection marker. OpenLara uses its own import-plan/launch helper.'),
 ('rsdk','rsdkv4-decompilation','GameInstallationRsdk.cs','ResolveRsdkMediaRecipe ValidateSonicData','Replace recipe contract locally with original Data.rsdk import plus index/GameConfig edition validation; generic ApplyRecipe completes.','Reads/decrypts a bounded GameConfig prefix for validation; original Data.rsdk copied unchanged.'),
 ('teamforever','sonic-1-forever-sonic-2-absolute sonic-1-forever sonic-2-absolute','GameInstallationTeamForeverBuild.cs','PrepareTeamForeverKit CompleteTeamForeverPreparation LaunchTeamForever','Unpack fixed official ModOnly packages, import validated Data.rsdk from RSDK/APK; launch actual official Windows game executable.','Three catalog IDs share two actual engines. Combined catalog ID is deprecated but still counted.'),
 ('sonicadventure','sarecomp-sonic-adventure-recompiled','GameInstallationSonicContent.cs','CompleteSonicPreparation','Extract fixed NSIS kit offline; validate original Dreamcast data and construct expected RAM/data through official bootstrap delta.','BuildSonicRam applies bundled upstream bootstrap.xor.z; not a copy-only path. Output hashes checked.'),
 ('mml','mega-man-legends-modernization-project','GameInstallationMmlResume.cs','CompleteMmlPreparation','Extract fixed PyInstaller package offline, validate original PC EXE edition and apply verified upstream binary patch plan to staging copy.','121 ranges/247 bytes plus 512-byte tail per US/JP EXE. Full plan independently equals upstream literal manifest at 09b8dd3; see verify_mml_parity.py.'),
 ('marathon','marathon-recompiled','GameInstallationXboxImport.cs','CompleteMarathonPreparation ImportVerifiedXboxFiles','Validate fixed official runtime kit and import original Xbox media against upstream expected file manifest.','Original content imported, no runtime rewrite in handler.'),
 ('edgeoftime','edge-of-time-recomp','GameInstallationEdgeOfTime.cs','CompleteEdgeOfTimePreparation LaunchEdgeOfTime','Validate original ISO plus Title Update STFS; copy official XEXP/DLLP patches and game data for official runtime.','Imports official update data; does not synthesize missing game code.'),
 ('gt4','gt4recomp','GameInstallationGt4.cs','ResumeGt4 VerifyGt4Preparation LaunchGt4','Validate original PS2 ISO/edition, call fixed helper to extract ELF/CORE and verify receipt; launch fixed official game runtime.','Normalizes receipt disc path; forces GT4_RENDERER=hw and GT4_HW_CORE=2 and shader-cache location. Helper provenance separate.'),
 ('linkedps4','tlg-pc iss-pc','GameInstallationLinkedPs4Ports.cs','ResumeLinkedPs4 LaunchLinkedPs4','Fetch fixed hash-pinned official prepare/link/content/patch/ISA scripts; generate linked modules and patch metadata from original PS4 dump.','Runs official tlg_patches.py/infamous_patches.py and isa_rewrite.py --red-zone. This modifies derived code by upstream procedure, not missing gameplay authored by AllFix.'),
 ('pt','pt-pc','GameInstallationPt.cs','ResumePt LaunchPt','Validate original PS4 dump and fixed runtime, import original data and invoke native preparation tools.','See handler body/required output checks; not a new Windows port authored in this method.'),
]:
    group(key, ids, file, methods, behavior, changes=changes)

# Source-build bodies have separate named reviewers. This ledger records the real
# call, not an independent clearance of code those reviewers must inspect.
for key, ids, file, methods in [
 ('mariobuild','sm64ex render96ex sm64rt','GameInstallationMarioBuild.cs','PrepareMarioSource ResumeMarioSource'),
 ('sm64plus','sm64plus','GameInstallationSm64PlusBuild.cs','CompleteSm64PlusBuild'),
 ('ctrbuild','crash-team-racing-turbocharged','GameInstallationCtrBuild.cs','PrepareCtrSourceBuild'),
 ('smbuild','sm sm-rewrite','GameInstallationSmBuild.cs','PrepareSmSourceBuild'),
 ('mkddcpp','mariokartdd-recomp','GameInstallationMkddBuild.cs','PrepareMkddSource ResumeMkdd'),
 ('mkddrust','mkdd-recomp','GameInstallationMkddAltBuild.cs','CompleteMkddAltBuild'),
 ('strikersgc','strikersrecomp','GameInstallationStrikersRecompBuild.cs','CompleteStrikersRecompBuild'),
 ('strikerswii','strikers-wiicompiled','GameInstallationStrikersWiiBuild.cs','CompleteStrikersWiiBuild'),
 ('drmario','drmario64-recomp','GameInstallationDrMario64Build.cs','CompleteDrMario64Preparation'),
 ('wipeoutbuild','wipeout-rewrite','GameInstallationWipeoutBuild.cs','CompleteWipeoutBuild'),
 ('gowkiexster','god-of-war-recomp','GameInstallationGowKiexsterBuild.cs','CompleteGowKiexsterBuild'),
 ('gow','god-of-war-native-pc-port-gow-pc-port','GameInstallationGowBuild.cs','CompleteGowPreparation'),
 ('metaforce','metaforce','GameInstallationMetaforceBuild.cs','CompleteMetaforcePreparation'),
 ('consolebuild','burnout3-recomp gt5-recomp','GameInstallationConsoleBuild.cs','PrepareConsoleSource ResumeConsoleSource'),
 ('sotc','shadow-of-the-colossus-pc','GameInstallationSotcBuild.cs','CompleteSotcPreparation'),
 ('savagewind','savagewindrecomp','GameInstallationSavageWindBuild.cs','ResumeSavageWind CompleteSavageWindPreparation'),
 ('totk','totk-pc-recomp','GameInstallationTotkBuild.cs','CompleteTotkPreparation'),
 ('odyssey','super-odyssey-pc-recomp','GameInstallationOdysseyBuild.cs','CompleteOdysseyPreparation'),
 ('las','lasrecomp','GameInstallationLasBuild.cs','CompleteLasPreparation'),
 ('dkb','dkb-pc-recomp','GameInstallationDkbBuild.cs','CompleteDkbPreparation'),
 ('ps4build','rygt-gt7 spartanport','GameInstallationPs4Build.cs','CompletePs4Preparation'),
 ('doax','doaxvb-re','GameInstallationDoaxBuild.cs','CompleteDoaxPreparation'),
 ('pinyon','pinyon-shift','GameInstallationPinyonBuild.cs','CompletePinyonPreparation'),
 ('ssx','ssx-recomp','GameInstallationSsxBuild.cs','CompleteSsxPreparation'),
 ('gtastories','gta-stories-recompiled','GameInstallationGtaStoriesBuild.cs','CompleteGtaStoriesPreparation'),
 ('forza','fh1-reimagined','GameInstallationForzaXex.cs','StageForzaCompilerInputs'),
 ('hookshot','hookshot-zelda-oot-port','GameInstallationHookshotBuild.cs','CompleteHookshotPreparation'),
 ('mkw','mkw-recomp','GameInstallationMkwBuild.cs','CompleteMkwPreparation'),
]:
    group(key, ids, file, methods, 'Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers.',
          review='dispatch_and_recipe_contract_confirmed_body_delegated',
          changes='Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports.')

def decoded(path):
    b = path.read_bytes()
    try: return b.decode('utf-8-sig')
    except UnicodeDecodeError: return b.decode('cp1252')

def method_ref(path, name):
    text = decoded(DESKTOP / path)
    matches = []
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r'^\s*(?:private|internal|public)\s+.*\b' + re.escape(name) + r'\s*\(', line):
            matches.append(i)
    assert len(matches) >= 1, (path, name)
    return {'path': path, 'method': name, 'lines': matches,
            'url': f'https://github.com/brad38/Allfix/blob/{PIN}/{path}#L{matches[0]}'}

def categories(pid, key):
    if GROUPS[key]['review_scope'].endswith('delegated'):
        return ['source_build_body_review_in_companion_report']
    if key in {'torch_staged','soh','2ship','starship','spaghetti','lighthouse','bluewake','nectar','picori','gt4'}:
        result = ['release_plus_fixed_native_helper_not_rebuilt_in_this_review']
        if key in {'picori','gt4'}: result.append('generated_metadata_or_launch_configuration_changed')
        return result
    if key in {'goldensun','opengoal','wwhd','knowyourrole'}:
        result = ['official_generator_or_compiler_invoked_no_source_edit_observed_in_caller']
        if key == 'wwhd': result.append('upstream_feature_options_selected')
        return result
    if key == 'radz': return ['official_source_compile_with_local_feature_flags']
    if key in {'sonicadventure','mml','linkedps4'}: return ['upstream_binary_patch_delta_or_code_generation']
    if key == 'severed': return ['custom_adapter_source_calls_upstream_unpacker']
    if key == 'kingsfield': return ['custom_extractor_adapter_with_build_source_edit']
    if pid == 'unleashedrecomp': return ['custom_patcher_adapter_using_verified_upstream_patcher_sources', 'original_title_update_applied']
    if pid == 're-blue': return ['original_media_language_configuration_rewritten']
    if pid in {'dead-rising-2-case-zero-xenon-recomp','dead-rising-2-case-west-xenon-recomp'}:
        return ['official_runtime_extraction_shader_cache_overlay_commands']
    if pid in {'ng2recomp','downpourrecomp','pgr4-recomp','edge-of-time-recomp'}:
        return ['release_and_original_title_update_import_no_runtime_source_edit_observed']
    if key in {'pt','redriver'}: return ['release_plus_bundled_official_extraction_conversion_tool_not_rebuilt']
    return ['release_import_no_runtime_source_edit_observed_in_installer']

def main():
    cat = json.loads((OUT / 'catalog-review.json').read_text())
    actual = {p['project_id'] for p in cat['projects'] if p['recipes']}
    assert set(PROJECTS) == actual, {'missing': sorted(actual - set(PROJECTS)), 'extra': sorted(set(PROJECTS) - actual)}
    for group_id, data in GROUPS.items():
        data['method_references'] = [method_ref(data['service'], name) for name in data['methods']]
        for helper in data['helper_files']: assert (DESKTOP / helper).is_file(), helper
        data['source_sha256'] = hashlib.sha256((DESKTOP / data['service']).read_bytes()).hexdigest()
        data['project_ids'] = sorted(pid for pid, key in PROJECTS.items() if key == group_id)
    rows = []
    for project in cat['projects']:
        if not project['recipes']: continue
        for recipe in project['recipes']:
            tag = recipe['contract']['tag']
            key = PROJECTS[project['project_id']]
            if project['project_id'] == 'sm64plus' and tag == 'LauncherMirror': key = 'generic'
            if project['project_id'] == 'crash-team-racing-turbocharged' and tag == 'ci-07d0c49': key = 'generic'
            rows.append({'project_id': project['project_id'], 'tag': tag, 'recipe_path': recipe['path'],
                         'source_url': recipe['contract'].get('source_url'), 'repository': recipe['repository'],
                         'route': key, 'build_profile': recipe['contract'].get('build_profile'),
                         'launch_file_declared': recipe['contract'].get('launch_file'),
                         'recipe_has_manual_steps': bool(recipe['contract'].get('manual_steps')),
                         'route_refs': GROUPS[key]['method_references'],
                         'review_scope': GROUPS[key]['review_scope'],
                         'observed_categories': categories(project['project_id'], key),
                         'boot_evidence': project['boot_evidence']})
    assert len(rows) == 145 and len({r['project_id'] for r in rows}) == 142
    counts = {'indexed_ids': len(actual), 'recipes': len(rows), 'unmapped_ids': 0,
              'groups': len(GROUPS), 'recipe_routes': dict(Counter(row['route'] for row in rows)),
              'recipe_review_scope': dict(Counter(row['review_scope'] for row in rows))}
    findings = [
        {'id': 'completion_is_not_boot', 'severity': 'semantic', 'source': 'Services/GameInstallationPreparedBuildTransaction.cs:24-49',
         'finding': 'Completion executes callback, validates output launch format (or Java contract), reads manifest and publishes with Verified=true/Completed. It does not run gameplay or establish upstream completeness.'},
        {'id': 'no_unknown_promote_fallback', 'severity': 'scope', 'source': 'Services/GameInstallationPreparationResume.cs:183-188,260-302',
         'finding': 'Unknown/ineligible kit is rejected. Last fallback saves media selection in existing partial state; it does not change status to Completed. Recognized paths can Complete after structural prep without first boot.'},
        {'id': 'forza_rank_mismatch', 'severity': 'catalog_semantics', 'source': 'Services/GameInstallationPreparationResume.cs:18-38,256-298; Services/StoreAddonProviders.cs:137-143',
         'finding': 'ForzaInnoProfile has a complete resume branch into BuildForzaGame through StageForzaCompilerInputs, but is missing from CanCompletePreparation. AutomationRank therefore reports 1 for that recipe; this is a static classification mismatch, not a proven UI block.'},
        {'id': 'official_launchers_not_always_handoff', 'severity': 'scope', 'source': 'Radz/GoldenSun/OpenGoal/WindWakerHd/KnowYourRole methods in this ledger',
         'finding': 'Some upstream launchers generate/compile code from original media. AllFix invokes their fixed CLI functions. That is distinct from authoring missing gameplay; also distinct from merely copying a launcher.'},
        {'id': 'config_and_binary_transforms', 'severity': 'disclosure', 'source': 'Radz/SonicContent/MmlResume/ReBlue/Unleashed/LinkedPs4/Gt4 methods in this ledger',
         'finding': 'These paths apply configuration changes, upstream binary deltas or official generation scripts. They cannot be described collectively as absolutely unmodified.'},
        {'id': 'helper_provenance_boundary', 'severity': 'limitation', 'source': 'Tools/NativeExtractors and Tools/UnleashedHelper',
         'finding': 'This handler review establishes call/dataflow and guards. Fixed hashes do not alone establish helper source parity. Companion native-extractor audit covers available sources and remaining provenance gaps.'},
    ]
    project_rows = []
    for project in cat['projects']:
        variants = [row for row in rows if row['project_id'] == project['project_id']]
        route_ids = sorted({row['route'] for row in variants})
        seen = set()
        sources = []
        for route in route_ids:
            data = GROUPS[route]
            for ref in data['method_references']:
                ident = (ref['path'], ref['method'])
                if ident in seen: continue
                seen.add(ident)
                sources.append({**ref, 'coverage': data['review_scope']})
        project_rows.append({
            'project_id': project['project_id'], 'has_recipe': bool(variants),
            'routes': route_ids, 'recipe_paths': [row['recipe_path'] for row in variants],
            'observed_categories': sorted({category for row in variants for category in row['observed_categories']}) if variants else ['no_indexed_recipe_no_build_route'],
            'sources_read': sources,
            'shared_dispatch_read': ['Services/GameInstallationService.cs:140-338,454-512,646-810,950-1140',
                                     'Services/GameInstallationPreparationResume.cs:18-302',
                                     'Services/GameInstallationPreparedBuildTransaction.cs:1-53'] if variants else [],
            'helper_binary_reproduction': 'Not rebuilt in this review; available source parity or companion provenance audit must be consulted separately.' if variants else 'not_applicable',
            'gameplay_evidence': project['boot_evidence'],
            'interpretation_limit': 'A no-source-edit category applies to observed installer statements only, not to provenance/completeness of every upstream binary or all transitive dependencies.',
        })
    payload = {'desktop_commit': PIN, 'method': 'Manual reading of shared dispatch/transaction and listed handler method bodies; declarative recipes read in full; route ledger then asserts 145 recipes/142 IDs and resolves every listed method locator.',
               'limits': ['No game execution or commercial-media boot performed.', 'Body reviews delegated in rows explicitly marked accordingly.', 'Native helper caller review alone is not source/binary parity proof.', 'No claim of upstream completeness is inferred from successful build, imported assets, executable format or output hashes.'],
               'counts': counts, 'groups': GROUPS, 'findings': findings, 'recipes': rows, 'projects': project_rows,
               'absent_catalog_ids': cat['absent_ids']}
    (OUT / 'service-routing-review.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    lines = ['# Matriz de roteamento Desktop por receita', '',
             f'Fonte fixada: Desktop `{PIN}`. Cobertura: **145 receitas / 142 IDs; zero IDs sem rota atribuída**. Os seis IDs sem receita constam separadamente no inventário.', '',
             '## Método e limite', '',
             'Foram lidos os contratos completos e os corpos dos dispatchers `GameInstallationService`, `GameInstallationPreparationResume` e da transação `RunPreparedBuildTransaction`. Os handlers de mídia/launcher listados como `handler_body_and_shared_dispatch` tiveram seu corpo de preparação e lançamento inspecionado; não são conclusões extraídas de busca literal. As rotas de build marcadas como delegadas dependem dos relatórios dos outros revisores, e não recebem absolvição neste documento.', '',
             'Nenhum boot com mídia comercial foi executado. `Completed`/`Verified` nesta implementação representa publicação dos arquivos após o contrato de preparação e verificações estruturais; não é teste de jogo completo. A presença de um launcher oficial também não permite concluir que ele esteja funcional sem observar sua implementação/pacote.', '',
             '## Achados transversais', '']
    for finding in findings:
        lines.append(f'- **{finding["id"]}**: {finding["finding"]} Fonte: `{finding["source"]}`.')
    lines += ['', '## Cobertura por família de método', '', '| Família | IDs | Corpo revisado nesta fatia | Método/pin | Comportamento e alterações |', '| --- | ---: | --- | --- | --- |']
    for key, data in GROUPS.items():
        ref = data['method_references'][0]
        status = 'sim, handler e dispatch' if data['review_scope'] == 'handler_body_and_shared_dispatch' else 'dispatch; corpo em relatório complementar'
        desc = data['behavior'] + (' ' + data['local_changes_or_transform'] if data['local_changes_or_transform'] else '')
        lines.append(f'| {key} | {len(data["project_ids"])} | {status} | [{ref["method"]}]({ref["url"]}) | {desc.replace("|", "/")} |')
    lines += ['', '## Todas as receitas', '', '| ID | Tag | Rota | Perfil de preparação | Cobertura do corpo |', '| --- | --- | --- | --- | --- |']
    for row in rows:
        status = 'handler revisado' if row['review_scope'] == 'handler_body_and_shared_dispatch' else 'relatório complementar'
        lines.append(f'| `{row["project_id"]}` | `{row["tag"]}` | {row["route"]} | {row["build_profile"] or "por ID/tag/pacote"} | {status} |')
    lines += ['', '## Reprodução', '',
              '`python docs/audits/source-integrity-20261127/service_routing_inventory.py` valida a cobertura contra o inventário e a existência de cada definição de método no snapshot fixado. Ele não substitui a leitura humana que fundamentou as decisões de rota e escopo. Grava somente os dois relatórios de roteamento.', '']
    (OUT / 'service-routing-review.md').write_text('\n'.join(lines))
    print(json.dumps(counts, ensure_ascii=False))

if __name__ == '__main__':
    main()
