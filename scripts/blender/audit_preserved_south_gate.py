"""Compare the explicitly deferred south reverse wall to the accepted baseline.
Checks mesh, transform, modifiers and assigned shader/photo contents, not names alone.
"""
import bpy,sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
version=sys.argv[sys.argv.index('--')+1]
target=ROOT/'models/campus'/('WZMS_Campus_v%03d.blend'%int(version.rsplit('.',1)[1]))
def digest():
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
      'transform':[list(row) for row in o.matrix_world],
      'modifiers':[(m.name,m.type) for m in o.modifiers],'materials':mats}
    return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'models/campus/WZMS_Campus_v006.blend'))
baseline=digest()
bpy.ops.wm.open_mainfile(filepath=str(target))
current=digest()
report={'baseline':'v0.0.6','version':version,'object':'South name wall reverse photo surface',
        'baseline_digest':baseline,'current_digest':current,'unchanged':baseline==current,
        'scope':'mesh, UVs, transform, modifier names/types, shader sockets/links and packed image bytes'}
(ROOT/'deliverables'/version/'preservation_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('SOUTH_REVERSE_WALL_PRESERVED',baseline==current,flush=True)
if baseline!=current:raise RuntimeError('Deferred south reverse wall changed')
