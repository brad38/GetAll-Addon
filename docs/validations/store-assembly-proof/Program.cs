using System.Diagnostics;
using System.Reflection;
using System.Runtime.ExceptionServices;
using System.Runtime.Loader;
using System.Security.Cryptography;
using System.Text.Json;

// This runner loads the actual Desktop assembly. It neither copies service
// implementations nor substitutes HTTP handlers, resolution, paths or caches.
internal static class Program
{
    private const string Repository = "adriadam10/mkw-recomp";
    private const string Tag = "v0.1.18-allfix-cli";
    private const string FileName = "mkw-recomp-0.1.18-windows-x64.zip";
    private const long Size = 221949886;
    private const string Sha256 = "ff655d6dc566d315c9f33f96b9b94b7dc7e9c1b383091ed36c7f35921b6444c8";
    private const string SourceUrl = "https://github.com/adriadam10/mkw-recomp/releases/tag/v0.1.18";
    private const string AssetUrl = "https://github.com/adriadam10/mkw-recomp/releases/download/v0.1.18/" + FileName;

    private static async Task<int> Main(string[] args)
    {
        try
        {
            if (args.Length != 1) throw new ArgumentException("Pass the absolute path of the real Desktop AllFix.dll.");
            if (!Path.IsPathFullyQualified(args[0])) throw new ArgumentException("The Desktop assembly path must be absolute.");
            var path = Path.GetFullPath(args[0]);
            if (!File.Exists(path) || Path.GetFileName(path) != "AllFix.dll")
                throw new FileNotFoundException("The actual AllFix.dll is required.", path);
            var resolver = new AssemblyDependencyResolver(path);
            AssemblyLoadContext.Default.Resolving += (_, name) =>
            {
                var resolved = resolver.ResolveAssemblyToPath(name);
                return resolved is null ? null : AssemblyLoadContext.Default.LoadFromAssemblyPath(resolved);
            };
            using var monitor = new HttpMonitor();
            var assembly = AssemblyLoadContext.Default.LoadFromAssemblyPath(path);
            var passed = 0;
            void Check(bool ok, string label)
            {
                if (!ok) throw new InvalidDataException("FAIL MKW store assembly: " + label);
                passed++;
                Console.WriteLine("PASS MKW store assembly: " + label);
            }
            Check(assembly.GetName().Name == "AllFix", "real Desktop assembly loaded");
            using (var stream = File.OpenRead(path))
                Console.WriteLine("DESKTOP_ASSEMBLY_SHA256=" + Convert.ToHexString(SHA256.HashData(stream)).ToLowerInvariant());

            const string prefix = "AllFix.Desktop.Services.";
            var download = assembly.GetType(prefix + "StoreDownloadService", throwOnError: true)!;
            var catalog = assembly.GetType(prefix + "StoreCatalogService", throwOnError: true)!;
            var trusted = assembly.GetType(prefix + "StoreTrustedMkwCli", throwOnError: true)!;
            object Constant(string name) => trusted.GetField(name, BindingFlags.Static | BindingFlags.NonPublic)!
                .GetRawConstantValue()!;
            Check((string)Constant("Repository") == Repository && (string)Constant("Tag") == Tag &&
                  (string)Constant("AssetUrl") == AssetUrl && (string)Constant("SourceUrl") == SourceUrl &&
                  (string)Constant("FileName") == FileName && (long)Constant("Size") == Size &&
                  (string)Constant("Sha256") == Sha256,
                "loaded Desktop contains the reviewed alias and immutable official pin");
            var resolve = Method(download, "ResolveAsync", [typeof(string), typeof(string), typeof(string), typeof(bool)]);
            var read = Method(catalog, "ReadAsync", [typeof(string), typeof(string), typeof(bool), typeof(string)]);

            foreach (var repository in new[] { Repository, Repository.ToUpperInvariant() })
            {
                var asset = await InvokeAsync(resolve, [repository, Tag, AssetUrl, false]);
                Check(((Uri)Property(asset, "Url")).AbsoluteUri == AssetUrl &&
                      (string)Property(asset, "Name") == FileName && (long)Property(asset, "Size") == Size &&
                      (string)Property(asset, "Sha256") == Sha256,
                    "real resolver accepts the exact pin for " + repository);
            }
            var altered = new[]
            {
                SourceUrl,
                AssetUrl.Replace("https://", "http://", StringComparison.Ordinal),
                AssetUrl.Replace("github.com/", "github.com.evil.invalid/", StringComparison.Ordinal),
                AssetUrl.Replace("github.com/", "github.com:444/", StringComparison.Ordinal),
                AssetUrl.Replace("https://", "https://user@", StringComparison.Ordinal),
                AssetUrl.Replace("/download/v0.1.18/", "/download/" + Tag + "/", StringComparison.Ordinal),
                AssetUrl.Replace("/download/v0.1.18/", "/download/v0.1.17/", StringComparison.Ordinal),
                AssetUrl + "?download=1", AssetUrl + "#fragment", AssetUrl + ".altered", "relative.zip", ""
            };
            foreach (var url in altered)
            {
                try { await InvokeAsync(resolve, [Repository, Tag, url, false]); }
                catch (InvalidOperationException)
                {
                    Check(true, "real resolver rejects altered local-alias asset: " + url);
                    continue;
                }
                throw new InvalidDataException("The real resolver accepted an altered alias asset.");
            }
            foreach (var force in new[] { false, true })
            {
                var result = await InvokeAsync(read, ["release", Repository + "\n" + Tag, force, null]);
                var release = (JsonElement)Property(result, "Value");
                var assets = release.GetProperty("assets");
                Check((string)Property(result, "Source") == "local" &&
                      release.GetProperty("tag_name").GetString() == Tag &&
                      release.GetProperty("html_url").GetString() == SourceUrl &&
                      release.GetProperty("name").GetString()!.Contains("preparação automática All-Fix", StringComparison.Ordinal) &&
                      release.GetProperty("body").GetString()!.Contains("não representa uma tag publicada", StringComparison.Ordinal) &&
                      assets.GetArrayLength() == 1 && assets[0].GetProperty("name").GetString() == FileName &&
                      assets[0].GetProperty("size").GetInt64() == Size &&
                      assets[0].GetProperty("browser_download_url").GetString() == AssetUrl &&
                      assets[0].GetProperty("digest").GetString() == "sha256:" + Sha256,
                    "real catalog returns the explicit local variant, force=" + force);
            }
            var merge = Method(catalog, "MergeMkwCachedReleases", [typeof(JsonElement)]);
            using (var malformed = JsonDocument.Parse("[{},{\"tag_name\":null},null,42,{\"tag_name\":7}," +
                "{\"tag_name\":\"\"},{\"tag_name\":\"v0.1.18\",\"assets\":[]}," +
                "{\"tag_name\":\"v0.1.18-allfix-cli\",\"assets\":[]}]"))
            {
                var merged = (JsonElement)merge.Invoke(null, [malformed.RootElement])!;
                Check(merged.GetArrayLength() == 2 && merged[0].GetProperty("tag_name").GetString() == Tag &&
                      merged[1].GetProperty("tag_name").GetString() == "v0.1.18",
                    "actual cache merge rejects malformed entries and keeps both local and upstream identities");
            }
            Check(monitor.Requests == 0, "no HTTP request started in either real service");
            Console.WriteLine("MKW_CLI_STORE_ASSEMBLY_PASS checks=" + passed);
            return 0;
        }
        catch (Exception error)
        {
            Console.Error.WriteLine(error);
            return 1;
        }
    }

    private static MethodInfo Method(Type type, string name, Type[] arguments) =>
        type.GetMethod(name, BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static, null, arguments, null)
        ?? throw new MissingMethodException(type.FullName, name);

    private static object Property(object value, string name) => value.GetType().GetProperty(name)!.GetValue(value)!;

    private static async Task<object> InvokeAsync(MethodInfo method, object?[] arguments)
    {
        object? invoked;
        try { invoked = method.Invoke(null, arguments); }
        catch (TargetInvocationException error) when (error.InnerException is not null)
        {
            ExceptionDispatchInfo.Capture(error.InnerException).Throw();
            throw;
        }
        if (invoked is not Task task) throw new InvalidDataException("The real service did not return a Task.");
        // Local metadata must finish immediately. A regression into a remote
        // lookup must not turn this offline contract test into an unbounded wait.
        await task.WaitAsync(TimeSpan.FromSeconds(5));
        return Property(task, "Result");
    }

    private sealed class HttpMonitor : IObserver<DiagnosticListener>, IObserver<KeyValuePair<string, object?>>, IDisposable
    {
        private readonly List<IDisposable> subscriptions = [];
        private readonly IDisposable listeners;
        private int requests;
        internal int Requests => Volatile.Read(ref requests);
        internal HttpMonitor() => listeners = DiagnosticListener.AllListeners.Subscribe(this);
        public void OnNext(DiagnosticListener value)
        {
            if (value.Name == "HttpHandlerDiagnosticListener") subscriptions.Add(value.Subscribe(this));
        }
        public void OnNext(KeyValuePair<string, object?> value)
        {
            if (value.Key == "System.Net.Http.HttpRequestOut.Start") Interlocked.Increment(ref requests);
        }
        public void OnCompleted() { }
        public void OnError(Exception error) { }
        public void Dispose()
        {
            listeners.Dispose();
            foreach (var subscription in subscriptions) subscription.Dispose();
        }
    }
}
