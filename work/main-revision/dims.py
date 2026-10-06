from PIL import Image
from pathlib import Path
import json
for p in Path('public/assets/sprites/generated').glob('*.webp'):
 im=Image.open(p); print(p.stem,im.size)
