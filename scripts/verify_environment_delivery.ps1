param([string]$Proxy='')
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $taskRoot
try {
 $taskDirectory='deliverables/v0.0.43'
 $taskManifest=Get-Content "$taskDirectory/delivery_validation.json" -Raw | ConvertFrom-Json
 $taskHash=(Get-FileHash -LiteralPath $taskManifest.model -Algorithm SHA256).Hash.ToLowerInvariant()
 if ($taskHash -ne $taskManifest.sha256 -or (Get-Item -LiteralPath $taskManifest.model).Length -ne $taskManifest.bytes) { throw 'Model differs from reviewed file' }
 if (-not $taskManifest.images_visually_reviewed -or $taskManifest.previews.Count -ne 4) { throw 'Review incomplete' }
 foreach ($taskImage in $taskManifest.previews) {
  if ((Get-FileHash -LiteralPath "$taskDirectory/$($taskImage.file)").Hash.ToLowerInvariant() -ne $taskImage.sha256) { throw 'Image differs from reviewed file' }
 }
 $taskLayout=Get-Content "$taskDirectory/saved_layout_validation.json" -Raw | ConvertFrom-Json
 if (-not $taskLayout.all_passed -or $taskLayout.tennis_count -ne 4 -or $taskLayout.tennis_rotation_degrees -ne 90 -or $taskLayout.tennis_long_axis -ne 'Y' -or $taskLayout.tennis_net_count -ne 4 -or $taskLayout.basketball_count -ne 8) { throw 'Court layout mismatch' }
 $taskExpectedX=@(22,40,58,76)
 if ($taskLayout.tennis_centres.Count -ne 4) { throw 'Four-court row incomplete' }
 for ($taskIndex=0; $taskIndex -lt 4; $taskIndex++) {
  if ($taskLayout.tennis_centres[$taskIndex][0] -ne $taskExpectedX[$taskIndex] -or $taskLayout.tennis_centres[$taskIndex][1] -ne -31) { throw 'Four-court row mismatch' }
 }
 $taskPreservation=Get-Content "$taskDirectory/preservation_validation.json" -Raw | ConvertFrom-Json
 $taskRegistration=Get-Content "$taskDirectory/south_registration_validation.json" -Raw | ConvertFrom-Json
 if (-not $taskRegistration.all_passed -or $taskRegistration.right_gate_post_count -ne 18) { throw 'South registration incomplete' }
 if (-not $taskPreservation.all_unexpected_changes_absent) { throw 'Unexpected predecessor changes' }
 $taskGeometry=Get-Content "$taskDirectory/geometry_validation.json" -Raw | ConvertFrom-Json
 if (-not $taskGeometry.all_passed -or $taskGeometry.routes.Count -ne 74) { throw 'Route validation incomplete' }
 $taskWall=Get-Content "$taskDirectory/south_gate_preservation_validation.json" -Raw | ConvertFrom-Json
 if (-not $taskWall.content_unchanged -or -not $taskWall.approved_motion_matches -or $taskWall.baseline_digest -ne $taskWall.current_digest) { throw 'Deferred wall changed' }
 $taskRender=Get-Content "$taskDirectory/render_validation.json" -Raw | ConvertFrom-Json
 if ($taskRender.samples -ne 96 -or $taskRender.missing_external_images.Count) { throw 'Rendering incomplete' }
 $taskUE=Get-Content "$taskDirectory/ue_transfer_validation.json" -Raw | ConvertFrom-Json
 if (-not $taskUE.roundtrip_all_passed -or $taskUE.source_sha256 -ne $taskHash -or $taskUE.zones -ne 5) { throw 'UE transfer incomplete' }
 if ((Get-FileHash -LiteralPath $taskUE.archive.file).Hash.ToLowerInvariant() -ne $taskUE.archive.sha256) { throw 'UE archive hash mismatch' }
 $taskArgs=@('-c','http.version=HTTP/1.1','-c','http.sslBackend=schannel')
 if ($Proxy) { $taskArgs+=@('-c',('http.proxy='+$Proxy)) }
 $taskRemote=& git @taskArgs ls-remote origin refs/heads/main refs/tags/v0.0.43
 if ($LASTEXITCODE -ne 0) { throw 'Remote unavailable' }
 $taskHead=git rev-parse HEAD
 if (-not ($taskRemote -contains "$taskHead`trefs/heads/main") -or -not ($taskRemote -contains "$taskHead`trefs/tags/v0.0.43")) { throw 'Remote version mismatch' }
 $taskPointer=git show "v0.0.43:$($taskManifest.model)"
 if (-not ($taskPointer -contains "oid sha256:$taskHash")) { throw 'LFS pointer differs' }
 if (git diff --name-only v0.0.42 HEAD -- models/campus/WZMS_Campus_v042.blend deliverables/v0.0.42 web-preview reference/source reference/reports) { throw 'Frozen previous version or references changed' }
 $taskUEPointer=git show "v0.0.43:$($taskUE.archive.file)"
 if (-not ($taskUEPointer -contains "oid sha256:$($taskUE.archive.sha256)")) { throw 'UE archive LFS mismatch' }
 git lfs fsck
 if ($LASTEXITCODE -ne 0) { throw 'LFS integrity check failed' }
 if (git status --porcelain) { throw 'Uncommitted changes remain' }
 [pscustomobject]@{Version='v0.0.43';Commit=$taskHead;ModelSHA256=$taskHash;ReviewedImages=4;Routes=74;UEFiles=$taskUE.mesh_files;UEArchiveSHA256=$taskUE.archive.sha256;UERuntimeTested=$false;Verified=$true} | ConvertTo-Json | Set-Content builds/final_environment_delivery_audit.json -Encoding utf8
 Write-Output 'v0.0.43: model, 4 images, 74 routes, UE transfer ZIP, remote tag and LFS verified. UE runtime remains untested.'
}
finally { Pop-Location }
