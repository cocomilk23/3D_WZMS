"""Build isolated camera-only sequences over the shipped campus, without editing its actors."""
import json,math,unreal
from pathlib import Path
root=Path(unreal.Paths.project_dir()).resolve();ue=root.parent
plan=json.loads((ue/'SourceReference/demo_shots_055.json').read_text(encoding='utf8'))
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assets=unreal.AssetToolsHelpers.get_asset_tools();folder='/Game/WZMS/Cinematics'

def pose(shot,u):
    # Gentle eased travel with nonzero speed through most of the shot.
    v=u*u*(3-2*u)
    p=[a+(b-a)*v for a,b in zip(shot['start'],shot['end'])]
    q=[a+(b-a)*v for a,b in zip(shot['target_start'],shot['target_end'])]
    dx,dy,dz=q[0]-p[0],-(q[1]-p[1]),q[2]-p[2]
    return [p[0]*100,-p[1]*100,p[2]*100,0,math.degrees(math.atan2(dz,math.hypot(dx,dy))),math.degrees(math.atan2(dy,dx))]

def build(name,preview):
    assert not unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+name),'Preserve existing sequence; choose a new revision.'
    seq=assets.create_asset(name,folder,unreal.LevelSequence,unreal.LevelSequenceFactoryNew())
    seq.set_display_rate(unreal.FrameRate(plan['fps'],1));seq.set_playback_start(0)
    cuts=seq.add_track(unreal.MovieSceneCameraCutTrack);cursor=0;rows=[]
    for shot in plan['shots']:
        positions=[0,.5,1] if preview else [None]
        for u in positions:
            length=1 if preview else round(shot['seconds']*plan['fps'])
            actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
            camera=actors.spawn_actor_from_class(unreal.CameraActor,unreal.Vector(0,0,0))
            component=camera.get_component_by_class(unreal.CameraComponent);assert component
            component.set_editor_property('field_of_view',shot['fov']);component.set_editor_property('aspect_ratio',16/9)
            binding=seq.add_spawnable_from_instance(camera)
            binding.set_display_name(shot['id']+(f'_{u}' if preview else ''))
            actors.destroy_actor(camera)
            section=binding.add_track(unreal.MovieScene3DTransformTrack).add_section();section.set_range(cursor-1,cursor+length+1)
            channels=section.get_all_channels();assert len(channels)==9
            for c in channels[6:]:c.set_default(1.0)
            for f in range(-1,length+1):
                values=pose(shot,u if preview else max(0,min(1,f/max(1,length-1))))
                for channel,value in zip(channels[:6],values):
                    channel.add_key(unreal.FrameNumber(cursor+f),float(value),interpolation=unreal.MovieSceneKeyInterpolation.LINEAR)
            cut=cuts.add_section();cut.set_range(cursor,cursor+length)
            cut.set_camera_binding_id(seq.get_binding_id(binding))
            rows.append({'id':shot['id'],'sample':u,'start':cursor,'end':cursor+length});cursor+=length
    seq.set_playback_end(cursor);unreal.EditorAssetLibrary.save_loaded_asset(seq)
    return {'sequence':seq.get_path_name(),'frames':cursor,'cuts':rows}

result={'preview':build('LS_Demo055_Contact_r02',True),'final':build('LS_Demo055_Campus_r02',False),'source':'Game campus 0.1.0-test.54; camera-only cinematic, not continuous player control.'}
(ue/'Reports/demo_sequences_055.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
