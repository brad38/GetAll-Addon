using System.IO;
using System.IO.Compression;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using AllFix.Addons;

namespace AllFix.Desktop.Services;

internal sealed partial class GameInstallationService
{
    internal const string MkwCliProfile = "mkw-0.1.18-cli-prepare";
    internal const string MkwCliSupportHash = "1c79d30594951495f210a349da05aabe0e240f0189dba87c95a78da73a4500ce";
    private const int MkwCliSupportBytes = 63227;
    private const string MkwCliResource = "MkwSm86.cli-support.zip";
    private const string MkwCliConsumer = "006d48de08849495e01e151602690d0ec322af82";
    private const string MkwNvdisasmHash = "f0ab98df225b9f2568e8f56c24a919a4e1362425fb7c02101afbf85022324add";
    private const string MkwNvdisasmLicenseHash = "e2c71babfd18a8e69542dd7e9ca018f9caa438094001a58e6bc4d8c999bf0d07";
    private static readonly ToolchainPackage MkwNvdisasm = new(
        "mkw-nvdisasm-12.8.90", "cuda_nvdisasm-windows-x86_64-12.8.90-archive.zip",
        "https://developer.download.nvidia.com/compute/cuda/redist/cuda_nvdisasm/windows-x86_64/cuda_nvdisasm-windows-x86_64-12.8.90-archive.zip",
        5368805, "a348209c803fa67b7bc216a5b4d7a6f9a117ccc60a8c567eb94cf25ba737ec47",
        "cuda_nvdisasm-windows-x86_64-12.8.90-archive/");

    internal static RecipePreparationMedia[] MkwCliMedia() => [MkwMedia()[0]];

    internal static byte[] ReadMkwCliSupport(CancellationToken token)
    {
        token.ThrowIfCancellationRequested();
        using var input = typeof(GameInstallationService).Assembly.GetManifestResourceStream(MkwCliResource)
            ?? throw new InvalidDataException("MKW: suporte de shaders incorporado ausente.");
        if (input.Length != MkwCliSupportBytes)
            throw new InvalidDataException("MKW: tamanho do suporte de shaders incorreto.");
        var bytes = new byte[MkwCliSupportBytes];
        input.ReadExactly(bytes);
        ValidateMkwCliSupport(bytes, token);
        return bytes;
    }

    internal static void ValidateMkwCliSupport(byte[] bytes, CancellationToken token)
    {
        token.ThrowIfCancellationRequested();
        if (bytes.Length != MkwCliSupportBytes ||
            !WindowsPaths.Equals(Convert.ToHexString(SHA256.HashData(bytes)), MkwCliSupportHash))
            throw new InvalidDataException("MKW: suporte de shaders incorporado alterado.");
    }

    private static byte[] ReadMkwCliEntry(ZipArchive zip, string name)
    {
        var entry = zip.GetEntry(name) ?? throw new InvalidDataException("MKW: suporte incompleto: " + name);
        if (entry.Length is <= 0 or > 1024 * 1024 ||
            ((entry.ExternalAttributes >> 16) & 0xf000) == 0xa000 ||
            (entry.ExternalAttributes & (int)FileAttributes.ReparsePoint) != 0)
            throw new InvalidDataException("MKW: entrada de suporte invalida.");
        using var input = entry.Open();
        var bytes = new byte[checked((int)entry.Length)];
        input.ReadExactly(bytes);
        return bytes;
    }

    private static Dictionary<string, byte[]> ReadMkwCliMembers(ZipArchive zip, JsonElement manifest,
        CancellationToken token)
    {
        if (manifest.GetProperty("format").GetInt32() != 1 ||
            manifest.GetProperty("consumer_commit").GetString() != MkwCliConsumer)
            throw new InvalidDataException("MKW: contrato de shaders desconhecido.");
        var files = new Dictionary<string, byte[]>(StringComparer.Ordinal);
        foreach (var record in manifest.GetProperty("files").EnumerateArray())
        {
            token.ThrowIfCancellationRequested();
            var name = record.GetProperty("path").GetString()!;
            var bytes = ReadMkwCliEntry(zip, name);
            if (bytes.LongLength != record.GetProperty("bytes").GetInt64() ||
                !WindowsPaths.Equals(Convert.ToHexString(SHA256.HashData(bytes)), record.GetProperty("sha256").GetString()) ||
                !files.TryAdd(name, bytes))
                throw new InvalidDataException("MKW: arquivo de suporte alterado ou duplicado.");
        }
        if (zip.Entries.Count != files.Count + 1 || zip.Entries.Any(entry =>
            entry.FullName != "manifest.json" && !files.ContainsKey(entry.FullName)))
            throw new InvalidDataException("MKW: arquivo inesperado no suporte.");
        return files;
    }

    private static void CheckMkwCliFile(string path, long bytes, string hash, CancellationToken token)
    {
        EnsureOrdinaryPath(path);
        using var input = File.OpenRead(path);
        if (input.Length != bytes || !WindowsPaths.Equals(Digest(input, token), hash))
            throw new InvalidDataException("MKW: arquivo fixado alterado: " + Path.GetFileName(path));
    }

    internal static void ApplyMkwCliBackendSources(string output, byte[] support, CancellationToken token)
    {
        ValidateMkwCliSupport(support, token);
        using var stream = new MemoryStream(support, false);
        using var zip = new ZipArchive(stream, ZipArchiveMode.Read);
        using var document = JsonDocument.Parse(ReadMkwCliEntry(zip, "manifest.json"));
        var manifest = document.RootElement;
        var files = ReadMkwCliMembers(zip, manifest, token);
        var source = Inside(output, "setup/src");
        var overlays = manifest.GetProperty("overlays").EnumerateArray().ToArray();
        var modules = manifest.GetProperty("modules").EnumerateArray().Select(x => x.GetString()!).ToArray();
        // Check every original and every destination before changing the owned
        // source copy. A different port never receives a partial adaptation.
        foreach (var record in overlays)
        {
            token.ThrowIfCancellationRequested();
            var path = Inside(source, record.GetProperty("path").GetString()!);
            EnsureOrdinaryPath(path);
            using var input = File.OpenRead(path);
            if (input.Length > 1024 * 1024 ||
                !WindowsPaths.Equals(Digest(input, token), record.GetProperty("before_sha256").GetString()))
                throw new InvalidDataException("MKW: revisao de fonte diferente do perfil fechado.");
        }
        foreach (var relative in modules)
            if (Exists(Inside(source, relative)))
                throw new InvalidDataException("MKW: destino do novo decoder ja existe.");
        var descriptor = Inside(output, "sm86/instructions.json");
        if (Exists(descriptor)) throw new InvalidDataException("MKW: descritor anterior nao sera promovido silenciosamente.");
        var listPath = Inside(source, "FILES");
        EnsureOrdinaryPath(listPath);
        if (new FileInfo(listPath).Length > 2 * 1024 * 1024)
            throw new InvalidDataException("MKW: lista de fontes fora dos limites.");
        var names = File.ReadAllLines(listPath, Encoding.UTF8);
        foreach (var record in overlays)
        {
            token.ThrowIfCancellationRequested();
            var relative = record.GetProperty("path").GetString()!;
            var bytes = files["overlays/" + relative];
            if (!WindowsPaths.Equals(Convert.ToHexString(SHA256.HashData(bytes)), record.GetProperty("after_sha256").GetString()))
                throw new InvalidDataException("MKW: overlay de fonte alterado.");
            File.WriteAllBytes(Inside(source, relative), bytes);
        }
        foreach (var relative in modules)
        {
            token.ThrowIfCancellationRequested();
            var bytes = files["files/" + relative];
            using var input = new MemoryStream(bytes, false);
            CopyNew(input, Inside(source, relative), bytes.Length, token);
        }
        foreach (var entry in files.Where(x => x.Key.StartsWith("notices/", StringComparison.Ordinal)))
        {
            token.ThrowIfCancellationRequested();
            using var input = new MemoryStream(entry.Value, false);
            CopyNew(input, Inside(output, "licenses/MkwSm86/" + entry.Key["notices/".Length..]), entry.Value.Length, token);
        }
        var descriptorBytes = files["configuration/instructions.json"];
        using (var input = new MemoryStream(descriptorBytes, false)) CopyNew(input, descriptor, descriptorBytes.Length, token);
        token.ThrowIfCancellationRequested();
        File.WriteAllText(listPath, string.Join("\n", names.Concat(modules).Distinct(StringComparer.Ordinal)) + "\n", new UTF8Encoding(false));
    }

    internal void PrepareMkwCliBackend(string output, string cache, string work,
        Action<string> report, CancellationToken token)
    {
        var support = ReadMkwCliSupport(token);
        ApplyMkwCliBackendSources(output, support, token);
        report("Preparando o tradutor privado de shaders SM86.");
        var tool = ExtractConsolePackage(MkwNvdisasm, cache, Inside(work, "mkw-normal-nvdisasm"), token);
        using (var input = File.OpenRead(Inside(tool, "bin/nvdisasm.exe")))
            PublishVerifiedFile(input, Inside(output, "sm86/nvdisasm/nvdisasm.exe"), 5947392, MkwNvdisasmHash, token);
        using (var input = File.OpenRead(Inside(tool, "LICENSE")))
            PublishVerifiedFile(input, Inside(output, "sm86/nvdisasm/LICENSE"), 63021, MkwNvdisasmLicenseHash, token);
        ValidateMkwCliInstalled(output, token);
    }

    internal static void ValidateMkwCliInstalled(string output, CancellationToken token)
    {
        var support = ReadMkwCliSupport(token);
        using var stream = new MemoryStream(support, false);
        using var zip = new ZipArchive(stream, ZipArchiveMode.Read);
        using var document = JsonDocument.Parse(ReadMkwCliEntry(zip, "manifest.json"));
        var manifest = document.RootElement;
        var files = ReadMkwCliMembers(zip, manifest, token);
        foreach (var record in manifest.GetProperty("files").EnumerateArray())
        {
            token.ThrowIfCancellationRequested();
            var name = record.GetProperty("path").GetString()!;
            string? relative = name.StartsWith("files/", StringComparison.Ordinal) ? "setup/src/" + name[6..] :
                name.StartsWith("overlays/", StringComparison.Ordinal) ? "setup/src/" + name[9..] :
                name.StartsWith("notices/", StringComparison.Ordinal) ? "licenses/MkwSm86/" + name[8..] :
                name == "configuration/instructions.json" ? "sm86/instructions.json" : null;
            if (relative is not null)
                CheckMkwCliFile(Inside(output, relative), record.GetProperty("bytes").GetInt64(),
                    record.GetProperty("sha256").GetString()!, token);
        }
        var executable = Inside(output, "sm86/nvdisasm/nvdisasm.exe");
        CheckMkwCliFile(executable, 5947392, MkwNvdisasmHash, token);
        ValidateAmd64Image(executable, false);
        CheckMkwCliFile(Inside(output, "sm86/nvdisasm/LICENSE"), 63021, MkwNvdisasmLicenseHash, token);
        var listPath = Inside(output, "setup/src/FILES");
        EnsureOrdinaryPath(listPath);
        if (new FileInfo(listPath).Length > 2 * 1024 * 1024)
            throw new InvalidDataException("MKW: lista instalada fora dos limites.");
        var names = File.ReadAllLines(listPath).ToHashSet(StringComparer.Ordinal);
        if (manifest.GetProperty("modules").EnumerateArray().Any(item => !names.Contains(item.GetString()!)))
            throw new InvalidDataException("MKW: identidade de retomada omite o decoder instalado.");
    }
}
