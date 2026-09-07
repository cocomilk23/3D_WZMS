param([string]$Proxy='')
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $taskRoot
try {
    $taskGitArgs=@('-c','http.version=HTTP/1.1','-c','http.sslBackend=schannel')
    if ($Proxy) { $taskGitArgs+=@('-c',('http.proxy='+$Proxy)) }
    $taskRemote=& git @taskGitArgs ls-remote origin refs/heads/main 'refs/tags/v0.0.*'
    if ($LASTEXITCODE -ne 0) { throw 'Remote verification unavailable' }
    $taskRows=foreach ($taskRevision in 30..33) {
        $taskVersion="v0.0.$taskRevision"
        $taskDirectory=Join-Path $taskRoot "deliverables/$taskVersion"
        $taskManifest=Get-Content -LiteralPath (Join-Path $taskDirectory 'delivery_validation.json') -Raw | ConvertFrom-Json
        $taskModel=Join-Path $taskRoot $taskManifest.model
        $taskHash=(Get-FileHash -LiteralPath $taskModel -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($taskHash -ne $taskManifest.sha256 -or (Get-Item -LiteralPath $taskModel).Length -ne $taskManifest.bytes) { throw "$taskVersion changed after review" }
        if (-not $taskManifest.images_visually_reviewed -or -not $taskManifest.geometry_passed -or $taskManifest.unexpected_predecessor_changes) { throw "$taskVersion incomplete checks" }
        foreach ($taskPreview in $taskManifest.previews) {
            if ((Get-FileHash -LiteralPath (Join-Path $taskDirectory $taskPreview.file)).Hash.ToLowerInvariant() -ne $taskPreview.sha256) { throw "$taskVersion preview changed" }
        }
        $taskCommit=git rev-list -n 1 $taskVersion
        if ($LASTEXITCODE -ne 0 -or -not ($taskRemote -contains "$taskCommit`trefs/tags/$taskVersion")) { throw "$taskVersion remote tag mismatch" }
        git merge-base --is-ancestor $taskCommit HEAD
        if ($LASTEXITCODE -ne 0) { throw "$taskVersion is outside current history" }
        $taskPointer=git show "${taskVersion}:$($taskManifest.model)"
        if (-not ($taskPointer -contains "oid sha256:$taskHash")) { throw "$taskVersion model and LFS pointer disagree" }
        [pscustomobject]@{Version=$taskVersion;Commit=$taskCommit;Images=$taskManifest.previews.Count;ModelSHA256=$taskHash;Verified=$true}
    }
    $taskHead=git rev-parse HEAD
    if (-not ($taskRemote -contains "$taskHead`trefs/heads/main")) { throw 'Remote main differs' }
    $taskSouth=Get-Content -LiteralPath 'deliverables/v0.0.33/south_gate_preservation_validation.json' -Raw | ConvertFrom-Json
    if (-not $taskSouth.unchanged -or $taskSouth.baseline_digest -ne $taskSouth.current_digest) { throw 'Deferred south gate wall changed' }
    $taskRoutes=Get-Content -LiteralPath 'deliverables/v0.0.33/geometry_validation.json' -Raw | ConvertFrom-Json
    if (-not $taskRoutes.all_passed -or $taskRoutes.routes.Count -ne 47 -or ($taskRoutes.routes | Where-Object failure_count -ne 0)) { throw 'Final route checks incomplete' }
    if (git diff --name-only 38e3d1b HEAD -- web-preview reference/source reference/reports deliverables/v0.0.29 models/campus/WZMS_Campus_v029.blend) { throw 'Frozen baseline or website changed' }
    git lfs fsck
    if ($LASTEXITCODE -ne 0) { throw 'LFS integrity check failed' }
    if (git status --porcelain) { throw 'Uncommitted changes remain' }
    $taskRows | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath 'builds/final_sports_delivery_audit.json' -Encoding utf8
    $taskRows | Select-Object Version,Images,Verified | Format-Table
}
finally { Pop-Location }
