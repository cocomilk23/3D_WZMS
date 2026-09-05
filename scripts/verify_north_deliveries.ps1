param([switch]$LocalOnly)
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $taskRoot
Add-Type -AssemblyName System.Drawing
$taskResults = @()
$taskRemote = @{}
if (-not $LocalOnly) {
    $taskLines = & git ls-remote origin refs/heads/main 'refs/tags/v0.0.*'
    if ($LASTEXITCODE -ne 0) { throw 'Cannot verify remote Git refs' }
    foreach ($taskLine in $taskLines) {
        $taskParts = $taskLine -split '\s+'
        $taskRemote[$taskParts[1]] = $taskParts[0]
    }
}
foreach ($taskRev in 7..11) {
    $taskVersion = 'v0.0.' + $taskRev
    $taskDir = Join-Path $taskRoot "deliverables/$taskVersion"
    $taskDelivery = Get-Content -LiteralPath "$taskDir/delivery_validation.json" -Raw | ConvertFrom-Json
    $taskRender = Get-Content -LiteralPath "$taskDir/render_validation.json" -Raw | ConvertFrom-Json
    $taskGeometry = Get-Content -LiteralPath "$taskDir/geometry_validation.json" -Raw | ConvertFrom-Json
    $taskPreservation = Get-Content -LiteralPath "$taskDir/preservation_validation.json" -Raw | ConvertFrom-Json
    $taskFile = Get-Item -LiteralPath (Join-Path $taskRoot $taskDelivery.model)
    $taskHash = (Get-FileHash -LiteralPath $taskFile.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($taskHash -ne $taskDelivery.sha256.ToLowerInvariant() -or $taskFile.Length -ne $taskDelivery.bytes) { throw "$taskVersion saved model differs from manifest" }
    if (-not $taskGeometry.passed -or @($taskGeometry.failures).Count -gt 0) { throw "$taskVersion geometry validation failed" }
    if (-not $taskPreservation.unchanged -or $taskPreservation.baseline_digest -ne $taskPreservation.current_digest) { throw "$taskVersion modified the preserved south wall" }
    if ($taskRender.version -ne $taskVersion -or -not $taskRender.metric_units -or @($taskRender.missing_external_images).Count -gt 0) { throw "$taskVersion render/dependency validation failed" }
    if (([IO.Path]::GetFullPath($taskRender.opened_saved_blend)) -ne $taskFile.FullName) { throw "$taskVersion checked a different model" }
    if ([string]::IsNullOrWhiteSpace([string]$taskDelivery.visual_review)) { throw "$taskVersion has no visual review record" }
    $taskImages = @()
    foreach ($taskView in $taskRender.renders) {
        $taskImagePath = Join-Path $taskDir $taskView.file
        $taskImage = [Drawing.Image]::FromFile($taskImagePath)
        try {
            if ($taskImage.Width -ne 1600 -or $taskImage.Height -ne 1000) { throw "$taskVersion invalid render dimensions" }
            $taskImages += $taskView.camera
        } finally { $taskImage.Dispose() }
    }
    if ($taskImages.Count -lt 5) { throw "$taskVersion has fewer than five checked views" }
    if (-not (Test-Path -LiteralPath "$taskDir/交付说明.md")) { throw "$taskVersion delivery note missing" }
    $taskCommit = (& git rev-parse "${taskVersion}^{}").Trim()
    if ($LASTEXITCODE -ne 0) { throw "$taskVersion Git tag missing" }
    $taskPointer = (& git show ("${taskVersion}:" + $taskDelivery.model)) -join "`n"
    if ($taskPointer -notmatch ('oid sha256:' + $taskHash)) { throw "$taskVersion LFS pointer does not match saved model" }
    & git merge-base --is-ancestor $taskCommit HEAD
    if ($LASTEXITCODE -ne 0) { throw "$taskVersion commit is absent from main history" }
    if (-not $LocalOnly -and $taskRemote["refs/tags/${taskVersion}^{}"] -ne $taskCommit) { throw "$taskVersion remote tag differs" }
    $taskResults += [ordered]@{ version=$taskVersion; model=$taskDelivery.model; bytes=$taskFile.Length; sha256=$taskHash; commit=$taskCommit; render_cameras=$taskImages; geometry_passed=$true; preserved_south_wall=$true; remote_verified=(-not $LocalOnly) }
}
$taskIntegrated = Get-Content -LiteralPath 'deliverables/v0.0.11/integrated_route_validation.json' -Raw | ConvertFrom-Json
if (-not $taskIntegrated.passed -or @($taskIntegrated.failures).Count -gt 0) { throw 'Integrated route clearance failed' }
$taskHead = (& git rev-parse HEAD).Trim()
if (-not $LocalOnly -and $taskRemote['refs/heads/main'] -ne $taskHead) { throw 'Remote main differs from local HEAD' }
if (@($taskResults.commit | Select-Object -Unique).Count -ne 5) { throw 'Deliveries do not have five distinct commits' }
& git lfs fsck
if ($LASTEXITCODE -ne 0) { throw 'Git LFS integrity check failed' }
$taskStatus = & git status --porcelain
if ($taskStatus) { throw ('Working tree is not clean: ' + ($taskStatus -join ', ')) }
$taskFinal = [ordered]@{ checked_at_utc=[DateTime]::UtcNow.ToString('o'); passed=$true; head=$taskHead; deliveries=$taskResults; integrated_route_passed=$true; user_acceptance='pending'; ue_playthrough_verified=$false; absolute_scale_verified=$false }
$taskOut = Join-Path $taskRoot 'builds/final_north_delivery_audit.json'
[IO.File]::WriteAllText($taskOut,($taskFinal | ConvertTo-Json -Depth 8),[Text.UTF8Encoding]::new($false))
$taskResults | Select-Object version,bytes,commit,remote_verified | Format-Table
Write-Output 'WZMS_ALL_FIVE_DELIVERIES_VERIFIED'
