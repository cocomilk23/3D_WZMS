import bpy
from pathlib import Path
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
mesh=bpy.data.meshes.new('AxisFixture')
mesh.from_pydata([(0,0,0),(2,0,0),(0,3,0),(0,0,5)],[],[(0,2,1),(0,1,3),(0,3,2),(1,2,3)])
obj=bpy.data.objects.new('AxisFixture',mesh);sc.collection.objects.link(obj)
obj.select_set(True);bpy.context.view_layer.objects.active=obj
out=Path('E:/WZMS_UE_Cache/AxisFixture.fbx')
bpy.ops.export_scene.fbx(filepath=str(out),use_selection=True,object_types={'MESH'},use_mesh_modifiers=False,mesh_smooth_type='FACE',use_tspace=False,add_leaf_bones=False,bake_anim=False,axis_forward='-Y',axis_up='Z',apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS')
