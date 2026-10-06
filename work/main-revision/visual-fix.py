from pathlib import Path
p=Path('src/placements.ts');s=p.read_text(encoding='utf-8').replace('marketScales[p.id],','marketScales[p.id] ?? 1,');p.write_text(s,encoding='utf-8')
p=Path('src/main.ts');s=p.read_text(encoding='utf-8').replace('window.addEventListener("resize", () => game.scale.refresh());','''new ResizeObserver(() => {
  if(!game.scale.canvas)return;
  game.scale.getParentBounds();
  game.scale.refresh();
}).observe(document.querySelector('#game')!);''');p.write_text(s,encoding='utf-8')
p=Path('src/decisions/index.ts');s=p.read_text(encoding='utf-8');s+='''
export const practicalPledges:Record<string,string>={
 tap:'Evde damlayan muslukları kontrol edeceğiz.', 'waste-sort':'Temiz ambalajları kirli peçetelerden ayıracağız.',shower:'Duş başlığının akış özelliğini kontrol edeceğiz.',basin:'Duş ısınırken akan temiz suyu uygun bir işte kullanacağız.',flush:'Yeterli olduğunda yarım sifonu kullanacağız.',toothbrush:'Diş fırçalarken musluğu kapatacağız.',hygiene:'Kirli peçete ve ıslak mendilleri geri dönüşüme karıştırmayacağız.','light-home':'Evde sık kullandığımız lambalar için LED seçeneklerine bakacağız.','light-workshop':'Kooperatifin aydınlatma ihtiyacını gözden geçireceğiz.','office-power':'Mesai sonunda uygun cihazların elektriğini kapatacağız.','laundry-sort':'Çamaşırları renklerine ve bakım etiketlerine göre ayıracağız.','laundry-load':'Makineyi sıkıştırmadan uygun tam yükle çalıştıracağız.','laundry-program':'Günlük çamaşırlarda etikete uygun düşük sıcaklığı değerlendireceğiz.',irrigation:'Sulama suyunu bitkinin köküne yönlendireceğiz.','irrigation-time':'Sıcak günlerde sulamayı serin saatlere bırakacağız.','irrigation-timer':'Sulama ayarını toprağın ihtiyacına göre yapacağız.','pack-lentil':'Uygun gıdalar için iade ve dolum düzenini araştıracağız.','pack-apple':'Alışverişte filemizi tekrar kullanacağız.','pack-towel':'Elden teslimlerde gereksiz ikinci ambalajı azaltacağız.','pack-scarf':'Tekstil tesliminde ürüne yeterli ambalajı seçeceğiz.','roof-bonus':'Güneş yatırımı öncesinde çatı uygunluğunu araştıracağız.'};
export function pledgeFor(id:string){const o=opportunityFor(id)||opportunities.find(o=>`sort-${o.id}`===id);return o?practicalPledges[o.id]:undefined;}
''';p.write_text(s,encoding='utf-8')
p=Path('src/journey.ts');s=p.read_text(encoding='utf-8');s='import { pledgeFor } from "./decisions";\n'+s;s=s.replace('text: l.takeaway,','text: l.takeaway || l.result,').replace('pledges[l.id] ||','pledgeFor(l.id) || pledges[l.id] ||');p.write_text(s,encoding='utf-8')
