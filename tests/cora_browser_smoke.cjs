/* Optional real-browser check: NODE_PATH=<playwright modules> CHROMIUM_EXECUTABLE=<browser> node tests/cora_browser_smoke.cjs */
const {chromium}=require('playwright');
const {spawn}=require('node:child_process');
const assert=require('node:assert/strict');
const path=require('node:path');
(async()=>{
 const server=spawn('python',['-u','-c',"from http.server import ThreadingHTTPServer; from codeatlas.desktop import AtlasHandler; s=ThreadingHTTPServer(('127.0.0.1',0),AtlasHandler); print(s.server_port,flush=True); s.serve_forever()"],{cwd:path.resolve(__dirname,'..')});
 const port=await new Promise((resolve,reject)=>{server.stdout.once('data',data=>resolve(Number(data.toString().trim())));server.once('error',reject);server.once('exit',code=>reject(Error('Server exited '+code)))});
 let browser;
 try{
  browser=await chromium.launch({executablePath:process.env.CHROMIUM_EXECUTABLE||undefined,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'],headless:true});
  const page=await browser.newPage({viewport:{width:1600,height:1100}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${port}/`);await page.waitForSelector('#map .node');
  assert.equal(await page.locator('#map .node').count(),45);
  await page.locator('[data-id="C1"]').click();await page.locator('[data-id="C1a"]').click();
  assert.equal(await page.locator('[data-id="C1a.m1"]').count(),1);
  await page.getByRole('button',{name:'Modifica o sposta',exact:true}).click();
  await page.locator('dialog textarea').first().fill('Nota di verifica browser');
  await page.getByRole('button',{name:'Salva',exact:true}).click();await page.reload();
  await page.locator('[data-id="C1"]').click();await page.locator('[data-id="C1a"]').click();
  assert.match(await page.locator('#inspector').textContent(),/Nota di verifica browser/);
  await page.setViewportSize({width:390,height:844});await page.getByRole('button',{name:'Costellazione',exact:true}).click();
  assert.equal(await page.locator('#map .node').count(),45);
  await page.locator('#search').fill('Calendario');await page.locator('#results button').first().click();
  assert.match(await page.locator('#inspector').textContent(),/Calendario/);
  assert.deepEqual(errors,[]);console.log('Cora browser smoke: desktop launch, expansion, edit/reload, mobile search OK');
 }finally{if(browser)await browser.close();server.kill()}
})().catch(e=>{console.error(e);process.exitCode=1});
