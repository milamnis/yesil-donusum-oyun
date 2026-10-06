from pathlib import Path
import json
p=Path('outputs/yesil-donusum')
def read(f): return (p/f).read_text(encoding='utf-8-sig')
def write(f,s): (p/f).write_text(s,encoding='utf-8')
def data(f): return json.loads(read(f))
def dump(f,d): write(f,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
ops=data('src/decisions/opportunities.json'); cp=data('src/decisions/copy.json'); eco=data('src/decisions/economy.json')
catalog={}; aliases={}
for o in ops:
 if o['kind']!='product': continue
 for id in o['choices']:
  catalog[id]=dict(id=id,displayName=cp[id]['title'],priceTL=None,referencePriceTL=None,referenceDate='2026-10-06',referenceProduct='',referenceSpecification=cp[id]['shortDescription'],referenceSource='',priceStatus='needs_review',note='PRICE REVIEW REQUIRED: ürün sınıfı ve güncel satış tutarı birlikte doğrulanmalı.',previousPriceTL=eco[id]['priceTL'])
def price(ids,key,amount,ref,spec,url,origin='web',note=''):
 for id in ids:
  old=catalog.pop(id)
  aliases[id]=key
  if key not in catalog: catalog[key]={**old,'id':key,'priceTL':amount,'referencePriceTL':ref,'referenceProduct':spec,'referenceSpecification':spec,'referenceSource':url,'priceStatus':'verified','provenance':origin,'note':note}
price(['rev-light-home-led','rev-light-workshop-led'],'led_bulb_e27_9w',50,50,'Normal 9 W E27 LED ampul','', 'user_brief','Kullanıcının Ekim 2026 referansı; bağımsız fiyat teyidi olarak sunulmaz.')
price(['rev-light-home-halogen','rev-light-workshop-halogen'],'halogen_e27_42w',175,175,'42 W E27 halojen ampul','','user_brief')
price(['rev-light-home-incandescent','rev-light-workshop-incandescent'],'existing_incandescent',0,0,'Odadaki mevcut akkor ampul','','existing_fixture','Yeni satın alınabilir ürün değildir.')
price(['rev-roof-bonus-solar'],'solar_panel_550w',8475,8475,'550 W panel modülü','','user_brief','Yalnız panel; inverter, konstrüksiyon, kablolama, proje, montaj ve işçilik hariç.')
price(['rev-office-power-meter'],'plug_wattmeter_16a',778,778.48,'GESİ PM-1453 priz tipi 16 A / 3680 W wattmetre','https://www.hatfon.com/urun/gesi-pm-1453-dijital-enerji-tuketim-olcer-wattmetre-16a-104027',note='KDV dahil sayfa fiyatı; arama özeti farklı tutar gösterdi, açılan sayfa esas alındı. Tam TL yuvarlama.')
price(['rev-tap-filter'],'faucet_filter',399,399,'NOY musluk ucu filtre gövdesi, 5 filtre elemanı ve adaptör/conta','https://noyplus.com/urun/musluk-ucu-filtresi')
price(['rev-basin-place'],'plastic_basin_no3',76,75.50,'Hürsan 3 no derin plastik leğen','https://www.konerkayplastik.com.tr/mutfak-legen',note='Tam TL yuvarlama; görsel temsili, kapasite ilan edilmiyor.')
price(['rev-office-power-smart'],'wifi_smart_plug',499,499,'Şımart tekli Wi-Fi akıllı priz','https://www.koctas.com.tr/akilli-ev-sistemleri/akilli-priz/c/120001044',note='Kategori ilan fiyatı; kupon/sepette indirimi kullanılmadı.')
price(['rev-pack-apple-mesh'],'produce_mesh',100,99.75,'Tchibo 4 meyve/sebze filesi, paket 399 TL','https://www.tchibo.com.tr/products/120523574037/meyve-ve-sebze-filesi',note='Paket fiyatından bir file payı: 399 / 4. Oyunda 1 adet ambalaj maliyeti; tekli perakende satış iddiası değildir.')
price(['rev-pack-lentil-return'],'jar_1l',90,89.90,'Joy Kitchen metal kilitli ahşap kapaklı cam kavanoz 1 L','https://www.lcw.com/metal-kilitli-ahsap-kapakli-cam-kavanoz-1-lt-karisik-o-2966626',note='Yalnız boş kavanoz; gıda bedeli hariç.')
price(['rev-pack-towel-plastic','rev-pack-scarf-plastic'],'textile_opp_bag',2,1.9399,'25x30+5 cm 100 adet şeffaf bantlı OPP, paket 193,99 TL','https://www.posetambalaj.net/',note='193,99 / 100 adet payı; tekstil ürününün bedeli hariç.')
# Missing references remain explicitly unpriced, never replaced by the old game prices.
catalog['led_strip_3m_ready']=dict(id='led_strip_3m_ready',displayName='LED Şerit · 3 m',priceTL=None,referencePriceTL=None,referenceDate='2026-10-06',referenceProduct='',referenceSpecification='Görselde fiş ve anahtar görünmüyor; hazır set kapsamı teyit bekliyor.',referenceSource='',priceStatus='needs_review',note='PRICE REVIEW REQUIRED: çıplak şeride hazır set bedeli uygulanmaz.')
aliases['rev-led-strip']= 'led_strip_3m_ready'
(p/'src/data').mkdir(exist_ok=True)
dump('src/data/market-prices.json',{'catalog':catalog,'aliases':aliases})
write('src/data/market-prices.ts','''import data from "./market-prices.json";
import { fmtMoney } from "../economy";
export interface MarketPrice {
 id: string; displayName: string; priceTL: number | null; referencePriceTL: number | null;
 referenceDate: string; referenceProduct: string; referenceSpecification: string;
 referenceSource: string; priceStatus: string; note: string; provenance?: string; previousPriceTL?: number;
}
export const marketPrices = data.catalog as Record<string, MarketPrice>;
export const priceAliases = data.aliases as Record<string, string>;
export const marketPrice = (id: string) => marketPrices[priceAliases[id] ?? id];
export const existingFixture = (id: string) => priceAliases[id] === "existing_incandescent";
export const priceAvailable = (id: string) => marketPrice(id)?.priceTL != null;
export const priceLabel = (id: string, historicalPrice: number) => {
 const p = marketPrice(id);
 return p ? p.priceTL === null ? "Fiyat inceleniyor" : fmtMoney(p.priceTL) : fmtMoney(historicalPrice);
};
''')
for room in ['home','workshop']:
 for typ,title,desc in [('incandescent','Eski ampulle devam et','Yeni ürün almadan mevcut ampulü kullanmaya devam edersin.'),('halogen','Halojen Ampul','Standart E27 duyda kullanılan halojen ampul.'),('led','LED Ampul','Standart E27 duyda kullanılan 9 W LED ampul.')]:
  c=cp[f'rev-light-{room}-{typ}'];c['title']=title;c['shortDescription']=desc
  if typ=='incandescent':c.update(resultTitle='Mevcut ampulle devam ettin.',resultText='Yeni harcama yapmadın. Eski ampul aynı elektrik tüketimiyle çalışmaya devam ediyor.')
  if typ=='led':c.update(resultTitle='LED ampul takıldı.',resultText='Aynı aydınlatma ihtiyacını eski tip ampullere göre daha düşük elektrik tüketimiyle karşılar.',whyText='')
 for o in ops:
  if o['id']==f'light-{room}': o['scenario']='Odadaki eski ampul hâlâ çalışıyor. Ne yapacaksın?'
cp['rev-roof-bonus-solar'].update(title='550 W Güneş Paneli',shortDescription='Güneşten elektrik üretmek için kullanılan panel modülü.',resultTitle='Panel yerleştirildi.',resultText='Bu fiyat yalnız panel içindir. Tam kurulum için ek ekipman ve işçilik gerekir.',whyText='')
ops.append(dict(id='led-strip',roomId='home',title='Raf aydınlatması',scenario='Dinlenme köşesine yardımcı ışık eklemek ister misin?',x=74,y=39,kind='product',core=False,round=2,choices=['rev-led-strip']))
cp['rev-led-strip']=dict(title='LED Şerit · 3 m',shortDescription='Raf altında yardımcı veya dekoratif ışık.',resultTitle='Rafına yardımcı ışık ekledin.',resultText='Bu ek aydınlatma, ana ampulün yerine geçmez. İhtiyacın olmadığında kapatabilirsin.',whyText='Ek ışık almak tek başına enerji tasarrufu değildir.')
eco['rev-led-strip']={'billImpact':0,'impactStatus':'not_estimated'}
for id,e in eco.items():
 e.pop('priceTL',None);e.pop('priceStatus',None)
dump('src/decisions/economy.json',eco);dump('src/decisions/copy.json',cp);dump('src/decisions/opportunities.json',ops)
a=data('src/decisions/assets.json');a['rev-led-strip']={'asset':'obj_living_led_strip_3m','installationSlot':'home_shelf_underside'};dump('src/decisions/assets.json',a)
s=data('src/decisions/scores.json');s['rev-led-strip']={'decisionScore':0,'reason':'Opsiyonel yardımcı ışık; güç/kullanım karşılaştırması yok, çevresel puana dahil değil.'};dump('src/decisions/scores.json',s)
s=read('src/decisions/index.ts');s='import { marketPrice, existingFixture } from "../data/market-prices";\n'+s
s=s.replace('  economyData;','  Object.fromEntries(Object.entries(economyData).map(([id, value]) => [id, { ...value, priceTL: marketPrice(id)?.priceTL ?? 0 }]));')
s=s.replace('  const o = assertChoice(s, id);\n  return {','  const o = assertChoice(s, id);\n  if (o.kind === "product" && !existingFixture(id) && !s.installed.includes(id)) throw Error("Önce ürünü yerleştir.");\n  return {',1)
s=s.replace('lessons: [...(s.lessons || []), decisionLesson(id)],','lessons: [...(s.lessons || []), { ...decisionLesson(id), spent: existingFixture(id) ? 0 : s.moves.find(m => m.id === id)?.cost ?? decisionLesson(id).spent }],')
write('src/decisions/index.ts',s)
s=read('src/navigation.ts');s='import { existingFixture } from "./data/market-prices";\n'+s;s=s.replace('p.id !== "curtain" && p.room !== "waste";','p.id !== "curtain" && p.room !== "waste" && !existingFixture(p.id);');write('src/navigation.ts',s)
s=read('src/model.ts');s='import { marketPrice, existingFixture } from "./data/market-prices";\n'+s
s=s.replace('  if (!p) throw Error("Ürün bulunamadı.");','  if (!p) throw Error("Ürün bulunamadı.");\n  if (existingFixture(id)) throw Error("Mevcut ampul satın alınmaz; devam et seçeneğini kullan.");\n  if (marketPrice(id)?.priceTL === null) throw Error("Bu ürünün fiyatı inceleniyor. Şimdilik satın alınamaz.");',1)
s=s.replace('  if (!s) return db;','  if (!s) return db;\n  s.purchaseCosts ??= {};\n  for (const id of s.inventory) s.purchaseCosts[id] ??= marketPrice(id)?.previousPriceTL ?? productById(id).price;')
s=s.replace('  if (!validDecisions(s)) return false;','''  if (!validDecisions(s)) return false;
  if (s.salesIncomeGranted !== undefined && typeof s.salesIncomeGranted !== "boolean") return false;
  if (s.salesIncomeAcknowledged !== undefined && typeof s.salesIncomeAcknowledged !== "boolean") return false;
  if (s.salesIncomeGranted && s.round !== 4) return false;
  if (s.salesIncomeAcknowledged && !s.salesIncomeGranted) return false;
  if (s.purchaseCosts !== undefined && (!s.purchaseCosts || Array.isArray(s.purchaseCosts) || typeof s.purchaseCosts !== "object" || Object.entries(s.purchaseCosts).some(([id, cost]) => !products.some(p => p.id === id) || !Number.isFinite(cost) || cost < 0))) return false;''')
write('src/model.ts',s)
