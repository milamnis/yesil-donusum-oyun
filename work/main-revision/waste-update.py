from pathlib import Path
p=Path('src/scene.ts');s=p.read_text(encoding='utf-8');s='import { kitchenWasteAssets, renderKitchenWaste } from "./kitchen-waste";\n'+s;s=s.replace('    Object.values(placements).forEach','    kitchenWasteAssets.forEach(k=>keys.add(k));\n    Object.values(placements).forEach');s=s.replace('      state?.actions.join(","),','      state?.actions.join(","),\n      state?.sorting?.["waste-sort"]?.placed.join(","),');s=s.replace('    renderPlaced(this, s, r.id);','    renderPlaced(this, s, r.id);\n    if(r.id==="kitchen") renderKitchenWaste(this,s);');p.write_text(s,encoding='utf-8')
p=Path('src/main.ts');s=p.read_text(encoding='utf-8');s='import { wasteItemOrder, wasteTargetOrder } from "./kitchen-waste";\n'+s;s=s.replace('      } else openDecision(activeSort);','      } else {render();openDecision(activeSort);}')
s=s.replace('    const placed = db.active!.sorting?.[id]?.placed || [];','''    const placed = db.active!.sorting?.[id]?.placed || [];
    const waste=id==='waste-sort';
    const items=waste?wasteItemOrder.map(id=>o.items!.find(i=>i.id===id)!):o.items!;
    const targets=waste?wasteTargetOrder.map(id=>o.targets!.find(t=>t.id===id)!):o.targets!;''')
s=s.replace('${o\n        .items!.filter((i) => !placed.includes(i.id))','${items\n        .filter((i) => !placed.includes(i.id))')
s=s.replace('`aria-pressed="${selectedSortItem === i.id}"`,','`aria-pressed="${selectedSortItem === i.id}" data-waste="${i.id}"`,')
s=s.replace('${o.targets!.map((t) => btn(', '${targets.map((t) => btn(')
s=s.replace('    dialog.classList.add("sorting-dialog");','    dialog.classList.add("sorting-dialog");\n    if(waste)dialog.classList.add("waste-sorting-dialog");')
p.write_text(s,encoding='utf-8')
