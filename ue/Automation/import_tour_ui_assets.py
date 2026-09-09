"""Import the fixed campus map and an OFL Chinese font for runtime navigation."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();assets=unreal.EditorAssetLibrary;at=unreal.AssetToolsHelpers.get_asset_tools();logs={}
for filename,name,destination in [(root.parent/'SourceTextures/T_Tour_CampusMap.png','T_Tour_CampusMap','/Game/WZMS/Tour/UI')]:
 assert filename.exists(),filename
 task=unreal.AssetImportTask();task.filename=str(filename);task.destination_path=destination;task.destination_name=name;task.automated=True;task.replace_existing=True;task.save=True
 if filename.suffix=='.ttf':
  factory=unreal.FontFileImportFactory();factory.set_editor_property('batch_create_font_asset',unreal.BatchCreateFontAsset.CREATE_IF_NO_FONT_EXISTS);task.factory=factory
 at.import_asset_tasks([task]);logs[name]=list(task.imported_object_paths)
tx=assets.load_asset('/Game/WZMS/Tour/UI/T_Tour_CampusMap');assert tx;tx.set_editor_property('lod_group',unreal.TextureGroup.TEXTUREGROUP_UI);tx.set_editor_property('never_stream',True);assets.save_loaded_asset(tx)
for name in ['Font','FontFactory','FontFileImportFactory','FontFace','FontData','CompositeFont','Typeface','TypefaceEntry']:
 cls=getattr(unreal,name,None);logs[name]=str(cls.__doc__) if cls else None
face=assets.load_asset('/Game/WZMS/Tour/UI/FF_Tour_Chinese');logs['imported_font_class']=face.get_class().get_name() if face else None
logs['ui_assets']=list(assets.list_assets('/Game/WZMS/Tour/UI'))
(root/'Saved/Logs/tour_ui_assets.json').write_text(json.dumps(logs,indent=2),encoding='utf8')
