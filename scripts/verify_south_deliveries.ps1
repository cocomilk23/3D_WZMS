$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $taskRoot
try {
    $taskRemote = git ls-remote origin refs/heads/main 'refs/tags/v0.0.1[2-5]*'
    if ($LASTEXITCODE -ne 0) { throw 'Cannot verify remote delivery refs' }
    $taskRows = foreach ($taskRevision in 12..15) {
        $taskVersion = "v0.0.$taskRevision"
        $taskDirectory = Join-Path $taskRoot "deliverables/$taskVersion"
        $taskManifest = Get-Content -LiteralPath (Join-Path $taskDirectory 'delivery_validation.json') -Raw | ConvertFrom-Json
        $taskModel = Join-Path $taskRoot $taskManifest.model
        $taskHash = (Get-FileHash -LiteralPath $taskModel -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($taskHash -ne $taskManifest.sha256 -or (Get-Item -LiteralPath $taskModel).Length -ne $taskManifest.bytes) { throw "$taskVersion model changed after validation" }
        if (-not $taskManifest.images_visually_reviewed -or -not $taskManifest.geometry_passed -or -not ($taskManifest.previous_objects_preserved -or $taskManifest.only_documented_connection_adjustments)) { throw "$taskVersion incomplete validation" }
        foreach ($taskPreview in $taskManifest.previews) {
            $taskImage = Join-Path $taskDirectory $taskPreview.file
            if ((Get-FileHash -LiteralPath $taskImage).Hash.ToLowerInvariant() -ne $taskPreview.sha256) { throw "$taskVersion preview changed after review" }
        }
        $taskCommit = git rev-list -n 1 $taskVersion
        if ($LASTEXITCODE -ne 0) { throw "$taskVersion missing local tag" }
        if (-not ($taskRemote | Where-Object { $_ -eq "$taskCommit`trefs/tags/$taskVersion^{}" })) { throw "$taskVersion remote tag mismatch" }
        git merge-base --is-ancestor $taskCommit HEAD
        if ($LASTEXITCODE -ne 0) { throw "$taskVersion not part of current history" }
        $taskPointer = git show "${taskVersion}:$($taskManifest.model)"
        if (-not ($taskPointer -contains "oid sha256:$taskHash")) { throw "$taskVersion Git LFS pointer mismatch" }
        [pscustomobject]@{ Version=$taskVersion; Commit=$taskCommit; Images=$taskManifest.previews.Count; ModelSHA256=$taskHash; Verified=$true }
    }
    $taskHead = git rev-parse HEAD
    if (-not ($taskRemote -contains "$taskHead`trefs/heads/main")) { throw 'Remote main does not match HEAD' }
    git lfs fsck
    if ($LASTEXITCODE -ne 0) { throw 'Git LFS content validation failed' }
    if (git status --porcelain) { throw 'Worktree has uncommitted changes' }
    $taskRows | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskRoot 'builds/final_south_delivery_audit.json') -Encoding utf8
    $taskRows | Select-Object Version,Images,Verified | Format-Table
}
finally { Pop-Location }
