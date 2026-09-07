$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $taskRoot
try {
    $taskRemote = git ls-remote origin refs/heads/main 'refs/tags/v0.0.*'
    if ($LASTEXITCODE -ne 0) { throw 'Cannot verify remote refs' }
    $taskRows = foreach ($taskRevision in 26..29) {
        $taskVersion = "v0.0.$taskRevision"
        $taskDirectory = Join-Path $taskRoot "deliverables/$taskVersion"
        $taskManifest = Get-Content -LiteralPath (Join-Path $taskDirectory 'delivery_validation.json') -Raw | ConvertFrom-Json
        $taskModel = Join-Path $taskRoot $taskManifest.model
        $taskHash = (Get-FileHash -LiteralPath $taskModel -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($taskHash -ne $taskManifest.sha256 -or (Get-Item -LiteralPath $taskModel).Length -ne $taskManifest.bytes) { throw "$taskVersion model changed after review" }
        if (-not $taskManifest.images_visually_reviewed -or -not $taskManifest.geometry_passed -or $taskManifest.unexpected_predecessor_changes) { throw "$taskVersion incomplete validation" }
        foreach ($taskPreview in $taskManifest.previews) {
            if ((Get-FileHash -LiteralPath (Join-Path $taskDirectory $taskPreview.file)).Hash.ToLowerInvariant() -ne $taskPreview.sha256) { throw "$taskVersion image changed" }
        }
        $taskCommit = git rev-list -n 1 $taskVersion
        if ($LASTEXITCODE -ne 0) { throw "$taskVersion missing tag" }
        if (-not ($taskRemote -contains "$taskCommit`trefs/tags/$taskVersion")) { throw "$taskVersion remote tag mismatch" }
        git merge-base --is-ancestor $taskCommit HEAD
        if ($LASTEXITCODE -ne 0) { throw "$taskVersion not in current history" }
        $taskPointer = git show "${taskVersion}:$($taskManifest.model)"
        if (-not ($taskPointer -contains "oid sha256:$taskHash")) { throw "$taskVersion LFS pointer mismatch" }
        [pscustomobject]@{ Version=$taskVersion; Commit=$taskCommit; Images=$taskManifest.previews.Count; ModelSHA256=$taskHash; Verified=$true }
    }
    $taskHead = git rev-parse HEAD
    if (-not ($taskRemote -contains "$taskHead`trefs/heads/main")) { throw 'Remote main mismatch' }
    $taskSouthWall = Get-Content -LiteralPath 'deliverables/v0.0.29/south_gate_preservation_validation.json' -Raw | ConvertFrom-Json
    if (-not $taskSouthWall.unchanged -or $taskSouthWall.baseline_digest -ne $taskSouthWall.current_digest) { throw 'Deferred south wall changed' }
    $taskRoutes = Get-Content -LiteralPath 'deliverables/v0.0.29/geometry_validation.json' -Raw | ConvertFrom-Json
    if (-not $taskRoutes.all_passed -or $taskRoutes.routes.Count -ne 35 -or ($taskRoutes.routes | Where-Object failure_count -ne 0)) { throw 'Integrated route check incomplete' }
    if (git diff --name-only b0d4bb6 HEAD -- web-preview reference/source reference/reports deliverables/v0.0.25 models/campus/WZMS_Campus_v025.blend) { throw 'Frozen web, baseline or references changed' }
    git lfs fsck
    if ($LASTEXITCODE -ne 0) { throw 'Git LFS integrity failed' }
    if (git status --porcelain) { throw 'Uncommitted workspace changes' }
    $taskRows | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskRoot 'builds/final_west_delivery_audit.json') -Encoding utf8
    $taskRows | Select-Object Version,Images,Verified | Format-Table
}
finally { Pop-Location }
