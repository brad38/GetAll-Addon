# Metaforce: public native Windows build, 2026-11-27

**Result:** the complete pinned public Metaforce source built and linked with the
existing private LLVM-MinGW toolchain. The real executable's help/argument parser,
its local Dawn/SDL/nod C interfaces, and Borealis atomic file replacement passed.
No commercial disc, game boot, graphics adapter/device, or generated commercial
function fixture was used. This evidence supports implementing the installation
pipeline; the Desktop transaction and media policy are being integrated separately.

## Pinned source and identity

The catalog identity remains `AxioDL/metaforce`. Its exact public Git revision was
recovered from author fork `Antidote/metaforce` after the original GitHub endpoint
was unavailable. This is an explicit acquisition source, not a project rename.

- Commit: `de8fc69bd7f345d6cf5f0c8fc2798295e22522d3` (2026-10-10T18:24:46Z).
- Git tree: `9d693e8894c031e5d1d220f39a44999d4010dc9f`.
- ZIP: <https://codeload.github.com/Antidote/metaforce/zip/de8fc69bd7f345d6cf5f0c8fc2798295e22522d3>.
- ZIP: 21,536,851 bytes, SHA256 `e130131a1a41e8599541d8ab3dd2f31c6d8abaa9af03411f8bba25c3f5b63f21`.
- TAR: 20,496,145 bytes, SHA256 `efc58779e6b3ff62853e5c1d4f084a8a7744dee056d1c28faf3748dad1df524a`.
- Both archives have root `metaforce-de8fc69bd7f345d6cf5f0c8fc2798295e22522d3/`.

The nontruncated GitHub tree and all 2,070 file contents were checked. Two `.bat`
files receive CRLF from the pinned `.gitattributes`; their canonical Git blobs
were checked after only that prescribed conversion. Archive bytes remain intact.
All ZIP file contents also match the TAR checkout. Original sources are retained
separately from the adapted build copy. SWH queries stopped after rate limiting;
no parallel traversal, challenge bypass, or additional Vault polling was used.

See `metaforce-source-receipt.json`, `metaforce-source-zip-receipt.json`,
`metaforce-source-files.json`, and `public-fork-commit-probes.json`.

## Dependencies and adapters

`metaforce-native-pins.json` lists all 19 source/runtime archives with complete
URLs, byte lengths, SHA256 values, and extraction prefixes. `dependency-results.json`
is the Windows extraction receipt. The three gitlinks are Aurora
`40cf48fce6ce85366608596bae018c6188f2b2e7`, Borealis
`d4d7ff146ff4097d64bb24e52459152f1b5e597a`, and Musyx
`dc56c921528821209a8b53029114e5443435f40d`.

The native build uses the already available LLVM-MinGW 20261020 UCRT x64,
CMake, and Ninja under `gta-engine/preflight`. No global SDK, MSVC installation,
Python package installation, or additional toolchain download was required.
FetchContent is disconnected and all dependencies point at verified local sources.

There are 12 exact anchored edits in eight files, recorded with before/after
text and hashes in `metaforce-native-handoff.json`:

1. Aurora WMI strings use `SysAllocString`/`SysFreeString` RAII, preserving the
   queries while removing the proprietary `comsuppw` C++ dependency.
2. WMI libraries use the corresponding MinGW import-library names.
3. Dawn uses its published C descriptor chain across the MSVC/MinGW boundary.
   The portable toggles and required features remain; only the optional native
   C++ diagnostic descriptor is excluded on MinGW.
4. nod's imported shared target points at its actual `nod.dll` and `nod.lib`.
5. Borealis I/O targets Windows 10 RS1 so the actual private header exposes
   `FileRenameInfoEx`, which the upstream implementation already uses.
6. Aurora CARD includes the MinGW headers declaring the same known-folder API.
7. Two game-source files select `malloc.h` for their existing `alloca` calls on
   MinGW. Allocation and game algorithms are unchanged.

Renderer, UI, CARD, THP, DVD, and Musyx remain in the full native executable.
Zstd test sources are excluded before extraction because that unused subtree
contains symlinks; no link is materialized. Tests/programs/contrib are disabled.
The general archive/path restrictions were not relaxed.

## Windows evidence and reproduction

Let `B = C:\Users\bradg\Downloads\GetAll-R18` and
`W = B\evidence-r18\three-upstreams-20261127`.

- Original tree: `W\source-original\source-de8fc69`.
- Adapted sources: `W\native-1\game-src` and `deps-build`.
- Build products: `W\native-1\build`.
- Final build log: `W\native-1\metaforce-build-20261127T212731Z-a7e68b.log`.
- Final configure/build: exit 0, 1.594 s / 87.265 s, incremental after the
  precisely recorded header fixes. Earlier attempts are not represented as passes.
- Portable proof: `W\native-1\portable-check-1`.
- Runtime receipt: `portable-check-1\runtime-proof.json`.
- Interface log: `portable-check-1\runtime-interfaces.log`.
- Help logs: `portable-check-1\metaforce-help.log` and `metaforce-help-argv.log`.
- PE closure: `portable-check-1\pe-import-closure.json`, zero missing imports.

The replay scripts are `prepare_native_dependencies.py`, `build_metaforce.py`,
`prove_metaforce_runtime.py`, and the authored `metaforce_runtime_probe.cpp`.
They accept explicit base/work/source paths and operate inside new evidence areas.
`build_metaforce.py --resume` preserves completed objects and now gives each
configure/build run a unique log and result filename. The current build directory
must not be used as a fresh-run destination. The runtime proof likewise requires
a new direct-child output; its documented finish-only path validates prior
successful logs and unchanged PE hashes before completing the help assertion.

The first runtime attempt already passed its native interfaces and official help,
but the harness expected `--dvd` in help text. cxxopts hides this named option
because it is also positional. The assertion was corrected to the official
`<disc image>` usage, then the real parser was additionally exercised with
`--dvd <absent authored path> --user-dir <new owned path> --help`. It exited 0
without creating either path. No native game rebuild was repeated for this fix.

## Verified output

`metaforce.exe` is AMD64 PE, 18,186,752 bytes, SHA256
`dfb79798a507ac553d29fb2dda51939861d38f085c82dd77d8ec7534f112a249`.

The runtime needs nine local DLLs: `webgpu_dawn.dll`, `dxcompiler.dll`, `dxil.dll`,
`nod.dll`, `SDL3.dll`, `msvcp140.dll`, `msvcp140_atomic_wait.dll`,
`vcruntime140.dll`, and `vcruntime140_1.dll`. The private CRT copies retain their
already audited exact hashes. The authored probe is a separate evidence tool
and must not be treated as part of the game's launch output.

`metaforce-runtime-proof.json` records every PE hash/import, all 19 `res/` files,
and 62 preserved notice files. Four additional font notices remain at their
original paths inside `res/licenses/`. Notices include both Metaforce licenses,
all three gitlinks, dependency notices, explicit FreeType FTL/GPL texts, SQLite's
header notice, LLVM/MinGW notices, MSVC terms, and pinned Dawn/nod/DXC notices.
The four external notice pins are in `metaforce-notice-pins.json`.

The interface probe exited 0 after proving local SDL 3.4.10, a Dawn C instance
with the same portable descriptor/features, nod's defined invalid-disc result,
and real Borealis atomic replacement in an authored Unicode path. It also proved
that a failed replacement preserves source and existing destination. DLL module
locations were checked against the executable directory. The environment PATH
contained only Windows system directories.

## Media and integration boundary

This native build fixes `VERSION=1`, corresponding to GameCube Metroid Prime
`GM8E01` revision 0. The primary source pins `sys/main.dol` SHA1
`949c5ed7368aef547e0b0db1c3678f466e2afbff`. The selected ISO/GCM must pass the
Desktop's actual header, DOL, FST, bounds, and fingerprint checks before consent,
tools, or the preparation transaction. These checks are separate from this proof.

Launch is the real `metaforce.exe --dvd <selected-original> --user-dir <owned-data>`.
The original stays external and read-only; it must remain available for Jogar.
APPDATA/LOCALAPPDATA also need owned launch paths because Borealis initializes
its cache from SDL's preference path before applying `--user-dir`.

The remaining game validation needs the legitimate matching disc and a graphics
device: first boot, rendering/audio/input, and saves. This evidence does not claim
those tests occurred and does not itself promote the coverage count.
