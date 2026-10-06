from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
root=Path('outputs/yesil-donusum');target=Path('outputs/Ana-Revizyon-QA.zip')
with ZipFile(target,'w',ZIP_DEFLATED,compresslevel=6) as z:
 for p in (root/'qa/main-revision').iterdir():
  if p.is_file() and 'debug' not in p.name:z.write(p,p.name)
 z.write(root/'REVIZYON-RAPORU.md','REVIZYON-RAPORU.md');z.write(root/'premium-audit.json','premium-audit.json')
with ZipFile(target) as z:assert z.testzip() is None
print('Updated QA archive verified')
