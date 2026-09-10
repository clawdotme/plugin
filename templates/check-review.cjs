#!/usr/bin/env node
/** Browser checks against generated files, never production or private Pages. */
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'@playwright/test');
const output=path.resolve(process.argv[2]);const slugs=JSON.parse(fs.readFileSync(path.join(__dirname,'review-set.json'))).slugs;
(async()=>{const browser=await chromium.launch();const results=[];fs.mkdirSync(path.join(output,'screenshots'),{recursive:true});try{
 for(const slug of slugs){for(const width of [1440,390]){const page=await browser.newPage({viewport:{width,height:1000}});const errors=[];page.on('pageerror',error=>errors.push(error.message));await page.goto(pathToFileURL(path.join(output,slug+'.html')).href);await page.evaluate(()=>document.fonts.ready);
 const state=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,images:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.alt),anchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash),h1:document.querySelectorAll('h1').length}));
 if(state.overflow||state.images.length||state.anchors.length||state.h1!==1||errors.length)throw Error(slug+' '+width+' '+JSON.stringify({state,errors}));
 const disclosure=page.locator('details').first();if(await disclosure.count()){const wasOpen=await disclosure.evaluate(d=>d.open);await disclosure.locator('summary').click();if(await disclosure.evaluate(d=>d.open)===wasOpen)throw Error(slug+' disclosure does not toggle');await disclosure.evaluate(d=>d.open=false);}
 await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(output,'screenshots',`${slug}-${width}.png`),fullPage:true});results.push({slug,width,status:'passed'});await page.close();}console.log('PASS '+slug);}
 fs.writeFileSync(path.join(output,'browser-checks.json'),JSON.stringify(results,null,2)+'\n');
 }finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
