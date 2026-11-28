[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][ValidatePattern('^[0-9a-f]{40}$')][string]$DesktopCommit,
    [switch]$Execute,
    [string]$TaskRoot = 'C:\Users\bradg\Downloads\GetAll-R18',
    [string]$DesktopRoot = '',
    [string]$GitExecutable = 'C:\Program Files\Git\cmd\git.exe',
    [string]$DotNetExecutable = 'C:\Program Files\dotnet\dotnet.exe',
    [string]$PythonExecutable = ''
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $DesktopRoot) { $DesktopRoot = Join-Path $TaskRoot 'desktop-continuation-20261127' }
if (-not $PythonExecutable) { $PythonExecutable = Join-Path $TaskRoot 'evidence-r18\drmario-desktop-flow-20261127\source-tools-production-4\python\python.exe' }
$publish = Join-Path $TaskRoot 'publish-desktop-final-sdk169-20261127'
if (-not $Execute) {
    Write-Output ('PREPARED_ONLY: Desktop 3.0.0 / SDK 1.5.69, commit ' + $DesktopCommit)
    Write-Output ('Destination: ' + $publish + '; no addon package; preview138 preserved.')
    Write-Output 'Use -Execute only after final CI pin, clean commit and coordinated build have been confirmed.'
    return
}
if (Test-Path -LiteralPath $publish) { throw ('Candidate destination already exists: ' + $publish) }
foreach ($tool in @($GitExecutable, $DotNetExecutable, $PythonExecutable)) {
    if (-not (Test-Path -LiteralPath $tool -PathType Leaf)) { throw ('Missing tool: ' + $tool) }
}
$history = Join-Path $TaskRoot 'evidence-r18\complete-flows-publish-20261127'
$support = Join-Path $PSScriptRoot 'desktop_candidate_support.py'
$runName = 'run-' + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ') + '-' + [Guid]::NewGuid().ToString('N').Substring(0, 8)
$run = Join-Path $PSScriptRoot $runName
[IO.Directory]::CreateDirectory($run) | Out-Null
$staging = $publish + '.staging-' + $runName
if (Test-Path -LiteralPath $staging) { throw 'Candidate staging already exists' }
$inputs = Join-Path $run 'effective-desktop-inputs.json'
$auditDirectory = Join-Path $run 'assemblies'
$utf8 = [Text.UTF8Encoding]::new($false)
$request = [ordered]@{ desktop_commit = $DesktopCommit; desktop_root = $DesktopRoot; desktop_version = '3.0.0';
    sdk_version = '1.5.69'; addon_included = $false; publish = $publish; staging = $staging;
    started_utc = [DateTime]::UtcNow.ToString('o'); script_sha256 = (Get-FileHash -LiteralPath $PSCommandPath).Hash.ToLowerInvariant() }
[IO.File]::WriteAllText((Join-Path $run 'run-request.json'), ($request | ConvertTo-Json) + "`n", $utf8)
function Invoke-Logged {
    param([string]$Executable, [string[]]$Arguments, [string]$Name)
    $log = Join-Path $run ($Name + '.log')
    $saved = $ErrorActionPreference
    try { $ErrorActionPreference = 'Continue'; & $Executable @Arguments *> $log; $code = $LASTEXITCODE }
    finally { $ErrorActionPreference = $saved }
    Get-Content -LiteralPath $log -Tail 10
    if ($code -ne 0) { throw ($Name + ' failed with exit ' + $code + '; see ' + $log) }
}
$savedPath = $env:PATH
$savedTelemetry = $env:DOTNET_CLI_TELEMETRY_OPTOUT
$savedLogo = $env:DOTNET_NOLOGO
try {
    $env:PATH = (Split-Path -Parent $GitExecutable) + ';' + $savedPath
    $env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'; $env:DOTNET_NOLOGO = '1'
    Invoke-Logged $PythonExecutable @('-I', '-B', '-X', 'utf8', $support, 'preflight', '--task-root', $TaskRoot,
        '--desktop-root', $DesktopRoot, '--desktop-commit', $DesktopCommit, '--git', $GitExecutable, '--output', $inputs) 'preflight'
    $config = Get-Content -LiteralPath $inputs -Raw -Encoding UTF8 | ConvertFrom-Json
    $arguments = @('publish', (Join-Path $DesktopRoot 'AllFix.Desktop.csproj'), '-c', 'Release', '-r', 'win-x64',
        '--self-contained', 'true', '--nologo', '-o', $staging,
        ('-p:SourceRevisionId=' + $DesktopCommit), '-p:IncludeSourceRevisionInInformationalVersion=true')
    foreach ($property in $config.properties.PSObject.Properties) {
        $arguments += '-p:' + $property.Name + '=' + (Join-Path $TaskRoot ([string]$property.Value))
    }
    Push-Location (Join-Path $history 'resource-audit')
    try {
        Invoke-Logged $DotNetExecutable @('--version') 'dotnet-version'
        Invoke-Logged $DotNetExecutable $arguments 'publish-desktop'
    } finally { Pop-Location }
    Invoke-Logged $PythonExecutable @('-I', '-B', '-X', 'utf8', (Join-Path $history 'preview_support.py'), 'extract',
        '--exe', (Join-Path $staging 'AllFix.exe'), '--output', $auditDirectory) 'extract-bundle'
    Invoke-Logged $DotNetExecutable @([string]$config.audit_assembly, (Join-Path $auditDirectory 'AllFix.dll'),
        (Join-Path $auditDirectory 'AllFix.Addons.Sdk.dll'), $inputs, (Join-Path $auditDirectory 'resources.json')) 'audit-resources'
    Invoke-Logged $PythonExecutable @('-I', '-B', '-X', 'utf8', $support, 'finish', '--task-root', $TaskRoot,
        '--inputs', $inputs, '--publish', $staging, '--audit-dir', $auditDirectory, '--git', $GitExecutable) 'finish-desktop'
    [IO.Directory]::Move($staging, $publish)
    Invoke-Logged $PythonExecutable @('-I', '-B', '-X', 'utf8', $support, 'verify', '--task-root', $TaskRoot,
        '--publish', $publish, '--desktop-commit', $DesktopCommit) 'verify-desktop-final'
    $result = [ordered]@{ status = 'verified'; desktop_commit = $DesktopCommit; sdk_version = '1.5.69'; addon_included = $false;
        publish = $publish; completed_utc = [DateTime]::UtcNow.ToString('o');
        allfix_sha256 = (Get-FileHash -LiteralPath (Join-Path $publish 'AllFix.exe')).Hash.ToLowerInvariant();
        manifest_sha256 = (Get-FileHash -LiteralPath (Join-Path $publish 'ARTIFACT-MANIFEST.json')).Hash.ToLowerInvariant() }
    [IO.File]::WriteAllText((Join-Path $run 'desktop-candidate-result.json'), ($result | ConvertTo-Json) + "`n", $utf8)
    Write-Output ('DESKTOP_CANDIDATE_READY ' + $publish)
} catch {
    [IO.File]::WriteAllText((Join-Path $run 'failure.txt'), $_.ToString() + "`n", $utf8)
    throw
} finally {
    $env:PATH = $savedPath; $env:DOTNET_CLI_TELEMETRY_OPTOUT = $savedTelemetry; $env:DOTNET_NOLOGO = $savedLogo
}
