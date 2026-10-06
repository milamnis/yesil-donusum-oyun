from pathlib import Path
p=Path('src/main.ts');s=p.read_text(encoding='utf-8');s='import { opportunities as decisionOpportunities, nextOpportunity, zoneFor, copy as decisionCopy, recordChoice, sortItem, skipOptional } from "./decisions";\n'+s
s=s.replace('MEVCUT PARA','KALAN PARA')
s=s.replace('const s = start(team, db.results, organizations);','const s: State = { ...start(team, db.results, organizations), decisionVersion: 1, decisions: [], sorting: {} };')
s=s.replace('tutorial: false, room: "kitchen"','tutorial: false, room: "map"').replace('switchView("room");\n      break;\n    case "help":','switchView("map");\n      break;\n    case "help":')
s=s.replace('const rs = ranking(db.results),','const rs = ranking(db.results.filter(r=>r.rulesVersion===1)),')
s=s.replace('const next = install(s, id, s.room as RoomId, zone);','const next = install(s, id, s.room as RoomId, zone);\n    if(s.decisionVersion===1) return recordChoice(next,id);')
s=s.replace('const ps = zone ? solutions(room, zone, s.round).slice(0, 3) : [];','const op = decisionOpportunities.find(o=>zoneFor(o)===zone);\n  const ps = s.decisionVersion===1 ? (op?.choices||[]).map(productById).filter(Boolean) : zone ? solutions(room, zone, s.round).slice(0, 3) : [];')
s=s.replace('  switch (kind) {','''  switch (kind) {
    case "decision": openDecision(arg); break;
    case "choose": {
      const before=structuredClone(db.active!);
      await mutate(s=>recordChoice(s,arg));
      closeModal(); render(); animateMeters(before);
      decisionSound(db.active!.lessons!.at(-1)!.tone); scheduleLesson(); break;
    }
    case "optional-skip": await mutate(s=>skipOptional(s,arg)); closeModal();render();break;
    case "sort-select": selectedSortItem=arg; openDecision(activeSort);break;
    case "sort-target": {
      if(!selectedSortItem){announce("Önce bir nesne seç.");break;}
      const o=decisionOpportunities.find(o=>o.id===activeSort)!;
      const correct=o.items!.find(i=>i.id===selectedSortItem)!.target===arg;
      const before=structuredClone(db.active!);
      await mutate(s=>sortItem(s,activeSort,selectedSortItem,arg));
      if(correct)selectedSortItem='';
      announce(correct?'Yerine kondu.':'Bu nesne buraya uygun değil. Yeniden dene.',!correct);
      if(db.active!.decisions?.some(d=>d.opportunityId===activeSort)){closeModal();render();animateMeters(before);scheduleLesson();}
      else openDecision(activeSort);break;
    }''',1)
s=s.replace('const [room, zone] = arg.split(":");\n      marketContext', '''const [room, zone] = arg.split(":");
      const op=decisionOpportunities.find(o=>zoneFor(o)===zone);
      if(db.active!.decisionVersion===1 && op && op.kind!=='product'){openDecision(op.id);break;}
      marketContext''')
s=s.replace('      label = "ÇÖZÜM ARA";','      label = s.decisionVersion===1 && nextOpportunity(s,r.id)?.kind!=="product" ? "BAŞLA" : "ÇÖZÜM ARA";')
s=s.replace('      hint = "";\n    } else {','''      hint = "";
      const op=nextOpportunity(s,r.id);
      if(s.decisionVersion===1&&op&&!op.core) secondary=btn("Şimdilik geç",`optional-skip:${op.id}`,"ghost");
    } else {''',1)
s=s.replace(' : "Bir çözüm seç ve yerine koy."',' : s.decisionVersion===1 ? "Birlikte karar verin." : "Bir çözüm seç ve yerine koy."')
s=s.replace('${art(l.asset, "lesson-art")}','${l.asset ? art(l.asset, "lesson-art") : ""}')
s=s.replace('<p class="takeaway">${esc(l.takeaway)}</p>','${l.takeaway ? `<p class="takeaway">${esc(l.takeaway)}</p>` : ""}')
s=s.replace('<p class="eyebrow">BİR KÜÇÜK ADIM</p>','<p class="eyebrow">SEÇİMİN SONUCU</p>')
s=s.replace('Bütçeni akıllıca kullan ve aylık gideri mümkün olduğunca düşür.','Seçimlerini yap; sonuçlarını gör ve puanını topla.')
s=s.replace('Düşün, birlikte karar ver; fikri yanına al.','Her karar bir kez puanlanır. Aynı kararlar aynı puanı getirir.')
s+='''
let selectedSortItem = '', activeSort = '';
function openDecision(id:string){
 const o=decisionOpportunities.find(o=>o.id===id); if(!o)return;
 if(o.kind==='sorting'){
  if(activeSort!==id) selectedSortItem=''; activeSort=id;
  const placed=db.active!.sorting?.[id]?.placed||[];
  showModal(`<p class="eyebrow">${esc(roomById(o.roomId).name)} · ${placed.length} / ${o.items!.length}</p><h2 id="dialog-title">${esc(o.title)}</h2><p>${esc(o.scenario)}</p><p class="sort-instruction">${selectedSortItem?'Şimdi uygun yeri seç.':'Önce bir nesneye dokun.'}</p><div class="sorting-items">${o.items!.filter(i=>!placed.includes(i.id)).map(i=>btn(`${art(i.asset)}<span>${esc(i.title)}</span>`,`sort-select:${i.id}`,`sorting-piece ${selectedSortItem===i.id?'selected':''}`,`aria-pressed="${selectedSortItem===i.id}"`)).join('')}</div><div class="sorting-targets">${o.targets!.map(t=>btn(`${art(t.asset)}<span>${esc(t.title)}</span>`,`sort-target:${t.id}`,'sorting-target')).join('')}</div>${btn('Ara ver','close','ghost')}`);
  dialog.classList.add('sorting-dialog');
 }else{
  showModal(`<p class="eyebrow">${esc(roomById(o.roomId).name)}</p><h2 id="dialog-title">${esc(o.title)}</h2><p>${esc(o.scenario)}</p><div class="decision-options">${o.choices.map((id,i)=>btn(`${o.kind==='load'?`<span class="load-drum" style="--fill:${[25,50,80][i]}%" aria-hidden="true"></span>`:''}<b>${esc(decisionCopy[id].title)}</b><span>${esc(decisionCopy[id].shortDescription)}</span>`,`choose:${id}`,'decision-option')).join('')}</div>${btn('Bir daha bak','close','ghost')}`);
 }
}
'''
p.write_text(s,encoding='utf-8')
