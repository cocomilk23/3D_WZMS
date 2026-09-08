"""Release build memory, assemble completed zones and validate the saved campus."""
from ue_mcp import UnrealMcpClient
from run_campus_zone import restart_editor,run_job
client=UnrealMcpClient();client.connect()
client=restart_editor(client,'/Game/WZMS/Maps/L_WZMS_Campus')
try:
    run_job(client,'place_campus_zones.py')
    run_job(client,'validate_campus_delivery.py')
    print('CAMPUS CHECKPOINT VERIFIED',flush=True)
finally:client.close()
