from pathlib import Path
from PIL import Image,ImageDraw
import json
p=Path('outputs/yesil-donusum');ms=json.loads((p/'src/decisions/placements.json').read_text(encoding='utf-8'));ms.update({'rev-office-power-strip':{'x':1045,'y':380},'rev-office-power-meter':{'x':1113,'y':370},'rev-office-power-smart':{'x':1113,'y':370},'rev-roof-bonus-solar':{'x':840,'y':370}})
files=list((p/'qa/main-revision').glob('placement-rev-*.png'));out=Image.new('RGB',(1200,((len(files)+5)//6)*220),'#e6dfcf');d=ImageDraw.Draw(out)
for n,f in enumerate(files):
 key=f.stem.removeprefix('placement-');m=ms[key];x=68.6+m['x']*.8;y=m['y']*.8;y=max(85,y-22);im=Image.open(f);im=im.crop((int(x-100),int(y-85),int(x+100),int(y+105)));out.paste(im,(n%6*200,n//6*220));d.text((n%6*200+4,n//6*220+191),key.removeprefix('rev-'),fill='#263c31')
out.save(p/'qa/main-revision/placement-contact.png')

