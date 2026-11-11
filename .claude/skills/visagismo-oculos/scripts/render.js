#!/usr/bin/env node
/*
  Captura cada slide da apresentação em celular (390px) e desktop (1280px) e procura defeitos visuais.

  Uso:  node render.js apresentacao.html PASTA_SAIDA [--larguras 390,1280]

  Gera:
    PASTA/390/slide-01.png ...   uma imagem por slide (deviceScaleFactor 1, só para revisão)
    PASTA/folha-390.png          folha de contato com todos os slides (para o crítico ver de uma vez)
    PASTA/relatorio.json         overflow horizontal, elementos fora da tela, imagens quebradas, erros de console
  Sai com código 1 se houver overflow horizontal ou erro de script.
*/
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const args = process.argv.slice(2);
  if (args.length < 2) { console.error('uso: node render.js arquivo.html pasta [--larguras 390,1280]'); process.exit(2); }
  const arquivo = path.resolve(args[0]);
  const pasta = path.resolve(args[1]);
  const li = args.indexOf('--larguras');
  const larguras = (li > -1 ? args[li + 1] : '390,1280').split(',').map(Number);
  fs.mkdirSync(pasta, { recursive: true });

  const browser = await chromium.launch();
  const relatorio = { arquivo, larguras: {}, erros_console: [] };
  let falhou = false;

  for (const w of larguras) {
    const h = w < 600 ? 844 : 800;
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    page.on('pageerror', e => { relatorio.erros_console.push(`[${w}] ${e.message}`); falhou = true; });
    page.on('console', m => { if (m.type() === 'error') relatorio.erros_console.push(`[${w}] ${m.text()}`); });
    await page.goto('file://' + arquivo, { waitUntil: 'load' });
    await page.waitForTimeout(400);

    const info = await page.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      const overflow = document.documentElement.scrollWidth > vw + 1;
      const dentroDeRolagem = el => { for (let p = el.parentElement; p; p = p.parentElement) { const s = getComputedStyle(p); if (/(auto|scroll)/.test(s.overflowX)) return true; } return false; };
      const fora = [];
      document.querySelectorAll('.slide *').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) return;
        if ((r.right > vw + 1 || r.left < -1) && !dentroDeRolagem(el) && !el.closest('svg')) {
          const sl = el.closest('.slide');
          fora.push(`${sl ? '#' + sl.id : '?'} <${el.tagName.toLowerCase()} class="${el.className && el.className.baseVal === undefined ? el.className : ''}"> ${Math.round(r.left)}→${Math.round(r.right)}px`);
        }
      });
      const imgs = [...document.querySelectorAll('img')].filter(i => !i.complete || i.naturalWidth === 0).map(i => (i.src || '').slice(0, 60));
      const slides = [...document.querySelectorAll('.slide')].map(s => s.id || '(sem id)');
      // texto cortado: elemento com overflow hidden cujo conteúdo é maior que a caixa
      const cortado = [];
      document.querySelectorAll('.slide h1,.slide h2,.slide h3,.slide p,.slide span,.slide .v').forEach(el => {
        if (el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflow === 'hidden') cortado.push((el.textContent || '').trim().slice(0, 50));
      });
      return { overflow, fora: fora.slice(0, 40), imgs, slides, cortado };
    });
    relatorio.larguras[w] = info;
    if (info.overflow) falhou = true;

    const dir = path.join(pasta, String(w));
    fs.mkdirSync(dir, { recursive: true });
    const handles = await page.$$('.slide');
    const arquivos = [];
    for (let i = 0; i < handles.length; i++) {
      await handles[i].scrollIntoViewIfNeeded();
      const f = path.join(dir, `slide-${String(i + 1).padStart(2, '0')}.png`);
      await handles[i].screenshot({ path: f });
      arquivos.push(f);
    }
    await ctx.close();

    // folha de contato
    const cols = w < 600 ? 5 : 3;
    const thumb = w < 600 ? 230 : 420;
    const htmlFolha = `<html><body style="margin:0;background:#888;display:grid;grid-template-columns:repeat(${cols},${thumb}px);gap:6px;padding:6px;font:12px monospace">` +
      arquivos.map((f, i) => `<div style="background:#fff"><div style="padding:2px 4px">${i + 1} · ${info.slides[i]}</div><img src="file://${f}" style="width:${thumb}px;display:block"></div>`).join('') + '</body></html>';
    const fc = await browser.newContext({ viewport: { width: cols * (thumb + 6) + 6, height: 800 }, deviceScaleFactor: 1 });
    const fp = await fc.newPage();
    const tmp = path.join(pasta, `_folha-${w}.html`);
    fs.writeFileSync(tmp, htmlFolha);
    await fp.goto('file://' + tmp, { waitUntil: 'load' });
    await fp.screenshot({ path: path.join(pasta, `folha-${w}.png`), fullPage: true });
    fs.unlinkSync(tmp);
    await fc.close();
    console.log(`${w}px: ${arquivos.length} slides · overflow horizontal: ${info.overflow ? 'SIM' : 'não'} · elementos fora da tela: ${info.fora.length} · texto cortado: ${info.cortado.length}`);
  }
  await browser.close();
  fs.writeFileSync(path.join(pasta, 'relatorio.json'), JSON.stringify(relatorio, null, 2));
  if (relatorio.erros_console.length) console.log('erros de console:\n  ' + relatorio.erros_console.join('\n  '));
  console.log(`relatório: ${path.join(pasta, 'relatorio.json')}`);
  process.exit(falhou ? 1 : 0);
})();
