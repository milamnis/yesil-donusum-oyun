from pathlib import Path
import json,re
r=Path('outputs/yesil-donusum')
prices=json.loads((r/'src/data/legacy-paid-prices.json').read_text(encoding='utf-8'))
def read(f):return (r/f).read_text(encoding='utf-8-sig')
def write(f,s):(r/f).write_text(s,encoding='utf-8')
s=read('src/data.ts');s=s.replace('import { marketPrice } from "./data/market-prices";\n','').replace('price: number | null;','price: number;').replace('for (const p of products) p.price = marketPrice(p.id).priceTL;\n','')
s=re.sub(r'(id: "([^"]+)",[\s\S]*?price: )null,',lambda m:m[1]+str(prices[m[2]])+',' if m[2] in prices else m[0],s)
# Match each product block locally, because rooms also have id fields.
for id,price in prices.items():
 s=re.sub(r'(id: "'+re.escape(id)+r'",\s*name: "[^"]+",\s*price: )null,',lambda m:m[1]+str(price)+',',s)
write('src/data.ts',s)
s=read('src/decisions/index.ts').replace('import { marketPrice, isExistingFixture } from "../data/market-prices";\n','')
s=re.sub(r'export const economy:[\s\S]*?(?=export const points:)', 'export const economy: Record<string, { priceTL: number; billImpact: number }> = economyData;\n',s)
s=s.replace('spent: economy[id].priceTL ?? 0,','spent: economy[id].priceTL,')
s=re.sub(r'  if \(\n    o.kind === "product" &&[\s\S]*?throw Error\("Önce ürünü satın alıp yerleştir\."\);\n','',s)
s=re.sub(r'    lessons: \[\n      \.\.\.\(s.lessons \|\| \[\]\),\n      \{\n        \.\.\.decisionLesson\(id\),\n        spent: s.moves.find\(\(m\) => m.id === id\)\?\.cost \?\? 0,\n      \},\n    \],','    lessons: [...(s.lessons || []), decisionLesson(id)],',s)
s=s.replace('            isExistingFixture(d.choiceId) ||\n','');write('src/decisions/index.ts',s)
e=json.loads(read('src/decisions/economy.json'))
for id,v in e.items():
 if id in prices:e[id]={'priceTL':prices[id],'billImpact':v['billImpact'],'priceStatus':'provisional','impactStatus':'simulation'}
write('src/decisions/economy.json',json.dumps(e,ensure_ascii=False,indent=2)+'\n')
s=read('src/model.ts');s=s.replace('import { purchasePrice } from "./data/market-prices";\n','').replace('import legacyPaidPrices from "./data/legacy-paid-prices.json";\n','').replace('  purchaseCosts?: Record<string, number>;\n','');s=s.replace('  const price = purchasePrice(id);\n','').replace('if (s.budget < price)','if (s.budget < p.price)').replace('const budget = s.budget - price;','const budget = s.budget - p.price;').replace('    purchaseCosts: { ...s.purchaseCosts, [id]: price },\n','');s=re.sub(r'cost:\s*s.purchaseCosts\?\.\[id\] \?\?\s*\(legacyPaidPrices as Record<string, number>\)\[id\],','cost: p.price,',s);s=re.sub(r'  if \(\n    s.purchaseCosts !== undefined[\s\S]*?    return false;\n','',s);s=s.replace('s.lessons.push({ ...lesson, spent: m.cost, acknowledged: true });','s.lessons.push({ ...lesson, acknowledged: true });');write('src/model.ts',s)
s=read('src/learning.ts').replace('import legacyPaidPrices from "./data/legacy-paid-prices.json";\n','').replace('spent: p.price ?? (legacyPaidPrices as Record<string, number>)[p.id] ?? 0,','spent: p.price,');write('src/learning.ts',s)
s=read('src/navigation.ts').replace('import { isExistingFixture } from "./data/market-prices";\n','').replace(' && !isExistingFixture(p.id)','');write('src/navigation.ts',s)
s=read('src/main.ts').replace('import { isExistingFixture, priceLabel } from "./data/market-prices";\n','').replace('priceLabel(p.id)','fmtMoney(p.price)')
start=s.index('${\n    contextIds()');end=s.index('${!ps.length',start);s=s[:start]+s[end:]
start=s.index('  if (isExistingFixture(id) || p.price === null) {');end=s.index('  const owned =',start);s=s[:start]+s[end:]
start=s.index('    case "keep-existing": {');end=s.index('    case "choose": {',start);s=s[:start]+s[end:]
s=s.replace('<p class="subtle">Bugünkü harcama: ${fmtMoney(l.spent)} · Dönemlik gider etkisi: ${signedMoney(l.billImpact)}<br/>Gider etkisi oyun simülasyonudur.</p>','');write('src/main.ts',s)
s=read('src/style.css');s=s.split('/* Financial context must remain readable on the cream learning card. */')[0].rstrip()+'\n';write('src/style.css',s)
s=read('src/economy.ts').replace('Ürün fiyatları sağlanan piyasa referanslarına dayanır. Fatura etkileri örnek simülasyondur; gerçek tasarruf garantisi değildir.','Oyundaki tutarlar bütçe karşılaştırması için hazırlanmış örnek simülasyon değerleridir.');write('src/economy.ts',s)
c=json.loads(read('src/decisions/copy.json'))
for room in ['home','workshop']:
 for key in ['incandescent','halogen','led']:c[f'rev-light-{room}-{key}']['shortDescription']='Aynı duy ve parlaklık için bir seçenek.'
 c[f'rev-light-{room}-incandescent'].update(title='Klasik Ampul',resultTitle='Oda aydınlandı.',resultText='Akkor ampul, aynı ışığı üretirken enerjinin daha büyük bölümünü ısıya çevirir.',whyText='')
c['rev-shower-classic'].update(title='Klasik Ayarlı Başlık',shortDescription='Püskürtme biçimi elle ayarlanır.',resultTitle='Püskürtme biçimini değiştirdin.',resultText='Bu modelin ayarı suyu dağıtır; akışı kompakt model kadar sınırlamaz.')
write('src/decisions/copy.json',json.dumps(c,ensure_ascii=False,indent=2)+'\n')
s=read('src/decisions/sourceNotes.json').replace('Fiyat kaynağı src/data/market-prices.json dosyasıdır; eksik referanslar needs_review durumundadır;','Fiyatlar geçici örneklerdir;');write('src/decisions/sourceNotes.json',s)
for f in ['DESIGN.md','UX-CONTRACT.md','REVIZYON-RAPORU.md']:
 s=read(f).split('\n\n## Güncel piyasa fiyatı revizyonu')[0].rstrip()+'\n';write(f,s)
for p in (r/'tests').glob('*.test.ts'):
 if p.name=='market-prices.test.ts':continue
 s=p.read_text(encoding='utf-8');s=s.replace('import { purchase, legacyPrice } from "./legacy-price-fixture";\n','');s=s.replace('  start,','  start,\n  purchase,',1);s=s.replace('legacyPrice(old.id) - legacyPrice(p.id)','old.price - p.price').replace('9999 - legacyPrice(p.id)','9999 - p.price').replace('legacyPrice("curtain")','productById("curtain").price');s=s.replace('economy[id].priceTL === null || Number.isFinite(economy[id].priceTL)','Number.isFinite(economy[id].priceTL)');p.write_text(s,encoding='utf-8')
# Only files introduced by the reverted revision; no recursive deletion.
for f in ['src/data/market-prices.json','src/data/market-prices.ts','src/data/legacy-paid-prices.json','tests/legacy-price-fixture.ts','tests/market-prices.test.ts','scripts/market-prices-qa.cjs','scripts/price-report.py','PRICE-REVIEW.md']:
 (r/f).unlink(missing_ok=True)
for p in (r/'qa/main-revision').glob('prices-*.png'):p.unlink()
