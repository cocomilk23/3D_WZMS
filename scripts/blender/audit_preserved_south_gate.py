"""Compare the explicitly deferred south reverse wall to the accepted baseline.
Checks mesh, transform, modifiers and assigned shader/photo contents, not names alone.
"""
import bpy,sys,json,hashlib
from mathutils import Matrix
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
version=sys.argv[sys.argv.index('--')+1]
target=ROOT/'models/campus'/('WZMS_Campus_v%03d.blend'%int(version.rsplit('.',1)[1]))
def digest(normalize_gate_translation=False):
    o=bpy.data.objects['South name wall reverse photo surface']
    mats=[]
    for m in o.data.materials:
        nodes=[]
        for node in m.node_tree.nodes:
            item={'name':node.name,'type':node.type,'inputs':[]}
            for sock in node.inputs:
                if hasattr(sock,'default_value'):
                    val=sock.default_value
                    if not isinstance(val,(str,int,float,bool)):
                        try:val=list(val)
                        except TypeError:val=str(val)
                    item['inputs'].append([sock.name,val])
            if node.type=='TEX_IMAGE' and node.image:
                im=node.image
                item['image']={'size':list(im.size),'packed_sha256':hashlib.sha256(bytes(im.packed_file.data)).hexdigest() if im.packed_file else None}
            nodes.append(item)
        mats.append({'name':m.name,'nodes':nodes,'links':[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links]})
    value={'mesh_vertices':[list(v.co) for v in o.data.vertices],
      'mesh_faces':[list(f.vertices) for f in o.data.polygons],
      'uv':[[list(uv.uv) for uv in layer.data] for layer in o.data.uv_layers],
      'transform':[list(row) for row in (Matrix.Translation((26,25,0))@o.matrix_world if normalize_gate_translation else o.matrix_world)],
      'modifiers':[(m.name,m.type) for m in o.modifiers],'materials':mats}
    return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'models/campus/WZMS_Campus_v006.blend'))
baseline=digest()
baseline_matrix=bpy.data.objects['South name wall reverse photo surface'].matrix_world.copy()
bpy.ops.wm.open_mainfile(filepath=str(target))
relocated=int(version.rsplit('.',1)[1])>=42
current=digest(normalize_gate_translation=relocated)
expected=Matrix.Translation((-26,-25,0))@baseline_matrix if relocated else baseline_matrix
actual=bpy.data.objects['South name wall reverse photo surface'].matrix_world
motion_matches=max(abs(actual[r][k]-expected[r][k]) for r in range(4) for k in range(4))<1e-5
report={'baseline':'v0.0.6','version':version,'object':'South name wall reverse photo surface',
        'baseline_digest':baseline,'current_digest':current,'unchanged':baseline==current and not relocated,'content_unchanged':baseline==current,'approved_motion_matches':motion_matches,'approved_gate_translation':[-26,-25,0] if relocated else [0,0,0],
        'scope':'mesh, UVs, modifier names/types, shader sockets/links and packed image bytes; transform checked against explicitly approved rigid gate relocation introduced in v042 and retained thereafter'}
(ROOT/'deliverables'/version/'preservation_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('SOUTH_REVERSE_WALL_PRESERVED',baseline==current,flush=True)
if baseline!=current or not motion_matches:raise RuntimeError('Deferred south reverse wall changed')
