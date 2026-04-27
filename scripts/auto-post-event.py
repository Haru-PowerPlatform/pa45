"""
PA45 開催後 全自動サイト更新スクリプト
GitHub Actions (木曜 21:15 JST) から自動実行される

処理内容:
  1. data/config/upcoming-event.json の date が今日(JST)と一致するか確認
  2. connpassから参加者数を自動取得
  3. data/activities/ に JSON を作成
  4. data/meta/activities-index.json を更新
  5. index.html の回数・参加者数を更新
  6. sessions/index.html に新しい回のカードを追加 & next-event を更新
  7. WordPress PA45ランディングページを更新
  8. data/config/upcoming-event.json をクリア（次回のために空にする）
"""

import sys
import io
import re
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

JST = timezone(timedelta(hours=9))
ROOT = Path(__file__).parent.parent
ACTIVITIES_DIR = ROOT / "data" / "activities"
INDEX_PATH     = ROOT / "data" / "meta" / "activities-index.json"
CONFIG_PATH    = ROOT / "data" / "config" / "upcoming-event.json"
INDEX_HTML     = ROOT / "index.html"
SESSIONS_HTML  = ROOT / "sessions" / "index.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "ja,en;q=0.9",
}

AVATAR_URL = "https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png"


# ── ユーティリティ ────────────────────────────────────────────

def today_jst():
    return datetime.now(JST).strftime("%Y-%m-%d")


def fetch_participants(event_id):
    urls = [
        f"https://powerautomate-create.connpass.com/event/{event_id}/",
        f"https://connpass.com/event/{event_id}/",
    ]
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode("utf-8")
                final_url = resp.geturl()
            m = re.search(r'class="amount"[^>]*>\s*<span[^>]*>\s*(\d+)\s*</span>', html)
            if not m:
                m = re.search(r'参加者数[^\d]*(\d+)', html)
            if m:
                return int(m.group(1)), final_url
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
            raise
    return None, None


def load_env():
    env_path = ROOT / ".env"
    env = {}
    if not env_path.exists():
        return env
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip()
    return env


# ── 参加者数・開催回数を activities から集計 ─────────────────

def calc_totals():
    """現在の activities JSON から PA45 の回数・累計参加者を集計"""
    total_sessions = 0
    total_participants = 0
    for f in sorted(ACTIVITIES_DIR.glob("*-pa45-vol*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if data.get("type") == "PA45":
                total_sessions += 1
                total_participants += data.get("participants", 0)
        except Exception:
            pass
    return total_sessions, total_participants


# ── index.html 更新 ──────────────────────────────────────────

def update_index_html(vol, participants_total):
    html = INDEX_HTML.read_text(encoding="utf-8")

    # hero-stat: 回数
    html = re.sub(
        r'(<div class="hero-stat-n">)\d+回(</div>\s*<div class="hero-stat-l">PA45開催)',
        rf'\g<1>{vol}回\2',
        html
    )
    # hero-stat: 参加者数
    html = re.sub(
        r'(<div class="hero-stat-n">)\d+名\+(</div>\s*<div class="hero-stat-l">累計参加者)',
        rf'\g<1>{participants_total}名+\2',
        html
    )
    # proof: 回数
    html = re.sub(
        r'(<div class="proof-n">)\d+回(</div>\s*<div class="proof-l">PA45 開催)',
        rf'\g<1>{vol}回\2',
        html
    )
    # proof: 参加者数
    html = re.sub(
        r'(<div class="proof-n">)\d+名(</div>\s*<div class="proof-l">累計参加者（確定）)',
        rf'\g<1>{participants_total}名\2',
        html
    )
    # proof: 合計テキスト
    html = re.sub(
        r'(<div class="proof-link">第1〜)\d+(回 合計</div>)',
        rf'\g<1>{vol}\2',
        html
    )

    INDEX_HTML.write_text(html, encoding="utf-8")
    print(f"  index.html 更新: 第{vol}回 / 累計{participants_total}名")


# ── sessions/index.html 更新 ─────────────────────────────────

def build_past_card(vol, date_str, theme, description, participants, connpass_url):
    """Vol.Nの past-card HTML を生成"""
    vol3 = f"{vol:03d}"
    date_nodash = date_str.replace("-", "")
    slide_url = f"https://haru-powerplatform.github.io/pa45/assets/pa45/P{vol3}_PA45_{theme}_{date_nodash}.pptx"

    card = f"""
      <!-- ★第{vol}回 -->
      <div class="past-card" data-vol="{vol}">
        <div class="past-card-thumb">
          <div class="past-card-thumb-banner">
            <div class="past-card-thumb-banner-inner">
              <div class="banner-pill">PA45 第{vol}回</div>
              <div class="banner-title">{theme}</div>
              <img class="banner-avatar" src="{AVATAR_URL}" alt="Haru">
            </div>
          </div>
          <span class="past-card-vol">Vol.{vol}</span>
        </div>
        <div class="past-card-body">
          <div class="past-num">第{vol}回：{theme}</div>
          <div class="past-date">{date_str} · 参加者{participants}名</div>
          <div class="past-theme">{description}</div>
          <a href="{slide_url}"
             target="_blank" rel="noopener" class="btn-slide">📥 資料閲覧はこちら（PPTX）→</a>
        </div>
      </div>"""
    return card


def update_sessions_html(vol, date_str, theme, description, participants, connpass_url):
    html = SESSIONS_HTML.read_text(encoding="utf-8")

    # 新しいカードを生成
    new_card = build_past_card(vol, date_str, theme, description, participants, connpass_url)

    # 「★次回以降の回はここに追加」マーカーの直前に挿入
    marker = "<!-- ★次回以降の回はここに追加 -->"
    if marker in html:
        html = html.replace(marker, new_card + "\n\n      " + marker)
        print(f"  sessions/index.html: 第{vol}回カードを追加")
    else:
        print("  ⚠ sessions/index.html: 挿入マーカーが見つかりません。手動で追加してください。")

    # next-event セクションを「次回未定」に更新
    next_event_pattern = re.compile(
        r'<div class="next-event">.*?</div>\s*</div>',
        re.DOTALL
    )
    next_event_replacement = """<div class="next-event">
  <div class="next-label">Next Session — 準備中</div>
  <div class="next-date">次回日程は調整中です</div>
  <div class="next-title">PA45 第{next_vol}回（準備中）</div>
  <div class="next-meta">オンライン（Microsoft Teams）· 約45分 · 無料</div>
  <p>次回のconnpassイベントが公開されたらここに掲載します。</p>
  <a href="https://powerautomate-create.connpass.com/" class="btn-connpass">
    connpassグループをフォローする →
  </a>
</div>
      </div>""".format(next_vol=vol + 1)

    m = next_event_pattern.search(html)
    if m:
        html = html[:m.start()] + next_event_replacement + html[m.end():]
        print(f"  sessions/index.html: next-event を「準備中」に更新")

    SESSIONS_HTML.write_text(html, encoding="utf-8")


# ── WordPress 更新 ───────────────────────────────────────────

def update_wp_pa45_page(vol, theme, participants):
    env = load_env()
    wp_user = env.get("WP_USER", "")
    wp_pass = env.get("WP_PASS", "")
    wp_url  = env.get("WP_URL", "").rstrip("/")
    if not (wp_user and wp_pass and wp_url):
        print("  ⚠ WordPress認証情報が .env にありません。スキップします。")
        return

    import base64
    token = base64.b64encode(f"{wp_user}:{wp_pass}".encode()).decode()
    headers_auth = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

    req = urllib.request.Request(
        f"{wp_url}/wp-json/wp/v2/pages/2228?_fields=content",
        headers={"Authorization": f"Basic {token}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            page = json.load(resp)
    except Exception as e:
        print(f"  ⚠ WP取得エラー: {e}")
        return

    content = page["content"]["rendered"]
    new_li = f"<li>第{vol}回：{theme}— {participants}名参加</li>"
    if f"第{vol}回" in content:
        print(f"  WP: 第{vol}回は既に記載済み。スキップ。")
        return

    prev_pattern = re.compile(rf"(<li>第{vol-1}回[^<]*</li>)")
    m = prev_pattern.search(content)
    if m:
        updated = content[:m.end()] + f"\n{new_li}" + content[m.end():]
    else:
        updated = content.replace("</ul>", f"{new_li}\n</ul>", 1)

    body = json.dumps({"content": updated}).encode("utf-8")
    req2 = urllib.request.Request(
        f"{wp_url}/wp-json/wp/v2/pages/2228",
        data=body, headers=headers_auth, method="POST"
    )
    try:
        with urllib.request.urlopen(req2, timeout=15) as resp:
            if resp.status == 200:
                print(f"  WP: 第{vol}回を追加 ✓")
    except Exception as e:
        print(f"  ⚠ WP更新エラー: {e}")


# ── activities-index 更新 ────────────────────────────────────

def update_activities_index(activity_path_str):
    if INDEX_PATH.exists():
        index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    else:
        index = []
    if activity_path_str not in index:
        index.append(activity_path_str)
        index.sort()
    INDEX_PATH.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(f"  activities-index.json 更新")


# ── メイン ───────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="PA45 開催後自動更新")
    parser.add_argument("--force", action="store_true", help="日付チェックをスキップして強制実行")
    parser.add_argument("--dry-run", action="store_true", help="ファイルを書き換えずに動作確認")
    args = parser.parse_args()

    print("\n=== PA45 開催後 自動更新 ===\n")

    # 1. upcoming-event.json を読み込む
    if not CONFIG_PATH.exists():
        print("  data/config/upcoming-event.json が存在しません。終了します。")
        sys.exit(0)

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if not config.get("vol"):
        print("  upcoming-event.json が空です（イベントなし）。終了します。")
        sys.exit(0)

    vol        = config["vol"]
    event_id   = config["event_id"]
    date_str   = config["date"]
    theme      = config["theme"]
    description = config.get("description", theme)
    connpass_url = config.get("connpass_url",
                              f"https://powerautomate-create.connpass.com/event/{event_id}/")

    print(f"  イベント: 第{vol}回「{theme}」({date_str})")

    # 2. 今日の日付チェック（JST）
    today = today_jst()
    if not args.force and today != date_str:
        print(f"  本日は {today}、イベント日は {date_str} — 実行日が違うためスキップします。")
        print(f"  強制実行するには --force を使ってください。")
        sys.exit(0)

    print(f"  日付一致: {today} ✓")

    # 3. 参加者数を connpass から取得
    print(f"  connpassから参加者数を取得中... (event_id={event_id})")
    participants, fetched_url = fetch_participants(event_id)
    if participants is None:
        print("  ⚠ 参加者数を取得できませんでした。あとで手動で post-event.py を実行してください。")
        sys.exit(1)
    print(f"  参加者数: {participants}人 ({fetched_url})")

    if args.dry_run:
        print("\n[DRY RUN] ファイル書き換えはスキップします。")
        print(f"  → 第{vol}回 {theme} / {participants}人")
        sys.exit(0)

    # 4. activity JSON 作成
    activity_id = f"{date_str}-pa45-vol{vol}"
    filename    = f"{activity_id}.json"
    filepath    = ACTIVITIES_DIR / filename

    activity = {
        "id": activity_id,
        "type": "PA45",
        "title": f"PA45 第{vol}回：{theme}",
        "date": date_str,
        "public": True,
        "summary": f"Power Automate 45 第{vol}回。テーマ：{theme}",
        "tags": ["PA45", "Power Automate", "ハンズオン"],
        "connpass_event_id": int(event_id),
        "participants": participants,
        "evidence": {
            "connpass": connpass_url,
        },
    }
    filepath.write_text(json.dumps(activity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  activity JSON 作成: {filename}")

    # 5. activities-index 更新
    update_activities_index(f"data/activities/{filename}")

    # 6. 合計を再計算してから index.html 更新
    total_sessions, total_participants = calc_totals()
    print(f"  集計: {total_sessions}回 / 累計{total_participants}名")
    update_index_html(total_sessions, total_participants)

    # 7. sessions/index.html 更新
    update_sessions_html(vol, date_str, theme, description, participants, connpass_url)

    # 8. WordPress 更新
    print("  WordPress を更新中...")
    update_wp_pa45_page(vol, theme, participants)

    # 9. upcoming-event.json をクリア（次回まで空にする）
    CONFIG_PATH.write_text(json.dumps({}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("  upcoming-event.json をクリア（次回イベント設定待ち）")

    print(f"\n✅ 完了！第{vol}回（{participants}名）の情報を更新しました。")
    print("  → git commit & push は GitHub Actions が自動実行します。")


if __name__ == "__main__":
    main()
