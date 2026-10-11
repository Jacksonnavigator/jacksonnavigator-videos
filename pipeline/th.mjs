import chromium from '@sparticuz/chromium'; import p from 'puppeteer-core';
const b=await p.launch({args:chromium.args,executablePath:await chromium.executablePath(),headless:true});
const pg=await b.newPage(); await pg.setViewport({width:1280,height:720});
await pg.goto('http://127.0.0.1:8765/thumb.html',{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,500));
await pg.screenshot({path:'/home/claude/yt/v1/thumbnail.png'}); await b.close();
