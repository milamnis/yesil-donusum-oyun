from pathlib import Path
p=Path('tests/economy.test.ts');s=p.read_text(encoding='utf-8-sig').replace(',-old.impact)',',-old.impact || 0)');p.write_text(s,encoding='utf-8')
p=Path('src/main.ts');s=p.read_text(encoding='utf-8-sig')
s='import { INITIAL_BILL, INITIAL_BUDGET, LARGE_PURCHASE_SHARE, fmtMoney, signedMoney, SIMULATION_NOTE } from "./economy";\n'+s
# Format every monetary expression, leaving counts / percentages / scores alone.
for expr in ['s.bill','s.budget','p.price','h.before','h.after','h.saving','h.reward','m.impact','l.billImpact','l.spent','l.comboImpact','to - from']:
 s=s.replace('fmt('+expr+')','fmtMoney('+expr+')')
s=s.replace('1000 - s.bill','INITIAL_BILL - s.bill').replace('1000 - before.bill','INITIAL_BILL - before.bill').replace('fmt(INITIAL_BILL - s.bill)','fmtMoney(INITIAL_BILL - s.bill)')
s=s.replace('<strong>1.000</strong>','<strong>${fmtMoney(INITIAL_BILL)}</strong>').replace('<small>ŞİMDİ</small>','<small>ŞİMDİ · AYLIK GİDER</small>').replace('<small>TASARRUF</small>','<small>CEBİNDE KALAN</small>')
s=s.replace('${p.price} kredi','${fmtMoney(p.price)}').replace('${fmtMoney(p.price)} kredi','${fmtMoney(p.price)}')
s=s.replace('el.textContent = fmt(','el.textContent = fmtMoney(').replace(' : 1000,',' : INITIAL_BILL,')
s=s.replace('Başlangıç faturası 1.000','Başlangıç gideri ${fmtMoney(INITIAL_BILL)}')
s=s.replace('s.moves.some((m) => m.room === r.id && m.impact < 0)','r.zones.some(z=>zoneResolved(s,r.id,z.id))')
s=s.replace('<h2>${r.name}</h2><p>${selectedProduct','<h2>${r.name}</h2>${opportunities(r.id)}<p>${selectedProduct')
s=s.replace('btn("Soruna dön"','btn("Fırsata dön"')
s=s.replace('${marketContext ? "Aynı ihtiyaca farklı cevaplar. Hangisini seçersiniz?" : "Raftan bir ürün seçin. Özelliğini inceleyin."}</div>', '${marketContext ? "Aynı ihtiyaca farklı cevaplar. Hangisini seçersiniz?" : "Raftan bir ürün seçin. Özelliğini inceleyin."}${btn("Tutarlar hakkında", "money-info", "market-info")}</div>')
# Summary owner, compact physical recap.
a=s.index('function summaryScreen()');b=s.index('\nfunction awards()',a)
s=s[:a]+'''function summaryScreen() {
 const s=db.active!, h=s.history.at(-1)!;
 const changes=s.moves.filter(m=>m.round===s.round);
 return `<section class="summary-screen period-result"><p class="eyebrow">DÖNEM ${s.round} TAMAMLANDI</p><h2>${roundNames[s.round-1]}</h2><div class="bill-journey"><div><small>ÖNCE</small><span class="before">${fmtMoney(h.before)}</span></div><span aria-hidden="true">→</span><div><small>ŞİMDİ</small><strong class="big-number" id="result-bill">${fmtMoney(h.after)}</strong></div></div><div class="period-totals"><p><small>BU DÖNEM CEBİNDE KALAN</small><b id="result-saving">${fmtMoney(h.saving)}</b></p><p><small>YEŞİL KASA’YA GERİ DÖNEN</small><b id="result-reward">${signedMoney(h.reward)}</b></p></div>${h.after>h.before?'<p class="subtle">Bu dönem gider yükseldi. Seçiminizi sonradan değiştirebilirsiniz.</p>':''}<p class="period-goals">3 fırsattan ${miniGoals(s).filter(g=>g.done).length}’si tamamlandı.</p>${changes.length?`<div class="round-recap" aria-label="Bu dönem değiştirdikleriniz">${changes.slice(0,6).map(m=>{const a=productById(m.id)??freeActions.find(a=>a.id===m.id)!;return `<figure>${art(a.asset)}<figcaption>${esc(m.name)}${m.replacedBy?' · Değiştirildi':''}</figcaption></figure>`}).join('')}${changes.length>6?`<span>+${changes.length-6} hamle</span>`:''}</div>`:''}<div class="period-idea"><span class="eyebrow">BU DÖNEMİN FİKRİ</span><p>“${esc(roundIdea(s))}”</p></div>${btn(s.round===4?'BÜYÜK FİNALE GEÇ →':`${s.round+1}. DÖNEME GEÇ →`,'continue','gold')}</section>`;
}''' +s[b:]
s=s.replace('.filter((m) => m.impact < 0)','.filter((m) => !m.replacedBy && m.impact < 0)').replace('.filter((m) => m.cost > 0 && m.impact < 0)','.filter((m) => !m.replacedBy && m.cost > 0 && m.impact < 0)')
s=s.replace('EN GÜÇLÜ HAMLEMİZ','EN GÜÇLÜ HAMLENİZ').replace('EN AKILLI YATIRIMIMIZ','EN AKILLI BÜTÇE KARARINIZ').replace('>BİR SONRAKİ SEFER<','>BİR SONRAKİ SEFER DÜŞÜNEBİLECEĞİNİZ<')
s=s.replace('${bad ? esc(bad.name)', '${s.replacedInstallations.length ? "Bir kararınızı sonradan değiştirdiniz." : bad ? esc(bad.name)')
s=s.replace('<span>1.000 <span','<span>${fmtMoney(INITIAL_BILL)} <span').replace('FİNAL FATURA','FİNAL AYLIK GİDER').replace('pct >= 0 ? "TASARRUF" : "ARTIŞ"','pct >= 0 ? "DAHA AZ GİDER" : "DAHA FAZLA GİDER"')
s=s.replace('Resmî sonuç bu cihazın liderlik tablosuna kaydedildi."}</p></section>`;', 'Resmî sonuç bu cihazın liderlik tablosuna kaydedildi."}</p><p class="simulation-note">Bu oyundaki TL tutarları karşılaştırma için hazırlanmış örnek değerlerdir. Gerçek ürün fiyatı ve tasarruf kullanım koşullarına göre değişir.</p></section>`;')
# Neutral pre-purchase owner: no kind, impact or feedback.
a=s.index('async function productDetail(');b=s.index('\nasync function goRoom',a)
s=s[:a]+'''async function productDetail(id: string) {
 const p=productById(id),s=db.active!; if(!p)return;
 await mutate(s=>consider(s,id));render();
 const owned=s.inventory.includes(id)||s.installed.includes(id), affordable=s.budget>=p.price;
 const remaining=s.budget-p.price,large=p.price>s.budget*LARGE_PURCHASE_SHARE;
 showModal(`<p class="eyebrow">YEŞİL MARKET · ${esc(p.category)}</p>${art(p.asset,'product-art')}<h2 id="dialog-title">${esc(p.name)}</h2><p class="product-feature">${esc(p.feature)}</p><p class="product-use">${esc(p.description)}</p><dl class="purchase-math"><div><dt>Fiyat</dt><dd>${fmtMoney(p.price)}</dd></div><div><dt>Şu an Yeşil Kasa</dt><dd>${fmtMoney(s.budget)}</dd></div><div class="remaining"><dt>${affordable?'Bu ürünü alırsanız kasada kalır':'Bu ürün için eksik'}</dt><dd id="purchase-remaining">${fmtMoney(affordable?remaining:-remaining)}</dd></div></dl>${!owned&&!affordable?'<p class="error">Yeşil Kasa bu ürüne yetmiyor.</p>':!owned&&large?'<p class="budget-question">Bu büyük bir harcama. Birlikte karar verin.</p>':''}<div class="actions">${btn(large?'BİR DAHA BAKALIM':'BİR DAHA BAK','close','ghost')}${btn(owned?'Zaten sizde':'ALALIM',`buy:${id}`,'primary',owned||!affordable?'disabled':'')}</div>`);
 dialog.classList.add('product-dialog');
}''' +s[b:]
# Installation education separates removed impact from combo.
s=s.replace('next.bill - s.bill,\n          !p.requires || s.installed.includes(p.requires),','next.bill - s.bill,\n          !p.requires || s.activeInstallations.includes(p.requires),\n          next.moves.at(-1)!.reversalImpact ?? 0,')
s=s.replace('    id === "meter" && db.active!.bill !== before.bill','    db.active!.moves.at(-1)?.reversalImpact !== undefined\n      ? "Seçiminizi değiştirdiniz. Önceki harcama kasaya dönmez."\n      : id === "meter" && db.active!.bill !== before.bill')
# Purchase receipt is non-modal, short; permanent inventory provides later navigation.
a=s.index('    case "buy":');b=s.index('\n    case "take":',a)
s=s[:a]+'''    case "buy":
    case "buy-confirm": {
      const before=structuredClone(db.active!),p=productById(arg);
      const source=document.querySelector(`[data-action="product:${arg}"]`)?.getBoundingClientRect();
      await mutate(s=>purchase(s,arg));closeModal();render();animateMeters(before);
      purchaseAnimation(p.id,source);cueSound('purchase');
      showReceipt(p.id);
      if(!(before.budgetMoments||[]).includes(before.round)&&(db.active!.budgetMoments||[]).includes(before.round)) showBudgetMoment();
      break;
    }''' +s[b:]
s=s.replace('    case "take":\n      closeModal();','    case "take":\n      hideReceipt();\n      closeModal();')
s=s.replace('for (const root of [ui, dialog, learningDialog])','for (const root of [ui, dialog, learningDialog, gentleOverlay, purchaseReceipt])')
s=s.replace('  switch (kind) {','''  switch (kind) {
    case "money-info": showModal(`<h2 id="dialog-title">Oyundaki tutarlar</h2><p>${SIMULATION_NOTE}</p>${btn('ANLADIM','close','primary')}`);break;
    case "receipt-close": hideReceipt();break;
    case "idle-hint": gentleOverlay.innerHTML='<p>Bu odadaki parlayan noktalara bir göz atın.</p>';window.setTimeout(()=>gentleOverlay.replaceChildren(),6000);break;''')
s=s.replace('  marketSelected = "";\n  clearTimeout(comboTimer);','  marketSelected = "";\n  hideReceipt();\n  resetIdle();\n  clearTimeout(comboTimer);')
s=s.replace('Oyun faturası <b>','Aylık gider etkisi <b>')
s=s.replace('${l.comboImpact ? `<span>Birlikte etki', '${l.replacementImpact ? `<span>Önceki etki kaldırıldı <b>${signedMoney(l.replacementImpact)}</b></span>` : ""}${l.comboImpact ? `<span>Birlikte etki')
s=s.replace('PARA HARCAMADAN DA OLABİLİR','PARASIZ FİKİR').replace('"BU HAMLEYİ YAP"','"BUNU YAPALIM"')
s=s.replace('İki doğru adımı bir araya getirdiniz.','İki hamle birbirini tamamladı.').replace('Ek tasarruf kazandınız · +${earned.reduce((n, c) => n + c.bonus, 0)}','Ek kazanç · ${fmtMoney(-earned.reduce((n, c) => n + c.bonus, 0))}')
s=s.replace('2700','3000')
# Copy in intros/start uses aggregate monthly expense.
s=s.replace('Faturanı düşür.','Aylık gideri düşür.').replace('faturayı mümkün olduğunca düşür.','aylık gideri mümkün olduğunca düşür.')
# Restore missing mini-goal cue using existing owner.
pos=s.index('\n}\nwindow.addEventListener("storage"',s.index('async function mutate'))
s=s[:pos]+'''
  goalFlash=db.active?.phase==='playing'?miniGoals(db.active).filter(g=>g.done&&!before.includes(g.id)).map(g=>g.id):[];
  if(goalFlash.length)cueSound('goal');'''+s[pos:]
# Result amount counters all three, cancellable when detached.
a=s.index('function animateResult()');b=s.index('\nfunction attachPledges()',a)
s=s[:a]+'''function animateResult() {
 const s=db.active!;if(reduced())return;
 const values: [string,number,number,boolean][]=[['result-bill',view==='summary'?s.history.at(-1)!.before:INITIAL_BILL,s.bill,false]];
 if(view==='summary'){const h=s.history.at(-1)!;values.push(['result-saving',0,h.saving,false],['result-reward',0,h.reward,true]);}
 for(const [id,from,to,signed] of values){const el=document.getElementById(id);if(!el)continue;const began=performance.now();
 const frame=(now:number)=>{const t=Math.min(1,(now-began)/1100);el.textContent=(signed?signedMoney:fmtMoney)(Math.round(from+(to-from)*(1-(1-t)**3)));if(t<1&&el.isConnected)requestAnimationFrame(frame)};requestAnimationFrame(frame);}
}''' +s[b:]
# Setup below imports but before first load/render; declarations must exist before callbacks.
a=s.index('function announce(')
s=s[:a]+'''const gentleOverlay=document.createElement('aside');gentleOverlay.id='gentle-hint';gentleOverlay.setAttribute('aria-live','polite');document.body.append(gentleOverlay);
const purchaseReceipt=document.createElement('aside');purchaseReceipt.id='purchase-receipt';purchaseReceipt.setAttribute('aria-label','Satın alma');document.body.append(purchaseReceipt);
const budgetThought=document.createElement('aside');budgetThought.id='budget-thought';budgetThought.setAttribute('role','status');document.body.append(budgetThought);
let idleTimer=0,receiptTimer=0,budgetTimer=0;
const idleShown=new Set<string>();
function resetIdle(){clearTimeout(idleTimer);gentleOverlay.replaceChildren();idleTimer=window.setTimeout(()=>{
 const s=db.active;if(!s||s.phase!=='playing'||view!=='room'||dialog.open||learningDialog.open||inventoryOpen||document.hidden)return;
 const key=`${s.id}:${s.round}:${s.room}`;if(idleShown.has(key))return;idleShown.add(key);
 gentleOverlay.innerHTML=`<p>Bir yerde takıldınız mı?</p>${btn('KÜÇÜK BİR İPUCU','idle-hint','ghost')}`;
},40000);}
window.addEventListener('pointerdown',e=>{if(!gentleOverlay.contains(e.target as Node))resetIdle()});
window.addEventListener('keydown',e=>{if(!gentleOverlay.contains(e.target as Node))resetIdle()});
function hideReceipt(){clearTimeout(receiptTimer);purchaseReceipt.replaceChildren();}
function showReceipt(id:string){const p=productById(id);hideReceipt();purchaseReceipt.innerHTML=`${art(p.asset)}<div><b>Çantana eklendi.</b><p>${esc(roomById(p.room).name)} alanında kullanabilirsin.</p></div>${btn('MEKÂNA GİT →',`take:${p.room}`,'primary')}${btn('×','receipt-close','ghost','aria-label="Satın alma bilgisini kapat"')}`;receiptTimer=window.setTimeout(()=>{if(purchaseReceipt.contains(document.activeElement)){receiptTimer=window.setTimeout(hideReceipt,4000)}else hideReceipt()},3000);}
function purchaseAnimation(id:string,source?:DOMRect){if(reduced())return;const target=document.querySelector('[data-action="inventory"]')?.getBoundingClientRect();if(!source||!target)return;const img=document.createElement('img');img.src=asset(productById(id).asset);img.alt='';img.className='purchase-flight';document.body.append(img);img.style.left=`${source.x+source.width/2-35}px`;img.style.top=`${source.y+source.height/2-35}px`;const anim=img.animate([{transform:'scale(1)',opacity:1},{transform:'scale(1.2)',opacity:1,offset:.2},{transform:`translate(${target.x-source.x}px,${target.y-source.y}px) scale(.3)`,opacity:0}],{duration:700,easing:'ease-in-out'});anim.onfinish=()=>img.remove();}
function showBudgetMoment(){clearTimeout(budgetTimer);budgetThought.innerHTML=`<p>Yeşil Kasa’da <b>${fmtMoney(db.active!.budget)}</b> kaldı.</p><p>Bir büyük yatırım mı,<br/>birkaç küçük dokunuş mu?</p>`;budgetTimer=window.setTimeout(()=>budgetThought.replaceChildren(),7000);}
function opportunities(room:RoomId){const s=db.active!,r=roomById(room),done=r.zones.filter(z=>zoneResolved(s,room,z.id)).length;return `<div class="opportunities"><span>${r.zones.length} fırsat · ${done} tamamlandı</span><span aria-hidden="true">${r.zones.map(z=>zoneResolved(s,room,z.id)?'✓':'●').join(' ')}</span>${done===r.zones.length?'<small>Bu alanı güzel toparladınız.</small>':''}</div>`;}

''' +s[a:]
p.write_text(s,encoding='utf-8')
p=Path('src/model.ts');s=p.read_text(encoding='utf-8-sig');s=s.replace('return { ...s, budget: s.budget - p.price, inventory: [...s.inventory, id] };','''const budget=s.budget-p.price;
  const budgetMoments=s.budgetMoments||[];
  return { ...s, budget, inventory: [...s.inventory, id],budgetMoments:budget<=INITIAL_BUDGET*.36&&!budgetMoments.includes(s.round)?[...budgetMoments,s.round]:budgetMoments };''');p.write_text(s,encoding='utf-8')
p=Path('src/learning.ts');s=p.read_text(encoding='utf-8-sig').replace('  comboImpact: number;','  comboImpact: number;\n  replacementImpact?: number;')
s=s.replace('  hasRequirement: boolean,','  hasRequirement: boolean,\n  replacementImpact = 0,').replace('comboImpact: totalImpact - impact,','comboImpact: totalImpact - impact - replacementImpact,\n    replacementImpact,').replace('tone: impact < 0 ? "good" : impact > 0 ? "bad" : "neutral",','tone: totalImpact < 0 ? "good" : totalImpact > 0 ? "bad" : "neutral",')
s=s.replace('[l.billImpact, l.comboImpact, l.spent].every(Number.isFinite)','[l.billImpact, l.comboImpact, l.spent].every(Number.isFinite) &&\n    (l.replacementImpact===undefined||Number.isFinite(l.replacementImpact))')
s=s.replace('Aynı ihtiyacı daha verimli bir seçenekle karşıladın.','Bu LED ampulle aynı ihtiyacı daha az enerjiyle karşıladın.')
p.write_text(s,encoding='utf-8')
p=Path('src/scene.ts');s=p.read_text(encoding='utf-8-sig');s='import {signedMoney} from "./economy";\n'+s;s=s.replace('`${delta > 0 ? "+" : ""}${delta}`','signedMoney(delta)')
s=s.replace('.filter((k) => this.textures.exists(k))','.filter((k) => this.textures.exists(k) && !s.activeInstallations.some(id=>productById(id).asset===k))')
p.write_text(s,encoding='utf-8')
p=Path('src/sound.ts');s=p.read_text(encoding='utf-8-sig').replace('"goal" | "combo" | "round" | "final"','"goal" | "combo" | "round" | "final" | "purchase"').replace('    goal: [880],','    purchase: [660, 880],\n    goal: [880],');p.write_text(s,encoding='utf-8')
