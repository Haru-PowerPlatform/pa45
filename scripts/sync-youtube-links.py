"""
PA45 セッションカードに YouTube 録画リンクを同期する。

動画の「正」は videos/index.html の VIDEOS 配列（メモリ: 動画の正=videos/index.htmlのVIDEOS）。
そこにある回の録画URLを、sessions/index.html の該当 past-card に
「▶ YouTube動画を見る →」リンクとして入れる。既に入っている回はスキップ（冪等）。

録画が存在する回にだけ入れる（VIDEOS に無い回は何もしない）。
post-event-auto / ローカルの定期実行から毎回呼ばれる想定。

使い方:
  python scripts/sync-youtube-links.py            # 反映
  python scripts/sync-youtube-links.py --dry-run  # 追加対象の確認のみ
"""

import sys
import io
import re
import argparse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
VIDEOS_HTML = ROOT / "videos" / "index.html"
SESSIONS_HTML = ROOT / "sessions" / "index.html"


def load_video_map():
    """videos/index.html の VIDEOS から {vol: youtube_id} を作る。"""
    html = VIDEOS_HTML.read_text(encoding="utf-8")
    m = re.search(r"const\s+VIDEOS\s*=\s*\[(.*?)\];", html, re.S)
    body = m.group(1) if m else html
    out = {}
    # { vol:21, id:"24c58380CYg", ... } のような並びを拾う（vol と id の順不同に対応）
    for obj in re.finditer(r"\{([^{}]*)\}", body):
        chunk = obj.group(1)
        vm = re.search(r"vol\s*:\s*(\d+)", chunk)
        im = re.search(r"id\s*:\s*[\"']([A-Za-z0-9_-]{6,})[\"']", chunk)
        if vm and im:
            out[int(vm.group(1))] = im.group(1)
    return out


def yt_anchor(video_id):
    return (
        f'          <a href="https://youtu.be/{video_id}"\n'
        f'             target="_blank" rel="noopener" class="btn-slide-blog">▶ YouTube動画を見る →</a>\n'
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    vmap = load_video_map()
    html = SESSIONS_HTML.read_text(encoding="utf-8")

    added = []
    # past-card ブロックごとに処理。body の閉じ（10スペースのリンク群のあとの 8スペース </div>）直前に挿入。
    card_re = re.compile(
        r'(<div class="past-card" data-vol="(\d+)">.*?)(\n        </div>\n      </div>)',
        re.S,
    )

    def repl(m):
        block, vol_s, tail = m.group(1), m.group(2), m.group(3)
        vol = int(vol_s)
        if vol not in vmap:
            return m.group(0)               # 録画なし → 触らない
        if "youtu" in block:
            return m.group(0)               # 既にリンクあり → スキップ
        added.append(vol)
        return block + "\n" + yt_anchor(vmap[vol]).rstrip("\n") + tail

    new_html = card_re.sub(repl, html)

    if added:
        added_sorted = sorted(set(added))
        if args.dry_run:
            print(f"[DRY RUN] YouTubeリンクを追加する回: {added_sorted}")
        else:
            SESSIONS_HTML.write_text(new_html, encoding="utf-8")
            print(f"[OK] sessions/index.html に YouTubeリンクを追加: 第{added_sorted}回")
    else:
        print("[OK] 追加対象なし（録画のある回はすべてリンク済み）")


if __name__ == "__main__":
    main()
