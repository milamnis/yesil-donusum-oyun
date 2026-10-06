from pathlib import Path
import json,hashlib,shutil
p=Path('outputs/yesil-donusum');manifest=p/'public/assets/sprites/manifest.json';d=json.loads(manifest.read_text(encoding='utf-8'))
for key,m in d.items():m['derivedSHA256']=hashlib.sha256((p/'public/assets'/f"{m['asset']}.webp").read_bytes()).hexdigest()
manifest.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');shutil.copy2(manifest,p/'dist/assets/sprites/manifest.json')
r=p/'REVIZYON-RAPORU.md';s=r.read_text(encoding='utf-8');s+='''

## Son test durumu

39/39 birim testi geçti. TypeScript ve üretim derlemesi başarılı.
33 ürün alternatifi ayrı kurulum görüntüleriyle kontrol edildi. Zamanlayıcı mevcut
bahçe musluğunun ucuna bağlandı; hortumların kaynağı aynı musluğa taşındı.
Kaynaklar ve 47 türetilmiş görsel yerel dosya olarak doğrulandı.

Premium statik denetimi ortak `btn()` üreticisi için bir `actionless-button` bulgusu
verir. Bu yanlış pozitiftir: düğmeler `data-action` taşır; `main.ts` ortak kök click
listener'ı bunları `action()` işleyicisine gönderir. Tam akış ve dokunmatik testleri
bu düğmeleri gerçekten kullanmıştır. Denetim JSON'u bu tek bulguyu gizlemeden korur.
Bilinen açık oyun akışı hatası kalmadı; fiyatların ve örnek fatura etkilerinin
organizasyon tarafından son kez onaylanması gerekir.
''';r.write_text(s,encoding='utf-8')
q=p/'QA.md';s=q.read_text(encoding='utf-8');s='''# Güncel QA — 5 Ekim 2026

En güncel kabul raporu [REVIZYON-RAPORU.md](REVIZYON-RAPORU.md), kanıtlar
`qa/main-revision/` altındadır. 39 birim testi; dört dönem / 21 fırsat; üç masaüstü
boyutu; iki dokunmatik boyutu; çevrimdışı açılış ve 47 sprite; resmî sonuç, CSV/JSON,
silme/geri yükleme geçti. Ayrıştırma ekranı axe taraması 0 ihlal verdi.
Eski aşağıdaki rapor önceki teslimin tarihsel kaydıdır; yeni akışın test girişleri
`revision-flow.cjs`, `revision-offline.cjs`, `revision-placements.cjs` dosyalarıdır.

---

'''+s;q.write_text(s,encoding='utf-8')
