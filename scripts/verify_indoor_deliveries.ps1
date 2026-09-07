param([string]$Proxy='')
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $taskRoot
try {
 $taskGitArgs=@('-c','http.version=HTTP/1.1','-c','http.sslBackend=schannel')
 if ($Proxy) { $taskGitArgs+=@('-c',('http.proxy='+$Proxy)) }
 $taskRemote=& git @taskGitArgs ls-remote origin refs/heads/main 'refs/tags/v0.0.*'
 if ($LASTEXITCODE -ne 0) { throw 'Remote verification unavailable' }
 $taskRows=foreach ($taskRevision in 34..39) {
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
  $taskLayout=Get-Content -LiteralPath (Join-Path $taskDirectory 'saved_layout_validation.json') -Raw | ConvertFrom-Json
  if (-not $taskLayout.all_passed -or $taskLayout.basketball_count -ne 8 -or $taskLayout.basketball_rotation_degrees -ne 90) { throw "$taskVersion incorrect basketball layout" }
  if ($taskRevision -ge 35 -and ($taskLayout.tennis_count -ne 4 -or -not $taskLayout.solid_divider)) { throw "$taskVersion incorrect tennis layout" }
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
 $taskSouth=Get-Content -LiteralPath 'deliverables/v0.0.39/south_gate_preservation_validation.json' -Raw | ConvertFrom-Json
 if (-not $taskSouth.unchanged -or $taskSouth.baseline_digest -ne $taskSouth.current_digest) { throw 'Deferred south gate wall changed' }
 $taskRoutes=Get-Content -LiteralPath 'deliverables/v0.0.39/geometry_validation.json' -Raw | ConvertFrom-Json
 if (-not $taskRoutes.all_passed -or $taskRoutes.routes.Count -ne 68 -or ($taskRoutes.routes | Where-Object failure_count -ne 0)) { throw 'Integrated route checks incomplete' }
 if (git diff --name-only a194cc8 HEAD -- web-preview reference/source reference/reports deliverables/v0.0.33 models/campus/WZMS_Campus_v033.blend deliverables/v0.0.34 models/campus/WZMS_Campus_v034.blend) { throw 'Frozen baseline or website changed' }
 git lfs fsck
 if ($LASTEXITCODE -ne 0) { throw 'LFS integrity check failed' }
 if (git status --porcelain) { throw 'Uncommitted changes remain' }
 $taskRows | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath 'builds/final_indoor_delivery_audit.json' -Encoding utf8
 $taskRows | Select-Object Version,Images,Verified | Format-Table
}
finally { Pop-Location }
