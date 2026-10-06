from pathlib import Path
p=Path('src/model.ts');s=p.read_text(encoding='utf-8').replace('  decisionScore,','  decisionScore,\n  decisionLesson,');s=s.replace('? productLesson(p, m.impact, m.impact, m.impact !== 0 || !p.requires)','? p.id.startsWith("rev-") ? decisionLesson(p.id) : productLesson(p, m.impact, m.impact, m.impact !== 0 || !p.requires)');p.write_text(s,encoding='utf-8')
p=Path('tests/decisions.test.ts');s=p.read_text(encoding='utf-8').replace('  start,','  start,\n  migrateDatabase,');s+='''
test("new product learning history can be recovered without legacy copy lookup",()=>{const s=commit(fresh(),'rev-tap-repair');const repaired=migrateDatabase({...emptyDatabase(),active:{...s,lessons:[]}});assert.equal(repaired.active!.lessons![0].id,'rev-tap-repair');assert(validDatabase(repaired));});
''';p.write_text(s,encoding='utf-8')
