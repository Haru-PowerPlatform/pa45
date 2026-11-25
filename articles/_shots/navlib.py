# Edge (--remote-debugging-port=9333) につないで操作・撮影する共通部品。
# 使い方: from navlib import run ; run(async def main(pg, shot, opts, fields): ...)
import asyncio, pathlib
from playwright.async_api import async_playwright

import os
RAW = pathlib.Path(__file__).parent / os.environ.get("RAWDIR", "raw-nav")
RAW.mkdir(exist_ok=True)

FIELDS_JS = ("Array.from(document.querySelectorAll('input,textarea,[role=combobox],[contenteditable=true],button[id^=wd-field]'))"
             ".map(e=>e.tagName+'|'+(e.getAttribute('aria-label')||'').slice(0,24)+'|'+(e.getAttribute('placeholder')||'').slice(0,16)"
             "+'|'+(e.value||e.innerText||'').slice(0,50)).join(' ;; ')")


def run(fn, match="copilotstudio"):
    async def main():
        async with async_playwright() as p:
            b = await p.chromium.connect_over_cdp("http://127.0.0.1:9333")
            pages = [x for x in b.contexts[0].pages if match in x.url] or b.contexts[0].pages
            pg = pages[-1]

            async def shot(n, w=900):
                await pg.wait_for_timeout(w)
                await pg.screenshot(path=str(RAW / f"{n}.png"))
                print("shot", n)

            async def opts(sel="[role=option]"):
                o = await pg.locator(sel).all_inner_texts()
                print("opts", [x.replace("\n", "/")[:40] for x in o[:25]])
                return o

            async def fields():
                print("fields:", (await pg.evaluate(FIELDS_JS)).replace(" ;; ", "\n  "))

            try:
                await fn(pg, shot, opts, fields)
            except Exception as e:
                print("ERR", str(e)[:500])
                await shot("zz-error")
    asyncio.run(main())
