#!/usr/bin/env python3
"""
PA45 YouTube公開後の一括更新スクリプト

Usage:
    python scripts/youtube-release.py <vol番号> <YouTube URL>

Example:
    python scripts/youtube-release.py 2 https://youtu.be/XXXXXXXX

実行内容:
    1. data/activities/pa45-volN.json に youtube URL を追記
    2. sessions/index.html の Vol.N カードに YouTube ボタンを追加
    3. git commit & push
    4. YouTube タイトル・説明文をターミナルに出力（コピペ用）
"""

import sys
import json
import re
import subprocess
from pathlib import Path

# Windows ターミナルの文字化け対策
if sys.stdout.encoding and sys.stdout.encoding.lower() in ("cp932", "shift_jis", "mbcs"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).parent.parent


def find_activity_json(vol: int) -> Path:
    index_path = REPO / "data" / "meta" / "activities-index.json"
    with open(index_path, encoding="utf-8") as f:
        paths = json.load(f)

    for p in paths:
        if re.search(rf"pa45-vol0?{vol}\.json$", p, re.IGNORECASE):
            full = REPO / p
            if full.exists():
                return full

    # フォールバック: data/activities/ 直接検索
    for p in sorted((REPO / "data" / "activities").glob(f"*pa45-vol{vol}*.json")):
        return p

    raise FileNotFoundError(f"PA45 Vol.{vol} の activity JSON が見つかりません")


def update_activity_json(json_path: Path, youtube_url: str) -> dict:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    if "evidence" not in data:
        data["evidence"] = {}

    if data["evidence"].get("youtube") == youtube_url:
        print(f"  （スキップ）youtube フィールドは既に設定されています")
        return data

    data["evidence"]["youtube"] = youtube_url

    with open(json_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data


def update_sessions_html(vol: int, youtube_url: str) -> bool:
    html_path = REPO / "sessions" / "index.html"
    content = html_path.read_text(encoding="utf-8")

    # Vol.N カードの範囲を特定
    start_marker = f'data-vol="{vol}"'
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print(f"  警告: sessions/index.html に Vol.{vol} カードが見つかりません")
        return False

    # このカード内にすでにYouTubeリンクがあるか確認
    # 次のカード or セクション終了までの範囲を取る
    next_card_idx = content.find('class="past-card"', start_idx + len(start_marker))
    card_region = content[start_idx:next_card_idx] if next_card_idx != -1 else content[start_idx:]

    if "youtu.be" in card_region or "youtube.com" in card_region:
        print(f"  （スキップ）Vol.{vol} の YouTube ボタンは既に追加済みです")
        return False

    # past-card-body の閉じタグ直前にボタンを挿入
    # パターン: "        </div>\n      </div>" の最初の出現（カード内）
    close_pattern = "        </div>\n      </div>"
    close_idx = content.find(close_pattern, start_idx)
    if close_idx == -1:
        print(f"  警告: Vol.{vol} カードの閉じタグが見つかりません")
        return False

    youtube_btn = (
        f'          <a href="{youtube_url}"\n'
        f'             target="_blank" rel="noopener" class="btn-slide-blog">'
        f'▶ YouTube動画を見る →</a>\n'
    )

    new_content = content[:close_idx] + youtube_btn + content[close_idx:]
    html_path.write_text(new_content, encoding="utf-8")
    return True


def generate_youtube_text(data: dict, vol: int) -> str:
    title_full = data.get("title", f"PA45 第{vol}回")
    theme = title_full.split("：")[-1] if "：" in title_full else title_full
    ev = data.get("evidence", {})
    slide   = ev.get("slide", "")
    blog    = ev.get("blog", "")
    connpass = ev.get("connpass", "")

    yt_title = f"【Power Automate 45】第{vol}回：{theme}（PA45）"

    lines = [
        f"初心者向けPower Automateハンズオン勉強会「PA45」第{vol}回の録画です。",
        f"テーマ：{theme}",
        "",
    ]
    if slide:
        lines += ["▼ 資料（PPTX）", slide, ""]
    if blog:
        lines += ["▼ ブログ解説記事", blog, ""]
    if connpass:
        lines += ["▼ connpassイベントページ", connpass, ""]
    lines += [
        "▼ PA45 公式サイト",
        "https://haru-powerplatform.github.io/pa45/",
        "",
        "#PowerAutomate #PA45 #Microsoft #PowerPlatform #業務効率化",
    ]

    sep = "=" * 50
    return (
        f"\n{sep}\n"
        f"【YouTube タイトル】\n{yt_title}\n\n"
        f"【YouTube 説明文】\n" + "\n".join(lines) +
        f"\n{sep}\n"
    )


def git_commit_push(vol: int, files: list) -> None:
    subprocess.run(["git", "add"] + files, cwd=REPO, check=True)
    msg = f"feat: add YouTube link for PA45 Vol.{vol}"
    subprocess.run(["git", "commit", "-m", msg], cwd=REPO, check=True)
    subprocess.run(["git", "push"], cwd=REPO, check=True)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    vol = int(sys.argv[1])
    youtube_url = sys.argv[2].strip()

    print(f"\n=== PA45 Vol.{vol} YouTube公開処理 ===\n")

    # 1. activity JSON 更新
    print("[1/3] activity JSON を更新中...")
    json_path = find_activity_json(vol)
    data = update_activity_json(json_path, youtube_url)
    print(f"  ✓ {json_path.relative_to(REPO)}")

    # 2. sessions/index.html 更新
    print("[2/3] sessions/index.html を更新中...")
    html_updated = update_sessions_html(vol, youtube_url)
    if html_updated:
        print("  ✓ YouTube ボタンを追加しました")

    # 3. git commit & push
    print("[3/3] git commit & push...")
    changed_files = [str(json_path.relative_to(REPO))]
    if html_updated:
        changed_files.append("sessions/index.html")
    git_commit_push(vol, changed_files)
    print("  ✓ push 完了")

    # 4. YouTube用テキスト出力
    print(generate_youtube_text(data, vol))
    print("✅ 完了！ GitHub Pages のデプロイ後（1〜2分）に反映されます。")


if __name__ == "__main__":
    main()
