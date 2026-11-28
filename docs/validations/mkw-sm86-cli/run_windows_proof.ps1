$ErrorActionPreference='Stop'
$b='C:\Users\bradg\Downloads\GetAll-R18'
$r=Join-Path $b 'evidence-r18\mkw-independent-20261127'
$data=Get-Content -LiteralPath (Join-Path $r 'backend-input.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$enc=[Text.UTF8Encoding]::new($false)
$zip=Join-Path $r $data.package.path
if((Get-FileHash $zip).Hash.ToLowerInvariant() -ne $data.package.sha256){throw 'Support SHA mismatch'}
$kit=Join-Path $b 'evidence-r18\priority-mkw\official-run\preflight\kit'
$nv=Join-Path $r 'nvidia-normal-cli\extracted\cuda_nvdisasm-windows-x86_64-12.8.90-archive\bin\nvdisasm.exe'
$llvm=Join-Path $b 'gta-engine\preflight\llvm\llvm-mingw-20261020-ucrt-x86_64'
& (Join-Path $llvm 'bin\llvm-readobj.exe') --coff-imports $nv *> (Join-Path $r 'nvdisasm-imports.log')
if($LASTEXITCODE -ne 0){throw 'NVIDIA import scan failed'}
$work=Join-Path $r 'backend-native-8'
if(Test-Path -LiteralPath $work){throw 'Fresh proof work required'}
[IO.Directory]::CreateDirectory($work) | Out-Null
$runner=Join-Path $b 'evidence-r18\complete-install-flows-20261127\native-diagnostic-runner\bin\Release\net8.0\NativeDiagnosticRunner.dll'
$common=@{Harness=(Join-Path $b 'evidence-r18\flow-completion-20261127\harness-build30\AddonInfrastructure.dll');Llvm=$llvm;Cmake=(Join-Path $b 'burnout-engine\preflight\cmake');Ninja=(Join-Path $b 'burnout-engine\preflight\ninja');Python=(Join-Path $b 'pinyon-engine\preflight\python');Minutes=10}
$req=$common.Clone()
$req.Exe=Join-Path $kit 'setup\python\python.exe'
$req.Arguments=@('-I',(Join-Path $r 'prove_backend.py'),'--kit',$kit,'--support',$zip,'--support-sha256',$data.package.sha256,'--nvdisasm',$nv,'--fixtures',(Join-Path $r 'backend-fixtures.json'),'--work',$work,'--official-archive',(Join-Path $b 'evidence-r18\priority-mkw\mkw-official.zip'))
$req.Work=$work
$req.Log=Join-Path $r 'backend-native-8.log'
$request=Join-Path $r 'backend-native-8-request.json'
[IO.File]::WriteAllText($request,($req|ConvertTo-Json -Depth 6),$enc)
$ErrorActionPreference='Continue'
& dotnet $runner $request *> (Join-Path $r 'backend-native-8-runner.log')
$nativeExit=$LASTEXITCODE
$ErrorActionPreference='Stop'
[IO.File]::WriteAllText((Join-Path $r 'backend-native-8.exit'),[string]$nativeExit,$enc)
$summary=@{native_exit=$nativeExit;extra=@()}
if($nativeExit -eq 0){
    $extra=Join-Path $r 'final-glsl'
    [IO.Directory]::CreateDirectory($extra)|Out-Null
    foreach($item in $data.extra_shaders){
        if($item.name -notmatch '^[a-z0-9-]+\.(frag|comp)$'){throw 'Invalid authored shader name'}
        $src=Join-Path $extra $item.name
        $spv=$src+'.spv'
        [IO.File]::WriteAllText($src,$item.content,$enc)
        $step=$common.Clone()
        $step.Exe=Join-Path $kit 'setup\glslc\glslc.exe'
        $step.Arguments=@('--target-env=vulkan1.3',('-fshader-stage='+$item.stage),$src,'-o',$spv)
        $step.Work=$extra
        $step.Log=$src+'.compile.log'
        $rp=$src+'.compile-request.json'
        [IO.File]::WriteAllText($rp,($step|ConvertTo-Json -Depth 6),$enc)
        & dotnet $runner $rp *> ($src+'.compile-runner.log')
        $compileExit=$LASTEXITCODE
        $validateExit=-1
        if($compileExit -eq 0){
            $step.Exe=Join-Path $kit 'setup\glslc\spirv-val.exe'
            $step.Arguments=@('--target-env','vulkan1.3',$spv)
            $step.Log=$src+'.validate.log'
            $rp=$src+'.validate-request.json'
            [IO.File]::WriteAllText($rp,($step|ConvertTo-Json -Depth 6),$enc)
            & dotnet $runner $rp *> ($src+'.validate-runner.log')
            $validateExit=$LASTEXITCODE
        }
        $row=@{name=$item.name;compile_exit=$compileExit;validate_exit=$validateExit;source_sha256=(Get-FileHash $src).Hash.ToLowerInvariant()}
        if(Test-Path -LiteralPath $spv){$row.bytes=(Get-Item $spv).Length;$row.sha256=(Get-FileHash $spv).Hash.ToLowerInvariant()}
        $summary.extra+=@($row)
    }
}
[IO.File]::WriteAllText((Join-Path $r 'backend-native-8-summary.json'),($summary|ConvertTo-Json -Depth 6),$enc)
Write-Output ($summary|ConvertTo-Json -Depth 6 -Compress)
