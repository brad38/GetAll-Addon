# MKW local alias: actual Desktop service proof

This optional offline runner loads the real `AllFix.dll` and invokes its
`StoreDownloadService.ResolveAsync` and `StoreCatalogService.ReadAsync` by
reflection. It does not substitute either service, HTTP, paths or caches. The
central `MkwCliReleaseIntegration.Policy` remains independent of these services.

Build this package-free runner only in the coordinator's allocated build window.
After the final Desktop build, use the runner's framework-dependent runtime
configuration. The self-contained Desktop runtimeconfig lists included frameworks
and is not a framework-dependent test host. AssemblyDependencyResolver reads the
real Desktop dependency manifest and resolves adjacent dependencies. No WPF references are added to this
runner or to the central harness. Use the normal build output with `AllFix.dll`,
its `.deps.json`, `.runtimeconfig.json` and adjacent dependencies, before the
single-file publication is bundled.

```powershell
dotnet build '<proof>\StoreAssemblyProof.csproj' -c Release --configfile '<proof>\NuGet.Config' -o '<new-proof-output>'
dotnet exec --runtimeconfig '<new-proof-output>\StoreAssemblyProof.runtimeconfig.json' '<new-proof-output>\StoreAssemblyProof.dll' '<desktop-output>\AllFix.dll'
```

The runner checks the real assembly's constants, exact asset resolution,
repository case handling, twelve altered assets, and local catalog resolution
with and without refresh, and the actual cache merge with malformed entries and
both local and upstream tags. It subscribes to the real HTTP diagnostics and fails
if a request starts. No upstream release listing, download, kit extraction,
media access or game execution is requested. Each service call is limited to
five seconds; a loader error or timeout fails the proof.

Expected success marker: `MKW_CLI_STORE_ASSEMBLY_PASS checks=20`. The output also
records the SHA-256 of the Desktop assembly actually tested. This is prepared
test code; no execution result is claimed here.
