exec(open('work/economy-revision.py',encoding='utf-8').read().split('ops=data')[0])
s=read('src/model.ts').replace('s.round === 3 && !s.salesIncomeGranted','s.round === 3 && s.decisionVersion === 1 && !s.salesIncomeGranted');write('src/model.ts',s)
s=read('tests/economy.test.ts').replace('score(continueRound(endRound(s))), 848','score(continueRound(endRound(s))), 839');write('tests/economy.test.ts',s)
s=read('tests/model.test.ts');s='import { marketPrice, existingFixture } from "../src/data/market-prices";\n'+s
s=s.replace('50% of new','25% of new').replace('s.budget, 2440','s.budget, 2395').replace('s.history[0].reward, 90','s.history[0].reward, 45').replace('360 + (235 + 9) * 2','360 + (235 + 4.5) * 2').replace('s.history[0].reward, 500','s.history[0].reward, 250').replace('next.history[1].reward, 150','next.history[1].reward, 75')
s=s.replace('    const next = put(s, p.id);','    if (existingFixture(p.id) || marketPrice(p.id)?.priceTL === null) { assert.throws(() => purchase(s,p.id)); continue; }\n    const next = put(s, p.id);')
write('tests/model.test.ts',s)
s=read('tests/save-compatibility.test.ts');s=s.replace('  assert(\n    !validDatabase({\n      ...emptyDatabase(),\n      active: recordChoice(s, "rev-tap-repair"),\n    }),\n  );','  assert.throws(() => recordChoice(s, "rev-tap-repair"), /yerleştir/);\n  assert(!validDatabase({...emptyDatabase(), active:{...s, decisions:[{opportunityId:"tap",choiceId:"rev-tap-repair",round:1}]}}));')
write('tests/save-compatibility.test.ts',s)
s=read('tests/decisions.test.ts');s='import { marketPrice, existingFixture } from "../src/data/market-prices";\n'+s
s=s.replace('o.kind === "product"\n      ?','o.kind === "product" && !existingFixture(id)\n      ?').replace('decisionProducts.length, 33','decisionProducts.length, 34').replace('s.decisions!.length, 21','s.decisions!.length, 22')
s=s.replace('          const candidate = valid(commit(s, id));','''          if (marketPrice(id)?.priceTL === null) {
            assert.throws(() => purchase(s,id), /fiyatı inceleniyor/);
            continue;
          }
          // Isolate consequence checks from real-price affordability.
          const candidate = valid(commit({...s,budget:20000}, id));''')
s=s.replace('const id = [...o.choices].sort(','const id = o.choices.filter(id => marketPrice(id)?.priceTL !== null).sort(')
write('tests/decisions.test.ts',s)
