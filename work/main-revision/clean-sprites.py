from pathlib import Path
from PIL import Image
from collections import deque
import json
root=Path('public/assets/sprites/generated')
for name in ['shower-classic','shower-compact','shower-rain','irrigation-hose','irrigation-sprinkler','waste-tissue','waste-plastic','waste-metal','waste-organic','scarf-box','faucet-filter']:
 p=root/(name+'.webp'); im=Image.open(p).convert('RGBA');w,h=im.size;a=im.getchannel('A'); v=bytearray(a.tobytes());parts=[]
 for n in range(len(v)):
  if v[n]<16:continue
  q=[n];v[n]=0;part=[]
  while q:
   t=q.pop();part.append(t);x=t%w
   for j in ([t-1] if x else [])+([t+1] if x<w-1 else [])+([t-w] if t>=w else [])+([t+w] if t+w<len(v) else []):
    if v[j]>=16:v[j]=0;q.append(j)
  parts.append(part)
 parts.sort(key=len,reverse=True); alpha=bytearray(a.tobytes())
 for part in parts[1:]:
  for n in part:alpha[n]=0
 im.putalpha(Image.frombytes('L',(w,h),bytes(alpha)));im=im.crop(im.getbbox());im.save(p,lossless=True)
 print(name,im.size)
