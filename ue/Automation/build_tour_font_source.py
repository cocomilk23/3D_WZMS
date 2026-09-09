"""Generate a renamed static regular-weight font from the preserved OFL variable source."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,'E:/WZMS_UE_Cache/Python')
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
root=Path(__file__).resolve().parents[1];p=root/'SourceFonts/NotoSansSC';font=TTFont(p/'NotoSansSC.ttf',recalcTimestamp=False);font=instantiateVariableFont(font,{'wght':400},inplace=True);font.recalcTimestamp=False
names={1:'WZMS Tour Sans',2:'Regular',3:'WZMS Tour Sans Regular 1.0',4:'WZMS Tour Sans Regular',6:'WZMSTourSans-Regular',16:'WZMS Tour Sans',17:'Regular'}
for row in font['name'].names:
 if row.nameID in names:row.string=names[row.nameID].encode(row.getEncoding(),errors='replace')
out=p/'WZMSTourSans-Regular.ttf';font.save(out)
(p/'DERIVATIVE.json').write_text(json.dumps({'source':'NotoSansSC.ttf','source_url':'https://github.com/google/fonts/tree/main/ofl/notosanssc','license':'OFL.txt','change':'Instantiate weight 400; rename family to WZMS Tour Sans; preserve copyright and license.','fonttools_version':'4.60.1','file':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2),encoding='utf8')
