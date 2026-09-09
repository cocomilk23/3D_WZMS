"""Record an observed real-input result; never synthesize an input or a runtime state."""
import argparse,json,time,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('--expected',required=True);p.add_argument('--screenshot');a=p.parse_args()
root=Path(__file__).resolve().parents[1];source=root/'WZMS/Saved/Logs/tour_ui_observation.json'
observed=json.loads(source.read_text(encoding='utf8'));assert time.time()-observed['observed_unix']<180,'Capture a fresh runtime observation after the input.'
expected=json.loads(a.expected);checks=[]
for key,value in expected.items():
 actual=observed
 for part in key.split('.'):actual=actual[part]
 ok=abs(actual-value)<.001 if isinstance(value,float) else actual==value
 checks.append({'property':key,'expected':value,'actual':actual,'passed':ok})
case={'name':a.name,'observed_unix':observed['observed_unix'],'checks':checks,'passed':all(c['passed'] for c in checks),'state':observed}
if a.screenshot:
 image=Path(a.screenshot).resolve();assert image.is_file();case['screenshot']=str(image.relative_to(root)).replace('\\','/');case['screenshot_sha256']=hashlib.sha256(image.read_bytes()).hexdigest()
dest=root/'Reports/tour_ui_interaction.json';report=json.loads(dest.read_text(encoding='utf8')) if dest.exists() else {'method':'Real mouse/key input through Windows Computer Use; subsequently observed native UE state. Function-level navigation tests are separate.','cases':[]}
report['cases']=[c for c in report['cases'] if c['name']!=a.name]+[case]
required={'initial_menu','help_open','help_close','quality_low','quality_medium','quality_high','volume_full','volume_off','volume_low','volume_medium','poi_card','menu_key','poi_map','flight_on','flight_off','continue','exit'}
report['remaining']=sorted(required-{c['name'] for c in report['cases']});report['complete']=not report['remaining'];report['passed']=report['complete'] and all(c['passed'] for c in report['cases'])
dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(a.name,case['passed']);assert case['passed']
