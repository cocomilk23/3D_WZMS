"""Prepare identical stationary views for before/after temporal checks."""
import json,math
from pathlib import Path
ue=Path(__file__).resolve().parents[1];r=json.loads((ue/'Reports/final057_probe.json').read_text())
keys=['188_South_gate','05_Plaza','172_Refined_facade','187_Tennis','18_Buqing','63_Library','67_Library','69_Library','70_Library','106_Zhouyuan','111_Alumni','139_Basketball','141_Basketball','174_Refined','38_North_gate','148_Gym','150_Gym','153_Math','157_Math','159_History','161_History','164_Canteen','182_Refined_whole','177_Refined_landscape']
shots=[]
for k in keys:
 a=next(x for x in r['cameras'] if k in x['label']);p=[a['location'][0]/100,-a['location'][1]/100,a['location'][2]/100];pitch,yaw=map(math.radians,a['rotation'][1:]);q=[p[0]+math.cos(pitch)*math.cos(yaw)*30,p[1]-math.cos(pitch)*math.sin(yaw)*30,p[2]+math.sin(pitch)*30]
 shots.append({'id':a['label'],'seconds':1,'start':p,'end':p,'target_start':q,'target_end':q,'fov':65})
for name,p,q in [('Crest_top',[54,150,21],[54,157,0]),('Court_ground',[10,235,1.7],[-1,248,0]),('Court_top',[14.5,265,86],[14.5,265,0]),('Track_goals',[-105,214,4],[-85,235,1]),('East_islands',[224,155,12],[272,134,4]),('North_exterior',[84,330,5],[125,363,10])]:
 shots.append({'id':name,'seconds':1,'start':p,'end':p,'target_start':q,'target_end':q,'fov':65})
(ue/'SourceReference/final057_review_shots.json').write_text(json.dumps({'fps':24,'resolution':[1280,720],'shots':shots},indent=2)+'\n')
(ue/'WZMS/Saved/Logs/demo_build_request.json').write_text(json.dumps({'plan':'final057_review_shots.json','prefix':'LS_Final057','revision':'audit','report':'final057_review_sequences.json'}))
print('Stationary views',len(shots))
