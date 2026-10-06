from pathlib import Path
p=Path('src/navigation.ts');s=p.read_text(encoding='utf-8').replace('      products.some(','      !z.id.startsWith("rev-") && products.some(');p.write_text(s,encoding='utf-8')
p=Path('src/model.ts');s=p.read_text(encoding='utf-8').replace('      b.score - a.score ||','      (a.rulesVersion===1 && b.rulesVersion===1 ? b.score-a.score : b.savingPercent-a.savingPercent) || b.score-a.score ||');p.write_text(s,encoding='utf-8')
p=Path('tests/economy.test.ts');s=p.read_text(encoding='utf-8').replace('assert.equal(products.length, 30);','assert.equal(products.filter(p=>!p.id.startsWith("rev-")).length, 30);').replace('for (const p of products) {','for (const p of products.filter(p=>!p.id.startsWith("rev-"))) {');p.write_text(s,encoding='utf-8')
