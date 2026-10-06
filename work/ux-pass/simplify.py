from pathlib import Path
p=Path('outputs/yesil-donusum')
f=p/'src/main.ts'; s=f.read_text(encoding='utf-8')
s='import { activeOpportunity, nextRoom } from "./navigation";\n'+s
s=s.replace('let continueReady = false;\n','').replace('  continueReady = false;\n','').replace('      continueReady = true;\n','')
a=s.index('function hud()');b=s.index('function readyProduct()',a)
s=s[:a]+'''function hud() {
  const s = db.active!;
  return `<header class="hud simple-hud"><div class="hud-brand"><small>DÖNEM</small><b>${s.round} / 4</b></div><div class="meters"><div class="meter cash"><small>MEVCUT PARA</small><strong id="budget-value">${fmtMoney(s.budget)}</strong></div><div class="meter score"><small>SKOR</small><strong id="score-value">${fmt(score(s))}</strong></div></div>${btn(soundEnabled() ? "Ses açık" : "Ses kapalı", "sound", "ghost sound-toggle")}${btn("?", "help", "ghost help-button", 'aria-label="Oyun rehberi"')}</header>`;
}
'''+s[b:]
a=s.index('function footer()');b=s.index('function inventory()',a)
s=s[:a]+'''function footer() {
  const s = db.active!;
  let label = "DEVAM ET", action = "end", hint = "Bu dönem için hazırsınız.";
  let secondary = btn("Dönemi bitir", "end", "ghost quiet-end");
  if (view === "market") {
    const origin = s.originScene || marketContext?.room || "kitchen";
    label = "GERİ DÖN"; action = `take:${origin}`; hint = "Bir seçeneğe dokunup inceleyebilirsin.";
    secondary = "";
  } else if (view === "room") {
    const p = readyProduct(), r = roomById(s.room as RoomId), z = activeOpportunity(s,r.id);
    if (p) {
      label = "YERLEŞTİR"; action = "place-ready"; hint = "Seçimin hazır. Haydi bunu yerine koyalım.";
      secondary = btn("Daha sonra", "map", "ghost quiet-end");
    } else if (z) { label = "ÇÖZÜM ARA"; action = `solve:${r.id}:${z.id}`; hint = ""; }
    else { action = "continue-room"; hint = "Buradaki adım tamam. Bir sonrakine bakalım."; }
  } else {
    const next = nextRoom(s);
    if (next) { action = `room:${next.id}`; hint = `${next.name} ile devam edebilirsin.`; }
  }
  if (action === "end") secondary = "";
  return `<nav class="nav-footer contextual-footer" aria-label="Sonraki adım"><div class="contextual-action">${hint ? `<p>${esc(hint)}</p>` : ""}<div class="actions">${btn(label,action,action === "end" ? "ghost" : "primary")}${secondary}</div></div></nav>`;
}
'''+s[b:]
s=s.replace('${hud()}${goalCard()}<section', '${hud()}<section')
start=s.index('${btn("Yeşil Market ↗", "market", "hotspot"');end=s.index('<div class="map-hint">',start)
s=s[:start]+s[end:]
s=s.replace('${roundHints[s.round - 1]}<br/><span class="muted">Bir tabelaya dokunun, içeri girin.</span>','Bir odaya dokunun, birlikte başlayalım.')
a=s.index('function roomScreen()');b=s.index('function marketScreen()',a)
s=s[:a]+'''function roomScreen() {
  const s = db.active!, r = roomById(s.room as RoomId), z = activeOpportunity(s,r.id), p = readyProduct();
  return `${hud()}<section aria-label="${r.name}"><div class="location task-panel"><h2>${r.name}</h2>${z ? `<small>Bugünkü hedef</small><ul><li>${p ? "Seçimin hazır." : z.problem}</li><li>${p ? "Haydi bunu yerine koyalım." : "Bir çözüm seç ve yerine koy."}</li></ul>` : '<p>Buradaki adım tamam.</p>'}</div>${z && !p ? btn(z.problem,`zone:${z.id}`,"zone active-problem",`style="left:${z.x}%;top:${z.y+9}%"`) : ""}</section>${footer()}`;
}
'''+s[b:]
a=s.index('function marketScreen()');b=s.index('function summaryScreen()',a)
s=s[:a]+'''function marketScreen() {
  const s = db.active!, ps = world.stock(category,s.round,0,contextIds());
  return `${hud()}<section aria-label="Yeşil Market"><div class="market-sign"><h2>Yeşil Market</h2><p>${marketContext ? roomById(marketContext.room).name + " için seçenekler" : "Bir çözüm seçelim."}</p></div>${ps.map((p,i) => {
    const slot = shelfSlots(category)[i];
    return `<div class="market-product ${marketSelected === p.id ? "selected" : ""}" data-slot="${slot.id}" style="left:${slot.x/W*100}%;top:${slot.y/H*100}%">${btn("",`product:${p.id}`,"market-hit",`aria-label="${esc(p.name)}, ${fmtMoney(p.price)}. İncele." aria-expanded="${marketSelected===p.id}"`)}<div class="product-peek"><b>${esc(p.name)}</b><small>${fmtMoney(p.price)}</small>${btn("İncele",`inspect:${p.id}`,"ghost")}</div></div>`;
  }).join("")}${!ps.length ? '<div class="market-empty"><p>Burada bekleyen bir seçim yok. Odaya dönebilirsin.</p></div>' : ""}</section>${footer()}`;
}
'''+s[b:]
s=s.replace('${btn("Fikir Çantam", "memory", "ghost")}','')
s=s.replace('<p class="period-goals">3 fırsattan ${miniGoals(s).filter((g) => g.done).length}’si tamamlandı.</p>','')
s=s.replace('    ["bill", before.bill, s.bill],','    ["score", score(before), score(s)],').replace('    ["saving", INITIAL_BILL - before.bill, INITIAL_BILL - s.bill],','')
s=s.replace('el.textContent = fmtMoney(\n          Math.round(from + (to - from) * (1 - Math.pow(1 - t, 3))),\n        );','el.textContent = (id === "score" ? fmt : fmtMoney)(Math.round(from + (to - from) * (1 - Math.pow(1-t,3))));')
s=s.replace('id === "bill" && to > from','id === "score" && to < from').replace('${fmtMoney(to - from)}`','${id === "score" ? fmt(to - from) : fmtMoney(to - from)}`')
s=s.replace('<div><dt>Şu an Kasa</dt><dd>${fmtMoney(s.budget)}</dd></div>','').replace('<div><dt>Kasa</dt><dd>${fmtMoney(s.budget)}</dd></div>','')
s=s.replace('Kasa bu ürüne yetmiyor.','Mevcut para bu ürüne yetmiyor.').replace('"ALALIM", `buy:${id}`','"SATIN AL", `buy:${id}`')
a=s.index('    case "help":');b=s.index('    case "pause":',a)
s=s[:a]+'''    case "help":
      showModal(`<h2 id="dialog-title">Birlikte, adım adım.</h2><p>Soruna bak, bir çözüm seç, yerine koy.</p><p>Oyun kendiliğinden kaydolur.</p>${btn("ANLADIM","close","primary")}<div class="secondary-tools">${btn("Başka odaya geç","map","ghost")}${btn("Mola ver","pause","ghost")}${btn("Tutarlar hakkında","money-info","ghost")}</div>`);
      break;
'''+s[b:]
# Persist context alongside the existing origin; old saves infer an active zone.
s=s.replace('originScene: room as RoomId,\n        room: "market",','originScene: room as RoomId,\n        originZone: zone,\n        room: "market",')
a=s.index('      const source = document',s.index('case "buy-confirm"'));b=s.index('      break;',a)
s=s[:a]+'''      await mutate((s) => ({ ...purchase(s,arg), originScene:p.room, originZone:p.zone, room:p.room }));
      closeModal();
      switchView("room");
      animateMeters(before);
      cueSound("purchase");
      document.querySelector<HTMLButtonElement>('[data-action="place-ready"]')?.focus();
'''+s[b:]
# Acknowledge opens the next opportunity without going through the overview.
a=s.index('    case "end": {');b=s.index('    case "end-confirm":',a)
s=s[:a]+'''    case "end": {
      showModal(`<h2 id="dialog-title">Bu dönemi bitirelim mi?</h2><p>İstersen biraz daha gezebilirsin.</p><div class="actions">${btn("DEVAM EDELİM","close","primary")}${btn("DÖNEMİ BİTİR","end-confirm","ghost")}</div>`);
      break;
    }
'''+s[b:]
a=s.index('  learningDialog.innerHTML =');b=s.index('\n  if (!learningDialog.open)',a)
s=s[:a]+'''  learningDialog.innerHTML = `<div class="lesson-top">${art(l.asset,"lesson-art")}<div><p class="eyebrow">BİR KÜÇÜK ADIM</p><h2 id="lesson-title">${esc(l.title)}</h2></div></div><p>${esc(l.result)}</p><p class="takeaway">${esc(l.takeaway)}</p><div class="actions">${btn("ANLADIM","lesson-ack","primary")}</div>`;'''+s[b:]
a=s.index('function contextIds()');b=s.index('function goalCard()',a)
s=s[:a]+'''function contextIds() {
  if (view !== "market" || !db.active) return undefined;
  const s = db.active, room = s.originScene || "kitchen";
  const zone = s.originZone || activeOpportunity(s,room)?.id;
  marketContext = zone ? {room,zone} : null;
  const ps = zone ? solutions(room,zone,s.round).slice(0,3) : [];
  category = ps[0]?.category || "Su";
  return ps.map(p=>p.id);
}
'''+s[b:]
# Evaluate category before passing it to canvas.
s=s.replace('  world.show(view, db.active, category, marketPage, false, contextIds());','  const stockIds = contextIds();\n  world.show(view, db.active, category, 0, false, stockIds);')
# Keep learning only feedback after install; no duplicate verdict toast or combo overlay.
a=s.index('  announce(\n',s.index('async function installProduct'));b=s.index('\n}',a)
s=s[:a]+'  scheduleLesson();'+s[b:]
f.write_text(s,encoding='utf-8')
f=p/'src/model.ts';s=f.read_text(encoding='utf-8').replace('  originScene?: RoomId;','  originScene?: RoomId;\n  originZone?: string;');s=s.replace('(s.originScene === undefined || !!roomById(s.originScene)) &&','(s.originScene === undefined || !!roomById(s.originScene)) &&\n    (s.originZone === undefined || (!!s.originScene && roomById(s.originScene)?.zones.some(z => z.id === s.originZone))) &&');s=s.replace('Yeşil Kasa','Mevcut para').replace('Kasa bu ürüne yetmiyor','Mevcut para bu ürüne yetmiyor');f.write_text(s,encoding='utf-8')
# Moving rooms invalidates the old zone; the next market visit gets its new explicit zone.
f=p/'src/main.ts';s=f.read_text(encoding='utf-8').replace('room: id, originScene: id','room: id, originScene: id, originZone: undefined');f.write_text(s,encoding='utf-8')
f=p/'src/scene.ts';s=f.read_text(encoding='utf-8');s='import { activeOpportunity } from "./navigation";\n'+s;s=s.replace('    for (const z of r.zones) {','    const active = activeOpportunity(s,r.id);\n    for (const z of r.zones.filter(z => z.id === active?.id)) {');f.write_text(s,encoding='utf-8')
f=p/'src/style.css';f.write_text(f.read_text(encoding='utf-8')+'''
/* Focused room flow: one money figure, one task, one problem. */
.simple-hud { align-items:center; }
.simple-hud .meters { margin-left:0; }
.simple-hud .hud-brand { min-width:80px; padding:8px 13px; box-shadow:none; }
.simple-hud .hud-brand small { margin:0 0 3px; }
.simple-hud .meter { min-width:100px; padding:8px 13px; box-shadow:none; }
.simple-hud .meter strong { font-size:26px; }
.simple-hud .sound-toggle { margin-left:auto; }
.simple-hud .sound-toggle, .simple-hud .help-button { min-height:44px; padding:8px 12px; font-size:12px; }
.task-panel { max-width:280px; background:rgba(38,53,31,.92); border-radius:12px; padding:16px 20px; }
.task-panel h2 { font-size:28px; margin:0 0 12px; }
.task-panel small { color:#e2cc95; font-size:12px; }
.task-panel ul { padding-left:17px; margin:8px 0 0; font-size:14px; line-height:1.5; }
.task-panel li + li { margin-top:5px; }
.contextual-action { background:transparent; padding:0; max-width:560px; }
.contextual-action p { background:rgba(38,53,31,.93); border-radius:8px; padding:10px 16px; font-size:14px; }
.contextual-action .actions { justify-content:center; margin:0; gap:14px; }
.contextual-action .primary { min-width:220px; }
.contextual-action .quiet-end { font-size:12px; min-height:44px; background:#303729ed; }
#learning-dialog { max-width:480px; }
#learning-dialog .lesson-art { width:76px; height:76px; }
#learning-dialog .lesson-top h2 { font-size:24px; }
@media (max-width:1100px) {
  .task-panel { max-width:225px; padding:12px 15px; }
  .task-panel h2 { font-size:23px; }
  .task-panel ul { font-size:12px; }
  .simple-hud .meter strong { font-size:23px; }
}
''',encoding='utf-8')
