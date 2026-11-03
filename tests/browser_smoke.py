"""Optional real Chromium checks. Runtime CodeAtlas needs no extra dependencies.

python -m pip install playwright
python tests/browser_smoke.py --chromium /usr/bin/chromium --output /tmp/codeatlas-qa \
    --benchmark /path/to/other/repo
"""
import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


def geometry(page):
    return page.evaluate('''() => {
      const svg=document.querySelector('#graph svg'), stage=svg.getBoundingClientRect();
      const labels=[...svg.querySelectorAll('.node-label')].map(e=>e.getBoundingClientRect());
      let overlaps=0;
      for(let i=0;i<labels.length;i++)for(let j=i+1;j<labels.length;j++){
        const a=labels[i],b=labels[j];
        if(a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top)overlaps++;
      }
      const points=[...svg.querySelectorAll('.node')].map(e=>{
        const t=e.transform.baseVal.getItem(0).matrix;
        const p=new DOMPoint(t.e,t.f).matrixTransform(e.parentNode.getScreenCTM());
        return {x:p.x,y:p.y};
      });
      return {renderedNodes:points.length,labels:labels.length,labelOverlaps:overlaps,
        pointsOutsideStage:points.filter(p=>p.x<stage.left||p.x>stage.right||p.y<stage.top||p.y>stage.bottom).length,
        horizontalOverflow:document.documentElement.scrollWidth>innerWidth};
    }''')


def run(args):
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='codeatlas-browser-') as temporary:
        empty = Path(temporary) / 'empty'
        empty.mkdir()
        log = (Path(temporary) / 'server.log').open('w+')
        server = subprocess.Popen([sys.executable, '-u', '-m', 'codeatlas.desktop', '--port', '0'], cwd=ROOT, stdout=log, stderr=log)
        try:
            address = None
            for _ in range(100):
                log.seek(0)
                for line in log.read().splitlines():
                    if line.startswith('CodeAtlas: '):
                        address = line.split(' ', 1)[1]
                if address:
                    break
                if server.poll() is not None:
                    raise RuntimeError('Desktop server failed to launch')
                time.sleep(.05)
            assert address, 'Desktop server did not start'
            with sync_playwright() as playwright:
                launch = {'headless': True, 'args': ['--no-sandbox']}
                if args.chromium:
                    launch['executable_path'] = args.chromium
                browser = playwright.chromium.launch(**launch)
                page = browser.new_page(viewport={'width':1440,'height':900}, device_scale_factor=1)
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.goto(address)
                expect(page.locator('#inspector')).to_contain_text('Ogni programma')
                page.screenshot(path=str(output/'welcome.png'))
                def open_project(path):
                    page.locator('#projectPath').fill(str(path))
                    page.locator('#openProject').click()
                    expect(page.locator('#status')).to_contain_text('nodi principali', timeout=30000)
                results=[]
                for path in [ROOT, *map(Path,args.benchmark)]:
                    open_project(path)
                    overview=geometry(page)
                    assert not overview['labelOverlaps'], overview
                    positions=page.evaluate("() => {const l=AtlasViews.functionalLayout(map,visible());return visible().map(n=>({role:AtlasViews.role(n),y:l.positions.get(n.id).y}));}")
                    caps=[n['y'] for n in positions if n['role']=='capability'];processes=[n['y'] for n in positions if n['role']=='process'];bases=[n['y'] for n in positions if n['role']=='foundation']
                    if caps and processes: assert max(caps)<min(processes)
                    if bases and processes: assert max(processes)<min(bases)
                    assert not overview['pointsOutsideStage'], overview
                    assert not overview['horizontalOverflow'], overview
                    page.screenshot(path=str(output/(path.name+'-overview.png')))
                    assert page.locator('#perspective option').count()==6
                    snapshot=page.evaluate('() => JSON.stringify(map)')
                    for perspective in ['network','layers','matrix','files','flow','graph']:
                        page.locator('#perspective').select_option(perspective)
                        expect(page.locator('#viewHelp')).not_to_be_empty()
                        assert page.evaluate('() => JSON.stringify(map)')==snapshot
                        if perspective=='matrix':
                            expect(page.locator('#textView table')).to_be_visible()
                        else:
                            expect(page.locator('#graph svg')).to_be_visible()
                        page.screenshot(path=str(output/(path.name+'-'+perspective+'.png')))
                    # File inventory has independent expansion and links back to the shared model.
                    page.locator('#perspective').select_option('files')
                    page.locator('.node[data-file-id="dir:codeatlas"]').click() if path==ROOT else page.locator('.node[data-file-id="project"]').click()
                    assert page.evaluate('() => JSON.stringify(map)')==snapshot
                    page.locator('#perspective').select_option('graph')

                    # Use actual UI clicks to open responsibility -> file -> declaration.
                    branch=page.locator('.node[aria-expanded="false"]').first
                    branch_id=branch.get_attribute('data-id')
                    branch.click()
                    expect(page.locator('#inspector')).to_contain_text('Sottopunti')
                    g=geometry(page)
                    assert not g['labelOverlaps'], g
                    page.screenshot(path=str(output/(path.name+'-explore.png')))
                    child_id=page.evaluate('(id) => map.groups.find(n=>n.parent===id && map.groups.some(c=>c.parent===n.id))?.id',branch_id)
                    if child_id:
                        page.locator(f'.node[data-id={json.dumps(child_id)}]').click()
                    assert not geometry(page)['labelOverlaps']
                    page.locator('#zoomIn').click()
                    page.locator('#zoomOut').click()
                    page.locator('#fit').click()
                    stage=page.locator('#graph').bounding_box()
                    page.mouse.move(stage['x']+35,stage['y']+35)
                    page.mouse.down()
                    page.mouse.move(stage['x']+65,stage['y']+55)
                    page.mouse.up()
                    assert page.evaluate('() => pan.x !== 0 && pan.y !== 0')
                    page.mouse.wheel(0,-200)
                    page.wait_for_timeout(100)
                    assert page.evaluate('() => zoom > 1')
                    page.locator('#fit').click()
                    # Deliberate worst case: all nodes visible; labels appear with zoom.
                    start=time.monotonic()
                    total=page.evaluate('() => {selected=null;expanded=new Set(map.groups.map(n=>n.id));zoom=1;pan={x:0,y:0};draw();return map.groups.length;}')
                    expanded=geometry(page)
                    assert expanded['renderedNodes']==total, (expanded,total)
                    assert not expanded['labelOverlaps'], expanded
                    assert not expanded['pointsOutsideStage'], expanded
                    elapsed=round(time.monotonic()-start,3)
                    page.screenshot(path=str(output/(path.name+'-all.png')))
                    page.locator('#modeText').click()
                    assert page.locator('#textView button').count()==total
                    page.locator('#modeGraph').click()
                    page.locator('#collapse').click()
                    for width,height in [(1024,768),(768,900),(390,844)]:
                        page.set_viewport_size({'width':width,'height':height})
                        page.wait_for_timeout(100)
                        g=geometry(page)
                        assert not g['horizontalOverflow'], (width,g)
                        assert not g['labelOverlaps'], (width,g)
                        page.screenshot(path=str(output/(path.name+f'-{width}.png')),full_page=True)
                    page.set_viewport_size({'width':1440,'height':900})
                    results.append({'project':path.name,'overview':overview,'allExpanded':expanded,'expandedDrawSeconds':elapsed,
                        'scanErrors':page.evaluate('() => report.atlas.errors')})
                open_project(ROOT)
                page.locator('.node[data-id="concept:analysis"]').click()
                page.locator('.node[data-id="concept:file:codeatlas/engine.py"]').click()
                page.screenshot(path=str(output/'qwe-detail.png'))
                chosen=page.evaluate('() => selected')
                for perspective in ['network','layers','matrix','flow','graph']:
                    page.locator('#perspective').select_option(perspective)
                    assert page.evaluate('() => selected')==chosen
                    expect(page.locator('#inspector h2')).to_have_text('codeatlas/engine.py')
                page.locator('#perspective').select_option('files')
                page.locator('#search').fill('engine.py')
                page.locator('.node[data-file-id="file:codeatlas/engine.py"]').click()
                page.get_by_role('button',name='codeatlas/engine.py → albero',exact=True).click()
                assert page.evaluate('() => selected')==chosen
                page.locator('#search').fill('')

                page.get_by_text('Modifica classificazione e scheda',exact=True).click()
                page.get_by_label('Nome',exact=True).fill('Motore personalizzato')
                page.get_by_role('button',name='Aggiorna scheda',exact=True).click()
                page.reload()
                expect(page.locator('#status')).to_contain_text('correzioni locali ripristinate')
                page.locator('#search').fill('Motore personalizzato')
                expect(page.locator('.node[data-id="concept:file:codeatlas/engine.py"]')).to_be_visible()
                page.locator('.node[data-id="concept:file:codeatlas/engine.py"]').press('Enter')
                expect(page.locator('#inspector h2')).to_have_text('Motore personalizzato')
                with page.expect_download() as info:
                    page.locator('#export').click()
                download=output/'exported-map.json'
                info.value.save_as(download)
                data=json.loads(download.read_text())
                assert any(n['name']=='Motore personalizzato' for n in data['groups'])
                page.locator('#search').fill('')
                page.locator('#import').set_input_files(str(download))
                page.get_by_role('button',name='Applica modifiche',exact=True).click()
                page.locator('#perspective').select_option('matrix')
                page.locator('#projectPath').fill('/this-folder-does-not-exist')
                page.locator('#openProject').click()
                expect(page.locator('#status')).to_have_class('error')
                expect(page.locator('#project')).to_have_text(ROOT.name)
                open_project(empty)
                expect(page.locator('#empty')).to_contain_text('Nessuna responsabilità')
                page.locator('#import').set_input_files(str(download))
                page.get_by_role('button',name='Applica modifiche',exact=True).click()
                expect(page.locator('#empty')).to_be_hidden()
                page.locator('#add').click()
                expect(page.locator('#inspector h2')).to_have_text('Nuovo elemento')
                assert not errors, errors
                browser.close()
                (output/'results.json').write_text(json.dumps({'projects':results,'browserErrors':errors,
                    'flows':['desktop open','responsibility/file expansion','zoom','text view','responsive','keyboard',
                             'manual edit/reload','search','export/import','invalid path preserves map','empty project','manual node']},indent=2))
                print(json.dumps(results,indent=2))
                print('Browser checks passed; artifacts:',output)
        finally:
            server.terminate()
            server.wait(timeout=10)
            log.close()


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--chromium')
    parser.add_argument('--output',default='/tmp/codeatlas-qa')
    parser.add_argument('--benchmark',action='append',default=[])
    run(parser.parse_args())
