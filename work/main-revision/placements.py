from pathlib import Path
from PIL import Image,ImageDraw
import json
root=Path('public/assets/sprites/generated')
for name,box,erase in [('compact',(212,179,485,517),(0,0,10,65)),('classic',(143,160,519,574),(0,0,85,69)),('rain',(0,136,662,608),(0,0,233,45))]:
 im=Image.open(root/f'shower-{name}.webp').crop(box);ImageDraw.Draw(im).rectangle(erase,fill=(0,0,0,0));im.save(root/f'shower-{name}-installed.webp',lossless=True)
assets=json.loads(Path('src/decisions/assets.json').read_text(encoding='utf-8-sig'));meta={}
def entry(room,slot,x,y,scale,**kw):return dict(sceneId=room,slotId=slot,x=x,y=y,scale=scale,rotation=0,anchorX=.5,anchorY=.98,zIndex=12,replaceExisting=True,**kw)
for id,a in assets.items():
 if not a['asset']:continue
 asset=a['asset']; m=None
 if id=='rev-tap-aerator':m=entry('kitchen',a['installationSlot'],762,346,.047);m.update(anchorX=.6,anchorY=.12,rotation=-8)
 elif id=='rev-tap-filter':m=entry('kitchen',a['installationSlot'],762,346,.11);m.update(anchorX=.85,anchorY=.68)
 elif id=='rev-tap-repair':m=entry('kitchen',a['installationSlot'],805,369,1,render='maintenance')
 elif id.startswith('rev-shower-'):
  name=id.removeprefix('rev-shower-');m=entry('bathroom','shower_arm_tip',1108,67,{'compact':.16,'classic':.15,'rain':.16}[name]);m.update(asset=f'sprites/generated/shower-{name}-installed',anchorY=.015,anchorX={'compact':.28,'classic':.36,'rain':.45}[name],rotation=7)
 elif id=='rev-basin-place':m=entry('bathroom','basin_floor',1105,690,.19,shadow=dict(x=1105,y=684,width=175,height=32,alpha=.12))
 elif id.startswith('rev-light-home'):m=entry('home','pendant_bulb',815,55,.068);m.update(anchorY=.99,rotation=180)
 elif id.startswith('rev-light-workshop'):m=entry('workshop','office_pendant',854,111,.073);m.update(anchorY=.99,rotation=180)
 elif id.startswith('rev-office-power'):continue
 elif id=='rev-irrigation-drip':m=entry('garden','planted_rows',902,505,1,render='irrigation')
 elif id=='rev-irrigation-hose':m=entry('garden','garden_hose',834,630,.19,shadow=dict(x=834,y=625,width=100,height=18,alpha=.12),cable=[[780,601],[729,543],[693,423],[731,254]])
 elif id=='rev-irrigation-sprinkler':m=entry('garden','garden_sprinkler',1010,540,.16,shadow=dict(x=1010,y=537,width=100,height=15,alpha=.12),cable=[[958,531],[800,520],[731,254]])
 elif id=='rev-irrigation-timer-timer':m=entry('garden','garden_timer',729,217,.065);m.update(anchorY=.18)
 elif id.startswith('rev-pack-'):
  im=Image.open(Path('public/assets')/(asset+'.webp'));m=entry('storage','packing_table',797,606,125/im.height,shadow=dict(x=797,y=603,width=85,height=17,alpha=.1))
 elif id=='rev-roof-bonus-solar':continue
 if m:meta[id]=m
Path('src/decisions/placements.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
p=Path('src/placements.ts');s=p.read_text(encoding='utf-8');s='import decisionPlacements from "./decisions/placements.json";\n'+s;s+='''
Object.assign(placements, decisionPlacements);
placements['rev-office-power-strip']={...placements.strip};
placements['rev-office-power-meter']={...placements.meter};
placements['rev-office-power-smart']={sceneId:'workshop',slotId:'office_smart_socket',x:1113,y:348,scale:.14,rotation:0,anchorX:.73,anchorY:.15,zIndex:14,replaceExisting:true,asset:'obj_laundry_smart_plug_installed'};
placements['rev-roof-bonus-solar']={...placements.solar};
''';p.write_text(s,encoding='utf-8')
p=Path('src/physical.ts');s=p.read_text(encoding='utf-8').replace('if (id !== "tap-a") return;','if (id !== "tap-a" && id !== "rev-tap-aerator") return;');s=s.replace('    if (m.flipX) img.setFlipX(true);','''    if(id==='rev-basin-place'){
      const water=scene.add.ellipse(1105,596,150,57,0x8fcbd0,.55).setDepth(m.zIndex+.1).setScale(.25);
      scene.tweens.add({targets:water,scaleX:1,scaleY:1,duration:1600,ease:'Sine.Out'});
    }
    if (m.flipX) img.setFlipX(true);''');p.write_text(s,encoding='utf-8')
p=Path('scripts/offline.mjs');s=p.read_text().replace('!p.endsWith("sw.js")','!p.endsWith("sw.js") && !p.includes("/assets/source/")');p.write_text(s)
