from pathlib import Path
import re
root=Path.cwd()
(root/'src/economy.ts').write_text('''/** Example simulation amounts, not market prices. */
export const MONEY_SCALE = 10;
export const INITIAL_BILL = 10_000;
export const INITIAL_BUDGET = 2_500;
export const ROUND_REWARD_RATE = 0.5;
export const ROUND_REWARD_CAP = 500;
export const LARGE_PURCHASE_SHARE = 0.3;
const money = new Intl.NumberFormat("tr-TR", { maximumFractionDigits: 0 });
export const fmtMoney = (value: number) => `${value < 0 ? "-" : ""}₺${money.format(Math.abs(value))}`;
export const signedMoney = (value: number) => `${value > 0 ? "+" : ""}${fmtMoney(value)}`;
export const SIMULATION_NOTE = "Oyundaki tutarlar bütçe karşılaştırması için hazırlanmış örnek simülasyon değerleridir.";
''',encoding='utf-8')
p=root/'src/data.ts';s=p.read_text(encoding='utf-8-sig')
s=s.replace('  requires?: string;','  requires?: string;\n  exclusiveGroup?: string;')
s=re.sub(r'\b(price|impact|bonus): (-?\d+)',lambda m:f'{m[1]}: {int(m[2])*10}',s)
copy={
 'tap-a':('Musluk Ucu','Küçük metal aparat.','Musluğun ucuna takılır.'),
 'repair':('Musluk Bakım Seti','Conta ve küçük bağlantı parçaları.','Musluk bağlantılarında kullanılır.'),
 'shower-a':('Kompakt Duş Başlığı','Dengeli ve kompakt başlık.','Mevcut duş başlığının yerine takılır.'),
 'shower-b':('Geniş Duş Başlığı','Geniş başlıklı metal tasarım.','Daha dolgun bir duş akışı sunar.'),
 'led':('Mat Gövdeli Ampul','Mat gövdeli ampul.','Günlük aydınlatma için kullanılır.'),
 'bulb':('Klasik Cam Ampul','Şeffaf cam gövdeli ampul.','Sıcak ışık verir.'),
 'curtain':('Kalın Perde','Kalın dokulu kumaş.','Pencerenin önüne asılır.'),
 'seal':('Pencere Şeridi','Esnek yapışkan şerit.','Pencere kenarına uygulanır.'),
 'containers':('Saklama Kapları','Kapaklı ve yıkanabilir kaplar.','Hazırlanan yiyecekleri saklamak için kullanılır.'),
 'wrap':('Tek Kullanımlık Örtü','Kesilerek kullanılan ince rulo.','Yiyeceklerin üzerini kapatır.'),
 'strip':('Anahtarlı Çoklu Priz','Anahtarlı çoklu priz.','Birden fazla cihazı aynı noktada toplar.'),
 'basic-strip':('Standart Çoklu Priz','Standart çoklu priz.','Ek bağlantı noktaları sağlar.'),
 'meter':('Tüketim Göstergesi','Küçük ekranlı priz cihazı.','Elektrik kullanımını görmeyi sağlar.'),
 'smart-plug':('Zaman Ayarlı Priz','Zaman ayarlı priz.','Çalışma saatleri ayarlanabilir.'),
 'rack':('Katlanır Kurutmalık','Katlanır ahşap kurutmalık.','Kullanılmadığında kapatılabilir.'),
 'rope':('İp ve Mandallar','İp ve mandal seti.','Uygun bir alana kurulabilir.'),
 'drip':('Kök Sulama Seti','Hortum ve bağlantı seti.','Ekim sıralarına yerleştirilir.'),
 'watering':('Sulama Kabı','Elle kullanılan sulama kabı.','Küçük alanlarda kullanılabilir.'),
 'mulch':('Toprak Örtüsü','Toprak üzerine serilen örtü.','Bitki çevresine uygulanır.'),
 'rain':('Yağmur Biriktirme Seti','Oluk bağlantılı toplama seti.','Yağmur suyunu bir kapta biriktirir.'),
 'tank':('Su Deposu','Geniş su saklama kabı.','Toplanan suyu depolamak için kullanılır.'),
 'bags':('Bez Çantalar','Yıkanabilir kumaş çantalar.','Alışverişte ve ürün taşımada kullanılır.'),
 'jars':('Cam Kavanozlar','Kapaklı cam kaplar.','Kuru ürünleri paketlemek için kullanılır.'),
 'crate':('Ahşap Kasa','Üst üste konabilen ahşap kasa.','Ürünleri taşımak için kullanılır.'),
 'sort':('Ayırma Kutuları','Birden fazla ayrı bölme.','Farklı atıkları ayrı toplar.'),
 'bin':('Büyük Atık Kutusu','Geniş tek atık kutusu.','Tüm atıkları aynı yerde toplar.'),
 'compost':('Kompost Kutusu','Kapaklı ahşap bahçe kutusu.','Uygun organik artıklar için kullanılır.'),
 'solar':('Çatı Güneş Seti','Çatıya sabitlenen panel seti.','Güneş alan çatı için tasarlanmıştır.'),
 'portable-solar':('Taşınabilir Güneş Seti','Taşınabilir küçük panel.','Ayaklı şekilde kurulabilir.'),
 'solar-lamp':('Güneşli Bahçe Lambası','Güneşle şarj olan bahçe lambası.','Akşamları ortam ışığı sağlar.')}
groups={**dict.fromkeys(['shower-a','shower-b'],'bathroom-shower-head'),**dict.fromkeys(['led','bulb'],'home-light-bulb'),**dict.fromkeys(['strip','basic-strip'],'workshop-power-strip'),**dict.fromkeys(['sort','bin'],'waste-collection-choice'),**dict.fromkeys(['solar','portable-solar','solar-lamp'],'roof-energy-choice')}
for id,(name,feature,desc) in copy.items():
 start=s.index(f'    id: "{id}",',s.index('export const products'))
 end=s.index('\n  },',start)
 block=s[start:end]
 for key,val in [('name',name),('feature',feature),('description',desc)]: block=re.sub(rf'{key}: "[^"]*"',f'{key}: "{val}"',block)
 if id in groups: block+=f'\n    exclusiveGroup: "{groups[id]}",'
 s=s[:start]+block+s[end:]
# One fixed shelf order for every player; no outcome-based sorting.
order=['repair','shower-b','tap-a','shower-a','tank','rain','bulb','meter','strip','led','basic-strip','smart-plug','solar-lamp','solar','portable-solar','rope','curtain','rack','seal','watering','compost','drip','mulch','wrap','containers','jars','bin','bags','sort','crate']
s=s.replace('export const categories:', 'const marketOrder = '+str(order).replace("'",'"')+';\nproducts.sort((a,b)=>marketOrder.indexOf(a.id)-marketOrder.indexOf(b.id));\nexport const categories:')
p.write_text(s,encoding='utf-8')
p=root/'src/model.ts';s=p.read_text(encoding='utf-8-sig')
s='import { INITIAL_BILL, INITIAL_BUDGET, MONEY_SCALE, ROUND_REWARD_RATE, ROUND_REWARD_CAP } from "./economy";\n'+s
s=s.replace('  version: 1;','  version: 1 | 2;').replace('  version: 1,','  version: 2,')
s=s.replace('export interface Move {','export interface Move {\n  replacedBy?: string;\n  reversalImpact?: number;')
s=s.replace('  installed: string[];','  installed: string[]; // All purchases ever installed; never refunded.\n  activeInstallations: string[];\n  replacedInstallations: string[];\n  legacyAdjustment?: number;\n  budgetMoments?: number[];')
s=s.replace('(1000 - s.bill) * 20','((INITIAL_BILL - s.bill) / MONEY_SCALE) * 20').replace('s.budget * 2','(s.budget / MONEY_SCALE) * 2')
s=s.replace('Math.round(((1000 - s.bill) / 10) * 10) / 10','Math.round(((INITIAL_BILL - s.bill) / INITIAL_BILL) * 1000) / 10')
s=s.replace('if (!clean.first || !clean.second)','if (!clean.organization || !clean.first || !clean.second)').replace('İki katılımcının adını da yazın.','Kooperatifi ve iki katılımcının adını da yazın.')
s=s.replace('  if (!clean.organization) throw Error("Kurum adını yazın.");\n','')
s=s.replace('bill: 1000,','bill: INITIAL_BILL,').replace('budget: 250,','budget: INITIAL_BUDGET,').replace('    installed: [],','    installed: [],\n    activeInstallations: [],\n    replacedInstallations: [],\n    budgetMoments: [],')
s=s.replace('c.products.every((id) => s.installed.includes(id))','c.products.every((id) => s.activeInstallations.includes(id))')
a=s.index('  const impact = p.requires',s.index('export function install('));b=s.index('\n}\nexport function freeMove',a)
s=s[:a]+'''  const previous = p.exclusiveGroup ? s.activeInstallations.find(id => productById(id).exclusiveGroup === p.exclusiveGroup) : undefined;
  const oldImpact = previous ? s.moves.find(m => m.id === previous)!.impact : 0;
  const requested = p.requires && !s.activeInstallations.includes(p.requires) ? 0 : p.impact;
  const withoutOld = Math.max(0, s.bill - oldImpact);
  const bill = Math.max(0, withoutOld + requested);
  const impact = bill - withoutOld;
  return applyCombos({
    ...s, bill,
    inventory: s.inventory.filter(x=>x!==id),
    installed: [...s.installed,id],
    activeInstallations: [...s.activeInstallations.filter(x=>x!==previous),id],
    replacedInstallations: previous ? [...s.replacedInstallations,previous] : s.replacedInstallations,
    moves: [...s.moves.map(m=>m.id===previous ? {...m,replacedBy:id} : m),
      {id,name:p.name,impact,cost:p.price,room,round:s.round,...(previous?{reversalImpact:withoutOld-s.bill}:{})}],
  });''' +s[b:]
s=s.replace('Dört ücretsiz hamle hakkını kullandınız.','Dört parasız fikri uyguladınız.')
s=s.replace('s.history.at(-1)?.after ?? 1000','s.history.at(-1)?.after ?? INITIAL_BILL').replace('Math.min(Math.floor(saving / 2), 50)','Math.min(Math.floor(saving * ROUND_REWARD_RATE), ROUND_REWARD_CAP)')
s=s.replace('m.room === room &&\n        m.impact < 0','m.room === room &&\n        !m.replacedBy &&\n        s.activeInstallations.includes(m.id) &&\n        m.impact < 0')
s=s.replace('p.requires && !s.installed.includes(p.requires)','p.requires && !s.activeInstallations.includes(p.requires)')
s=s.replace('d.version !== 1 ||','![1,2].includes(d.version) ||').replace('s.version === 1 &&','s.version === d.version &&')
s=s.replace('  return s.phase !== "finished" || s.round === 4;','''  if (s.version === 2) {
    const active=s.activeInstallations, retired=s.replacedInstallations;
    if (![active,retired].every(a=>Array.isArray(a)&&new Set(a).size===a.length&&a.every(id=>s.installed.includes(id)))) return false;
    if (active.some(id=>retired.includes(id)) || active.length+retired.length!==s.installed.length) return false;
    const groups=active.map(id=>productById(id).exclusiveGroup).filter(Boolean);
    if (new Set(groups).size!==groups.length) return false;
    if (s.installed.some(id=>s.moves.filter(m=>m.id===id).length!==1)) return false;
    if (s.moves.some(m => (m.reversalImpact!==undefined&&!Number.isFinite(m.reversalImpact)) ||
      (m.replacedBy!==undefined&&(!retired.includes(m.id)||!s.installed.includes(m.replacedBy)||productById(m.id)?.exclusiveGroup!==productById(m.replacedBy)?.exclusiveGroup)))) return false;
    if (s.legacyAdjustment!==undefined&&!Number.isFinite(s.legacyAdjustment)) return false;
    if (s.budgetMoments!==undefined&&(!Array.isArray(s.budgetMoments)||new Set(s.budgetMoments).size!==s.budgetMoments.length||s.budgetMoments.some(n=>!Number.isInteger(n)||n<1||n>s.round))) return false;
  }
  return s.phase !== "finished" || s.round === 4;''')
s=s.replace('"Fatura",','"Aylık gider (TL)",').replace('"Kalan kredi",','"Yeşil Kasa (TL)",')
a=s.index('  if (!s) return db;',s.index('export function migrateDatabase'))
s=s[:a]+'''  if (db.version===1) {
    for(const result of db.results){result.bill*=MONEY_SCALE;result.budget*=MONEY_SCALE;}
    if(s){
      s.bill*=MONEY_SCALE;s.budget*=MONEY_SCALE;
      s.moves=s.moves.map(m=>({...m,cost:m.cost*MONEY_SCALE,impact:m.impact*MONEY_SCALE}));
      s.history=s.history.map(h=>({...h,before:h.before*MONEY_SCALE,after:h.after*MONEY_SCALE,saving:Math.max(0,h.before-h.after)*MONEY_SCALE,reward:h.reward*MONEY_SCALE}));
      s.lessons=s.lessons?.map(l=>({...l,billImpact:l.billImpact*MONEY_SCALE,comboImpact:l.comboImpact*MONEY_SCALE,spent:l.spent*MONEY_SCALE}));
      s.activeInstallations=[];s.replacedInstallations=[];
      for(const id of s.installed){
        const group=productById(id).exclusiveGroup;
        const previous=group?s.activeInstallations.find(x=>productById(x).exclusiveGroup===group):undefined;
        if(previous){s.activeInstallations=s.activeInstallations.filter(x=>x!==previous);s.replacedInstallations.push(previous);s.moves=s.moves.map(m=>m.id===previous?{...m,replacedBy:id}:m);}
        s.activeInstallations.push(id);
      }
      // Preserve historical net amounts; do not re-score old games on migration.
      s.legacyAdjustment=s.moves.filter(m=>s.replacedInstallations.includes(m.id)).reduce((n,m)=>n+m.impact,0);
      s.version=2;
    }
    db.version=2;
  }
  if (!s) return db;
  s.budgetMoments ??= [];
''' +s[a+len('  if (!s) return db;'):]
p.write_text(s,encoding='utf-8')
p=root/'src/physical.ts';s=p.read_text(encoding='utf-8-sig').replace('const current = s.installed.filter','const current = s.activeInstallations.filter');p.write_text(s,encoding='utf-8')
p=root/'src/scene.ts';s=p.read_text(encoding='utf-8-sig').replace('state?.installed.join', 'state?.activeInstallations.join');p.write_text(s,encoding='utf-8')
