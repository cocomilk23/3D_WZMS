"""Add a quiet optional ambient bed and sound-mix assets for the volume control."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();assets=unreal.EditorAssetLibrary;at=unreal.AssetToolsHelpers.get_asset_tools();base='/Game/WZMS/Tour/Audio'
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
soundclass=assets.load_asset(base+'/SC_Tour') or at.create_asset('SC_Tour',base,unreal.SoundClass,unreal.SoundClassFactory())
mix=assets.load_asset(base+'/Mix_Tour') or at.create_asset('Mix_Tour',base,unreal.SoundMix,unreal.SoundMixFactory())
task=unreal.AssetImportTask();task.filename=str(root.parent/'SourceAudio/Tour_Gentle_Air.wav');task.destination_path=base;task.destination_name='SW_Gentle_Air';task.automated=True;task.replace_existing=True;task.save=True;at.import_asset_tasks([task]);wave=assets.load_asset(base+'/SW_Gentle_Air');assert wave
wave.set_editor_property('looping',True);wave.set_editor_property('sound_class_object',soundclass)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors={a.get_actor_label():a for a in sub.get_all_level_actors()};a=actors.get('Tour_Gentle_Ambience') or sub.spawn_actor_from_class(unreal.AmbientSound,unreal.Vector());a.set_actor_label('Tour_Gentle_Ambience');a.set_folder_path('Tour Environment/Ambience');c=a.get_component_by_class(unreal.AudioComponent);c.set_sound(wave);c.set_volume_multiplier(.25);c.set_editor_property('allow_spatialization',False);c.set_editor_property('auto_activate',True)
for o in [wave,soundclass,mix]:assets.save_loaded_asset(o)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
(root.parent/'Reports/tour_audio_build.json').write_text(json.dumps({'source':'SourceAudio/SOURCE.json','sound':wave.get_path_name(),'sound_class':soundclass.get_path_name(),'mix':mix.get_path_name(),'component_volume':.25,'looping':True,'volume_control_and_listening_test_pending':True},indent=2),encoding='utf8')
