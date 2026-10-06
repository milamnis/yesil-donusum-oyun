from pathlib import Path
import zipfile, shutil, json

root = Path(__file__).resolve().parents[2]
project = root / 'outputs/yesil-donusum'
qa = project / 'qa'
assert json.loads((qa/'ux.json').read_text())['passed']
assert json.loads((qa/'refinement.json').read_text())['passed']
gallery = root / 'outputs/Sade-Arayuz-QA'
gallery.mkdir(exist_ok=True)
cards=[]
for width in [1920,1366,1024]:
    for state in ['overview','kitchen','kitchen-market','kitchen-purchased','kitchen-ready','kitchen-lesson','bathroom','bathroom-market','bathroom-purchased','bathroom-ready','bathroom-lesson','workshop','laundry','garden']:
        name=f'ux-{width}-{state}.png'
        shutil.copy2(qa/name,gallery/name)
        cards.append(f'<figure><a href="{name}"><img loading="lazy" src="{name}" alt="{width} · {state}"></a><figcaption>{width} · {state}</figcaption></figure>')
for name in ['ux.json','ux-preservation.json','refinement.json','full-flow.json','touch.json','vertical-slice.json']:
    shutil.copy2(qa/name,gallery/name)
shutil.copy2(project/'QA.md',gallery/'QA.md')
(gallery/'index.html').write_text('''<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sade arayüz — QA</title><style>body{background:#193c30;color:#fff3d8;font:16px system-ui;padding:24px}main{max-width:1500px;margin:auto}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px}figure{margin:0;background:#2a4c3e;border-radius:12px;overflow:hidden}img{width:100%;display:block}figcaption{padding:12px}a{color:inherit}</style><main><h1>Yeşil Dönüşüm · Sade arayüz</h1><p>Tek sorun → ilgili seçenekler → otomatik dönüş → Yerleştir → Anladım.</p><p>1920×1080, 1366×768 ve 1024×768 tablet emülasyonu. Testler izole kayıtlardadır. Görsele tıklayarak tam boy açabilirsiniz.</p><section>'''+''.join(cards)+'</section></main></html>',encoding='utf-8')
for folder,archive in [(gallery,root/'outputs/Sade-Arayuz-QA.zip'),(project,root/'outputs/Yesil-Donusum-Oyun.zip')]:
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for f in folder.rglob('*'):
            rel=f.relative_to(folder)
            if f.is_file() and not any(part in {'node_modules','.git','.vite','qa','__pycache__'} for part in rel.parts):
                z.write(f,folder.name+'/'+rel.as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
    print(archive.name,archive.stat().st_size,'bytes, CRC verified')
print('QA screenshots:',len(cards))
