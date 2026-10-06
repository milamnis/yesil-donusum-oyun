from pathlib import Path
import json,re
p=Path('src/data/market-prices.json');d=json.loads(p.read_text(encoding='utf-8'))
# A single inner OPP bag does not substantiate a two-bag product price.
r=d['catalog']['textile_opp_bag'];r['priceTL']=None;r['priceStatus']='needs_review';r['note']='PRICE REVIEW REQUIRED: kaynak yalnız iç OPP paketi fiyatlandırıyor; taşıma poşeti dahil değil.'
s=Path('src/data.ts').read_text(encoding='utf-8');legacy={}
for m in re.finditer(r'id: "([^"]+)"[\s\S]*?price: (\d+),',s):
 legacy[m[1]]=int(m[2])
# Historical prices are preserved separately and never presented as researched current prices.
d['historicalLegacyPrices']=legacy
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for k,v in legacy.items():
 s=re.sub(r'(id: "'+re.escape(k)+r'"[\s\S]*?price: )'+str(v)+',',lambda m:m[1]+'historicalLegacyPrices["'+k+'"],',s,count=1)
s='import { historicalLegacyPrices } from "./data/market-prices";\n'+s
Path('src/data.ts').write_text(s,encoding='utf-8')
p=Path('src/data/market-prices.ts');p.write_text(p.read_text(encoding='utf-8')+'\nexport const historicalLegacyPrices: Record<string, number> = data.historicalLegacyPrices;\n',encoding='utf-8')
p=Path('scripts/revision-flow.cjs');s=p.read_text(encoding='utf-8');s=s.replace('const current = (await state()).active;','const current = (await state()).active;')
s=s.replace('if (o.kind === "sorting") {','if (!o.core) {\n        await click(`optional-skip:${o.id}`);\n        console.log("SKIP OPTIONAL", o.id);\n        continue;\n      }\n      if (o.kind === "sorting") {')
s=s.replace('await click("continue");','await click("continue");\n    if (round === 3) { await shot("sales-income"); await click("sales-start"); }')
s=s.replace('final.active.decisions.length, 21','final.active.decisions.filter(d => !d.skipped).length, 18').replace('decisions: 21','decisions: final.active.decisions.length')
p.write_text(s,encoding='utf-8')
