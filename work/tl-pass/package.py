from pathlib import Path
import zipfile, json, shutil, html

root = Path(__file__).resolve().parents[2]
project = root / 'outputs/yesil-donusum'
with zipfile.ZipFile(root / 'work/tl-pass/before.zip') as previous:
    protected = [p for p in project.rglob('*') if p.is_file() and (p.is_relative_to(project / 'public/assets') or p == project / 'src/placements.ts')]
    changed = [str(p.relative_to(project)) for p in protected if previous.read('yesil-donusum/' + p.relative_to(project).as_posix()) != p.read_bytes()]
    assert not changed, changed
print('Protected files unchanged:', len(protected))
report = json.loads((project / 'qa/tl.json').read_text(encoding='utf-8'))
print('TL audits:', len(report['audits']))
gallery = root / 'outputs/QA-Ekranlari'
gallery.mkdir(exist_ok=True)
cards = []
for p in sorted((project / 'qa').glob('tl-*.png')):
    shutil.copy2(p, gallery / p.name)
    title = p.stem.removeprefix('tl-')
    cards.append(f'<figure><a href="{p.name}"><img loading="lazy" src="{p.name}" alt="{title}"></a><figcaption>{title}</figcaption></figure>')
(gallery / 'index.html').write_text('''<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Yeşil Dönüşüm — QA ekranları</title><style>body{margin:0;padding:32px;background:#173b30;color:#fff3d8;font:16px system-ui}main{max-width:1500px;margin:auto}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}figure{margin:0;background:#244c3e;border-radius:12px;overflow:hidden}img{width:100%;display:block}figcaption{padding:14px}p{line-height:1.6}</style><main><h1>Yeşil Dönüşüm — TL ve seçim QA</h1><p>1920×1080, 1366×768 ve 1024×768 tablet emülasyonu. Görselleri tam boy açmak için tıklayın. İzole test kayıtlarında bütün değiştirme seçeneklerini denemek için kasa yükseltilmiştir; gerçek oyunun başlangıç kasası ₺2.500’dür.</p><section>''' + ''.join(cards) + '</section></main></html>', encoding='utf-8')
with zipfile.ZipFile(root / 'outputs/QA-Ekranlari.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for p in gallery.iterdir():
        z.write(p, 'QA-Ekranlari/' + p.name)
with zipfile.ZipFile(root / 'outputs/QA-Ekranlari.zip') as z:
    assert z.testzip() is None
print('Gallery images:', len(cards))
with zipfile.ZipFile(root / 'outputs/Yesil-Donusum-Oyun.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for p in project.rglob('*'):
        rel = p.relative_to(project)
        if p.is_file() and not any(part in {'node_modules', '.git', '.vite', 'qa', '__pycache__'} for part in rel.parts):
            z.write(p, 'yesil-donusum/' + rel.as_posix())
with zipfile.ZipFile(root / 'outputs/Yesil-Donusum-Oyun.zip') as z:
    assert z.testzip() is None
    assert 'yesil-donusum/src/economy.ts' in z.namelist()
    assert 'yesil-donusum/dist/index.html' in z.namelist()
print('Game archive verified')
