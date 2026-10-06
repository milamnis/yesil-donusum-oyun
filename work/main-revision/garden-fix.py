from pathlib import Path
from PIL import Image,ImageDraw
import json
p=Path('src/decisions/placements.json');d=json.loads(p.read_text(encoding='utf-8'));d['rev-irrigation-timer-timer'].update(x=672,y=186,scale=.06,anchorX=.45,anchorY=.015,crop=[0,433,583,930]);d['rev-irrigation-drip']['slotId']='garden_drip_rows'
for id in ['rev-irrigation-hose','rev-irrigation-sprinkler']:d[id]['cable'][-1:]=[[674,260],[672,187]]
p.write_text(json.dumps(d,indent=2),encoding='utf-8')
p=Path('src/physical.ts');s=p.read_text(encoding='utf-8');s=s.replace('  [...headers, ...rows].forEach((points) => {','''  if(m.slotId==='garden_drip_rows') headers[2].splice(0,1,[672,187],[674,260]);
  [...headers, ...rows].forEach((points) => {''');p.write_text(s,encoding='utf-8')
p=Path('public/assets/sprites/generated/shower-rain-installed.webp');im=Image.open(p);ImageDraw.Draw(im).rectangle((0,0,220,80),fill=(0,0,0,0));im.save(p,lossless=True)
p=Path('scripts/build_revision_sprites.py');s=p.read_text(encoding='utf-8').replace("('rain',(0,136,662,608),(0,0,233,45))","('rain',(0,136,662,608),(0,0,233,80))");p.write_text(s,encoding='utf-8')
p=Path('package.json');d=json.loads(p.read_text(encoding='utf-8'));d['scripts']['test:offline']='node scripts/revision-offline.cjs';d['scripts']['test:touch']='node scripts/revision-offline.cjs';d['scripts']['test:placements']='tsx scripts/revision-fixtures.ts && node scripts/revision-placements.cjs';p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
