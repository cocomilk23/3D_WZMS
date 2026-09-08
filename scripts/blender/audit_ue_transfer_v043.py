"""Reimport every generated FBX in fresh empty scenes; not an Unreal runtime test."""
import bpy,json,hashlib,sys,math,gc
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];OUT=R/'builds/v043_ue_bundle';reports=[]
zone=sys.argv[sys.argv.index('--')+1]
manifest=json.loads((OUT/f'zone_{zone}.json').read_text(encoding='utf8'))
material_source=json.loads((OUT/'materials.json').read_text(encoding='utf8'))
photo_map={m['id']:m['textures'][0] for m in material_source['materials'] if m['textures']}
for rec in manifest['chunks']:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
    file=OUT/rec['file'];assert hashlib.sha256(file.read_bytes()).hexdigest()==rec['sha256']
    bpy.ops.import_scene.fbx(filepath=str(file),use_custom_normals=True,use_anim=False)
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(meshes)==1,(file,len(meshes))
    o=meshes[0];m=o.data;m.calc_loop_triangles();assert len(m.loop_triangles)==rec['triangles'],file
    co=np.empty(len(m.vertices)*3,dtype=np.float32);m.vertices.foreach_get('co',co);co=co.reshape(-1,3)
    mat=np.array(o.matrix_world);world=co@mat[:3,:3].T+mat[:3,3]
    assert np.isfinite(world).all()
    bounds=[world.min(axis=0).tolist(),world.max(axis=0).tolist()];err=float(np.abs(np.array(bounds)-np.array(rec['bounds_m'])).max());assert err<.005,(file,err,bounds,rec['bounds_m'])
    assert m.uv_layers.active,(file,'UV0 absent')
    uv=np.empty(len(m.loops)*2,dtype=np.float32);m.uv_layers.active.data.foreach_get('uv',uv);assert np.isfinite(uv).all()
    slots=[s.name for s in m.materials];assert slots==rec['materials'],(file,slots,rec['materials'])
    for material in m.materials:
        if material.name not in photo_map:continue
        linked_images=[n.image for n in material.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
        expected=hashlib.sha256((OUT/photo_map[material.name]).read_bytes()).hexdigest()
        assert any(Path(bpy.path.abspath(im.filepath)).is_file() and hashlib.sha256(Path(bpy.path.abspath(im.filepath)).read_bytes()).hexdigest()==expected for im in linked_images),(file,material.name,'Photo transfer missing')
    ids=np.empty(len(m.loop_triangles),dtype=np.int32);m.loop_triangles.foreach_get('material_index',ids)
    assert np.bincount(ids,minlength=len(slots)).tolist()==rec['material_triangle_counts'],(file,'face/material mapping')
    reports.append({'file':rec['file'],'triangles':len(m.loop_triangles),'bounds_error_m':err,'uv0_finite':True,'material_assignment_matches':True})
    print('UE_FBX_ROUNDTRIP_OK',rec['name'],flush=True)
    gc.collect()
result={'zone':zone,'all_passed':len(reports)==len(manifest['chunks']),'source_sha256':manifest['source_sha256'],'chunks':reports,'ue_runtime_tested':False,'shader_equivalence_claimed':False}
(OUT/f'roundtrip_{zone}.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print('UE_ROUNDTRIP_ZONE_COMPLETE',zone,flush=True)
