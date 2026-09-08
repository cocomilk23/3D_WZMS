"""Compare actual saved shader graphs with the recorded material scope."""
import bpy,json,hashlib,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];out=R/'deliverables/v0.0.40'
def signatures():
    result={}
    for m in bpy.data.materials:
        nodes=[]
        if not m.use_nodes:result[m.name]=str(list(m.diffuse_color));continue
        for n in m.node_tree.nodes:
            values=[]
            for s in n.inputs:
                if not hasattr(s,'default_value'):continue
                v=s.default_value
                if not isinstance(v,(str,bool,int,float)):
                    try:v=list(v)
                    except TypeError:v=str(v)
                values.append([s.name,v])
            record=[n.name,n.type,values]
            if n.type=='VALTORGB':record.append([(e.position,list(e.color)) for e in n.color_ramp.elements])
            if n.type=='TEX_IMAGE' and n.image:
                record.append([n.image.name,list(n.image.size),hashlib.sha256(bytes(n.image.packed_file.data)).hexdigest() if n.image.packed_file else None])
            nodes.append(record)
        links=[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links]
        result[m.name]=hashlib.sha256(json.dumps([nodes,links],sort_keys=True).encode()).hexdigest()
    return result
bpy.ops.wm.open_mainfile(filepath=str(R/'models/campus/WZMS_Campus_v039.blend'));before=signatures()
image_materials={m.name for m in bpy.data.materials if m.use_nodes and any(n.type=='TEX_IMAGE' for n in m.node_tree.nodes)}
bpy.ops.wm.open_mainfile(filepath=str(R/'models/campus/WZMS_Campus_v040.blend'));after=signatures()
manifest=json.loads((out/'refinement_manifest.json').read_text(encoding='utf8'));allowed={r['material'] for r in manifest['materials']}
changed=[n for n in before if n in after and before[n]!=after[n]]
unexpected=[n for n in changed if n not in allowed]
changed_images=sorted(n for n in image_materials if before[n]!=after.get(n))
report={'baseline':'v0.0.39','version':'v0.0.40','material_count_checked':len(before),'changed_existing_materials':changed,'unexpected_changes':unexpected,'all_passed':not unexpected and not changed_images,'image_materials_checked':sorted(image_materials),'changed_image_materials':changed_images,'original_image_materials_preserved':not changed_images}
(out/'material_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
assert report['all_passed'] and report['original_image_materials_preserved'],unexpected
print('REFINEMENT_MATERIAL_AUDIT_PASSED',len(changed),flush=True)
