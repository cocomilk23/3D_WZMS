param([string]$Proxy='')
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $taskRoot
try {
 $taskDirectory='deliverables/v0.0.40'
 $taskManifest=Get-Content "$taskDirectory/delivery_validation.json" -Raw | ConvertFrom-Json
 $taskHash=(Get-FileHash -LiteralPath $taskManifest.model -Algorithm SHA256).Hash.ToLowerInvariant()
 if ($taskHash -ne $taskManifest.sha256 -or (Get-Item -LiteralPath $taskManifest.model).Length -ne $taskManifest.bytes) { throw 'Model differs from reviewed file' }
 if (-not $taskManifest.images_visually_reviewed -or $taskManifest.previews.Count -ne 14) { throw 'Review incomplete' }
 foreach ($taskImage in $taskManifest.previews) {
  if ((Get-FileHash -LiteralPath "$taskDirectory/$($taskImage.file)").Hash.ToLowerInvariant() -ne $taskImage.sha256) { throw 'Image differs from reviewed file' }
 }
 $taskLayout=Get-Content "$taskDirectory/saved_layout_validation.json" -Raw | ConvertFrom-Json
 if (-not $taskLayout.all_passed -or $taskLayout.tennis_count -ne 4 -or $taskLayout.tennis_rotation_degrees -ne 90 -or $taskLayout.tennis_long_axis -ne 'Y' -or $taskLayout.tennis_net_count -ne 4 -or $taskLayout.basketball_count -ne 8) { throw 'Court layout mismatch' }
 $taskGeometry=Get-Content "$taskDirectory/geometry_validation.json" -Raw | ConvertFrom-Json
 if (-not $taskGeometry.all_passed -or $taskGeometry.routes.Count -ne 68) { throw 'Route validation incomplete' }
 $taskMaterials=Get-Content "$taskDirectory/material_validation.json" -Raw | ConvertFrom-Json
 if (-not $taskMaterials.all_passed -or -not $taskMaterials.original_image_materials_preserved) { throw 'Material preservation mismatch' }
 $taskComponents=Get-Content "$taskDirectory/component_validation.json" -Raw | ConvertFrom-Json
 if (-not $taskComponents.all_passed -or $taskComponents.hollow_reveal_centres_checked -ne 578 -or $taskComponents.concave_stools_checked -ne 112) { throw 'Physical component checks incomplete' }
 $taskWall=Get-Content "$taskDirectory/south_gate_preservation_validation.json" -Raw | ConvertFrom-Json
 if (-not $taskWall.unchanged -or $taskWall.baseline_digest -ne $taskWall.current_digest) { throw 'Deferred wall changed' }
 $taskRender=Get-Content "$taskDirectory/render_validation.json" -Raw | ConvertFrom-Json
 if ($taskRender.samples -ne 96 -or $taskRender.missing_external_images.Count) { throw 'Rendering incomplete' }
 $taskArgs=@('-c','http.version=HTTP/1.1','-c','http.sslBackend=schannel')
 if ($Proxy) { $taskArgs+=@('-c',('http.proxy='+$Proxy)) }
 $taskRemote=& git @taskArgs ls-remote origin refs/heads/main refs/tags/v0.0.40
 if ($LASTEXITCODE -ne 0) { throw 'Remote unavailable' }
 $taskHead=git rev-parse HEAD
 if (-not ($taskRemote -contains "$taskHead`trefs/heads/main") -or -not ($taskRemote -contains "$taskHead`trefs/tags/v0.0.40")) { throw 'Remote version mismatch' }
 $taskPointer=git show "v0.0.40:$($taskManifest.model)"
 if (-not ($taskPointer -contains "oid sha256:$taskHash")) { throw 'LFS pointer differs' }
 if (git diff --name-only v0.0.39 HEAD -- models/campus/WZMS_Campus_v039.blend deliverables/v0.0.39 web-preview reference/source reference/reports) { throw 'Frozen previous version or references changed' }
 git lfs fsck
 if ($LASTEXITCODE -ne 0) { throw 'LFS integrity check failed' }
 if (git status --porcelain) { throw 'Uncommitted changes remain' }
 [pscustomobject]@{Version='v0.0.40';Commit=$taskHead;ModelSHA256=$taskHash;ReviewedImages=14;Routes=68;Verified=$true} | ConvertTo-Json | Set-Content builds/final_refinement_delivery_audit.json -Encoding utf8
 Write-Output 'v0.0.40: model, 14 images, 68 routes, court orientation, materials, deferred wall, remote tag and LFS verified.'
}
finally { Pop-Location }
