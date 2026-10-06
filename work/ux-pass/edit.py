from pathlib import Path
p=Path('outputs/yesil-donusum')
f=p/'src/main.ts'; s=f.read_text(encoding='utf-8')
s='import { returnLabels, roomLocatives, offeredProduct } from "./navigation";\n'+s
s=s.replace('let marketContext:', 'let continueReady = false;\nlet marketContext:')
s=s.replace('Yeşil Kasa', 'Kasa').replace('YEŞİL KASA','KASA').replace('Bu ürünü alırsanız kasada kalır','Kalan').replace('Şu an Kasa','Kasa')
a=s.index('  purchaseReceipt.innerHTML ='); b=s.index('\n  receiptTimer =',a)
s=s[:a]+'''  purchaseReceipt.innerHTML = `${art(p.asset)}<div><b>Çantana eklendi.</b><p>${roomLocatives[p.room]} yerine koyabilirsin.</p></div>`;'''+s[b:]
s=s.replace(".querySelector('[data-action=\"inventory\"]')", ".querySelector('.contextual-action .primary')")
a=s.index('function footer()'); b=s.index('function inventory()',a)
s=s[:a]+'''function readyProduct() {
  const s = db.active!;
  return s.inventory.map(productById).find((p) => p.room === s.room && offeredProduct(p));
}
function footer() {
  const s = db.active!;
  let label = "DÖNEMİ BİTİR", action = "end", hint = "Hazır olduğunuzda dönemin sonucuna bakın.";
  if (view === "market") {
    const origin = s.originScene || marketContext?.room || "kitchen";
    label = returnLabels[origin]; action = `take:${origin}`;
    hint = s.inventory.some((id) => productById(id).room === origin)
      ? `${roomLocatives[origin]} yerine koyabilirsin.` : "Bir ürüne dokunup inceleyebilirsin.";
  } else if (view === "room") {
    const p = readyProduct();
    const r = roomById(s.room as RoomId);
    const z = r.zones.find((z) => !zoneResolved(s, r.id, z.id) && solutions(r.id, z.id, s.round).some((p) => !s.installed.includes(p.id)));
    if (p) { label = "YERLEŞTİR"; action = "place-ready"; hint = `${p.name} yerine koyulmaya hazır.`; }
    else if (continueReady || !z) { label = "DEVAM ET"; action = "continue-room"; hint = "Bir sonraki fırsata bakabilirsin."; }
    else { label = "ÇÖZÜM ARA"; action = `solve:${r.id}:${z.id}`; hint = z.problem; }
  } else {
    const next = rooms.find((r) => r.id !== "waste" && r.round <= s.round && r.zones.some((z) => !zoneResolved(s, r.id, z.id) && solutions(r.id,z.id,s.round).some((p) => !s.installed.includes(p.id))));
    if (next) { label = "DEVAM ET"; action = `room:${next.id}`; hint = `${next.name} içinde bir fırsata bakalım.`; }
  }
  return `<nav class="nav-footer contextual-footer" aria-label="Sonraki adım">${view !== "map" ? btn("← Yerleşke", "map", "ghost compact-back") : btn("Mola ver", "pause", "ghost compact-back")}<div class="contextual-action"><p>${esc(hint)}</p>${btn(label, action, "primary")}</div></nav>`;
}
'''+s[b:]
s=s.replace('${rooms.map((r)', '${rooms.filter((r) => r.id !== "waste").map((r)')
s=s.replace('${hud()}${goalCard()}${sceneIdea(r.id)}', '${hud()}')
a=s.index('${selectedProduct ? `<div class="selection-bar">');b=s.index('\n}',a)
s=s[:a]+'`;'+s[b:]
s=s.replace('(p) => p.category === category && roomById(p.room).round <= s.round,','(p) => offeredProduct(p) && p.category === category && roomById(p.room).round <= s.round,')
s=s.replace('btn("TÜM MARKETE BAK", "all-market", "gold") + btn("Fırsata dön", `room:${marketContext.room}`, "ghost")','btn("Diğer raflar", "all-market", "ghost")')
s=s.replace('  switchView("room");\n}\nasync function installProduct', '  continueReady = false;\n  switchView("room");\n}\nasync function installProduct')
s=s.replace('    case "money-info":', '''    case "place-ready": {
      const p = readyProduct();
      if (p) await installProduct(p.id, p.zone);
      break;
    }
    case "continue-room":
      continueReady = false;
      await action("map");
      break;
    case "money-info":''')
s=s.replace('${btn("DEVAM EDELİM", "close", "primary")}', '${btn("DEVAM EDELİM", "close", "primary")}<div class="secondary-tools">${btn("Parasız fikir", "free", "ghost")}${btn("Fikir Çantam", "memory", "ghost")}${btn("Dönemi bitir", "end", "ghost")}</div>')
s=s.replace('case "market":\n      marketContext', 'case "market":\n      marketContext')
old='await mutate((s) => ({ ...s, room: "market" }));'
s=s.replace(old, 'await mutate((s) => ({ ...s, originScene: s.room !== "map" && s.room !== "market" ? s.room : s.originScene || "kitchen", room: "market" }));',1)
s=s.replace(old, 'await mutate((s) => ({ ...s, originScene: room as RoomId, room: "market" }));',1)
s=s.replace('      learningDialog.close();\n      activeLesson', '      learningDialog.close();\n      continueReady = true;\n      activeLesson')
s=s.replace('.querySelector<HTMLButtonElement>("[data-action=memory]")', '.querySelector<HTMLButtonElement>(".contextual-action .primary")')
s=s.replace('      inventoryOpen = true;\n      render();\n      break;\n    case "inventory":', '      render();\n      break;\n    case "inventory":')
s=s.replace('      await mutate((s) => purchase(s, arg));', '      await mutate((s) => ({ ...purchase(s, arg), originScene: p.room }));')
s=s.replace('      const relevant = solutions(marketContext.room, zone, db.active!.round);','      await mutate((s) => discover(s, room as RoomId, zone));\n      const relevant = solutions(marketContext.room, zone, db.active!.round);')
s=s.replace('    case "room":\n      await goRoom', '    case "room":\n      closeModal();\n      await goRoom')
f.write_text(s,encoding='utf-8')
f=p/'src/model.ts'; s=f.read_text(encoding='utf-8').replace('  tutorial: boolean;', '  tutorial: boolean;\n  originScene?: RoomId;');f.write_text(s,encoding='utf-8')
f=p/'src/data.ts'; s=f.read_text(encoding='utf-8').replace('name: "Yaşam alanı"','name: "Oturma odası"').replace('name: "Atölye / ofis"','name: "Ofis"');f.write_text(s,encoding='utf-8')
for name in ['journey.ts','scene.ts']:
 f=p/'src'/name; s=f.read_text(encoding='utf-8'); s='import { offeredProduct } from "./navigation";\n'+s
 if name=='journey.ts': s=s.replace('p.room === room && p.zone === zone', 'offeredProduct(p) && p.room === room && p.zone === zone')
 else:
  s=s.replace('rooms.forEach((r) => {\n        if (state', 'rooms.filter((r) => r.id !== "waste").forEach((r) => {\n        if (state')
  s=s.replace('(ids ? ids.includes(p.id)', 'offeredProduct(p) && (ids ? ids.includes(p.id)')
 f.write_text(s,encoding='utf-8')
f=p/'src/style.css'; f.write_text(f.read_text(encoding='utf-8')+'''
/* One next step, shared by every room and the shop. */
.contextual-footer { justify-content: center; align-items: end; }
.contextual-footer .compact-back { position: absolute; left: 0; bottom: 0; }
.contextual-action { text-align: center; max-width: 520px; padding: 12px 24px; border-radius: 14px; background: rgba(35,48,29,.93); }
.contextual-action p { margin: 0 0 10px; color: #fff3d8; font-size: 15px; }
.contextual-action .primary { min-width: 240px; min-height: 54px; }
.secondary-tools { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 24px; }
.contextual-footer ~ .selection-bar { display:none; }
@media (max-width: 1100px) { .contextual-action { max-width: 420px; padding: 10px 16px; } .contextual-action p { font-size: 13px; } }
''',encoding='utf-8')
