import chromium from '@sparticuz/chromium';
import p from 'puppeteer-core';
import fs from 'fs'; import {execSync} from 'child_process';
const [dir, only] = process.argv.slice(2);
const FPS=15;
const sc=JSON.parse(fs.readFileSync(`${dir}/timed.json`));
const b=await p.launch({args:chromium.args,executablePath:await chromium.executablePath(),headless:true});
const pg=await b.newPage(); await pg.setViewport({width:1280,height:720});
await pg.goto('http://127.0.0.1:8765/stage.html');
fs.mkdirSync(`${dir}/seg`,{recursive:true});
for(const s of sc){
  if(only && s.id!==only) continue;
  const out=`${dir}/seg/${s.id}.mp4`; if(fs.existsSync(out) && !only) continue;
  const fd=`${dir}/frames/${s.id}`; fs.rmSync(fd,{recursive:true,force:true}); fs.mkdirSync(fd,{recursive:true});
  await pg.evaluate(x=>window.setScene(x), s);
  const n=Math.ceil(s.dur*FPS);
  for(let i=0;i<n;i++){ await pg.evaluate((t,d)=>window.setT(t,d), i/FPS, s.dur);
    await pg.screenshot({path:`${fd}/${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:88}); }
  execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${fd}/%05d.jpg -i ${dir}/audio/${s.id}.wav -c:v libx264 -preset veryfast -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -ar 48000 -shortest ${out}`);
  fs.rmSync(fd,{recursive:true,force:true});
  console.log('done',s.id,n);
}
await b.close();
