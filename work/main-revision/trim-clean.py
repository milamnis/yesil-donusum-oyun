from pathlib import Path
from PIL import Image
import json
root=Path('public/assets/sprites/generated')
for name in ['shower-classic','shower-compact','shower-rain','irrigation-hose','irrigation-sprinkler','waste-tissue','waste-plastic','waste-metal','waste-organic','scarf-box','faucet-filter']:
 p=root/(name+'.webp');im=Image.open(p);im.putalpha(im.getchannel('A').point(lambda a:0 if a<16 else a));im=im.crop(im.getbbox());im.save(p,lossless=True);print(name,im.size)
