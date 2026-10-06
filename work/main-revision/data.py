from pathlib import Path
import json
root=Path('outputs/yesil-donusum/src/decisions')
ops=[]; econ={}; scores={}; copy={}; assets={}
def op(id,room,title,scenario,xy,kind='product',core=True,round=1):
 d=dict(id=id,roomId=room,title=title,scenario=scenario,x=xy[0],y=xy[1],kind=kind,core=core,round=round,choices=[]);ops.append(d);return d
def choice(o,key,title,desc,asset,price,points,result,why,impact=0,slot=None):
 id='rev-'+o['id']+'-'+key;o['choices'].append(id)
 econ[id]=dict(priceTL=price,billImpact=impact,priceStatus='provisional',impactStatus='simulation')
 scores[id]=dict(decisionScore=points if o['core'] else 0,reason=why)
 copy[id]=dict(title=title,shortDescription=desc,resultTitle=result,resultText=why,whyText='')
 assets[id]=dict(asset=('sprites/generated/'+asset if asset and not asset.startswith('old:') else asset.removeprefix('old:') if asset else ''),installationSlot=slot or o['id'])
 return id
x=op('tap','kitchen','Damlayan musluk','Musluk kapalıyken damlatıyor. Sorun, içindeki aşınmış conta.',[50,37])
choice(x,'aerator','Musluk Ucu (Perlatör)','Musluğun ucuna takılan bir aparat.','faucet-aerator',150,20,'Damlatma devam ediyor.','Musluk ucu akışı düzenler; aşınmış contayı onarmaz.',0,'faucet_outlet')
choice(x,'repair','Tamir Seti','Conta ve bağlantı parçaları içerir.','faucet-repair',120,100,'Damlatma durdu.','Conta yenilendiği için kaçak kesildi.',-180,'faucet_joint')
choice(x,'filter','Musluk Filtresi','Musluğa takılan filtre kartuşu.','faucet-filter',260,20,'Filtre takıldı; kaçak sürüyor.','Filtre suyu süzer, fakat arızalı contayı onarmaz.',0,'faucet_filter')
x=op('waste-sort','kitchen','Mutfaktaki atıklar','Bu oyunda temiz ambalajlar ayrı, yemek artıkları organik, kirli peçeteler diğer atıkta toplanıyor.',[53,66],'sorting')
x['targets']=[dict(id=k,title=t,asset='sprites/generated/bag-'+k) for k,t in [('paper','Kâğıt / karton'),('plastic','Plastik'),('glass','Cam'),('metal','Metal'),('organic','Organik'),('other','Diğer atık')]]
x['items']=[dict(id=k,title=t,asset='sprites/generated/waste-'+k,target=g) for k,t,g in [('paper','Temiz karton','paper'),('plastic','Boş plastik şişe','plastic'),('glass','Boş cam kavanoz','glass'),('metal','Boş metal konserve','metal'),('organic','Sebze artıkları','organic'),('tissue','Kirli peçete','other')]]
x=op('shower','bathroom','Duş başlığı','Aynı süre duş alınacak. Bu üç modelin akış düzenleri farklı.',[70,43])
for k,t,d,a,pr,sc,re,wh,im in [('compact','Kompakt Başlık','İçinde akış sınırlayıcı parça bulunur.','shower-compact',280,100,'Su akışı sınırlandı.','Bu model, duş sırasında gereksiz akışı azaltan bir iç parçaya sahip.',-260),('classic','Klasik Ayarlı Başlık','Püskürtme biçimi elle ayarlanır.','shower-classic',230,60,'Püskürtme biçimini değiştirdin.','Bu modelin ayarı suyu dağıtır; akışı kompakt model kadar sınırlamaz.',-120),('rain','Geniş Yağmur Başlığı','Geniş yüzeyden su verir.','shower-rain',480,20,'Daha geniş bir akış seçtin.','Bu senaryodaki geniş başlık aynı sürede daha fazla su kullanır.',80)]:choice(x,k,t,d,a,pr,sc,re,wh,im,'shower_arm_tip')
x=op('basin','bathroom','Isınırken akan su','Duş ısınana kadar akan temiz suyu biriktirebilirsin. Bu isteğe bağlı adım puan getirmez.',[64,70],core=False)
choice(x,'place','Leğen','Duş alanına konan su kabı.','basin',80,0,'Su leğende birikti.','Bu suyu temizlikte veya uygun başka bir işte yeniden kullanabilirsin.',0,'basin_floor')
x=op('flush','bathroom','Sifon seçimi','Bu kullanımda yarım sifon yeterli. Düğme bırakılınca akış duruyor.',[40,59],'behavior')
for k,t,sc,re,why in [('half','Yarım sifon',100,'Yeterli suyu kullandın.','Bu kullanımda yarım sifon işi tamamladı.'),('full','Tam sifon',40,'Gerekenden fazla su aktı.','Bu kullanımda tam sifona ihtiyaç yoktu.'),('hold','Düğmeyi basılı tut',20,'Su daha uzun süre aktı.','Düğmeyi basılı tutmak bu kullanım için gerekli değildi.')]:choice(x,k,t,'',None,0,sc,re,why)
x=op('toothbrush','bathroom','Diş fırçalarken su','Dişlerini fırçalarken musluğu nasıl kullanırsın?',[29,42],'behavior')
for k,t,sc,re,why in [('open','Fırçalarken açık bırak',20,'Kullanmadığın sırada su aktı.','Fırçalama boyunca akan suyun çoğu kullanılmadan gidere gitti.'),('closed','Fırçalarken kapat',100,'Kullanmadığın suyu durdurdun.','Musluğu yalnız durularken açmak yeterliydi.'),('brief','Gerektikçe kısa aç',100,'Suyu gerektiği anda kullandın.','Fırçalama aralarında musluğu kapalı tuttun.')]:choice(x,k,t,'',None,0,sc,re,why)
x=op('hygiene','bathroom','Kirli kâğıt','Bu kirli peçete nereye gitmeli? Burada hijyenik atık için ayrı diğer atık kabı var.',[36,68],'behavior')
for k,t,sc,re,why in [('paper','Kâğıt / karton',20,'Kirli peçete kâğıt kutusuna uygun değil.','Kirli hijyenik kâğıdı temiz kâğıt ve kartondan ayrı tut.'),('other','Diğer atık',100,'Kirli peçeteyi ayırdın.','Temiz karton rulo kâğıda; kirli peçete ve ıslak mendil diğer atığa gider.'),('organic','Organik artıklar',20,'Bu toplama sisteminde organik kaba uygun değil.','Bu kap yalnız yemek ve bitki artıkları için ayrıldı.')]:choice(x,k,t,'',None,0,sc,re,why)
for room,xy,rnd in [('home',[79,37],1),('workshop',[60,18],2)]:
 x=op('light-'+room,room,'Aydınlatma','Aynı odayı aynı parlaklıkta aydınlatacak bir ampul seç.',xy,round=rnd)
 for k,t,a,pr,sc,re,why,im in [('incandescent','Klasik Ampul','bulb-incandescent',60,20,'Oda aydınlandı.','Akkor ampul, aynı ışığı üretirken enerjinin daha büyük bölümünü ısıya çevirir.',0),('halogen','Halojen Ampul','bulb-halogen',90,60,'Halojen ampulü taktın.','Aynı aydınlık için klasik ampulden az, LED’den fazla elektrik kullanır.',-80),('led','LED Ampul','bulb-led',140,100,'Aynı alanı daha az elektrikle aydınlattın.','LED, aynı parlaklıktaki akkor ve halojen ampullerden daha az elektrik kullanır.',-200)]:choice(x,k,t,'Aynı duy ve parlaklık için bir seçenek.',a,pr,sc,re,why,im,'light-'+room)
x=op('office-power','workshop','Mesai sonrası cihazlar','Bilgisayar ve yazıcı mesai sonrası beklemede. Otomatik priz mesai bitimine ayarlanacak; anahtarlı priz her akşam kapatılacak.',[66,50],round=2)
for k,t,d,a,pr,sc,re,why,im in [('strip','Anahtarlı Çoklu Priz','Bağlı cihazları tek düğmeyle kapatır.','old:obj_workshop_power_strip_installed',260,100,'Cihazların elektriği kesildi.','İş bitince anahtarı kapatmak bekleme tüketimini durdurur.',-200),('smart','Akıllı Priz','Belirlenen saatte elektriği kesebilir.','old:obj_laundry_smart_plug_installed',350,100,'Mesai bitince elektrik kesildi.','Saati mesaiye göre ayarladığın için cihazlar beklemede kalmadı.',-200),('meter','Wattmetre / Enerji Ölçer','Bağlı cihazın tüketimini ölçer.','old:obj_workshop_wattmeter_installed',300,20,'Tüketimi görebiliyorsun.','Ölçmek tek başına tüketimi azaltmaz; cihazların kapanması da gerekir.',0)]:choice(x,k,t,d,a,pr,sc,re,why,im,'office-'+k)
x=op('laundry-sort','laundry','Çamaşırları ayır','Etiketleri aynı yıkamaya uygun olan günlük çamaşırları renklerine göre ayır.',[50,65],'sorting',round=2)
x['targets']=[dict(id=k,title=t,asset='sprites/generated/basket-'+k) for k,t in [('white','Beyazlar'),('color','Renkliler'),('dark','Koyular')]]
x['items']=[dict(id=k,title=t,asset='sprites/generated/clothes-'+k,target=k) for k,t in [('white','Beyaz çamaşırlar'),('color','Renkli çamaşırlar'),('dark','Koyu çamaşırlar')]]
x=op('laundry-load','laundry','Makineyi ne zaman çalıştıralım?','Aynı gruptan daha fazla çamaşır var. Acil yıkama gerekmiyor; makinenin önerilen kapasitesini aşma.',[31,49],'load',round=2)
for k,t,sc,re,why in [('quarter','%25 doluluk',20,'Az çamaşırla çalıştırdın.','Aynı çamaşırları bitirmek için daha çok yıkama gerekebilir.'),('half','%50 doluluk',60,'Yarım yükle çalıştırdın.','Biraz daha biriktirmek yıkama sayısını azaltabilirdi.'),('full','Uygun tam yük',100,'Önerilen kapasiteyle çalıştırdın.','Çamaşırları sıkıştırmadan biriktirmek, aynı miktar için gereken yıkama sayısını azaltır.')]:choice(x,k,t,'',None,0,sc,re,why)
x=op('laundry-program','laundry','Yıkama programı','Günlük, normal kirli çamaşırlar; özel hijyen gereksinimi yok. Etiketleri düşük sıcaklığa uygun.',[31,49],'behavior',round=2)
for k,t,sc,re,why in [('eco','30°C / ECO',100,'Düşük sıcaklıkta yıkadın.','Bu günlük çamaşırlar için yüksek ısı gerekmiyordu; daha az su ısıttın.'),('normal','40°C / NORMAL',60,'Normal programı seçtin.','Bu çamaşırlar düşük sıcaklıkta da yıkanabilirdi; daha fazla su ısıttın.'),('hot','60°C / YOĞUN',20,'Gerekenden yüksek ısı seçtin.','Bu senaryoda özel hijyen ihtiyacı yoktu; yüksek ısıya gerek kalmıyordu.')]:choice(x,k,t,'',None,0,sc,re,why)
x=op('irrigation','garden','Sebze sıraları','Sıra aralarında bitki yok. Amaç suyu yalnız köklere vermek; hortumu seçersen her köke tek tek yönelteceksin.',[53,63],round=3)
for k,t,d,a,pr,sc,re,why,im in [('hose','Hortum Tabancası','Elle yönlendirilen sulama.','irrigation-hose',180,100,'Suyu her köke elle yönelttin.','Hortumu kökte tutup geçişlerde kapattığında boş alanları sulamadın.',-180),('sprinkler','Fıskiye','Suyu geniş alana dağıtır.','irrigation-sprinkler',240,40,'Bitki dışındaki alanlar da ıslandı.','Fıskiye suyu sebze sıralarının arasına da dağıttı.',-40),('drip','Damla Hattı','Bitki sıraları boyunca döşenir.','irrigation-drip',380,100,'Su kök bölgesine ulaştı.','Damla hattı suyu sıra aralarına dağıtmak yerine bitki dibine verdi.',-180)]:choice(x,k,t,d,a,pr,sc,re,why,im,'garden-'+k)
x=op('irrigation-time','garden','Sulama zamanı','Sıcak ve kuru bir günde sulama yapacaksın. Toprak sulamaya ihtiyaç duyuyor.',[53,63],'behavior',round=3)
for k,t,sc,re,why in [('morning','Sabah',100,'Serin saati seçtin.','Güneş yükselmeden sulamak sıcak öğle saatine göre buharlaşmayı azaltır.'),('noon','Öğle',40,'Sıcak saatte suladın.','Bu senaryoda sıcaklık nedeniyle su daha çabuk buharlaşır.'),('evening','Akşam',100,'Serin saati seçtin.','Güneşin etkisi azaldığında sulamak sıcak öğleye göre buharlaşmayı azaltır.')]:choice(x,k,t,'',None,0,sc,re,why)
x=op('irrigation-timer','garden','Sulama süresi','Süreyi takip etmek için yardımcı ekipman ekleyebilirsin. Bu isteğe bağlı adım puan getirmez.',[47,29],core=False,round=3)
choice(x,'timer','Sulama Zamanlayıcısı','Ayarlanan sürede suyu kapatır.','irrigation-timer',240,0,'Sulama süresini ayarlayabilirsin.','Zamanlayıcı unutmayı azaltır; doğru süreyi seçmek yine senin kararındır.',0,'garden-timer')
for kind,title,scenario,keys in [
 ('lentil','Mercimek ambalajı','Aynı miktar mercimeği düzenli alıyorsun. Cam kavanoz burada iade edilip tekrar dolduruluyor.',['plastic','paper','return']),
 ('apple','Elma ambalajı','Aynı miktar elmayı her hafta alıyorsun. Fileyi sonraki alışverişlere de getireceksin.',['plastic','paper','mesh']),
 ('towel','Havlu teslimi','Müşteri aynı havluyu standından alıp yanında götürüyor. Kargo yok; paketlerin hepsi taşımaya hazır.',['plastic','box','kraft']),
 ('scarf','Şal teslimi','Müşteri aynı şalı standından alıp yanında götürüyor. Kargo yok; paketlerin hepsi taşımaya hazır.',['plastic','box','kraft'])]:
 x=op('pack-'+kind,'storage',title,scenario,[51,63],round=3 if kind in ['lentil','apple'] else 4)
 for key in keys:
  if kind=='lentil':
   title={'plastic':'Plastik Paket','paper':'Kâğıt Paket','return':'İadeli Cam Kavanoz'}[key];strong=key=='return';why='Kavanoz iade edilip yeniden doldurulacak; her alışverişte yeni ambalaj gerekmiyor.' if strong else 'Bu paketin tekrar dolum sistemi yok; her alışverişte yeni paket kullanılıyor.';score=100 if strong else 40
  elif kind=='apple':
   title={'plastic':'İnce Plastik Poşet','paper':'Kâğıt Torba','mesh':'Tekrar Kullanılabilir File'}[key];strong=key=='mesh';why='Fileyi sonraki alışverişlerde de kullanarak yeni torba ihtiyacını azalttın.' if strong else 'Bu senaryoda torba bir kez kullanılıyor; sonraki alışverişte yenisi gerekiyor.';score=100 if strong else 40
  else:
   title={'plastic':'İç Paket + Taşıma Poşeti','box':'Karton Kutu','kraft':'Tek Kraft Çanta'}[key];strong=key=='kraft';why={'plastic':'İç paket ve taşıma poşetiyle aynı ürün için iki ambalaj kullandın.','box':'Kargo yapılmayan bu teslimde sert kutu yerine daha az malzemeli çanta yeterliydi.','kraft':'Ürünü tek ambalajla teslim ettin; ek taşıma poşetine gerek kalmadı.'}[key];score={'plastic':20,'box':60,'kraft':100}[key]
  choice(x,key,title,'Aynı ürün ve miktar, farklı ambalaj.',kind+'-'+key,{'plastic':10,'paper':15,'return':35,'mesh':25,'box':30,'kraft':15}[key],score,'Ürün teslim edildi.',why,0,'packing-table')
x=op('roof-bonus','roof','Güneş yatırımı','Bu örnek yatırım puanlanmaz. Gerçek kurulumda çatı, izinler ve tüketim ayrıca değerlendirilir.',[55,51],core=False,round=4)
choice(x,'solar','Çatı Paneli','Çatıya kurulan güneş paneli.','old:obj_solar_array',800,0,'Panel kuruldu.','Gerçek yatırım için çatı uygunluğu ve tüketim birlikte değerlendirilmelidir.',0,'roof-plane')
for o in ops:
 if o['kind']=='sorting':o['result']={'title':'Ayırma tamamlandı.','text':'Kirli peçete temiz kâğıda karışmadı.' if o['id']=='waste-sort' else 'Çamaşırları renk gruplarına ayırdın.','why':'Her toplama sisteminin kabul ettiği atıkları ayrıca kontrol et.' if o['id']=='waste-sort' else 'Yıkamadan önce giysilerin bakım etiketlerini de kontrol et.'}
for name,data in [('opportunities',ops),('economy',econ),('scores',scores),('copy',copy),('assets',assets)]:
 (root/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Opportunities',len(ops),'choices',len(copy),'core',sum(o['core'] for o in ops))
