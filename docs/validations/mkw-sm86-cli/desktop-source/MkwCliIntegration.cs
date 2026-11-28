using System.IO.Compression;
using System.Reflection;
using System.Runtime.ExceptionServices;
using System.Security.Cryptography;
using System.Text.Json;
using AllFix.Addons;
using AllFix.Desktop.Services;

internal static class MkwCliIntegration
{
    private static void Check(bool value, string message)
    {
        if (!value) throw new InvalidDataException("FAIL MKW CLI " + message);
        Console.WriteLine("PASS MKW CLI " + message);
    }

    private static void Reject<T>(Action action, string message) where T : Exception
    {
        try { action(); }
        catch (T) { Check(true, message); return; }
        throw new InvalidDataException("FAIL MKW CLI " + message);
    }

    private static string Hash(string path)
    {
        using var input = File.OpenRead(path);
        return Convert.ToHexString(SHA256.HashData(input)).ToLowerInvariant();
    }

    internal static void Policy()
    {
        var support = GameInstallationService.ReadMkwCliSupport(default);
        Check(GameInstallationService.MkwCliProfile != GameInstallationService.MkwProfile,
            "the new closed profile does not replace the legacy profile");
        Check(GameInstallationService.GetResumeMedia(GameInstallationService.MkwCliProfile) is { Length: 1 } one && one[0].Id == "original-game",
            "the CLI selector requests only the original directory");
        Check(GameInstallationService.GetResumeMedia(GameInstallationService.MkwProfile).Length == 2,
            "the legacy selector retains its independent shader-spec input");
        Check(GameInstallationService.RequiresLocalBuildConsent(GameInstallationService.MkwCliProfile),
            "the new profile retains native-build consent");
        var game = new LocalPreparationMediaReference("original-game", "directory", Path.GetFullPath("authored-original"),
            1, new string('0', 64), 1);
        var spec = new LocalPreparationMediaReference(GameInstallationService.MkwSpecId, "file", Path.GetFullPath("authored-spec.json"),
            1, new string('1', 64), 1);
        Check(GameInstallationService.ValidateMkwSelectionContract(GameInstallationService.MkwCliProfile, [game]),
            "the single-media contract selects the CLI branch");
        Check(!GameInstallationService.ValidateMkwSelectionContract(GameInstallationService.MkwProfile, [game, spec]),
            "legacy selections stay on the legacy branch");
        Reject<InvalidDataException>(() => GameInstallationService.ValidateMkwSelectionContract(GameInstallationService.MkwCliProfile, [game, spec]),
            "an old two-media state is not silently promoted");
        Reject<InvalidDataException>(() => GameInstallationService.ValidateMkwSelectionContract(GameInstallationService.MkwProfile, [game]),
            "the old profile cannot discard its shader specification");
        Reject<InvalidDataException>(() => GameInstallationService.ValidateMkwSelectionContract(GameInstallationService.MkwCliProfile, [spec]),
            "the original media cannot be replaced with an arbitrary file");
        var changed = support.ToArray();
        changed[changed.Length / 2] ^= 1;
        Reject<InvalidDataException>(() => GameInstallationService.ValidateMkwCliSupport(changed, default),
            "same-size source-package corruption is rejected");
        Reject<InvalidDataException>(() => GameInstallationService.ValidateMkwCliSupport(support[..^1], default),
            "a truncated source package is rejected");
        using var cancellation = new CancellationTokenSource();
        cancellation.Cancel();
        Reject<OperationCanceledException>(() => GameInstallationService.ReadMkwCliSupport(cancellation.Token),
            "cancelled preparation does not open or extract support");
        var target = Path.Combine(Path.GetTempPath(), "allfix-mkw-cancel-" + Guid.NewGuid().ToString("N"));
        Reject<OperationCanceledException>(() => GameInstallationService.ApplyMkwCliBackendSources(target, support, cancellation.Token),
            "cancelled source adaptation stops before writing");
        Check(!Directory.Exists(target) && !File.Exists(target), "cancellation left no destination");
        Console.WriteLine("MKW_CLI_POLICY_PASS");
    }

    private static byte[] Entry(ZipArchive archive, string name)
    {
        using var input = (archive.GetEntry(name) ?? throw new InvalidDataException("Missing fixed entry " + name)).Open();
        using var output = new MemoryStream();
        input.CopyTo(output);
        return output.ToArray();
    }

    private static string InsideFixture(string root, string relative)
    {
        var path = Path.GetFullPath(Path.Combine(root, relative.Replace('/', Path.DirectorySeparatorChar)));
        if (!path.StartsWith(Path.GetFullPath(root).TrimEnd(Path.DirectorySeparatorChar) + Path.DirectorySeparatorChar,
            StringComparison.OrdinalIgnoreCase)) throw new InvalidDataException("Invalid fixture source path.");
        return path;
    }

    private static void Run(string executable, string[] args, string directory, string environmentRoot, string log)
    {
        var type = typeof(GameInstallationService);
        var environment = (Dictionary<string, string>)type.GetMethod("CtrValidationEnvironment", BindingFlags.NonPublic | BindingFlags.Static)!
            .Invoke(null, [environmentRoot])!;
        try
        {
            type.GetMethod("RunNativeBuildStep", BindingFlags.NonPublic | BindingFlags.Static)!
                .Invoke(null, [executable, args, directory, environment, log, TimeSpan.FromMinutes(15), CancellationToken.None]);
        }
        catch (TargetInvocationException error) when (error.InnerException is { } actual)
        { ExceptionDispatchInfo.Capture(actual).Throw(); }
    }

    internal static void Native(string officialArchive, string kit, string cache, string work)
    {
        officialArchive = Path.GetFullPath(officialArchive); kit = Path.GetFullPath(kit);
        cache = Path.GetFullPath(cache); work = Path.GetFullPath(work);
        if (Directory.Exists(work) || File.Exists(work)) throw new InvalidDataException("MKW CLI proof requires a fresh work directory.");
        Check(new FileInfo(officialArchive).Length == 221949886 && Hash(officialArchive) ==
            "ff655d6dc566d315c9f33f96b9b94b7dc7e9c1b383091ed36c7f35921b6444c8", "the alias uses the exact official v0.1.18 kit");
        Directory.CreateDirectory(work);
        var output = Directory.CreateDirectory(Path.Combine(work, "game with spaces á")).FullName;
        using (var archive = ZipFile.OpenRead(officialArchive))
        {
            const string sourcePrefix = "mkw-recomp/setup/src/";
            int toolsChecked = 0, sourcesCopied = 0;
            foreach (var entry in archive.Entries.Where(x => !x.FullName.EndsWith('/')))
            {
                if (entry.FullName.StartsWith(sourcePrefix, StringComparison.Ordinal))
                {
                    var relative = "setup/src/" + entry.FullName[sourcePrefix.Length..];
                    var destination = InsideFixture(output, relative);
                    Directory.CreateDirectory(Path.GetDirectoryName(destination)!);
                    using var input = entry.Open();
                    using var file = new FileStream(destination, FileMode.CreateNew, FileAccess.Write, FileShare.None);
                    input.CopyTo(file);
                    sourcesCopied++;
                }
                else if (entry.FullName.StartsWith("mkw-recomp/setup/python/", StringComparison.Ordinal) ||
                         entry.FullName.StartsWith("mkw-recomp/setup/glslc/", StringComparison.Ordinal))
                {
                    var path = InsideFixture(kit, entry.FullName["mkw-recomp/".Length..]);
                    using var input = entry.Open();
                    var expected = Convert.ToHexString(SHA256.HashData(input)).ToLowerInvariant();
                    if (new FileInfo(path).Length != entry.Length || Hash(path) != expected)
                        throw new InvalidDataException("The reused official Python/compiler tree changed: " + entry.FullName);
                    toolsChecked++;
                }
            }
            Check(sourcesCopied > 100 && toolsChecked > 10, "only official source is copied; the existing private Python/compiler closure is verified and reused");
        }
        var support = GameInstallationService.ReadMkwCliSupport(default);
        using var supportStream = new MemoryStream(support, false);
        using var zip = new ZipArchive(supportStream, ZipArchiveMode.Read);
        using var document = JsonDocument.Parse(Entry(zip, "manifest.json"));
        var overlays = document.RootElement.GetProperty("overlays").EnumerateArray().ToArray();
        var first = InsideFixture(output, "setup/src/" + overlays[0].GetProperty("path").GetString()!);
        var last = InsideFixture(output, "setup/src/" + overlays[^1].GetProperty("path").GetString()!);
        var beforeFirst = Hash(first); var beforeLast = File.ReadAllBytes(last);
        var altered = beforeLast.ToArray(); altered[altered.Length / 2] ^= 1;
        File.WriteAllBytes(last, altered);
        Reject<InvalidDataException>(() => GameInstallationService.ApplyMkwCliBackendSources(output, support, default),
            "a changed official source is rejected before any overlay is written");
        Check(Hash(first) == beforeFirst && File.ReadAllBytes(last).SequenceEqual(altered), "rejected preimages remain untouched");
        File.WriteAllBytes(last, beforeLast);
        var engine = new GameInstallationService(new GameInstallationStateStore(Path.Combine(work, "states")));
        engine.PrepareMkwCliBackend(output, cache, work, Console.WriteLine, default);
        GameInstallationService.ValidateMkwCliInstalled(output, default);
        Check(true, "the real provider stages and verifies decoder, CLI, source overlays and notices");
        var descriptor = Path.Combine(output, "sm86/instructions.json");
        var originalDescriptor = File.ReadAllBytes(descriptor);
        File.WriteAllText(descriptor, "{}");
        Reject<InvalidDataException>(() => GameInstallationService.ValidateMkwCliInstalled(output, default),
            "installed descriptor corruption is rejected before publication or launch");
        File.WriteAllBytes(descriptor, originalDescriptor);
        var listPath = Path.Combine(output, "setup/src/FILES");
        var listing = File.ReadAllBytes(listPath);
        File.WriteAllText(listPath, "tools/shaders/translate.py\n");
        Reject<InvalidDataException>(() => GameInstallationService.ValidateMkwCliInstalled(output, default),
            "a resume identity missing the added modules is rejected");
        File.WriteAllBytes(listPath, listing);

        var supportPath = Path.Combine(work, "source-support.zip");
        var proof = Path.Combine(work, "prove_backend.py");
        var fixtures = Path.Combine(work, "fixtures.json");
        File.WriteAllBytes(supportPath, support);
        File.WriteAllBytes(proof, Entry(zip, "proof/prove_backend.py"));
        File.WriteAllBytes(fixtures, Entry(zip, "proof/fixtures.json"));
        var proofWork = Directory.CreateDirectory(Path.Combine(work, "authored-pipeline")).FullName;
        Run(Path.Combine(kit, "setup/python/python.exe"), ["-I", proof, "--kit", kit, "--support", supportPath,
            "--support-sha256", GameInstallationService.MkwCliSupportHash, "--nvdisasm", Path.Combine(output, "sm86/nvdisasm/nvdisasm.exe"),
            "--fixtures", fixtures, "--work", proofWork, "--staged-game", output], proofWork, work, Path.Combine(work, "pipeline.log"));
        using var result = JsonDocument.Parse(File.ReadAllText(Path.Combine(proofWork, "result.json")));
        Check(result.RootElement.GetProperty("status").GetString() == "MKW_NORMAL_CLI_NATIVE_PASS" &&
            result.RootElement.GetProperty("programs").GetInt32() >= 12 &&
            result.RootElement.GetProperty("negative_translation_exit").GetInt32() != 0,
            "actual shaderstep/extract/Decoder/translate/pack succeeds and real lowering errors fail");
        Check(!result.RootElement.GetProperty("commercial_media").GetBoolean() && !result.RootElement.GetProperty("game_boot").GetBoolean(),
            "the proof contains only authored shaders and does not claim game boot");
        Console.WriteLine("MKW_CLI_NATIVE_PASS");
    }
}
