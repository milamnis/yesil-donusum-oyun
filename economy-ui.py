exec(open('work/economy-revision.py',encoding='utf-8').read().split('ops=data')[0])
s=read('src/main.ts');s='import { marketPrice, priceLabel, existingFixture } from "./data/market-prices";\nimport { acknowledgeSales } from "./model";\nimport { FINAL_SALES_INCOME } from "./economy";\n'+s
s=s.replace('function mapScreen() {\n  const s = db.active!;','''function mapScreen() {
  const s = db.active!;
  if (s.salesIncomeGranted && !s.salesIncomeAcknowledged) return `<section class="sales-screen"><div class="sales-panel"><p class="eyebrow">4. DÖNEM</p><h2>SATIŞLAR ARTTI</h2><p>Bu ay kooperatifin siparişleri arttı.</p><p class="sales-amount">Kasaya <strong>+${fmtMoney(FINAL_SALES_INCOME)}</strong> eklendi.</p><p>Kalan paranla birlikte artık daha büyük yatırımları da değerlendirebilirsin.</p><p class="sales-balance">Kalan para <b>${fmtMoney(s.budget)}</b></p>${btn("SON DÖNEME BAŞLA", "sales-start", "gold")}</div></section>`;''')
s=s.replace('${fmtMoney(p.price)}','${priceLabel(p.id, p.price)}')
needle='  return `${hud()}<section aria-label="Yeşil Market">'
s=s.replace(needle,'''  const existing = contextIds().find(existingFixture);
  return `${hud()}<section aria-label="Yeşil Market">''')
s=s.replace('${!ps.length ? \'<div class="market-empty">','${existing ? `<aside class="existing-choice"><b>Odadaki eski ampul hâlâ çalışıyor.</b><p>Yeni ürün almadan kullanmaya devam edebilirsin.</p>${btn("ESKİ AMPULLE DEVAM ET · ₺0", `keep-existing:${existing}`, "ghost")}</aside>` : ""}${!ps.length ? \'<div class="market-empty">')
s=s.replace('  }<div class="period-idea">','  }<p class="carryover-note">Tasarrufundan kasana ${signedMoney(h.reward)} geri döndü.${s.round < 4 ? " Kalan paran sonraki döneme aktarılacak." : ""}</p><div class="period-idea">')
s=s.replace('${awards()}<div class="row">','''<div class="final-economy"><p>Kalan para<b>${fmtMoney(s.budget)}</b></p><p>Toplam yatırım<b>${fmtMoney(s.moves.reduce((n,m)=>n+m.cost,0) + s.inventory.reduce((n,id)=>n+(s.purchaseCosts?.[id] ?? productById(id).price),0))}</b></p><p>Tahmini dönemsel tasarruf<b>${fmtMoney(Math.max(0,INITIAL_BILL-s.bill))}</b></p></div>${awards()}<div class="row">''')
s=s.replace('Bu oyundaki TL tutarları karşılaştırma için hazırlanmış örnek değerlerdir. Gerçek ürün fiyatı ve tasarruf kullanım koşullarına göre değişir.','${SIMULATION_NOTE}')
start=s.index('  const owned = s.inventory.includes(id)',s.index('async function productDetail'))
end=s.index('\n  dialog.classList.add("product-dialog");',start)
s=s[:start]+'''  const owned = s.inventory.includes(id) || s.installed.includes(id);
  const review = marketPrice(id)?.priceTL === null;
  const affordable = !review && s.budget >= p.price;
  const remaining = s.budget - p.price;
  const solar = id === "rev-roof-bonus-solar";
  const large = solar || (!review && p.price > s.budget * LARGE_PURCHASE_SHARE);
  const packaging = id.startsWith("rev-pack-");
  showModal(
    `<p class="eyebrow">YEŞİL MARKET · ${esc(p.category)}${solar ? " · BÜYÜK YATIRIM" : ""}</p>${art(p.asset, "product-art")}<h2 id="dialog-title">${esc(p.name)}</h2><p class="product-feature">${esc(p.feature)}</p><p class="product-use">${esc(p.description)}</p><dl class="purchase-math"><div><dt>${packaging ? "1 adet ambalaj payı" : "Fiyat"}</dt><dd>${priceLabel(id,p.price)}</dd>${solar ? '<p class="panel-price-note">Yalnız panel fiyatıdır.</p>' : ""}</div>${review ? "" : `<div class="remaining"><dt>${affordable ? "Kalan" : "Bu ürün için eksik"}</dt><dd id="purchase-remaining">${fmtMoney(Math.abs(remaining))}</dd></div>`}</dl>${solar ? '<details class="price-detail"><summary>Fiyata neler dahil?</summary><p>İnverter, konstrüksiyon, kablolama, proje, montaj ve işçilik dahil değildir.</p></details>' : ""}${packaging ? '<p class="panel-price-note">İçindeki ürünün bedeli hariçtir. Çoklu paketten hesaplanan adet payı olabilir.</p>' : ""}${review ? '<p class="error">Paket içeriği ve fiyatı doğrulanıyor. Şimdilik satın alınamaz.</p>' : !owned && !affordable ? `<p class="error">🔒 ${fmtMoney(-remaining)} daha gerekiyor.</p>` : !owned && large ? '<p class="budget-question">Bu büyük bir harcama. Birlikte karar verin.</p>' : ""}<div class="actions">${btn("BİR DAHA BAK", "close", "ghost")}${btn(owned ? "Zaten sizde" : "SATIN AL", `buy:${id}`, "primary", owned || !affordable ? "disabled" : "")}</div>`,
  );''' +s[end:]
s=s.replace('    case "decision":','''    case "sales-start":
      await mutate(acknowledgeSales);
      render();
      break;
    case "keep-existing": {
      if (!existingFixture(arg)) throw Error("Bu mevcut bir eşya değil.");
      const p = productById(arg);
      await mutate(s => ({ ...recordChoice(s,arg), room:p.room, originScene:p.room }));
      closeModal();
      switchView("room");
      scheduleLesson();
      break;
    }
    case "decision":''')
s=s.replace('  const next = db.active?.lessons?.find(', '  if (db.active?.salesIncomeGranted && !db.active.salesIncomeAcknowledged) return;\n  const next = db.active?.lessons?.find(')
s=s.replace('.register("./sw.js")','.register("./sw.js", { updateViaCache: "none" })\n      .then(async registration => { await registration.update(); return registration; })')
write('src/main.ts',s)
s=read('scripts/offline.mjs');s=s.replace("e.respondWith(caches.match(e.request", "if(e.request.mode==='navigate'){e.respondWith(fetch(e.request).then(r=>{if(!r.ok)throw Error('offline');return r;}).catch(()=>caches.match('./index.html')));return;}e.respondWith(caches.match(e.request")
write('scripts/offline.mjs',s)
write('src/style.css',read('src/style.css')+'''
/* Economy revision: readable, single-purpose income introduction. */
.sales-screen { position:absolute;inset:0;display:grid;place-items:center;background:#253b32e8;padding:24px; }
.sales-panel { max-width:740px;background:#f3e8d0;color:#263c32;border-top:5px solid #bd9855;border-radius:16px;padding:38px 48px;text-align:center;box-shadow:0 20px 60px #132a2640; }
.sales-panel h2 {font-size:clamp(30px,3.5vw,48px);margin:12px 0 22px;}
.sales-panel p {font-size:21px;line-height:1.45;}
.sales-panel .sales-amount strong {display:block;font-size:54px;color:#38583f;}
.sales-balance b {margin-left:12px;}
.sales-panel button,.product-dialog .actions button,.existing-choice button {min-height:56px;font-size:18px;}
.panel-price-note,.price-detail {font-size:18px!important;line-height:1.45;color:#304b39;}
.price-detail summary {cursor:pointer;padding:10px 0;min-height:44px;}
.price-detail p {margin:4px 0 14px;}
.existing-choice {position:absolute;left:4%;bottom:14%;max-width:420px;padding:18px 22px;border:1px solid #d7c7a2;border-radius:12px;background:#f5ebd8f5;color:#2a4031;box-shadow:0 5px 18px #172d2426;}
.existing-choice p {font-size:18px;margin:8px 0 12px;}
.existing-choice b {font-size:21px;}
.final-economy {display:flex;justify-content:center;gap:28px;margin:16px 0;}
.final-economy p {font-size:16px;margin:0;}
.final-economy b {display:block;font-size:25px;margin-top:5px;}
.carryover-note {font-size:18px;line-height:1.5;}
@media(max-height:800px) {.sales-panel{padding:22px 35px}.sales-panel p{font-size:19px}.sales-panel h2{margin:8px 0}.sales-panel .sales-amount strong{font-size:44px}.product-dialog .product-art{max-height:125px}.product-dialog .purchase-math{margin:14px 0}.final-economy{gap:20px;margin:10px 0}}
''')
