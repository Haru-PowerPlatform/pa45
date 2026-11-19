/* Vol.180（-1〜-4）共通の部品。vol-180b/c/d からも ../vol-180/kit.js で読む */
const A="../../pptx/_assets/";
const svgw=(p,sw)=>`<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${sw||2.4}" stroke-linecap="round" stroke-linejoin="round">${p}</svg>`;
const P={x:'<path d="M6 6l12 12M18 6L6 18"/>',ok:'<path d="M5 12l5 5 9-10"/>',arrow:'<path d="M4 12h15M13 6l6 6-6 6"/>',
  warn:'<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.5"/>',bulb:'<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.5 1 2.5h6c0-1 .3-1.8 1-2.5A6 6 0 0 0 12 3z"/>'};
const MS=(n,w)=>`<img class="msi" src="${A}icons/ms/${n}" alt="" style="width:${w||24}px;height:${w||24}px">`;
const PA=(w)=>`<img class="msi" src="${A}icons/pa_logo.png" alt="" style="width:${w||24}px;height:${w||24}px">`;
const CH=(e,h,st)=>`<img class="chara" src="${A}chara/chara_${e}.png" alt="" style="height:${h||112}px;${st||''}">`;

const DEFS=`<defs>
<linearGradient id="gGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FDE68A"/><stop offset=".55" stop-color="#F5B323"/><stop offset="1" stop-color="#B45309"/></linearGradient>
<linearGradient id="gGrayKey" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E5E7EB"/><stop offset=".55" stop-color="#9CA3AF"/><stop offset="1" stop-color="#4B5563"/></linearGradient>
<linearGradient id="gCard" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EEF2F7"/></linearGradient>
<linearGradient id="gBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#60A5FA"/><stop offset="1" stop-color="#1D4ED8"/></linearGradient>
<linearGradient id="gGreen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4ADE80"/><stop offset="1" stop-color="#15803D"/></linearGradient>
<linearGradient id="gRed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F87171"/><stop offset="1" stop-color="#B91C1C"/></linearGradient>
<linearGradient id="gGray" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CBD5E1"/><stop offset="1" stop-color="#64748B"/></linearGradient>
<linearGradient id="gViolet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A78BFA"/><stop offset="1" stop-color="#6D28D9"/></linearGradient>
<linearGradient id="gSteel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#94A3B8"/><stop offset=".5" stop-color="#E2E8F0"/><stop offset="1" stop-color="#94A3B8"/></linearGradient>
<linearGradient id="gBox" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E0B27A"/><stop offset="1" stop-color="#B07A3E"/></linearGradient>
<linearGradient id="gPaper" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFEF5"/><stop offset="1" stop-color="#FDF3C7"/></linearGradient>
<filter id="fSh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="2.5" stdDeviation="2.2" flood-color="#0F172A" flood-opacity=".28"/></filter>
</defs>`;

/* 名札（ストラップつきIDカード）。110x136。c=blue|green|red|gray|violet、o={dim,badge:'x'|'ok'|'lock',grp} */
function tagG(x,y,name,sub,c,o){
  o=o||{}; c=c||'blue';
  const G={blue:'gBlue',green:'gGreen',red:'gRed',gray:'gGray',violet:'gViolet'}[c];
  const ink={blue:'#1E3A8A',green:'#065F46',red:'#991B1B',gray:'#475569',violet:'#4C1D95'}[c];
  const face=o.grp
    ? `<circle cx="40" cy="62" r="8" fill="url(#${G})"/><path d="M27 84c0-9 6-13 13-13s13 4 13 13z" fill="url(#${G})"/><circle cx="70" cy="62" r="8" fill="url(#${G})"/><path d="M57 84c0-9 6-13 13-13s13 4 13 13z" fill="url(#${G})"/><circle cx="55" cy="58" r="9.5" fill="url(#${G})" stroke="#fff" stroke-width="2"/><path d="M39 86c0-11 7-15 16-15s16 4 16 15z" fill="url(#${G})" stroke="#fff" stroke-width="2"/>`
    : `<circle cx="55" cy="58" r="11" fill="url(#${G})"/><path d="M36 86c0-12 8-17 19-17s19 5 19 17z" fill="url(#${G})"/>`;
  let bd='';
  if(o.badge==='x') bd=`<circle cx="96" cy="34" r="13" fill="url(#gRed)" stroke="#fff" stroke-width="2.5"/><path d="M90 28l12 12M102 28l-12 12" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/>`;
  if(o.badge==='ok') bd=`<circle cx="96" cy="34" r="13" fill="url(#gGreen)" stroke="#fff" stroke-width="2.5"/><path d="M89.5 34.5l4.5 4.5 8-9.5" stroke="#fff" stroke-width="3.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
  if(o.badge==='lock') bd=`<circle cx="96" cy="34" r="13" fill="#475569" stroke="#fff" stroke-width="2.5"/><rect x="90" y="33" width="12" height="9" rx="2" fill="#fff"/><path d="M92.5 33v-3a3.5 3.5 0 0 1 7 0v3" stroke="#fff" stroke-width="2.4" fill="none"/>`;
  return `<g transform="translate(${x},${y})" opacity="${o.dim?0.55:1}">
  <path d="M40 0L52 20M70 0L58 20" stroke="${ink}" stroke-width="5" stroke-linecap="round" opacity=".75"/>
  <rect x="47" y="16" width="16" height="12" rx="3" fill="url(#gSteel)" stroke="#64748B" stroke-width="1.2"/>
  <rect x="4" y="24" width="102" height="108" rx="10" fill="url(#gCard)" stroke="${ink}" stroke-width="2.2" filter="url(#fSh)"/>
  <path d="M4 34a10 10 0 0 1 10-10h82a10 10 0 0 1 10 10v8H4z" fill="url(#${G})"/>
  <rect x="44" y="29" width="22" height="6" rx="3" fill="#fff" opacity=".85"/>
  ${face}
  <text x="55" y="107" text-anchor="middle" font-size="${o.fs||19}" font-weight="900" fill="#111827">${name}</text>
  <text x="55" y="124" text-anchor="middle" font-size="14.5" font-weight="900" fill="${ink}">${sub||''}</text>
  ${bd}</g>`;
}
/* 鍵。110x44。broken=true で折れた鍵 */
function keyG(x,y,o){
  o=o||{}; const g=o.gray?'gGrayKey':'gGold', st=o.gray?'#374151':'#92400E';
  const shaft=o.broken
    ? `<path d="M38 17h22l5 5-5 5 4 4H38z" fill="url(#${g})" stroke="${st}" stroke-width="1.8" stroke-linejoin="round"/><g transform="translate(12,7) rotate(14 80 22)"><path d="M70 17h34v7h-5v8h-7v-6h-5v8h-7v-8h-10l4-4-5-5z" fill="url(#${g})" stroke="${st}" stroke-width="1.8" stroke-linejoin="round"/></g>`
    : `<path d="M38 17h66v7h-5v9h-7v-7h-5v9h-7v-9H38z" fill="url(#${g})" stroke="${st}" stroke-width="1.8" stroke-linejoin="round"/>`;
  return `<g transform="translate(${x},${y}) scale(${o.s||1}) rotate(${o.rot||0} 55 22)" filter="url(#fSh)">
  ${shaft}
  <circle cx="22" cy="22" r="19" fill="url(#${g})" stroke="${st}" stroke-width="1.8"/>
  <circle cx="16" cy="22" r="6.5" fill="#fff" stroke="${st}" stroke-width="1.8"/>
  <path d="M10 10a17 17 0 0 1 22-3" stroke="#fff" stroke-width="2.4" fill="none" opacity=".7" stroke-linecap="round"/></g>`;
}
/* 南京錠。60x74 */
function lockG(x,y,o){
  o=o||{}; const g=o.c==='red'?'gRed':(o.c==='green'?'gGreen':'gGray');
  const sh=o.open?`<path d="M14 34V20a16 16 0 0 1 32 0v2" stroke="url(#gSteel)" stroke-width="8" fill="none" stroke-linecap="round" transform="translate(0,-8)"/>`
                 :`<path d="M14 34V22a16 16 0 0 1 32 0v12" stroke="url(#gSteel)" stroke-width="8" fill="none" stroke-linecap="round"/>`;
  return `<g transform="translate(${x},${y}) scale(${o.s||1})" filter="url(#fSh)">${sh}
  <rect x="4" y="32" width="52" height="40" rx="8" fill="url(#${g})" stroke="#1F2937" stroke-width="1.6"/>
  <rect x="8" y="35" width="44" height="6" rx="3" fill="#fff" opacity=".35"/>
  <circle cx="30" cy="49" r="6" fill="#111827"/><path d="M27 51h6l2 13h-10z" fill="#111827"/></g>`;
}
/* レンチ（直せる、の印）36x36 */
function wrenchG(x,y,s,col){
  return `<g transform="translate(${x},${y}) scale(${s||1})" filter="url(#fSh)"><path d="M33 9.5a9 9 0 0 1-12 8.5L8.5 30.5a3.6 3.6 0 0 1-5-5L16 13A9 9 0 0 1 27.5 2l-5.5 5.5 1.5 5 5 1.5z" fill="${col||'url(#gSteel)'}" stroke="#334155" stroke-width="1.6" stroke-linejoin="round"/></g>`;
}
const SV=(w,h,inner,st)=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" style="display:block;${st||''}" font-family="Noto Sans JP,sans-serif">${DEFS}${inner}</svg>`;
