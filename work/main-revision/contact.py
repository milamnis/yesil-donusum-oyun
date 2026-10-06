from PIL import Image,ImageDraw
from pathlib import Path
files=list(Path('public/assets/sprites/generated').glob('*.webp'))
out=Image.new('RGB',(1000,((len(files)+5)//6)*155),'#ddd7c7'); d=ImageDraw.Draw(out)
for n,p in enumerate(files):
 im=Image.open(p).convert('RGBA'); im.thumbnail((155,120)); x=n%6*166;y=n//6*155;out.paste(im,(x+(155-im.width)//2,y),im);d.text((x,y+122),p.stem,fill='black')
out.save('../../work/main-revision/sprites.png')
