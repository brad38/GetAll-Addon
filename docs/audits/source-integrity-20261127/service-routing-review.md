# Matriz de roteamento Desktop por receita

Fonte fixada: Desktop `921295de12349e726f7ca21a5edd8a8ecee123d8`. Cobertura: **145 receitas / 142 IDs; zero IDs sem rota atribuída**. Os seis IDs sem receita constam separadamente no inventário.

## Método e limite

Foram lidos os contratos completos e os corpos dos dispatchers `GameInstallationService`, `GameInstallationPreparationResume` e da transação `RunPreparedBuildTransaction`. Os handlers de mídia/launcher listados como `handler_body_and_shared_dispatch` tiveram seu corpo de preparação e lançamento inspecionado; não são conclusões extraídas de busca literal. As rotas de build marcadas como delegadas dependem dos relatórios dos outros revisores, e não recebem absolvição neste documento.

Nenhum boot com mídia comercial foi executado. `Completed`/`Verified` nesta implementação representa publicação dos arquivos após o contrato de preparação e verificações estruturais; não é teste de jogo completo. A presença de um launcher oficial também não permite concluir que ele esteja funcional sem observar sua implementação/pacote.

## Achados transversais

- **completion_is_not_boot**: Completion executes callback, validates output launch format (or Java contract), reads manifest and publishes with Verified=true/Completed. It does not run gameplay or establish upstream completeness. Fonte: `Services/GameInstallationPreparedBuildTransaction.cs:24-49`.
- **no_unknown_promote_fallback**: Unknown/ineligible kit is rejected. Last fallback saves media selection in existing partial state; it does not change status to Completed. Recognized paths can Complete after structural prep without first boot. Fonte: `Services/GameInstallationPreparationResume.cs:183-188,260-302`.
- **forza_rank_mismatch**: ForzaInnoProfile has a complete resume branch into BuildForzaGame through StageForzaCompilerInputs, but is missing from CanCompletePreparation. AutomationRank therefore reports 1 for that recipe; this is a static classification mismatch, not a proven UI block. Fonte: `Services/GameInstallationPreparationResume.cs:18-38,256-298; Services/StoreAddonProviders.cs:137-143`.
- **official_launchers_not_always_handoff**: Some upstream launchers generate/compile code from original media. AllFix invokes their fixed CLI functions. That is distinct from authoring missing gameplay; also distinct from merely copying a launcher. Fonte: `Radz/GoldenSun/OpenGoal/WindWakerHd/KnowYourRole methods in this ledger`.
- **config_and_binary_transforms**: These paths apply configuration changes, upstream binary deltas or official generation scripts. They cannot be described collectively as absolutely unmodified. Fonte: `Radz/SonicContent/MmlResume/ReBlue/Unleashed/LinkedPs4/Gt4 methods in this ledger`.
- **helper_provenance_boundary**: This handler review establishes call/dataflow and guards. Fixed hashes do not alone establish helper source parity. Companion native-extractor audit covers available sources and remaining provenance gaps. Fonte: `Tools/NativeExtractors and Tools/UnleashedHelper`.

## Cobertura por família de método

| Família | IDs | Corpo revisado nesta fatia | Método/pin | Comportamento e alterações |
| --- | ---: | --- | --- | --- |
| generic | 9 | sim, handler e dispatch | [Prepare](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationService.cs#L465) | Unpack official package, execute declarative input/copy/mkdir contract, verify required files and select declared executable. No game boot occurs in this completion path. Only the declarative operations/launch contract in the recipe; see complete recipe payload in catalog-review.json. This is not a binary-origin audit. |
| n64_portable | 30 | sim, handler e dispatch | [ResumeN64Portable](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationN64Portable.cs#L263) | Hash-check supported original ROM and fixed official runtime kit; copy media into runtime-specific portable location; set marker/arguments/environment. No reconstruction of missing gameplay in this C# path. |
| xbox_portable | 18 | sim, handler e dispatch | [ResumeXboxPortable](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationXboxPortable.cs#L359) | Fixed release kit plus title-specific original Xbox media validation/import. ReBlue and Unleashed dispatch to their own Resume methods; other branches import data or invoke bundled official extraction/cache commands. Original title updates imported for NG2/Downpour/PGR4. Unleashed applies original TU through helper. ReBlue merges original language configuration. Dead Rising invokes upstream shader-cache/overlay generation. No blanket copy-only classification. |
| direct_gamecube | 4 | sim, handler e dispatch | [ResumeDirectGameCube](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationDirectGameCube.cs#L94) | Verify exact kit manifest, original disc region/revision/size and SHA-1; copy original ISO/GCM unchanged; pass original disc argument/environment to official runtime. |
| direct_media | 5 | sim, handler e dispatch | [ResumeDirectMedia](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationDirectMedia.cs#L99) | Verify kit/media hash and size; copy original media (optional SNES copier header removed). God Hand additionally invokes official GHR.exe --prepare --iso and checks extracted boot ELF hash. Media-header normalization for supported SNES inputs; God Hand official preparation. No C# overwrite of runtime game code. |
| torch_staged | 3 | sim, handler e dispatch | [ResumeStagedTorch](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationPaperboat.cs#L136) | ROM import followed by fixed Torch asset-generation CLI; validate archive metadata/output; publish original runtime kit plus generated resources. Helper/source-origin verification is a separate NativeExtractors audit. Reading this caller does not establish that every helper is unmodified. |
| soh | 1 | sim, handler e dispatch | [ResumeSoh](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSoh.cs#L69) | Hash-check original ROM and official kit, run fixed Torch extraction for O2R resources, verify output. Deletes temporary Torch hash cache; helper provenance reviewed separately. |
| 2ship | 1 | sim, handler e dispatch | [ResumeTwoShip](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationTwoShip.cs#L132) | Validate original ROM, run fixed ZAPD resource extraction, validate generated O2R. Official extractor arguments; no game source rewrite in caller. |
| starship | 1 | sim, handler e dispatch | [ResumeStarship](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationStarship.cs#L60) | Validate fixed ROM editions and official kit; call Torch for resource extraction and validate output. Helper provenance reviewed separately. |
| spaghetti | 1 | sim, handler e dispatch | [ResumeSpaghetti](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSpaghetti.cs#L75) | Validate original MK64 ROM and official kit; call fixed Torch resource generation and validate output. Helper provenance reviewed separately. |
| lighthouse | 1 | sim, handler e dispatch | [ResumeLighthouse](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationLighthouse.cs#L45) | Validate original Banjo ROM and official kit; call fixed Torch resource generation and validate output. Helper provenance reviewed separately. |
| adam | 1 | sim, handler e dispatch | [ResumeAdam](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationAdamsAntFarm.cs#L56) | Use already imported verified original ROM; stage fixed runtime dependencies and portable launch. No game source generation in this method. |
| bluewake | 1 | sim, handler e dispatch | [ResumeBlueWake](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationBlueWake.cs#L78) | Validate original GZLE01 disc and official runtime kit; helper extracts original DOL/REL/resources and validates them. Helper provenance reviewed separately. |
| wwhd | 1 | sim, handler e dispatch | [ResumeWindWakerHd](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationWindWakerHd.cs#L31) | Invoke bundled official setup.py for original Wii U data; require real Windows installation and reject placeholder_code. Flags --no-decomp --code-mods 0 --skip-shader-prebuild select upstream options; not proof of game boot. |
| nectar | 1 | sim, handler e dispatch | [ResumeNectar](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationNectar.cs#L85) | Validate Pikmin/Pikmin2 original discs, call fixed native image extractor, verify resulting files and selection. Custom helper boundary, sources outside Git investigated separately. |
| radz | 2 | sim, handler e dispatch | [ResumeRadzLauncher](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationRadzLauncher.cs#L73) | Use fixed official launcher/tool bundle and original ROM; compile pinned snesrev sources with bundled TCC and generate assets. Compiler options STBI_NO_SIMD=1 and SYSTEM_VOLUME_MIXER_AVAILABLE=0 disable image SIMD and OS volume mixer integration. No source file overwrite found in caller. |
| phase | 1 | sim, handler e dispatch | [ResumePhase](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationPhaseDistorter.cs#L59) | Validate EarthBound/Mother2 ROM, normalize optional copier header, invoke official importer, verify required generated resources. Header normalization is media preparation, not new gameplay. |
| picori | 2 | sim, handler e dispatch | [ResumePicori](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationPicori.cs#L63) | Validate original GBA ROM, prepare Picori runtime and invoke extraction CLI; verify cache/pak/sound resources. AutoTMC route downloads the same Picori runtime. Normalizes generated rom_mtime stamp to zero. AutoTMC and Picori are two catalog IDs for this shared engine path. |
| goldensun | 1 | sim, handler e dispatch | [ResumeGoldenSun](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationGoldenSun.cs#L89) | Call official gsr_builder.exe --rom --work to generate game library from original ROM; require completion marker and fixed build/engine/library identity. Official source-generation boundary; not merely copying a launcher, not AllFix-authored gameplay. |
| opengoal | 1 | sim, handler e dispatch | [ResumeOpenGoal](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationOpenGoal.cs#L46) | Call official extractor.exe with --extract --validate --decompile --compile; validate serial/build-info and KERNEL.CGO/GAME.CGO. Upstream decompilation/compilation workflow; no AllFix source patch in caller. |
| shadowrome | 1 | sim, handler e dispatch | [ResumeShadowRome](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationShadowOfRome.cs#L79) | Validate original PS2 ISO and extract required original executable/data; select official runtime and retain original image reference. No gameplay implementation in C# handler. |
| symphony | 1 | sim, handler e dispatch | [ResumeSymphony](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSymphony.cs#L36) | Validate original PSX disc tracks, extract original resources and convert original CD audio. Data/media conversion; no runtime source write. |
| wipeoutphantom | 1 | sim, handler e dispatch | [ResumeWipeoutPhantom](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationWipeoutPhantom.cs#L73) | Validate nine original track hashes; import 517 named resources, XA sector data and convert CDDA to WAV. Custom data extractor; preserves official runtime kit. Not new levels/game logic. |
| redriver | 1 | sim, handler e dispatch | [ResumeRedriver](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationRedriver.cs#L77) | Validate two matching original discs; call bundled jpsxdec.jar to convert original videos/audio; verify RIFF and file plan; launch official runtime with original disc. Media conversion only in handler; original discs retained as launch inputs. |
| severed | 1 | sim, handler e dispatch | [ResumeSevered](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSevered.cs#L68) | Validate original disc set and bundled Java JARs; run official legend.game.unpacker.Unpacker through generated Java launcher. Writes temporary AllFixSeveredUnpack Java adapter calling official Unpacker; does not modify JAR game sources. |
| silenthill | 1 | sim, handler e dispatch | [ResumeSilentHill](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSilentHill.cs#L38) | Validate supported original BIN and stage media/launch configuration for fixed official runtime. No game source write in handler. |
| vandal | 1 | sim, handler e dispatch | [ResumeVandal](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationVandal.cs#L28) | Validate supported original BIN and stage media for fixed official runtime. No game source write in handler. |
| bloodyroar | 1 | sim, handler e dispatch | [ResumeBloodyRoar](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationBloodyRoar.cs#L34) | Validate original BIN, write CUE description, invoke official --headless --verify-disc. CUE launch descriptor; verification command is not gameplay homologation. |
| knowyourrole | 1 | sim, handler e dispatch | [ResumeKnowYourRole](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationKnowYourRole.cs#L47) | Validate original PSX BIN, invoke pinned official CLI generator with --cue --out; verify generated managed assemblies. Bundled custom-published CLI/extractor boundary; build script uses official source. No game source edit observed in caller. |
| kingsfield | 1 | sim, handler e dispatch | [ResumeKingsField](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationKingsField.cs#L48) | Validate original Japanese PSX disc; invoke fixed extraction helper and verify Japanese data. Helper adapter build includes conditional NOMINMAX edit in translation_ppf.cpp and optional empty English translation include. Do not classify as entirely unmodified. |
| trx | 2 | sim, handler e dispatch | [ResumeTombRaiderPc](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationTrx.cs#L127) | Validate original PC level formats and required files; map original level/media into TRX or OpenLara runtime layout. Layout/copy and game-selection marker. OpenLara uses its own import-plan/launch helper. |
| rsdk | 1 | sim, handler e dispatch | [ResolveRsdkMediaRecipe](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationRsdk.cs#L16) | Replace recipe contract locally with original Data.rsdk import plus index/GameConfig edition validation; generic ApplyRecipe completes. Reads/decrypts a bounded GameConfig prefix for validation; original Data.rsdk copied unchanged. |
| teamforever | 3 | sim, handler e dispatch | [PrepareTeamForeverKit](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationTeamForeverBuild.cs#L206) | Unpack fixed official ModOnly packages, import validated Data.rsdk from RSDK/APK; launch actual official Windows game executable. Three catalog IDs share two actual engines. Combined catalog ID is deprecated but still counted. |
| sonicadventure | 1 | sim, handler e dispatch | [CompleteSonicPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSonicContent.cs#L213) | Extract fixed NSIS kit offline; validate original Dreamcast data and construct expected RAM/data through official bootstrap delta. BuildSonicRam applies bundled upstream bootstrap.xor.z; not a copy-only path. Output hashes checked. |
| mml | 1 | sim, handler e dispatch | [CompleteMmlPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationMmlResume.cs#L75) | Extract fixed PyInstaller package offline, validate original PC EXE edition and apply verified upstream binary patch plan to staging copy. 121 ranges/247 bytes plus 512-byte tail per US/JP EXE. Full plan independently equals upstream literal manifest at 09b8dd3; see verify_mml_parity.py. |
| marathon | 1 | sim, handler e dispatch | [CompleteMarathonPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationXboxImport.cs#L30) | Validate fixed official runtime kit and import original Xbox media against upstream expected file manifest. Original content imported, no runtime rewrite in handler. |
| edgeoftime | 1 | sim, handler e dispatch | [CompleteEdgeOfTimePreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationEdgeOfTime.cs#L53) | Validate original ISO plus Title Update STFS; copy official XEXP/DLLP patches and game data for official runtime. Imports official update data; does not synthesize missing game code. |
| gt4 | 1 | sim, handler e dispatch | [ResumeGt4](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationGt4.cs#L49) | Validate original PS2 ISO/edition, call fixed helper to extract ELF/CORE and verify receipt; launch fixed official game runtime. Normalizes receipt disc path; forces GT4_RENDERER=hw and GT4_HW_CORE=2 and shader-cache location. Helper provenance separate. |
| linkedps4 | 2 | sim, handler e dispatch | [ResumeLinkedPs4](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationLinkedPs4Ports.cs#L62) | Fetch fixed hash-pinned official prepare/link/content/patch/ISA scripts; generate linked modules and patch metadata from original PS4 dump. Runs official tlg_patches.py/infamous_patches.py and isa_rewrite.py --red-zone. This modifies derived code by upstream procedure, not missing gameplay authored by AllFix. |
| pt | 1 | sim, handler e dispatch | [ResumePt](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationPt.cs#L66) | Validate original PS4 dump and fixed runtime, import original data and invoke native preparation tools. See handler body/required output checks; not a new Windows port authored in this method. |
| mariobuild | 3 | dispatch; corpo em relatório complementar | [PrepareMarioSource](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationMarioBuild.cs#L43) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| sm64plus | 1 | dispatch; corpo em relatório complementar | [CompleteSm64PlusBuild](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSm64PlusBuild.cs#L11) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| ctrbuild | 1 | dispatch; corpo em relatório complementar | [PrepareCtrSourceBuild](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationCtrBuild.cs#L25) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| smbuild | 2 | dispatch; corpo em relatório complementar | [PrepareSmSourceBuild](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSmBuild.cs#L34) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| mkddcpp | 1 | dispatch; corpo em relatório complementar | [PrepareMkddSource](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationMkddBuild.cs#L22) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| mkddrust | 1 | dispatch; corpo em relatório complementar | [CompleteMkddAltBuild](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationMkddAltBuild.cs#L158) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| strikersgc | 1 | dispatch; corpo em relatório complementar | [CompleteStrikersRecompBuild](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationStrikersRecompBuild.cs#L110) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| strikerswii | 1 | dispatch; corpo em relatório complementar | [CompleteStrikersWiiBuild](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationStrikersWiiBuild.cs#L94) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| drmario | 1 | dispatch; corpo em relatório complementar | [CompleteDrMario64Preparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationDrMario64Build.cs#L79) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| wipeoutbuild | 1 | dispatch; corpo em relatório complementar | [CompleteWipeoutBuild](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationWipeoutBuild.cs#L172) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| gowkiexster | 1 | dispatch; corpo em relatório complementar | [CompleteGowKiexsterBuild](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationGowKiexsterBuild.cs#L116) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| gow | 1 | dispatch; corpo em relatório complementar | [CompleteGowPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationGowBuild.cs#L94) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| metaforce | 1 | dispatch; corpo em relatório complementar | [CompleteMetaforcePreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationMetaforceBuild.cs#L94) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| consolebuild | 2 | dispatch; corpo em relatório complementar | [PrepareConsoleSource](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationConsoleBuild.cs#L41) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| sotc | 1 | dispatch; corpo em relatório complementar | [CompleteSotcPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSotcBuild.cs#L60) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| savagewind | 1 | dispatch; corpo em relatório complementar | [ResumeSavageWind](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSavageWindBuild.cs#L52) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| totk | 1 | dispatch; corpo em relatório complementar | [CompleteTotkPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationTotkBuild.cs#L263) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| odyssey | 1 | dispatch; corpo em relatório complementar | [CompleteOdysseyPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationOdysseyBuild.cs#L176) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| las | 1 | dispatch; corpo em relatório complementar | [CompleteLasPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationLasBuild.cs#L172) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| dkb | 1 | dispatch; corpo em relatório complementar | [CompleteDkbPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationDkbBuild.cs#L231) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| ps4build | 2 | dispatch; corpo em relatório complementar | [CompletePs4Preparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationPs4Build.cs#L90) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| doax | 1 | dispatch; corpo em relatório complementar | [CompleteDoaxPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationDoaxBuild.cs#L124) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| pinyon | 1 | dispatch; corpo em relatório complementar | [CompletePinyonPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationPinyonBuild.cs#L148) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| ssx | 1 | dispatch; corpo em relatório complementar | [CompleteSsxPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSsxBuild.cs#L133) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| gtastories | 1 | dispatch; corpo em relatório complementar | [CompleteGtaStoriesPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationGtaStoriesBuild.cs#L72) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| forza | 1 | dispatch; corpo em relatório complementar | [StageForzaCompilerInputs](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationForzaXex.cs#L144) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| hookshot | 1 | dispatch; corpo em relatório complementar | [CompleteHookshotPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationHookshotBuild.cs#L233) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |
| mkw | 1 | dispatch; corpo em relatório complementar | [CompleteMkwPreparation](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationMkwBuild.cs#L163) | Source-build route confirmed from dispatcher and fixed profile/tag identity; body changes and synthetic-test separation covered by the other source-integrity reviewers. Do not interpret this row as no source mutation. See the source-build/MKW/Metaforce/Rexglue companion reports. |

## Todas as receitas

| ID | Tag | Rota | Perfil de preparação | Cobertura do corpo |
| --- | --- | --- | --- | --- |
| `ghostship` | `3.0.0` | torch_staged | por ID/tag/pacote | handler revisado |
| `sm64coopdx-super-mario-64-coop-deluxe` | `v1.5.1` | generic | por ID/tag/pacote | handler revisado |
| `sm64plus` | `build-85c3e51` | sm64plus | por ID/tag/pacote | relatório complementar |
| `sm64plus` | `LauncherMirror` | generic | por ID/tag/pacote | handler revisado |
| `render96ex` | `build-48da5c4` | mariobuild | por ID/tag/pacote | relatório complementar |
| `sm64ex` | `build-d7ca2c0` | mariobuild | por ID/tag/pacote | relatório complementar |
| `sm64rt` | `build-20e618b` | mariobuild | por ID/tag/pacote | relatório complementar |
| `ship-of-harkinian-soh` | `9.3.1` | soh | por ID/tag/pacote | handler revisado |
| `hookshot-zelda-oot-port` | `v3.0.2` | hookshot | hookshot-3.0.2-prepare | relatório complementar |
| `zelda-64-recompiled` | `v1.2.2` | n64_portable | por ID/tag/pacote | handler revisado |
| `2-ship-2-harkinian-2s2h` | `5.0.1` | 2ship | por ID/tag/pacote | handler revisado |
| `starship` | `v2.0.0` | starship | por ID/tag/pacote | handler revisado |
| `spaghettikart` | `1.0.0` | spaghetti | por ID/tag/pacote | handler revisado |
| `mariokart-64-recompiled` | `v0.9.2` | n64_portable | por ID/tag/pacote | handler revisado |
| `battleship` | `v1.6` | torch_staged | por ID/tag/pacote | handler revisado |
| `paperboat` | `1.0.3` | torch_staged | por ID/tag/pacote | handler revisado |
| `donkey-kong-64-recompiled-dk64-rekongpiled` | `v1.0.3` | n64_portable | por ID/tag/pacote | handler revisado |
| `snap64-recomp` | `v1.1.8` | n64_portable | por ID/tag/pacote | handler revisado |
| `drmario64-recomp-plus` | `1.0.0` | n64_portable | por ID/tag/pacote | handler revisado |
| `drmario64-recomp` | `build-7892264` | drmario | por ID/tag/pacote | relatório complementar |
| `banjo-recompiled` | `v1.0.2` | n64_portable | por ID/tag/pacote | handler revisado |
| `lighthouse` | `1.2.2` | lighthouse | por ID/tag/pacote | handler revisado |
| `banjo-tooie-recompiled` | `v1.0.1` | n64_portable | por ID/tag/pacote | handler revisado |
| `perfect-dark-pc-port-perfect-dark` | `ci-dev-build` | generic | por ID/tag/pacote | handler revisado |
| `project-midas` | `1.0.2b` | generic | por ID/tag/pacote | handler revisado |
| `goldeneye-007-pc-port` | `v0.5.0` | generic | por ID/tag/pacote | handler revisado |
| `dinosaur-planet-recompiled-dino-recomp` | `v0.3.0` | n64_portable | por ID/tag/pacote | handler revisado |
| `bm64recomp` | `v1.0.0` | n64_portable | por ID/tag/pacote | handler revisado |
| `bmherorecomp` | `v0.7.1` | n64_portable | por ID/tag/pacote | handler revisado |
| `goemon64recomp` | `v0.2.0-dev` | n64_portable | por ID/tag/pacote | handler revisado |
| `ggarecomp` | `v0.3.0` | n64_portable | por ID/tag/pacote | handler revisado |
| `gga64recomp` | `v0.1.0` | n64_portable | por ID/tag/pacote | handler revisado |
| `dnzhrecomp` | `0.0.3` | n64_portable | por ID/tag/pacote | handler revisado |
| `adam-s-ant-farm` | `v0.11.14` | adam | por ID/tag/pacote | handler revisado |
| `body-harvest-recomp` | `v0.1.0` | n64_portable | por ID/tag/pacote | handler revisado |
| `sssv-recomp` | `v0.2.0` | n64_portable | por ID/tag/pacote | handler revisado |
| `quest64-recomp` | `v0.1` | n64_portable | por ID/tag/pacote | handler revisado |
| `megaman64recompiled` | `v0.9.1` | n64_portable | por ID/tag/pacote | handler revisado |
| `battletanx-global-assault-pc-port` | `v0.2.5` | n64_portable | por ID/tag/pacote | handler revisado |
| `btgarecomp` | `v0.1.13` | n64_portable | por ID/tag/pacote | handler revisado |
| `snowboardkids2-recomp` | `v2.0.2` | n64_portable | por ID/tag/pacote | handler revisado |
| `extremegrecomp` | `v1.0.0` | n64_portable | por ID/tag/pacote | handler revisado |
| `rocket-r` | `v.1.0.1` | n64_portable | por ID/tag/pacote | handler revisado |
| `chameleontwist1-jp-recomp` | `v0.1` | n64_portable | por ID/tag/pacote | handler revisado |
| `automobililamborghini-recomp` | `v0.11.1` | n64_portable | por ID/tag/pacote | handler revisado |
| `wcwvsnwoworldtourrecomp` | `v0.3.2` | n64_portable | por ID/tag/pacote | handler revisado |
| `wcwnworevengerecomp` | `v0.3.2` | n64_portable | por ID/tag/pacote | handler revisado |
| `wwfwrestlemania2000recomp` | `v0.3.2` | n64_portable | por ID/tag/pacote | handler revisado |
| `vpw64recomp` | `v0.3.2` | n64_portable | por ID/tag/pacote | handler revisado |
| `wwfnomercyrecomp` | `v0.3.2` | n64_portable | por ID/tag/pacote | handler revisado |
| `bluewake` | `v0.12.0` | bluewake | por ID/tag/pacote | handler revisado |
| `zeldawwhdrecomp` | `v0.5.1` | wwhd | por ID/tag/pacote | handler revisado |
| `dusklight-ex-dusk` | `v2.0.3` | direct_gamecube | por ID/tag/pacote | handler revisado |
| `foxhollow` | `v1.0.30` | direct_gamecube | por ID/tag/pacote | handler revisado |
| `nookery-ex-acgc-pc-port` | `v1.0.0` | direct_gamecube | por ID/tag/pacote | handler revisado |
| `open-nectar` | `1.3` | nectar | por ID/tag/pacote | handler revisado |
| `metaforce` | `build-de8fc69` | metaforce | por ID/tag/pacote | relatório complementar |
| `strikers` | `v2.0.0` | direct_gamecube | por ID/tag/pacote | handler revisado |
| `strikersrecomp` | `build-cd88f71` | strikersgc | por ID/tag/pacote | relatório complementar |
| `recharged` | `v1.1.7` | direct_media | por ID/tag/pacote | handler revisado |
| `strikers-wiicompiled` | `build-451e06b` | strikerswii | por ID/tag/pacote | relatório complementar |
| `mariokartdd-recomp` | `build-bd36eb9` | mkddcpp | por ID/tag/pacote | relatório complementar |
| `mkdd-recomp` | `build-e173ce4` | mkddrust | por ID/tag/pacote | relatório complementar |
| `zelda3` | `v0.3` | generic | por ID/tag/pacote | handler revisado |
| `zelda-3-launcher` | `v1.3.7.0` | radz | por ID/tag/pacote | handler revisado |
| `super-metroid-launcher` | `v1.0.1` | radz | por ID/tag/pacote | handler revisado |
| `sm` | `build-578f90b` | smbuild | por ID/tag/pacote | relatório complementar |
| `sm-rewrite` | `build-5237873` | smbuild | por ID/tag/pacote | relatório complementar |
| `supermarioworldrecomp` | `v0.15.11` | direct_media | por ID/tag/pacote | handler revisado |
| `smw` | `v0.1` | direct_media | por ID/tag/pacote | handler revisado |
| `phase-distorter` | `0.5` | phase | por ID/tag/pacote | handler revisado |
| `autotmc-auto-tmc` | `1.0.2` | picori | por ID/tag/pacote | handler revisado |
| `project-picori-999sian-tmc` | `v0.9.6` | picori | por ID/tag/pacote | handler revisado |
| `gsrecomp` | `0.8.4` | goldensun | por ID/tag/pacote | handler revisado |
| `opengoal` | `v0.3.9` | opengoal | por ID/tag/pacote | handler revisado |
| `god-of-war-native-pc-port-gow-pc-port` | `launcher-v0.4.0` | gow | gow-0.4.0-prepare | relatório complementar |
| `god-of-war-recomp` | `build-d1d11ec` | gowkiexster | por ID/tag/pacote | relatório complementar |
| `shadow-of-rome-recompiled` | `v2.9.5` | shadowrome | por ID/tag/pacote | handler revisado |
| `symphonyrecomp` | `v1.2.0p` | symphony | por ID/tag/pacote | handler revisado |
| `crash-team-racing-high-octane` | `v.1.5` | generic | por ID/tag/pacote | handler revisado |
| `crash-team-racing-turbocharged` | `ci-07d0c49` | generic | por ID/tag/pacote | handler revisado |
| `crash-team-racing-turbocharged` | `build-07d0c49` | ctrbuild | por ID/tag/pacote | relatório complementar |
| `ctr-native` | `beta-7.1` | generic | por ID/tag/pacote | handler revisado |
| `wipeout-phantom-edition` | `v1.2.256` | wipeoutphantom | por ID/tag/pacote | handler revisado |
| `wipeout-rewrite` | `build-b425ecb` | wipeoutbuild | por ID/tag/pacote | relatório complementar |
| `redriver2` | `7.4-rc2` | redriver | por ID/tag/pacote | handler revisado |
| `severed-chains` | `release-3.0.0` | severed | por ID/tag/pacote | handler revisado |
| `silent-hill-native-pc-port` | `crossplatform-beta` | silenthill | por ID/tag/pacote | handler revisado |
| `vandalhearts-pcport` | `v2.1.0` | vandal | por ID/tag/pacote | handler revisado |
| `bloodyroar2recomp` | `v0.7.1` | bloodyroar | por ID/tag/pacote | handler revisado |
| `knowyourrolerecomp` | `v0.2.0` | knowyourrole | por ID/tag/pacote | handler revisado |
| `kf1-enhanced` | `v0.1.0-pre.3` | kingsfield | por ID/tag/pacote | handler revisado |
| `yu-gi-oh-forbidden-memories-recompiled` | `v0.3.0` | direct_media | por ID/tag/pacote | handler revisado |
| `trx-tomb-raider-i-iii-community-edition` | `trx-1.12` | trx | por ID/tag/pacote | handler revisado |
| `openlara` | `latest` | trx | por ID/tag/pacote | handler revisado |
| `mega-man-legends-modernization-project` | `v0.9.6-beta` | mml | mml-0.9.6-beta-pyinstaller-prepare | handler revisado |
| `unleashedrecomp` | `v1.0.3` | xbox_portable | por ID/tag/pacote | handler revisado |
| `marathon-recompiled` | `v1.0.0` | marathon | marathon-1.0.0-xbox-import | handler revisado |
| `shadow-recompiled` | `v1.0.1` | xbox_portable | por ID/tag/pacote | handler revisado |
| `sarecomp-sonic-adventure-recompiled` | `v0.52.0` | sonicadventure | sarecomp-0.52.0-prepare | handler revisado |
| `rsdkv4-decompilation` | `1.3.3` | rsdk | por ID/tag/pacote | handler revisado |
| `sonic-1-forever-sonic-2-absolute` | `v1.5.2-v1.2.2` | teamforever | teamforever-1.5.2-1.2.2-prepare | handler revisado |
| `sonic-1-forever` | `v1.5.2` | teamforever | teamforever-sonic1-1.5.2 | handler revisado |
| `sonic-2-absolute` | `v1.2.2` | teamforever | teamforever-sonic2-1.2.2 | handler revisado |
| `sonic-3-a-i-r-oxygen-engine` | `v26.03.28.0-stable` | generic | por ID/tag/pacote | handler revisado |
| `cannonball` | `v0.34` | generic | por ID/tag/pacote | handler revisado |
| `pinyon-shift` | `v0.9.5` | pinyon | pinyon-0.9.5-prepare | relatório complementar |
| `fh1-reimagined` | `v0.3.9` | forza | fh1-0.3.9-inno-prepare | relatório complementar |
| `re-blue` | `nightly-v1.4.0-d187173d8-s44b7fdc5` | xbox_portable | por ID/tag/pacote | handler revisado |
| `the-darkness-recomp` | `v0.1.10` | xbox_portable | por ID/tag/pacote | handler revisado |
| `downpourrecomp` | `v1.1.8` | xbox_portable | por ID/tag/pacote | handler revisado |
| `dprecomp` | `v2.0.14` | xbox_portable | por ID/tag/pacote | handler revisado |
| `project8recomp` | `v0.3.0` | xbox_portable | por ID/tag/pacote | handler revisado |
| `edge-of-time-recomp` | `v1.1` | edgeoftime | edge-of-time-1.1-xbox-import | handler revisado |
| `king-kong-recompiled` | `v2.1.3` | xbox_portable | por ID/tag/pacote | handler revisado |
| `earthworm-jim-hd-recompiled` | `v0.9.6` | xbox_portable | por ID/tag/pacote | handler revisado |
| `thesimpsonsgamerecomp` | `v0.0.7.1` | xbox_portable | por ID/tag/pacote | handler revisado |
| `dead-rising-2-case-zero-xenon-recomp` | `v1.1.3` | xbox_portable | por ID/tag/pacote | handler revisado |
| `dead-rising-2-case-west-xenon-recomp` | `v1.1.2` | xbox_portable | por ID/tag/pacote | handler revisado |
| `doaxvb-re` | `v0.8.0` | doax | doax-0.8.0-prepare | relatório complementar |
| `3on3nhl-recomp` | `v0.1.1` | xbox_portable | por ID/tag/pacote | handler revisado |
| `shadow-of-the-colossus-pc` | `v0.77` | sotc | sotc-0.77-prepare | relatório complementar |
| `savagewindrecomp` | `v0.6.0-alpha.6` | savagewind | por ID/tag/pacote | relatório complementar |
| `totk-pc-recomp` | `v0.5.0` | totk | totk-0.5.0-prepare | relatório complementar |
| `gt4recomp` | `v1.3.0-rc16` | gt4 | por ID/tag/pacote | handler revisado |
| `gt5-recomp` | `build-64ca169` | consolebuild | por ID/tag/pacote | relatório complementar |
| `rygt-gt7` | `rygt-2026-11-23` | ps4build | rygt-2026-11-23-prepare | relatório complementar |
| `lasrecomp` | `v0.6.1` | las | las-0.6.1-prepare | relatório complementar |
| `super-odyssey-pc-recomp` | `v1.0.0` | odyssey | odyssey-1.0.0-prepare | relatório complementar |
| `god-hand-rearmed` | `v0.6.9.5` | direct_media | por ID/tag/pacote | handler revisado |
| `gta-stories-recompiled` | `v0.3.2` | gtastories | gta-stories-0.3.2-prepare | relatório complementar |
| `spartanport` | `windows-v3.2.1` | ps4build | spartanport-3.2.1-prepare | relatório complementar |
| `tlg-pc` | `v2026.11.14-ee3327d` | linkedps4 | por ID/tag/pacote | handler revisado |
| `iss-pc` | `v1.0` | linkedps4 | por ID/tag/pacote | handler revisado |
| `pt-pc` | `v1.1.1` | pt | por ID/tag/pacote | handler revisado |
| `gears-of-war-2-pc-port` | `v0.4.8` | xbox_portable | por ID/tag/pacote | handler revisado |
| `ng2recomp` | `v0.7.5` | xbox_portable | por ID/tag/pacote | handler revisado |
| `pgr4-recomp` | `v2.0.2` | xbox_portable | por ID/tag/pacote | handler revisado |
| `burnout3-recomp` | `build-3c85ed7` | consolebuild | por ID/tag/pacote | relatório complementar |
| `opence` | `build-387` | xbox_portable | por ID/tag/pacote | handler revisado |
| `lost-odyssey-recomp` | `v1.1.0` | xbox_portable | por ID/tag/pacote | handler revisado |
| `ssx-recomp` | `v2.0.0` | ssx | ssx-2.0.0-prepare | relatório complementar |
| `dkb-pc-recomp` | `v0.5.1` | dkb | dkb-0.5.1-44ba6b1-prepare | relatório complementar |
| `mkw-recomp` | `v0.1.18` | mkw | mkw-0.1.18-prepare | relatório complementar |
| `mkw-recomp` | `v0.1.18-allfix-cli` | mkw | mkw-0.1.18-cli-prepare | relatório complementar |

## Reprodução

`python docs/audits/source-integrity-20261127/service_routing_inventory.py` valida a cobertura contra o inventário e a existência de cada definição de método no snapshot fixado. Ele não substitui a leitura humana que fundamentou as decisões de rota e escopo. Grava somente os dois relatórios de roteamento.
