"""Verify the isolated WZMS MCP server with a temporary actor; no level is saved."""
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from ue_mcp import UnrealMcpClient

SCENE = 'editor_toolset.toolsets.scene.SceneTools'
ACTOR = 'editor_toolset.toolsets.actor.ActorTools'
client = UnrealMcpClient()
client.connect()
probe = None
report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'endpoint': 'http://127.0.0.1:8010/mcp'}

def call(toolset, name, args):
    return client.call_meta('call_tool', {'toolset_name': toolset, 'tool_name': name, 'arguments': args})['returnValue']

try:
    listed = client.call_meta('list_toolsets', {})
    report['toolset_count'] = len([line for line in listed.splitlines() if line.startswith('- ')])
    report['level'] = call(SCENE, 'get_current_level', {})
    # The bootstrap proof runs only against the empty startup map.
    if report['level'] != '/Engine/Maps/Entry':
        raise RuntimeError('Expected bootstrap Entry map; refusing to alter an active production level.')
    name = 'WZMS_MCP_Probe_' + uuid4().hex[:12]
    probe = call(SCENE, 'add_to_scene_from_class', {
        'actor_type': {'refPath': '/Script/Engine.StaticMeshActor'}, 'name': name,
        'xform': {'location': {'x': 100, 'y': 200, 'z': 300}}, 'snap_to_ground': False})
    report['created_actor'] = probe
    xform = call(ACTOR, 'get_actor_transform', {'actor': probe})
    report['readback_transform'] = xform
    assert xform['location'] == {'x': 100, 'y': 200, 'z': 300}, xform
    call(SCENE, 'remove_from_scene', {'actor': probe})
    probe = None
    remaining = call(SCENE, 'find_actors', {'name': name, 'tag': '', 'collision_channels': []})
    assert not remaining, remaining
    report.update(passed=True, temporary_actor_removed=True, campus_assets_imported=False)
    dest = Path(__file__).resolve().parents[1] / 'Reports/mcp_connection.json'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
finally:
    if probe:
        call(SCENE, 'remove_from_scene', {'actor': probe})
    client.close()
