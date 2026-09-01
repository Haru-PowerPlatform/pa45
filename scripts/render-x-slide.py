# -*- coding: utf-8 -*-
"""X技術Tipsの1枚スライド(1280x720)をPNG 2560x1440で書き出し、同時に見切れを実測する。

使い方:
    python scripts/render-x-slide.py vol-107 vol-107b ...
    python scripts/render-x-slide.py --all-missing      # 板が参照していてPNGが無いものを全部

各フォルダの index.html を開き、#slide を 1280x720・deviceScaleFactor=2 で撮って
同フォルダに <フォルダ名からハイフンを抜いた名前>.png を保存する。
撮る前に #slide 内の全要素の overflow（scrollHeight-clientHeight と はみ出し量）を測り、
5px を超えるものがあれば PNG を書かずに NG として報告する（マスコットの意図的なはみ出しは除外）。
"""
import sys
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "assets" / "x" / "html"

MEASURE = r"""
() => {
  const slide = document.getElementById('slide');
  if (!slide) return {error: 'no #slide'};
  const sr = slide.getBoundingClientRect();
  const bad = [];
  // マスコットは意図的に枠外へ出す設計なので、測る間だけ隠す（親のscrollHeightを汚さないため）
  const charas = [...slide.querySelectorAll('.title-chara, .chara')];
  charas.forEach(c => { c.dataset._d = c.style.display; c.style.display = 'none'; });
  slide.querySelectorAll('*').forEach(el => {
    if (el.classList.contains('title-chara') || el.classList.contains('chara')) return;
    // SVGの中身はSVGビューポートでクリップされるので、はみ出し判定の対象外
    // （viewBoxから溢れた文字は目視チェックで拾う）
    if (el.ownerSVGElement) return;
    const over = el.scrollHeight - el.clientHeight;
    if (over > 5 && el.clientHeight > 0) {
      bad.push({kind: 'scroll', px: over, cls: (typeof el.className==='string'?el.className:(el.getAttribute('class')||el.tagName)).slice(0,40),
                text: (el.innerText || '').replace(/\s+/g, ' ').slice(0, 34)});
    }
    const r = el.getBoundingClientRect();
    const outB = r.bottom - sr.bottom, outR = r.right - sr.right;
    const outT = sr.top - r.top, outL = sr.left - r.left;
    const out = Math.max(outB, outR, outT, outL);
    if (out > 5 && r.height > 0 && r.height < 720) {
      bad.push({kind: 'outside', px: Math.round(out), cls: (typeof el.className==='string'?el.className:(el.getAttribute('class')||el.tagName)).slice(0,40),
                text: (el.innerText || '').replace(/\s+/g, ' ').slice(0, 34)});
    }
  });
  // 情景SVGの viewBox と実寸の比が合っていないと slice で端が切れる（文字が消える事故の主因）
  slide.querySelectorAll('*').forEach(box => {
    if (box.ownerSVGElement) return;
    const svg = box.querySelector(':scope > svg');
    if (svg && getComputedStyle(box).overflow !== 'hidden') return;
    if (!svg || !svg.getAttribute('viewBox')) return;
    if ((svg.getAttribute('preserveAspectRatio') || '').includes('none')) return;
    const r = box.getBoundingClientRect();
    const vb = svg.getAttribute('viewBox').trim().split(/[\s,]+/).map(Number);
    if (vb.length !== 4 || !vb[2] || !vb[3] || !r.width || !r.height) return;
    const boxAR = r.width / r.height, vbAR = vb[2] / vb[3];
    const diff = Math.abs(boxAR - vbAR) / boxAR;
    if (diff > 0.03) {
      bad.push({kind: 'viewBox', px: Math.round(diff * 100),
                cls: (box.getAttribute('class') || '').slice(0, 40),
                text: `実寸 ${Math.round(r.width)}x${Math.round(r.height)} に対し viewBox ${vb[2]}x${vb[3]}`});
    }
  });
  charas.forEach(c => { c.style.display = c.dataset._d || ''; });
  const seen = new Set();
  return {bad: bad.filter(b => {
    const k = b.kind + b.cls + b.text;
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  }).slice(0, 12)};
}
"""


def targets_from_args(argv):
    if argv and argv[0] == "--all-missing":
        board = json.loads((ROOT / "data" / "x-tips-board.json").read_text(encoding="utf-8"))
        out = []
        for it in board["items"]:
            f = it["folder"]
            base = f.replace("-", "")
            for folder, name in ((f, base + ".png"), (f + "b", base + "b.png")):
                if not (HTML / folder / name).exists() and (HTML / folder / "index.html").exists():
                    out.append(folder)
        return out
    return list(argv)


def main(argv):
    names = targets_from_args(argv)
    if not names:
        print("対象なし")
        return 0
    ng = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720},
                                device_scale_factor=2)
        for name in names:
            d = HTML / name
            src = d / "index.html"
            if not src.exists():
                print(f"[SKIP] {name}: index.html が無い")
                ng += 1
                continue
            page.goto(src.as_uri())
            page.wait_for_timeout(1400)          # Webフォントとサブセットの読み込み待ち
            res = page.evaluate(MEASURE)
            bad = res.get("bad") or []
            png = d / (name.replace("-", "") + ".png")
            page.locator("#slide").screenshot(path=str(png))
            if bad:
                ng += 1
                print(f"[NG] {name}  見切れ {len(bad)}件")
                for b in bad:
                    unit = "%" if b['kind'] == 'viewBox' else "px"
                    print(f"      {b['kind']:7s} {b['px']:4}{unit}  .{b['cls']}  | {b['text']}")
            else:
                size = png.stat().st_size
                print(f"[OK] {name}  見切れ0  -> {png.name} ({size // 1024}KB)")
        browser.close()
    print(f"\n完了: {len(names)}枚 / NG {ng}枚")
    return 1 if ng else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
