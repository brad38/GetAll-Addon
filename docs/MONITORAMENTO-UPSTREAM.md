# GetAll-Addon — Relatório Técnico de Monitoramento Upstream

- **Escopo avaliado:** `all` (142 repositórios consultados, 145 projetos no catálogo `AllFix-Repo`)
- **Receitas no `index.json`:** 92
- **Fingerprint das novidades:** `dc7dfcc2eec5`

## Novos projetos identificados no AllFix-Repo

| Jogo | Projeto ID | Repositório | Provider |
|---|---|---|---|
| `burnout-3-takedown` | `burnout3-recomp` | `sp00nznet/burnout3` | `github` |
| `donkey-kong-bananza` | `dkb-pc-recomp` | `Lucas-blip-png/dkb-pc-recomp` | `github` |
| `forza-horizon` | `fh1-reimagined` | `FH1-ReImagined/ForzaHorizon1-ReImagined` | `github` |
| `gears-of-war-2` | `gears-of-war-2-pc-port` | `santiquiroz/gears-of-war-2-pc-port` | `github` |
| `god-hand` | `god-hand-rearmed` | `God-Hand-Rearmed/God-Hand-Rearmed` | `github` |
| `god-of-war-2005` | `god-of-war-recomp` | `KIexster/god-of-war-recomp` | `github` |
| `gran-turismo-4` | `gt4recomp` | `moesuito/gt4-staticrecomp` | `github` |
| `gran-turismo-5` | `gt5-recomp` | `MormonFTP-hub/gt5-recomp` | `github` |
| `grand-theft-auto-liberty-city-stories-vice-city-stories` | `gta-stories-recompiled` | `batinium/gta-stories-recompiled` | `github` |
| `the-legend-of-zelda-ocarina-of-time` | `hookshot-zelda-oot-port` | `ZuanCrisp/Zelda-OOT-Port` | `github` |
| `infamous-second-son` | `iss-pc` | `hayatog/iss_pc` | `github` |
| `the-legend-of-zelda-link-s-awakening` | `lasrecomp` | `peiikai/LASRecomp` | `github` |
| `lost-odyssey` | `lost-odyssey-recomp` | `freefrank/LostOdysseyRecomp` | `github` |
| `mario-kart-world` | `mkw-recomp` | `adriadam10/mkw-recomp` | `github` |
| `ninja-gaiden-ii` | `ng2recomp` | `gamboozino/ng2recomp` | `github` |
| `halo-combat-evolved` | `opence` | `OpenCommunityEdition/OpenCE` | `github` |
| `project-gotham-racing-4` | `pgr4-recomp` | `beatrixzy/PGR4-Recomp` | `github` |
| `pt` | `pt-pc` | `LoreanXavier/pt-pc` | `github` |
| `gran-turismo-7` | `rygt-gt7` | `RyGT-Team/RyGT` | `github` |
| `the-legend-of-zelda-breath-of-the-wild` | `savagewindrecomp` | `revivedx/savagewindrecomp` | `github` |
| `shadow-of-the-colossus` | `shadow-of-the-colossus-pc` | `AjncSystem/ShadowOfTheColossus-PC` | `github` |
| `god-of-war-iii-remastered` | `spartanport` | `FelipePrado0/SpartanPort` | `github` |
| `ssx-2012` | `ssx-recomp` | `AmarilloNL/ssx-recomp` | `github` |
| `super-mario-odyssey` | `super-odyssey-pc-recomp` | `Simon3Sarkis/super-odyssey-pc-recomp` | `github` |
| `the-last-guardian` | `tlg-pc` | `HayatoG/tlg_pc` | `github` |
| `the-legend-of-zelda-tears-of-the-kingdom` | `totk-pc-recomp` | `valentderah/totk-pc-recomp` | `github` |

## Pendências técnicas e atualizações que exigem revisão manual

| Projeto | Classe/Origem | Nova tag | Asset Windows | Motivo técnico / Evidência |
|---|---|---|---|---|
| `shadow-of-the-colossus-pc` | `NEW` | `v0.77` | `SotC-PC.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `79f6f4be4a6829b7...`, EXEs: `SotC-PC/SotC.exe, SotC-PC/bin/bb-gpu-capabilities.exe, SotC-PC/bin/bb-probe.exe`) |
| `ssx-recomp` | `NEW` | `v2.0.0` | `ssx-recomp-v2.0.0-Windows-x64.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `5dac697704a9121b...`, EXEs: `ssx-recomp.exe`) |
| `mega-man-legends-modernization-project` | `B` | `v0.9.7-beta` | `—` | Catalog project has a newer or newly added release not yet covered by a recipe |
| `fh1-reimagined` | `NEW` | `v0.4.2` | `—` | Catalog project has a newer or newly added release not yet covered by a recipe |
| `spartanport` | `NEW` | `windows-v3.2.1` | `spartanport-windows.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `9ecab74c862eb421...`, EXEs: `spartanport-windows/Play SpartanPort.exe, spartanport-windows/SpartanPort.exe, spartanport-windows/bin/spartanport-gpu-capabilities.exe`, SDK paths inválidos: `spartanport-windows/Play SpartanPort.exe`) |
| `god-hand-rearmed` | `NEW` | `v0.6.9.6` | `GHR-v0.6.9.6-Windows-x64.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `f8de4de9ba2414e2...`, EXEs: `God Hand Rearmed/GHR.exe`, SDK paths inválidos: `God Hand Rearmed/GHR.exe, God Hand Rearmed/LICENSE`) |
| `tlg-pc` | `NEW` | `v2026.11.14-ee3327d` | `tlg-windows-x86_64.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `08fdff781d79ec1d...`, EXEs: `tlg-windows-x86_64/Play The Last Guardian.exe, tlg-windows-x86_64/The Last Guardian (classic).exe, tlg-windows-x86_64/The Last Guardian.exe`, SDK paths inválidos: `tlg-windows-x86_64/Play The Last Guardian.exe, tlg-windows-x86_64/The Last Guardian (classic).exe`) |
| `pt-pc` | `NEW` | `v1.1.2` | `P.T.PC.Port-portable-windows.zip` | Catalog project has a newer or newly added release not yet covered by a recipe |
| `dkb-pc-recomp` | `NEW` | `v0.5.2` | `DKB-Setup-0.5.2+a58af05-windows.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `28536fe035ee710a...`, EXEs: `DKB-Setup/DKB-Setup.exe, DKB-Setup/bin/dkb_xlate.exe, DKB-Setup/bin/ninja.exe`, SDK paths inválidos: `DKB-Setup/python/Lib/site-packages/.lock, DKB-Setup/python/Lib/site-packages/numpy/f2py/tests/src/assumed_shape/.f2py_f2cmap`) |
| `gt5-recomp` | `NEW` | `v0.1.116` | `—` | Catalog project has a newer or newly added release not yet covered by a recipe |
| `opence` | `NEW` | `build-387` | `halo-windows-release.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `60c8fc8fc6596226...`, EXEs: `halo.exe`) |
| `redriver2` | `7.4-rc2` | `8.0` | `REDRIVER2_Win32_Release.zip` | Incompatible package layout (missing required_files in ZIP: Launcher.exe) (ZIP SHA-256: `ddc0106858ad91c3...`) |
| `rygt-gt7` | `NEW` | `rygt-2026-11-23` | `RyGT-2026-11-23.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `c987c09167477ead...`, EXEs: `RyGT-ci-889c5a7e/RyGTLauncher.exe, RyGT-ci-889c5a7e/converter/ryty.exe, RyGT-ci-889c5a7e/server/RyGTServer.exe`) |
| `gsrecomp` | `0.8.4` | `0.9` | `GoldenSunRecompiled-0.9-windows.zip` | SDK 1.2.0 path grammar rejects files: Golden Sun Recompiled/GoldenSunLauncher.exe, Golden Sun Recompiled/SDL2.dll, Golden Sun Recompiled/games/The Broken Seal/GoldenSunRecomp.exe, Golden Sun Recompiled/games/The Lost Age/TLARecomp.exe (ZIP SHA-256: `16a964b843ddb6c9...`) |
| `super-odyssey-pc-recomp` | `NEW` | `v1.0.2` | `Super.Odyssey.PC.Recomp-1.0.2-windows.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `0598372ccf9b4837...`, EXEs: `Super Odyssey PC Recomp/SuperOdysseyRecomp.exe, Super Odyssey PC Recomp/odysseygen/python.exe, Super Odyssey PC Recomp/zig/zig.exe`, SDK paths inválidos: `Super Odyssey PC Recomp/LICENSE, Super Odyssey PC Recomp/NvLowLatencyVk.dll`) |
| `silent-hill-native-pc-port` | `crossplatform-beta` | `uwp-alpha-1` | `—` | New release detected without an identifiable Windows .zip asset |
| `autotmc-auto-tmc` | `1.0.2` | `1.0.1` | `—` | New release detected without an identifiable Windows .zip asset |
| `hookshot-zelda-oot-port` | `NEW` | `v3.0.2` | `Hookshot-v3.0.2-Windows-x64.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `7ce0fb9d05b9cfed...`, EXEs: `HookshotBuilder.exe`) |
| `mkw-recomp` | `NEW` | `v0.1.18` | `mkw-recomp-0.1.18-windows-x64-noavx2.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `7ce3148d23a2fe25...`, EXEs: `mkw-recomp/mkw.exe, mkw-recomp/setup/clang/clang.exe, mkw-recomp/setup/glslc/Library/bin/glslang.exe`, SDK paths inválidos: `mkw-recomp/setup/python/Lib/site-packages/numpy/f2py/tests/src/assumed_shape/.f2py_f2cmap, mkw-recomp/setup/python/Lib/site-packages/numpy/f2py/tests/src/f2cmap/.f2py_f2cmap`) |
| `gta-stories-recompiled` | `NEW` | `v0.3.2` | `GTA-Stories-Recompiled-0.3.2-windows.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `fccbaa7a6e0ef9c6...`, EXEs: `GTA-Stories-Recompiled-0.3.2-windows/GTAStoriesLauncher.exe, GTA-Stories-Recompiled-0.3.2-windows/deps/libdwarf/test/testobjLE32PE.exe, GTA-Stories-Recompiled-0.3.2-windows/python/python.exe`, SDK paths inválidos: `GTA-Stories-Recompiled-0.3.2-windows/.gitattributes, GTA-Stories-Recompiled-0.3.2-windows/.github/ISSUE_TEMPLATE/bug_report.yml`) |
| `pgr4-recomp` | `NEW` | `v2.0.2` | `PGR4-Recomp-v2.0.2.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `853416bed60e6d07...`, EXEs: `pgr4_launcher.exe, pgr4_recompiled.exe`) |
| `lost-odyssey-recomp` | `NEW` | `v1.2.0` | `LostOdysseyRecomp-windows-x64-v1.2.0.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `31ac7b54544cfa4e...`, EXEs: `LostOdysseyRecomp-windows-x64-v1.2.0/LostOdysseyRecomp.exe`) |
| `ng2recomp` | `NEW` | `v0.8.0` | `NinjaGaiden2-windows-x64.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `78c61849c727c49f...`, EXEs: `NinjaGaiden2/ng2-avx2.exe, NinjaGaiden2/ng2.exe`) |
| `iss-pc` | `NEW` | `v1.0` | `infamous-windows-x86_64.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `25cf4c6a27547b0d...`, EXEs: `infamous-windows-x86_64/Play inFAMOUS Second Son.exe, infamous-windows-x86_64/inFAMOUS Second Son (classic).exe, infamous-windows-x86_64/inFAMOUS Second Son.exe`, SDK paths inválidos: `infamous-windows-x86_64/Play inFAMOUS Second Son.exe, infamous-windows-x86_64/_internal/PySide6/qml/QtQuick/Dialogs/quickimpl/qml/+Fusion/ColorDialog.qml`) |
| `gt4recomp` | `NEW` | `v1.3.0-rc16` | `GT4Recomp-1.3.0-rc16-portable.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `7b32e66e4e5c9962...`, EXEs: `GT4Recomp.exe, game/gt4-spec2.exe, game/gt4.exe`) |
| `lasrecomp` | `NEW` | `v0.6.1` | `LAS.Recomp-v0.6.1-windows.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `6ca08b02b6330a77...`, EXEs: `LAS Recomp/lasgen/lasgen.exe, LAS Recomp/lasrecomp.exe, LAS Recomp/rando-gen/rando-gen.exe`, SDK paths inválidos: `LAS Recomp/Baloo2-OFL.txt, LAS Recomp/Baloo2-SemiBold.ttf`) |
| `savagewindrecomp` | `NEW` | `v0.6.0-alpha.6` | `SavageWind-0.6.0-alpha.6-windows.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `9bfc05217ed7e690...`, EXEs: `Savage Wind/SW Update.exe, Savage Wind/Savage Wind Configuration.exe, Savage Wind/savagewind.exe`, SDK paths inválidos: `Savage Wind/AMD-FidelityFX-DLL-LICENSE.txt, Savage Wind/FidelityFX-LICENSE.txt`) |
| `gears-of-war-2-pc-port` | `NEW` | `v0.4.8` | `gow2-recomp-0.4.8-win64.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `af858040f87fa8f9...`, EXEs: `gow2-recomp-0.4.8-win64/gow2.exe, gow2-recomp-0.4.8-win64/keycaps/keycaps-pack.exe, gow2-recomp-0.4.8-win64/tools/realesrgan/realesrgan-ncnn-vulkan.exe`, SDK paths inválidos: `gow2-recomp-0.4.8-win64/Build keycap pack.cmd`) |
| `burnout3-recomp` | `NEW` | `v0.1.0` | `—` | Catalog project has a newer or newly added release not yet covered by a recipe |
| `totk-pc-recomp` | `NEW` | `v0.5.0` | `TotK-Setup-0.5.0-windows.zip` | Catalog project has a newer or newly added release not yet covered by a recipe (ZIP SHA-256: `201b08348ffb72c7...`, EXEs: `TotK-Setup-0.5.0-windows/TotK-Setup.exe, TotK-Setup-0.5.0-windows/bin/hactool.exe, TotK-Setup-0.5.0-windows/bin/ninja.exe`, SDK paths inválidos: `TotK-Setup-0.5.0-windows/python/Lib/site-packages/.lock, TotK-Setup-0.5.0-windows/python/Lib/site-packages/numpy/f2py/tests/src/assumed_shape/.f2py_f2cmap`) |
| `re-blue` | `nightly-v1.4.0-d187173d8-s44b7fdc5` | `v1.3.1` | `reblue-1.3.1-win-amd64.zip` | Incompatible package layout (missing required_files in ZIP: SDL3.dll, rexapp.dll) (ZIP SHA-256: `bf638798c2bef5f0...`) |
