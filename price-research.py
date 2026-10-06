exec(open('work/economy-revision.py',encoding='utf-8').read().split('ops=data')[0])
d=data('src/data/market-prices.json'); c=d['catalog']
def setp(id,price,ref,spec,url,note='',status='verified'):
 c[id].update(priceTL=price,referencePriceTL=ref,referenceProduct=spec,referenceSpecification=spec,referenceSource=url,priceStatus=status,provenance='web',note=note)
setp('rev-tap-repair',349,349,'Remtas 10 lu O-ring salmastra conta takımı','https://www.trendyol.com/remtas/oring-salmastra-set-10-lu-paket-conta-o-ring-lastik-sizdirmazlik-contasi-musluk-hortum-tamir-conta-seti-p-1146980014','Yalnız conta takımı; görseldeki el aletleri fiyata dahil değil. Bağlantı uyumu gerçek uygulamada ayrıca kontrol edilir.')
setp('rev-office-power-strip',139,138.90,'Koçtaş Basic 3 lü 2 m anahtarlı grup priz','https://www.koctas.com.tr/koctas-basic-3lu-2-mt-anahtarli-grup-priz/p/1000611163','Açılan sayfadaki indirimli referans, stok mağazaya bağlı; gerçek kullanımda yük ve topraklama uygunluğu ayrıca gerekir.')
setp('rev-irrigation-hose',300,299.90,'Verve gül başlıklı tek sulama tabancası','https://www.koctas.com.tr/bahce-sulama-urunleri/hortum-tabancalari/c/102006004','Mevcut hortuma takılan tabanca; hortum dahil değil.')
setp('rev-irrigation-sprinkler',300,299.90,'Verve multi fonksiyon fıskiye','https://www.koctas.com.tr/bahce-ve-balkon/bahce-sulama-urunleri/c/102006','Mevcut hortuma bağlanan fıskiye; hortum hariç.')
setp('rev-irrigation-drip',664,664,'Depolife 20 metre hortum ve bağlantılar, 45 parçalı damlalama seti','https://www.koctas.com.tr/depolife-deliksiz-duz-damla-sulama-sistemi-ve-parcalari-bahce-agac-fidan-sebze-damlama-hortumu/p/5000690512','Sayfa anlık stok göstergeleri tutarsız; fiyat referansı, stok garantisi değildir. Zamanlayıcı ayrıca.')
setp('rev-irrigation-timer-timer',769,769,'Neptun mekanik sulama saati 5–120 dakika','https://www.bauhaus.com.tr/neptun-sulama-saati-29226379')
setp('rev-pack-lentil-paper',1,958.8/825,'15x28x8 cm kraft kese; yaklaşık 825 adet / 958,80 TL KDV dahil','https://kullanatpazari.com/kraft-kese-kagidi-duz-15x28x8-cm','Tek ambalaj payı 958,80 / 825, tam TL yuvarlama; içindeki gıda hariç.')
setp('rev-pack-apple-paper',2,958.8/490,'25x33x7,5 cm kraft kese; yaklaşık 490 adet / 958,80 TL KDV dahil','https://kullanatpazari.com/kraft-kese-kagidi-duz-25x33x75-cm','Tek ambalaj payı 958,80 / 490; ürün sayfasında uzunluk 29/33 çelişkisi var, boy aralığı temsili; gıda hariç.')
for id in ['rev-pack-towel-box','rev-pack-scarf-box']:
 setp(id,None,798.83/50,'Unipak 30x20x10 cm 50 li kutu / 798,83 TL','https://www.unipak.com.tr/urun/30x20x10-cm-kesimli-e-ticaret-ve-kargo-kutusu-50-esmer','PRICE REVIEW REQUIRED: açılan ürün sayfasında stok yok; mevcut satış teyit edilemedi.',status='needs_review')
for id in ['rev-tap-aerator','rev-shower-compact','rev-shower-classic','rev-shower-rain']:
 amount={'rev-tap-aerator':90,'rev-shower-compact':280,'rev-shower-classic':150,'rev-shower-rain':2000}[id]
 c[id].update(referencePriceTL=amount,note='PRICE REVIEW REQUIRED: daha önce kullanıcı tarafından verilen referans var; bu araştırmada görsel sınıfı ve güncel satış birlikte doğrulanamadı. Önceki fiyat revizyonu geri alındığı için otomatik yeniden uygulanmadı.')
dump('src/data/market-prices.json',d)
cp=data('src/decisions/copy.json');cp['rev-tap-repair']['shortDescription']='Conta takımı. El aletleri fiyata dahil değildir.'
cp['rev-office-power-strip']['shortDescription']='Anahtarlı, üç çıkışlı, 2 metre grup priz.'
cp['rev-irrigation-hose']['shortDescription']='Mevcut hortuma takılan el tabancası.'
cp['rev-irrigation-drip']['shortDescription']='20 metre hortum ve bağlantı parçaları.'
dump('src/decisions/copy.json',cp)
