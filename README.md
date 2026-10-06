# Yeşil Dönüşüm

Mevcut Vite + TypeScript + Phaser 3 oyununun 5 Ekim 2026 revizyonu.
Arka planlar, kayıt sistemi, dört dönem ve oyun görsel dili korunmuştur.
Ayrıntılı değişiklik ve seçenek matrisi: [REVIZYON-RAPORU.md](REVIZYON-RAPORU.md).

## Oynama

Windows'ta **BASLAT.cmd** dosyasını açın. Node.js 22+ gerekir.
Tarayıcı `http://127.0.0.1:4173` adresinde açılır; konsol açık kalsın.
Alternatif: `node serve.mjs`. Hazır dosyalar `dist/` içindedir; oynamak için paket indirmek gerekmez.
`dist/index.html` dosyasını çift tıklamak yerine yerel sunucuyu kullanın.

## Güncel oyun

- 8 görünür alan, 4 dönem; 18 temel karar ve 3 puansız isteğe bağlı fırsat.
- 51 karar seçeneği; 33 kurulabilir ürün. Temel seçimlerin hepsinde en az 3 alternatif/hedef.
- Ürün: sorunu gör → markette incele → satın al → otomatik odaya dön → yerleştir → ANLADIM.
- Atık ve çamaşır ayırma: nesneye dokun, hedefe dokun. Yanlışlar düzeltilebilir; ilk eşleştirme puana sayılır.
- Doluluk ve yıkama programı, sifon, diş fırçalama, hijyen ve sulama saati kısa davranış seçimleridir.
- Leğen, sulama zamanlayıcısı ve çatı yatırımı isteğe bağlıdır; puan avantajı sağlamaz.
- HUD: DÖNEM, KALAN PARA, SKOR. Öğrenme kartları otomatik kapanmaz.
- Finalde kooperatif ve iki katılımcı, toplam skor ve üç gerçek hayat adımı korunur.

## Skor ve para

Yeni oyunlar `decisionVersion: 1` kullanır. Toplam en çok **1.800 karar puanı** alınır.
Aynı kararlar aynı puanı üretir; para, animasyon süresi veya rastgelelik puana eklenmez.
İki seçenek eşit gerekçeyle doğruysa eşit puan verilir. Her fırsat yalnız bir kez puanlanır.

Başlangıç aylık gideri ₺10.000, bütçe ₺2.500. Fiyatlar ve fatura etkileri geçici simülasyon değerleridir;
piyasa fiyatı veya gerçek tasarruf vaadi değildir. Satın alma bütçeyi, kurulum örnek gideri değiştirir.
Dönem ödülü mevcut kuralla korunur: yeni gider azalmasının %50'si, en çok ₺500.

## Kayıtlar ve kurumlar

`public/organizations.json` mevcut 26 kurumun tam adlarını içerir. İki katılımcı adı zorunludur.
Deneme sonuçları liderlik tablosuna eklenmez. Resmî sonuç kurumu kilitler; aynı kurum tekrar resmî sonuç yazamaz.
Otomatik kayıt anahtarı `yesil-donusum-v1`, veritabanı biçimi v2 olarak korunur.

Eski oyunlar eski karar/ekonomi kurallarıyla devam eder; eski sonuçlar yeniden puanlanmaz.
Yeni liderlik tablosu yalnız aynı karar puanı sürümünü karşılaştırır. Eski sonuçlar yönetim ve yedekte korunur.
Önceki sürümün 30 ürünü ve kaldırılan görevleri eski kayıt uyumluluğu için kodda bulunur, yeni akışta sunulmaz.

Yönetim: `http://127.0.0.1:4173/#admin`. CSV, JSON yedek, silme ve geri yükleme burada bulunur.
CSV puan kuralını da belirtir. Kayıtlar yalnız bu tarayıcıdadır; bulut eşitlemesi yoktur.
Yönetim ekranı kimlik doğrulama sınırı değildir. Etkinlikte görevli cihazı kullanın ve JSON yedeği alın.

## Veri ve görseller

`src/decisions/` altında fırsat, fiyat, puan, copy, asset, placement ve kaynak notları ayrı dosyalardadır.
`index.ts` bu verileri birleştirir. Eski `src/data.ts` kayıt uyumluluğu için korunur.
Yeni 47 WebP, kullanıcının sheet'lerinden kırpılmıştır; AI görseli üretilmemiştir.
19 orijinal `public/assets/source/` içinde değişmeden saklanır.
Kaynak hash'leri ve kesimler `public/assets/sprites/manifest.json` içindedir.
Yeniden üretim: `python scripts/build_revision_sprites.py` (Pillow gerekir).
Kurulum koordinatları `src/decisions/placements.json` ve `src/placements.ts` içindedir.

## Çevrimdışı

Tüm temel oyun dosyaları lokaldir. İlk başarılı üretim açılışında service worker önbelleğe alır.
Önbellekleme tamamlanmadan bağlantıyı kesmeyin. Orijinal üretim sheet'leri önbelleğe alınmaz;
oyunda kullanılan tüm kırpılmış görseller alınır. Tarayıcı verilerini silmek kayıtları da siler.
Geliştirme sunucusunda service worker kurulmaz.

## Geliştirme ve doğrulama

```sh
pnpm install
pnpm dev --port 5175
pnpm test
pnpm build
pnpm run format:check
```

Chrome kurulu olmalıdır. Tam akış `pnpm run test:e2e` (varsayılan 5175).
Üretim testleri için `pnpm preview --port 4180` açın; `GAME_URL` ile adresi değiştirebilirsiniz.
`pnpm run test:offline` internet kapalı açılış, dokunmatik, resmî sonuç, CSV/JSON ve erişilebilirlik testidir.
`pnpm run test:placements` 33 ürünün kurulu sahne görüntülerini üretir (4180).
`qa/main-revision/` test raporları ve ekran görüntülerini içerir.
Önceki `scripts/e2e.cjs`, `full-flow.cjs`, `tl.cjs`, `meaning.cjs`, `ux.cjs` eski akışın tarihsel testleridir;
yeni kabul testi giriş noktaları `revision-flow.cjs` ve `revision-offline.cjs` dosyalarıdır.
Testler izole tarayıcı bağlamında çalışır; kullanıcının açık oyun kaydını değiştirmez.
