param([switch]$WaitForExit,[string]$Map='')
$ErrorActionPreference='Stop'
$taskWorkspace=Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$taskProject=Join-Path $taskWorkspace 'ue/WZMS/WZMS.uproject'
$taskEngine='D:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe'
$taskCache='E:/WZMS_UE_Cache'
$taskLogs=Join-Path $taskWorkspace 'ue/WZMS/Saved/Logs'
foreach ($taskDirectory in @("$taskCache/DDC", "$taskCache/Temp", "$taskCache/Zen", $taskLogs)) {
    New-Item -ItemType Directory -Path $taskDirectory -Force | Out-Null
}
$taskExisting=Get-CimInstance Win32_Process -Filter "Name='UnrealEditor.exe'" | Where-Object { $_.CommandLine -like "*$taskProject*" }
if ($taskExisting) { Write-Output "WZMS editor already running: $($taskExisting.ProcessId)"; exit 0 }
${env:UE-LocalDataCachePath}="$taskCache/DDC"
$env:TEMP="$taskCache/Temp"
$env:TMP="$taskCache/Temp"
$taskArguments=@(('"'+$taskProject+'"'), '-NoSplash', '-Unattended', '-NoSound', '-culture=en', '-SCCProvider=None', '-ModelContextProtocolStartServer', '-ModelContextProtocolPort=8010', ('-AbsLog="'+$taskLogs+'/UnrealMCP.log"'))
if ($Map) {
    if ($Map -notmatch '^/Game/WZMS/Maps/[A-Za-z0-9_]+$') { throw 'Invalid WZMS map path' }
    $taskArguments=@(('"'+$taskProject+'"'),$Map)+$taskArguments[1..($taskArguments.Count-1)]
}
$taskEditor=Start-Process -FilePath $taskEngine -ArgumentList $taskArguments -WorkingDirectory $taskWorkspace -WindowStyle Hidden -PassThru
$taskEditor.Id | Set-Content (Join-Path $taskLogs 'editor_pid.txt')
Write-Output "WZMS editor launched: $($taskEditor.Id); MCP http://127.0.0.1:8010/mcp"
if ($WaitForExit) { $taskEditor.WaitForExit() }
