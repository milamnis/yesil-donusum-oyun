from pathlib import Path
from PIL import Image
import json,hashlib
base=Path('outputs/yesil-donusum/public/assets');out=base/'sprites/generated';out.mkdir(parents=True,exist_ok=True)
groups=[('OBJECT_SHEET_IRRIGATION_METHODS_FINAL.png.png',3,1,['faucet-aerator','faucet-repair','faucet-filter']),('OBJECT_SHEET_SHOWER_CHOICES_FINAL.png.png',3,1,['shower-compact','shower-classic','shower-rain']),('OBJECT_SHEET_LIGHTING_CHOICES.png.png',3,1,['bulb-incandescent','bulb-halogen','bulb-led']),('OBJ_IRRIGATION_TIMER_INSTALLED.png.png',3,1,['irrigation-hose','irrigation-sprinkler','irrigation-drip']),('OBJECT_SHEET_FOOD_PACKAGING_FINAL.png.png',3,2,['lentil-plastic','lentil-paper','lentil-return','apple-plastic','apple-paper','apple-mesh']),('OBJECT_SHEET_TEXTILE_PACKAGING_FINAL_V2.png.png',3,2,['towel-plastic','towel-box','towel-kraft','scarf-plastic','scarf-box','scarf-kraft']),('OBJECT_SHEET_WASTE_SORTING.png.png',3,2,['waste-paper','waste-plastic','waste-glass','waste-metal','waste-organic','waste-tissue']),('OBJECT_SHEET_LAUNDRY_CLOTHES.png.png',3,2,['clothes-white','clothes-color','clothes-dark','basket-white','basket-color','basket-dark']),('Renkli Mandallı Altı Plastik Torba.png',3,2,['bag-paper','bag-plastic','bag-glass','bag-metal','bag-organic','bag-other']),('OBJ_BATHROOM_BASIN.png.png',1,1,['basin']),('OBJ_IRRIGATION_TIMER.png.png',1,1,['irrigation-timer'])]
manifest={}
for name,cols,rows,keys in groups:
 f=base/'source'/name
 if not f.exists() and name.startswith('Renkli'):f=next((base/'source').glob('Renkli*'))
 im=Image.open(f).convert('RGBA');w,h=im.size
 for i,key in enumerate(keys):
  box=(round((i%cols)*w/cols),round((i//cols)*h/rows),round((i%cols+1)*w/cols),round((i//cols+1)*h/rows));tile=im.crop(box);bbox=tile.getchannel('A').point(lambda a:255 if a>15 else 0).getbbox();tile=tile.crop(bbox);tile.save(out/(key+'.webp'),lossless=True)
  manifest[key]={'source':f.name,'sourceSHA256':hashlib.sha256(f.read_bytes()).hexdigest(),'cell':box,'trim':bbox,'width':tile.width,'height':tile.height,'asset':'sprites/generated/'+key}
Path('work/main-revision/sprite-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(base/'sprites/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Generated',len(manifest),'sprites; originals unchanged')
