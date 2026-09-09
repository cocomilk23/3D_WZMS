"""Assemble a completed internal Windows build, provenance and checksums for owner testing."""
import argparse,hashlib,json,pathlib,shutil,zipfile

parser=argparse.ArgumentParser();parser.add_argument('build_directory');args=parser.parse_args()
build=pathlib.Path(args.build_directory).resolve();allowed=pathlib.Path('E:/WZMS_ValidationBuilds').resolve()
assert build.parent==allowed,build
root=pathlib.Path(__file__).resolve().parents[2];ue=root/'ue'
state=json.loads((build/'build-process.json').read_text(encoding='utf8'))
assert state['state']=='complete' and (build/'Windows/WZMS.exe').is_file()
destination=build/'Delivery';assert not destination.exists(),'Preserve the existing assembled delivery.'
destination.mkdir()
for source,name in [('TOUR_TEST_BUILD.md','开始游览.md'),('TOUR_USER_GUIDE.md','操作说明.md'),('TOUR_ASSET_SOURCES.md','素材来源.md')]:
 shutil.copy2(ue/'Docs'/source,destination/name)
shutil.copy2(build/'source-manifest.json',destination/'source-manifest.json')
licenses=destination/'Licenses/NotoSansSC';licenses.mkdir(parents=True)
for name in ['OFL.txt','SOURCE.json','DERIVATIVE.json']:shutil.copy2(ue/'SourceFonts/NotoSansSC'/name,licenses/name)
shutil.copy2(ue/'SourceAudio/SOURCE.json',destination/'Licenses/EnvironmentAudio.json')
# Keep the cooked Windows directory in its original location: ZIP streams it directly,
# avoiding another multi-gigabyte working copy on the user's disk.
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as stream:
  for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
 return h.hexdigest()
source_manifest=json.loads((build/'source-manifest.json').read_text(encoding='utf8'))
changed=[name for name,expected in source_manifest['source_files_sha256'].items() if digest(root/name)!=expected]
assert not changed,('Source assets/config changed during the build; inspect before delivering',changed)
files=[(p,'Windows/'+p.relative_to(build/'Windows').as_posix()) for p in sorted((build/'Windows').rglob('*')) if p.is_file()]
files += [(p,p.relative_to(destination).as_posix()) for p in sorted(destination.rglob('*')) if p.is_file()]
checks=''.join(f'{digest(p)}  {name}\n' for p,name in files)
(destination/'SHA256SUMS.txt').write_text(checks,encoding='utf8')
files.append((destination/'SHA256SUMS.txt','SHA256SUMS.txt'))
archive=build/f'WZMS-{state["version"]}-Windows.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
 for path,name in files:z.write(path,'WZMS-CampusTour/'+name)
with zipfile.ZipFile(archive) as z:
 failed=z.testzip();assert failed is None,failed
archive_hash=digest(archive)
(build/(archive.name+'.sha256')).write_text(archive_hash+'  '+archive.name+'\n',encoding='utf8')
report={'source_commit':state['source_commit'],'version':state['version'],'archive':str(archive),'archive_bytes':archive.stat().st_size,'archive_sha256':archive_hash,'windows_bytes':sum(p.stat().st_size for p,n in files if n.startswith('Windows/')),'file_count':len(files),'zip_crc_checked':True,'source_assets_unchanged_during_build':True,'standalone_user_acceptance_pending':True,'launcher':str(build/'Windows/WZMS.exe')}
(build/'delivery-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
