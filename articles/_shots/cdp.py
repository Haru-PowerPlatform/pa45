# 記事用：Edge（--remote-debugging-port=9333）につないで操作と撮影をする小道具（talks/2026-11-pl900-01/cdp.py の写し）
# 使い方: python cdp.py shot NAME            → shots/raw/NAME.png（画面全体）
#         python cdp.py goto URL
#         python cdp.py click "テキスト or css=..."   （テキストは完全一致を優先）
#         python cdp.py fill "css=..." "値"
#         python cdp.py text                  → 画面の文字（先頭3000字）
#         python cdp.py js "式"
import sys, asyncio, pathlib
from playwright.async_api import async_playwright
HERE = pathlib.Path(__file__).parent
RAW = HERE / "raw-nav"; RAW.mkdir(parents=True, exist_ok=True)

def loc(pg, t):
    if t.startswith("css="):
        return pg.locator(t[4:]).first
    if t.startswith("role="):
        role, name = t[5:].split(":", 1)
        return pg.get_by_role(role, name=name).first
    exact = pg.get_by_text(t, exact=True)
    return exact.first

async def main():
    cmd, args = sys.argv[1], sys.argv[2:]
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp("http://127.0.0.1:9333")
        ctx = b.contexts[0]
        pages = [x for x in ctx.pages if not x.url.startswith("edge://") and not x.url.startswith("devtools") and "claude.ai" not in x.url] or ctx.pages
        pg = pages[-1]
        if cmd == "pages":
            for x in ctx.pages: print(x.url, "|", await x.title())
        elif cmd == "goto":
            await pg.goto(args[0], wait_until="domcontentloaded"); await pg.wait_for_timeout(int(args[1]) if len(args) > 1 else 6000)
            print(pg.url)
        elif cmd == "shot":
            await pg.wait_for_timeout(int(args[1]) if len(args) > 1 else 800)
            await pg.screenshot(path=str(RAW / f"{args[0]}.png"))
            print("saved", args[0], pg.url)
        elif cmd == "click":
            await loc(pg, args[0]).click(timeout=15000); await pg.wait_for_timeout(int(args[1]) if len(args) > 1 else 2500)
            print("clicked", pg.url)
        elif cmd == "fill":
            await loc(pg, args[0]).fill(args[1]); await pg.wait_for_timeout(800); print("filled")
        elif cmd == "text":
            t = await pg.evaluate("document.body.innerText"); print(pg.url); print(t[: int(args[0]) if args else 3000])
        elif cmd == "js":
            print(await pg.evaluate(args[0]))
        elif cmd == "press":
            await pg.keyboard.press(args[0]); await pg.wait_for_timeout(int(args[1]) if len(args) > 1 else 800); print("pressed")
        elif cmd == "type":
            await pg.keyboard.type(args[0], delay=30); await pg.wait_for_timeout(800); print("typed")
        elif cmd == "hover":
            await loc(pg, args[0]).hover(); await pg.wait_for_timeout(1000); print("hover")
        elif cmd == "size":
            await pg.set_viewport_size({"width": int(args[0]), "height": int(args[1])}); print("ok")
asyncio.run(main())
