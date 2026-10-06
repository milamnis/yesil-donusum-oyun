from pathlib import Path
p=Path('README.md');s=p.read_text(encoding='utf-8-sig')
a=s.index('## Ekonomi');b=s.index('\n## Çevrimdışı',a)
s=s[:a]+'''## TL ekonomisi

Başlangıç aylık gideri **₺10.000**, Yeşil Kasa **₺2.500**. Bunlar piyasa fiyatları
veya gerçek tasarruf vaatleri değildir; karşılaştırma için örnek simülasyon tutarlarıdır.
Merkezi sabitler ve Türkçe para biçimleyici `src/economy.ts` içindedir.
Ürün fiyatları/etkileri, parasız fikirler ve kombinasyonlar önceki ölçeğin 10 katıdır.

Satın alma yalnız kasayı değiştirir; sonuç kurulumda görülür. Ürün detayında fiyat,
mevcut kasa ve alımdan sonra kalacak tutar birlikte gösterilir. Kasanın %30'undan
fazlasını kullanan alışverişte kısa bir ortak karar hatırlatması vardır.

Dönem ödülü: `min(floor(max(0, önceki dönem gideri - mevcut gider) * 0.5), 500)`.
İlk dönem ₺10.000'den başlar. Önceki tasarruf yeniden ödüllendirilmez.
Skor, gider ve kasayı MONEY_SCALE ile normalize eder; ölçek büyüdü diye skor 10 kat olmaz.
Sıralama önce gider azalma yüzdesi, sonra skor, sonra erken bitiriş kullanır.

### Seçimi sonradan değiştirme

Duş başlıkları, ampuller, çoklu prizler, atık toplama seçenekleri ve çatı enerji
ürünleri beş ayrı `exclusiveGroup` oluşturur. Yeni alternatif kurulduğunda eski
aktif etki kaldırılır ve yeni etki uygulanır. İki alışveriş de harcanmış kalır;
**iade yoktur**. Her ürün bir kez alınır. Eski karar ve düzeltme hamle geçmişinde saklanır.
Perlatör + tamir, perde + şerit, gösterge + priz, yağmur + depo/sulama birlikte çalışır.

Kayıt biçimi v2'dir; eski localStorage anahtarı veri kaybetmemek için korunur.
v1 kayıtların parasal alanları, kartları ve sonuç tutarları yalnız bir kez x10 çevrilir.
Yayımlanmış skorlar, yüzdeler ve sıralama değişmez. Eski sürümde üst üste kurulan
alternatiflerin sonuncusu aktif olur; tarihsel net tutarı koruyan fark, iç kayıtta
`legacyAdjustment` olarak tutulur. Önceden ödenmiş dönem ödülleri geri alınmaz.
''' +s[b:]
s=s.replace('en fazla 50 kredi','en fazla ₺500').replace('50 kredi tavanı','₺500 tavanı').replace('fatura etkileri','gider etkileri')
s=s.replace('Ürün fiyatları, gider etkileri, kombinasyonlar ve fiziksel kurulumlar korunmuştur.','Ürün fiyatları, gider etkileri ve kombinasyonlar TL ölçeğine taşınmıştır; fiziksel kurulumlar korunmuştur.')
s=s.replace('Kasa bakiyesinin en az %40’ını kullanacak alışverişlerde iki kişilik karar onayı çıkar.','Kasanın %30’undan fazlasını kullanacak alışverişlerde ortak karar hatırlatması gösterilir.').replace("Kasa bakiyesinin en az %40'ını kullanacak alışverişlerde iki kişilik karar onayı çıkar.","Kasanın %30'undan fazlasını kullanacak alışverişlerde ortak karar hatırlatması gösterilir.")
s+='''
## Market ve yönlendirme güncellemesi

30 ürünün kısa fiziksel özelliği ve kullanım cümlesi tarafsızdır; iyi/kötü türü
kurulum öncesinde renk, simge veya sıralama üretmez. Raf sırası sabit ve karışıktır,
resmî yarışmada herkese aynıdır. Satın alma sonrası kısa çanta animasyonu vardır.

Oda başlığı kaç fırsatın tamamlandığını gösterir. Yaklaşık 40 saniye hareketsizlikte
isteğe bağlı, ürün önermeyen bir ipucu çıkar. Düşük kasada dönem başına en fazla bir
kısa bütçe düşüncesi gösterilir; işaret autosave ile korunur.
Dönem sonunda TL sayaçları ve yapılan hamlelerin küçük görselleri görünür.
`pnpm test:tl` beş alternatif grubunu üç ekran boyutunda ve axe ile doğrular.
'''
p.write_text(s,encoding='utf-8')
p=Path('DESIGN.md');s=p.read_text(encoding='utf-8-sig').replace('fixture occupies a replacement slot; this visual rule does not change financial effects.','fixture occupies a replacement slot. Explicit exclusive groups now also reverse the retired financial effect, without a refund.')
s+='''
## TL and corrective choices

Currency owner: src/economy.ts; no decimal currency in player UI. Preserve the existing
palette, typefaces, scene anchors and shelf slots. Product details add one neutral
three-line budget calculation, shared by all consequence types. Kind is internal;
no pre-purchase class, color, order or badge depends on it. Market order is static.
Show comparison-only simulation wording in market help and once in the final.
Opportunity counts sit below room titles without colliding with the three-goal card.
Purchase receipt and flying thumbnail are brief; persistent education still follows installation.
Replacement impact is distinct from the new product impact and combo bonus in learning cards.
The period recap uses existing product thumbnails, not a new video or dashboard.

| Previous rule | Current decision |
| --- | --- |
| Financial effects accumulate for replacement slots | Five explicit exclusive groups replace their active effect; complementary items accumulate. |
| 40% purchase confirmation | A shared 30% budget note in the existing purchase detail; one ALALIM action. |
| Abstract credit values | TL examples at x10, score normalized, v1 records migrated once. |
'''
p.write_text(s,encoding='utf-8')
p=Path('UX-CONTRACT.md');s=p.read_text(encoding='utf-8-sig')
s=s.replace('Game credits and bills are simulation values, not money or real utility calculations.','TL amounts are example simulation values, not market prices or real utility calculations.')
s=s.replace('/ 2), 50)','* 0.5), 500)').replace('Use 1000 as the first period baseline.','Use INITIAL_BILL (10000) as the first period baseline.')
s=s.replace('or more credits','or extra spending').replace('Product effects, costs and combo bonuses remain unchanged; only period rewards change as requested.','All money scales by MONEY_SCALE; normalized score retains the previous range. Exclusive replacements reverse the previous active contribution.')
s=s.replace('Purchases consuming at least 40% of current cash require the explicit two-person confirmation.','Purchases consuming more than 30% of cash show a shared-decision sentence in the neutral product detail.')
s=s.replace('Combo surprise lasts 2.7 seconds','Combo surprise lasts 3 seconds')
s+='''
## TL v2 lifecycle

- economy.ts owns INITIAL_BILL, INITIAL_BUDGET, MONEY_SCALE, reward rate/cap, fmtMoney.
- installed retains historical ownership. activeInstallations alone renders installed products
  and supplies combo/zone checks. replacedInstallations records retired products; moves retain
  original cost/impact and replacedBy. New moves record reversalImpact separately.
- No refund or free re-purchase; a new alternative must first be purchased normally.
- Only the five user-specified groups are exclusive. Same room or zone alone never means exclusion.
- v1 to v2 conversion includes active bill/budget, moves, round history, lesson snapshots and
  result bill/budget. Stored scores and rankings are preserved. Repeated migration is idempotent.
- Existing additive v1 alternatives keep their historical net balance through legacyAdjustment;
  only the last fixture is active. Future changes use the new replacement rule.
- Atomic localStorage transactions, Web Locks, corrupt-record protection and quota rollback remain.
- The market uses neither kind nor feedback/lesson content before purchase. Static shelf order
  is shared by practice and official games; contextual shelves use exact room + zone + unlock.
- The detail always computes remaining cash; insufficient funds show the missing amount and
  disable ALALIM. Above 30%, a sentence prompts discussion without revealing the outcome.
- Receipt fades after 3 seconds (keyboard focus delays removal); inventory remains available.
- Idle hint appears after 40 seconds, only in a room without a modal, at most once per room/round.
  Pointer/key activity resets it. It names no product or correct answer.
- Budget thought appears once per round on a purchase leaving at most 36% of initial cash;
  budgetMoments persists that bound. It never changes the economy.
'''
p.write_text(s,encoding='utf-8')
