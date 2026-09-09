"""Package the validated content-only Windows tour using the installed UE runtime."""
import argparse,json,os,pathlib,subprocess,time,psutil,re,hashlib
root=pathlib.Path(__file__).resolve().parents[2];ue=root/'ue';project=ue/'WZMS/WZMS.uproject';parser=argparse.ArgumentParser();parser.add_argument('--version',default='0.1.0-preview');parser.add_argument('--validation-build',action='store_true',help='Internal test package in a separate directory; records unmet release checks and is not a public deliverable.');args=parser.parse_args();assert re.fullmatch(r'[0-9A-Za-z._-]+',args.version)
for p in psutil.process_iter(['name','cmdline']):
 try:
  if (p.info['name'] or '').lower()=='unrealeditor.exe' and str(project).replace('\\','/').lower() in ' '.join(p.info['cmdline'] or []).replace('\\','/').lower():raise RuntimeError('Save and close the owned project editor before cooking; keep source stable and free its memory.')
 except (psutil.NoSuchProcess,psutil.AccessDenied):pass
requirements={'tour_complete_routes_runtime.json':74,'tour_navigation_runtime.json':24,'tour_save_restore.json':None,'tour_perimeter_runtime.json':6,'tour_water_runtime.json':12,'tour_exposure_runtime.json':8,'tour_ui_interaction.json':None}
unmet=[]
for file,count in requirements.items():
 path=ue/'Reports'/file
 if not path.exists():unmet.append(file);continue
 data=json.loads(path.read_text(encoding='utf8'))
 if not data.get('passed') or (count is not None and not (data.get('complete') and len(data.get('cases',data.get('tests',[])))==count)):unmet.append(file)
assert args.validation_build or not unmet,('Release checks must pass',unmet)
dirty=subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip();assert not dirty,'Commit the validated working tree before a release build.'
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip();release=pathlib.Path('E:/WZMS_ValidationBuilds' if args.validation_build else 'E:/WZMS_Releases')/args.version;release.mkdir(parents=True,exist_ok=True)
binary=release/'Windows/WZMS.exe';assert not binary.exists(),'Use a new version directory; preserve previous deliverables.'
engine=pathlib.Path('D:/Program Files/Epic Games/UE_5.8/Engine');bat=engine/'Build/BatchFiles/RunUAT.bat';assert (engine/'Binaries/Win64/UnrealGame-Win64-Shipping.exe').exists()
env=os.environ.copy();env['UE-LocalDataCachePath']='E:/WZMS_UE_Cache/DDC';env['TEMP']='E:/WZMS_UE_Cache/Temp';env['TMP']=env['TEMP'];env['uebp_LogFolder']=str(release/'AutomationLogs')
for folder in [pathlib.Path(env['TEMP']),pathlib.Path(env['uebp_LogFolder'])]:folder.mkdir(parents=True,exist_ok=True)
command=[str(bat),f'-ScriptsForProject={project}','BuildCookRun',f'-project={project}','-installed','-noP4','-platform=Win64','-clientconfig=Shipping','-nocompile','-nocompileeditor','-skipbuildeditor','-cook','-map=/Game/WZMS/Maps/L_WZMS_Campus','-stage','-package','-pak','-iostore','-compressed','-prereqs','-archive',f'-archivedirectory={release}','-utf8output','-unattended']
files={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for folder in [ue/'WZMS/Content',ue/'WZMS/Config'] for p in sorted(folder.rglob('*')) if p.is_file()};files[str(project.relative_to(root)).replace('\\','/')]=hashlib.sha256(project.read_bytes()).hexdigest()
(release/'source-manifest.json').write_text(json.dumps({'source_commit':commit,'source_files_sha256':files,'purpose':'internal-validation' if args.validation_build else 'release-candidate','unmet_prebuild_checks':unmet,'standalone_acceptance_pending':True},indent=2),encoding='utf8');state={'version':args.version,'source_commit':commit,'state':'running','purpose':'internal-validation' if args.validation_build else 'release-candidate','unmet_prebuild_checks':unmet,'started_unix':time.time(),'command':command,'log':str(release/'build.log')}
with (release/'build.log').open('w',encoding='utf8') as log:
 process=subprocess.Popen(command,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW);state['pid']=process.pid;(release/'build-process.json').write_text(json.dumps(state,indent=2),encoding='utf8');print('Packaging PID',process.pid,'log',state['log'],flush=True);code=process.wait()
state.update(state='complete' if code==0 and binary.exists() else 'failed',exit_code=code,finished_unix=time.time(),launcher_exists=binary.exists());(release/'build-process.json').write_text(json.dumps(state,indent=2),encoding='utf8');print(json.dumps(state,indent=2),flush=True)
assert state['state']=='complete','Inspect the existing build log before resuming; no automatic restart.'
