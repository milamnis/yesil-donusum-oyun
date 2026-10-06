from pathlib import Path
import json,hashlib
from PIL import Image
project=Path('outputs/yesil-donusum');work=Path('work/main-revision')
crop=(work/'crop.py').read_text(encoding='utf-8-sig').replace("base=Path('outputs/yesil-donusum/public/assets')","base=Path(__file__).resolve().parents[1]/'public/assets'")
crop='import os\nos.chdir(Path(__file__).resolve().parents[1])\n'+crop if False else crop
crop=crop.replace("Path('work/main-revision/sprite-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')",'')
cleanup=(work/'clean-sprites.py').read_text(encoding='utf-8-sig').replace("Path('public/assets/sprites/generated')","base/'sprites/generated'")
trim=(work/'trim-clean.py').read_text(encoding='utf-8-sig').replace("Path('public/assets/sprites/generated')","base/'sprites/generated'")
heads=(work/'placements.py').read_text(encoding='utf-8-sig').split('assets=json.loads')[0].replace("Path('public/assets/sprites/generated')","base/'sprites/generated'")
end='''
for key,entry in manifest.items():
    target=out/(key+'.webp');image=Image.open(target)
    entry.update(width=image.width,height=image.height,derivedSHA256=hashlib.sha256(target.read_bytes()).hexdigest(),cleanup='alpha trim; isolated neighboring fragments removed on selected objects')
for name in ['compact','classic','rain']:
    key=f'shower-{name}-installed';target=out/(key+'.webp');image=Image.open(target)
    manifest[key]={'derivedFrom':f'shower-{name}','width':image.width,'height':image.height,'asset':'sprites/generated/'+key,'derivedSHA256':hashlib.sha256(target.read_bytes()).hexdigest(),'note':'Head and neck cropped from supplied shower; wall mount excluded.'}
(base/'sprites/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
'''
(project/'scripts/build_revision_sprites.py').write_text(crop+'\n'+cleanup+'\n'+trim+'\n'+heads+'\n'+end,encoding='utf-8')
base=project/'public/assets';out=base/'sprites/generated';manifest=json.loads((base/'sprites/manifest.json').read_text(encoding='utf-8'));exec(end)
ops=json.loads((project/'src/decisions/opportunities.json').read_text(encoding="utf-8"));scores=json.loads((project/'src/decisions/scores.json').read_text(encoding="utf-8"));rooms={'kitchen':'Mutfak','bathroom':'Banyo','home':'Oturma odası','workshop':'Ofis','laundry':'Çamaşırhane','garden':'Bahçe','storage':'Depo','roof':'Çatı'}
lines=['| ROOM | OPPORTUNITY | CHOICE COUNT | BEST SCORE | MIN SCORE | ASSET STATUS | COPY STATUS |','|---|---|---:|---:|---:|---|---|']
for o in ops:
 sort=o['kind']=='sorting';values=[scores[c]['decisionScore'] for c in o['choices']];count=len(o.get('targets',[])) if sort else len(o['choices']);mx=100 if sort else max(values);mn=0 if sort else min(values)
 lines.append(f"| {rooms[o['roomId']]} | {o['title']}{' (isteğe bağlı)' if not o['core'] else ''} | {count} | {mx} | {mn} | {'Kesilmiş sprite' if o['kind'] in ['sorting','product'] else 'UI / hotspot'} | Kısa sonuç + açıklama |")
report='''# Ana revizyon raporu — 5 Ekim 2026

Mevcut Phaser/Vite oyunu üzerinden devam edildi. Kayıt, 26 kurum, iki katılımcı,
arka planlar, dört dönem, ses, yönetim, CSV/JSON korunur.

## Değişiklikler

- 21 fırsat: 18 temel karar, 3 puansız isteğe bağlı adım. Her temel seçimde en az üç alternatif/hedef vardır.
- 51 karar seçeneği; bunların 33'ü satın alınıp kurulabilen ürünlerdir. İki ayrıştırma oyunu ayrıca 6 ve 3 hedef sunar.
- Market yalnız ilgili alternatifleri gösterir. Ürünler raf yüzeyine oturur; etiket dokunma/hover ile açılır.
- Satın alma → otomatik odaya dönüş → tek tık kurulum → kapanmayan ANLADIM kartı korunur.
- Atık ve çamaşır ayırma: nesne seç, hedefe dokun. İlk seçim puana sayılır; hatalar düzeltilebilir.
- Makine doluluğu: erken veya uygun tam yük seçilebilir; ardından BU YÜKLE ÇALIŞTIR. Sıcaklık senaryosu normal kir ve özel hijyen gereksinimi olmadığını belirtir.
- Banyoya su seviyesi motor efektiyle dolan leğen, sifon/diş fırçalama/hijyen kararları eklendi.
- Yeni oyunda çamaşır zamanlayıcısı, kurutmalık ve asma görevi kaldırıldı. Sulama zamanlayıcısı puansız yardımcı ekipman.
- Puan para bakiyesinden ayrıdır; en çok 1.800. Eşit iyi seçenekler eşit puan alır. Rastgele puan yoktur.
- Eski oyunlar eski kurallarla devam eder. Eski sonuçlar yönetim/yedekte korunur; farklı puan sürümleri yeni liderlik tablosunda karıştırılmaz.
- Ekran yeniden boyutlandırma ve statik dosya önbelleğindeki Origin varyasyonu hataları düzeltildi.

## Ana dosyalar

- `src/decisions/opportunities.json`: odalar, senaryolar, seçenekler ve mini oyun hedefleri.
- `src/decisions/economy.json`: fiyatlar ve örnek fatura etkileri.
- `src/decisions/scores.json`: karar puanları ve her puanın gerekçesi.
- `src/decisions/copy.json`: oyuncu metinleri.
- `src/decisions/assets.json`, `placements.json`: görsel eşlemesi ve ürün yerleşimleri.
- `src/decisions/sourceNotes.json`: kaynaklar, açık senaryo varsayımları.
- `src/decisions/index.ts`: veri bileşimi, deterministik karar/ayırma durumu ve doğrulama.
- `src/model.ts`, `navigation.ts`, `main.ts`: kayıt, akış, skor ve UI entegrasyonu.
- `src/scene.ts`, `physical.ts`, `placements.ts`, `style.css`: fiziksel kurulum, raflar, leğen suyu ve arayüz.
- `scripts/offline.mjs`: yerel uygulama önbelleği.

## Görseller

19 orijinal kaynak dosya `public/assets/source/` altında değişmeden saklandı.
44 oyun sprite'ı ve 3 yalnız duş başlığı kurulum kırpımı üretildi; toplam 47 yerel WebP.
`public/assets/sprites/manifest.json` kaynak SHA256, kesim ve türetilen dosya bilgisini taşır.
Tekrarlanabilir kesim: `scripts/build_revision_sprites.py` (Python + Pillow).
Dosya adı/içeriği uyuşmayan iki sheet görsele göre eşlendi: IRRIGATION_METHODS_FINAL musluk üçlüsü,
IRRIGATION_TIMER_INSTALLED hortum/fıskiye/damla üçlüsüdür. Yeni AI görseli üretilmedi.

## Fırsat matrisi

'''+ '\n'.join(lines)+'''

## Doğrulama ve sınırlar

- Dört dönem ve 21 fırsat üretim derlemesinde baştan sona oynandı. Bir atık hatası içeren koşu 1.783 / 1.800 puanla bitti.
- 1366×768, 1536×864, 1920×1080: marketler, odalar, karar ve öğrenme ekranları kaydedildi.
- 844×390 ve 390×844: dokunmatik nesne/hedef akışı, yatay taşma kontrolü.
- İnternet kapalı yeniden açılış, 47 sprite, resmî sonuç, iki isim, CSV ve JSON silme/geri yükleme geçti.
- Ayrıştırma ekranında axe WCAG A/AA taraması: 0 ihlal. Bu tüm uygulama için kapsamlı erişilebilirlik sertifikası değildir.
- Öğrenme kartı 4,2 saniye sonra ve Escape tuşunda açık kaldı; yalnız ANLADIM ile kapandı.

Tüm fiyatlar geçici oyun değeridir; piyasa araştırması yapılmadı. Fatura etkileri simülasyondur.
Duş seçenekleri örnek model profilleridir; küçük başlık her zaman verimlidir genellemesi yapılmaz.
Ambalaj puanları açık iade/tekrar kullanım/elden teslim senaryosuna bağlıdır; malzemeler için evrensel üstünlük iddiası yoktur.
Yerel atık toplama uygulamaları değişebilir. Kaynak açıklamaları veri dosyasında bulunur.
Kayıtlar bu tarayıcıdadır; çok cihazlı sunucu sıralaması bu revizyonun kapsamında değildir.
'''
(project/'REVIZYON-RAPORU.md').write_text(report,encoding='utf-8')
print(len(ops),'opportunities;',len(manifest),'sprites')

