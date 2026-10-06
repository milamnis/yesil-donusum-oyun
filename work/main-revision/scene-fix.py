from pathlib import Path
p=Path('src/data.ts');s=p.read_text(encoding='utf-8').replace("effect:o.roomId==='bathroom'||o.id==='tap'?'water':'waste'","effect:o.id.startsWith('light-')?'energy':o.id==='shower'||o.id==='tap'?'water':'waste'");p.write_text(s,encoding='utf-8')
p=Path('src/scene.ts');s=p.read_text(encoding='utf-8').replace('      "sheet-03-1",','      "sprites/generated/bag-other",\n      "sheet-03-1",',1);s=s.replace('    for (const z of r.zones.filter((z) => z.id === active?.id)) {','''    if(s.decisionVersion===1&&r.id==='bathroom')this.add.image(800,655,'sprites/generated/bag-other').setOrigin(.5,.98).setScale(.14).setDepth(12);
    for (const z of r.zones.filter((z) => z.id === active?.id)) {
      if(s.decisionVersion===1&&!['rev-tap','rev-shower','rev-light-home','rev-light-workshop'].includes(z.id))continue;''');p.write_text(s,encoding='utf-8')
p=Path('src/placements.ts');s=p.read_text(encoding='utf-8');s+='''
problemSources.kitchen!['rev-tap']=[762,347];
problemSources.bathroom!['rev-shower']=[1108,110];
problemSources.home!['rev-light-home']=[815,76];
problemSources.workshop!['rev-light-workshop']=[854,134];
''';p.write_text(s,encoding='utf-8')
