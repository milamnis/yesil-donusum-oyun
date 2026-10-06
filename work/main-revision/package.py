from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
root=Path('outputs/yesil-donusum');out=Path('outputs')
with ZipFile(out/'Yesil-Donusum-Oyun.zip','w',ZIP_DEFLATED,compresslevel=6) as z:
 for p in root.rglob('*'):
  if not p.is_file():continue
  rel=p.relative_to(root);parts=rel.parts
  if any(x in parts for x in ['node_modules','.git','qa','__pycache__']):continue
  if rel.as_posix().startswith('dist/assets/source/'):continue
  if '-debug.' in p.name:continue
  z.write(p,Path('yesil-donusum')/rel)
with ZipFile(out/'Ana-Revizyon-QA.zip','w',ZIP_DEFLATED,compresslevel=6) as z:
 for p in (root/'qa/main-revision').iterdir():
  if p.is_file() and 'debug' not in p.name:z.write(p,p.name)
 z.write(root/'REVIZYON-RAPORU.md','REVIZYON-RAPORU.md')
 z.write(root/'premium-audit.json','premium-audit.json')
for name in ['Yesil-Donusum-Oyun.zip','Ana-Revizyon-QA.zip']:
 p=out/name
 with ZipFile(p) as z:assert z.testzip() is None;print(name,round(p.stat().st_size/1024/1024,1),'MB',len(z.namelist()),'files')
