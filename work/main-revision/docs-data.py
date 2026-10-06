from pathlib import Path
import json
p=Path('src/main.ts');s=p.read_text(encoding='utf-8');s=s.replace('summary-screen final-result\"','summary-screen final-result ${s.decisionVersion===1?"decision-final":""}\"');p.write_text(s,encoding='utf-8')
p=Path('src/decisions/sourceNotes.json');ops=json.loads(Path('src/decisions/opportunities.json').read_text(encoding='utf-8-sig'))
notes={o['id']:{'note':'Senaryo ve puanlar eğitim oyunu için belirlenmiştir. Fiyatlar geçici örneklerdir; fatura etkisi gerçek tasarruf vaadi değildir.','sources':[]} for o in ops}
for id in ['waste-sort','hygiene']:notes[id]['sources']=['https://www.epa.gov/recycle/how-do-i-recycle-common-recyclables']
for id in ['laundry-load','laundry-program']:notes[id]['sources']=['https://energysavingtrust.org.uk/how-save-energy-when-using-your-washing-machine/']
for id in ['light-home','light-workshop']:notes[id]['sources']=['https://www.energy.gov/cmei/ssl/led-basics']
for id in ['irrigation','irrigation-time']:notes[id]['sources']=['https://www.epa.gov/watersense/microirrigation']
for id in ['pack-lentil','pack-apple','pack-towel','pack-scarf']:notes[id]['sources']=['https://www.epa.gov/recycle/frequent-questions-recycling'];notes[id]['note']+=' Malzemeler için evrensel üstünlük sırası yoktur; tekrar kullanım/iade ve teslim şartı senaryoda açıkça belirtilir.'
notes['shower']['note']+=' Görsel boyut performans kanıtı değildir. Seçenekler oyuna ait örnek model profilleridir; akış kontrol özelliği seçim öncesinde açıklanır.'
notes['hygiene']['note']+=' Yerel atık toplama kuralları kontrol edilmelidir; bu oyunun organik akışı yalnız gıda/bitki artıkları içindir.'
p.write_text(json.dumps(notes,ensure_ascii=False,indent=2),encoding='utf-8')
p=Path('src/decisions/index.ts');s=p.read_text(encoding='utf-8');s='import sourceNotes from "./sourceNotes.json";\n'+s;s+='''
export const choices=opportunities.flatMap(o=>o.choices.map(id=>({id,opportunityId:o.id,...copy[id],...economy[id],...points[id],...assets[id],sourceNote:sourceNotes[o.id as keyof typeof sourceNotes]})));
''';p.write_text(s,encoding='utf-8')
p=Path('package.json');d=json.loads(p.read_text());d['scripts']['test:e2e']='node scripts/revision-flow.cjs';d['scripts']['test:full']='node scripts/revision-flow.cjs';d['scripts']['test:revision']='node scripts/revision-flow.cjs';p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
p=Path('premium-ui.json');d=json.loads(p.read_text());d['evidence']['crudFullFlow']='scripts/revision-flow.cjs';d['evidence']['failurePaths']='tests/decisions.test.ts';p.write_text(json.dumps(d,indent=2),encoding='utf-8')
for name in ['DESIGN.md','UX-CONTRACT.md']:
 p=Path(name);s=p.read_text(encoding='utf-8');s+='''

## 5 Ekim 2026 — karar odaklı revizyon (önceki sadeleştirme kurallarını günceller)

Görsel dil, arka planlar, kayıt ve dönem sistemi korunur. Yeni oyun decisionVersion=1
ile başlar. Eski oyun ve sonuçlar eski kurallarla okunur; yeni liderlik tablosu yalnız
aynı karar puanı sürümünü karşılaştırır. Eski sonuçlar yönetimde ve CSV/JSON yedekte kalır.
HUD: DÖNEM, KALAN PARA, SKOR. Üç nötr seçenek aynı düğme/raf dilini kullanır.
Ürün: incele → satın al → otomatik odaya dön → yerleştir → kalıcı ANLADIM kartı.
Davranış: aynı ortak dialog içinde üç seçenek. Dolulukta seçim ardından ÇALIŞTIR.
Atık/çamaşır: nesneye dokun → hedefe dokun; klavye ile aynı düğmeler kullanılabilir.
İlk eşleştirme puana sayılır; yanlışlar düzeltilebilir, yeniden puan üretmez.
Temel kararlar 100 üzerinden; iki iyi seçenek eşit puan alabilir. Para puana eklenmez.
Leğen, zamanlayıcı ve çatı isteğe bağlı, puansız ve atlanabilir.
Tek aktif sorun gösterilir; öğrenme kartı onaylanmadan sıradaki soruna geçilmez.
Yeni veri src/decisions altında fırsat/fiyat/puan/metin/asset/kaynak olarak ayrıdır.
Sahne ve HTML boyutu ResizeObserver ile aynı parent ölçüsüne bağlanır.
Yeni sprite raf boyutu slot sınırından hesaplanır; oda kurulumları ayrı metadata taşır.
''';p.write_text(s,encoding='utf-8')
