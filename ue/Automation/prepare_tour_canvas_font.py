"""Create the Canvas-compatible composite font and preserve embedded Chinese glyph data."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();assets=unreal.EditorAssetLibrary;at=unreal.AssetToolsHelpers.get_asset_tools();log={}
factory=unreal.FontFileImportFactory();factory.set_editor_property('batch_create_font_asset',unreal.BatchCreateFontAsset.NO if assets.does_asset_exist('/Game/WZMS/Tour/UI/F_Tour_Chinese_Font') else unreal.BatchCreateFontAsset.YES)
task=unreal.AssetImportTask();task.filename=str(root.parent/'SourceFonts/NotoSansSC/WZMSTourSans-Regular.ttf');task.destination_path='/Game/WZMS/Tour/UI';task.destination_name='F_Tour_Chinese';task.automated=True;task.save=True;task.replace_existing=True;task.factory=factory
at.import_asset_tasks([task])
for path in assets.list_assets('/Game/WZMS/Tour/UI'):
 o=assets.load_asset(path);log[path]=o.get_class().get_name()
 if isinstance(o,unreal.Font):
  o.set_editor_property('legacy_font_size',48);assets.save_loaded_asset(o)
try:
 f=assets.load_asset('/Engine/EngineFonts/Roboto');cf=f.get_editor_property('composite_font');tf=cf.get_editor_property('default_typeface');log['typeface_probe']=str(tf);log['typeface_python_type']=str(type(tf));log['typeface_fonts']=str(tf.get_editor_property('fonts'))
except Exception as e:log['typeface_probe_error']=str(e)
(root/'Saved/Logs/tour_canvas_font.json').write_text(json.dumps(log,indent=2),encoding='utf8')
font=assets.load_asset('/Game/WZMS/Tour/UI/F_Tour_Chinese_Font');face=assets.load_asset('/Game/WZMS/Tour/UI/F_Tour_Chinese');assert isinstance(font,unreal.Font) and isinstance(face,unreal.FontFace)
face.set_editor_property('loading_policy',unreal.FontLoadingPolicy.INLINE);assets.save_loaded_asset(face);assets.save_loaded_asset(font)
(root.parent/'Reports/tour_font_assets.json').write_text(json.dumps({'font':font.get_path_name(),'font_face':face.get_path_name(),'legacy_canvas_size':48,'loading_policy':'Inline','license':'SourceFonts/NotoSansSC/OFL.txt','derivative':'SourceFonts/NotoSansSC/DERIVATIVE.json','glyph_render_validation_pending':True},indent=2),encoding='utf8')
