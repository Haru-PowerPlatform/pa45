"""
PA45 新Vol追加スクリプト
sessions/index.html に新しいVolカードを自動挿入し、
release-flow.bat と import-flow-zip.py のマッピングも更新する。

使い方:
  python scripts/add-vol-card.py --vol 10 --topic FormsTeams \\
      --title "Forms→Teams通知" --date "2026-05-14" \\
      --participants 30 --pptx P010_PA45_FormsTeams_20260514.pptx \\
      --solution-name PA45No10FormsTeams \\
      [--blog-slug pa45-vol10-forms-teams] \\
      [--youtube https://youtu.be/XXXX]
"""
import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SESSIONS_HTML = REPO / 'sessions' / 'index.html'
IMPORT_PY = REPO / 'scripts' / 'import-flow-zip.py'
RELEASE_BAT = REPO / 'scripts' / 'release-flow.bat'

CARD_TEMPLATE = '''      <!-- ★第{vol}回 -->
      <div class="past-card" data-vol="{vol}">
        <div class="past-card-thumb">
          <div class="past-card-thumb-banner">
            <div class="past-card-thumb-banner-inner">
              <div class="banner-pill">PA45 第{vol}回</div>
              <div class="banner-title">{title}</div>
              <img class="banner-avatar" src="https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png" alt="Haru">
            </div>
          </div>
          <span class="past-card-vol">Vol.{vol}</span>
        </div>
        <div class="past-card-body">
          <div class="past-num">第{vol}回：{title}</div>
          <div class="past-date">{date} · 参加者{participants}名</div>
          <div class="past-theme">{theme}</div>
          <a href="https://haru-powerplatform.github.io/pa45/assets/pa45/{pptx}"
             target="_blank" rel="noopener" class="btn-slide">📥 資料閲覧はこちら（PPTX）→</a>
{blog_link}{flow_zip_link}{youtube_link}        </div>
      </div>

'''

BLOG_LINK_TEMPLATE = '''          <a href="https://www.automate136.com/{blog_slug}/"
             target="_blank" rel="noopener" class="btn-slide-blog">📖 スライド解説ブログ →</a>
'''

FLOW_ZIP_LINK_TEMPLATE = '''          <a href="https://haru-powerplatform.github.io/pa45/flows/vol-{vol_padded}/PA45-Vol{vol_padded}-{topic}.zip"
             download="PA45-Vol{vol_padded}-{topic}.zip" class="btn-slide-blog">⬇ フローZIPをダウンロード →</a>
'''

YOUTUBE_LINK_TEMPLATE = '''          <a href="{url}"
             target="_blank" rel="noopener" class="btn-slide-blog">▶ YouTube動画を見る →</a>
'''


def insert_card(vol, topic, title, date, participants, pptx, blog_slug, youtube):
    """sessions/index.html に新カードを挿入"""
    html = SESSIONS_HTML.read_text(encoding='utf-8')

    blog_link = BLOG_LINK_TEMPLATE.format(blog_slug=blog_slug) if blog_slug else ''
    flow_zip_link = FLOW_ZIP_LINK_TEMPLATE.format(vol_padded=f'{vol:02d}', topic=topic)
    youtube_link = YOUTUBE_LINK_TEMPLATE.format(url=youtube) if youtube else ''

    card_html = CARD_TEMPLATE.format(
        vol=vol,
        title=title,
        date=date,
        participants=participants,
        theme=f'{title}を学ぶ回です。',
        pptx=pptx,
        blog_link=blog_link,
        flow_zip_link=flow_zip_link,
        youtube_link=youtube_link,
    )

    # 「★次回以降の回はここに追加」コメントの直前に挿入
    marker = '<!-- ★次回以降の回はここに追加 -->'
    if marker not in html:
        print(f'  ✗ marker not found in sessions/index.html')
        return False

    # 既に同じVolカードがある場合はスキップ
    if f'data-vol="{vol}"' in html:
        print(f'  ⚠ Vol{vol} のカードは既に存在します。スキップ')
        return False

    new_html = html.replace(marker, card_html + '      ' + marker)
    SESSIONS_HTML.write_text(new_html, encoding='utf-8')
    print(f'  ✓ sessions/index.html に Vol{vol} カードを追加')
    return True


def update_import_py(vol, topic):
    """import-flow-zip.py の VOL_TOPIC マッピングに追加"""
    text = IMPORT_PY.read_text(encoding='utf-8')

    # 既に登録済みならスキップ
    if re.search(rf"^\s*{vol}:\s*'[^']+',", text, re.M):
        print(f'  ⚠ import-flow-zip.py に Vol{vol} は既に登録済み')
        return False

    # 最後の Vol エントリを見つけて、その後に追加
    pattern = re.compile(r"(VOL_TOPIC = \{[^}]*?)(\n\})", re.S)
    new_text, n = pattern.subn(rf"\1    {vol}: '{topic}',\n\2", text, count=1)
    if n == 0:
        print(f'  ✗ import-flow-zip.py の VOL_TOPIC が見つかりません')
        return False

    IMPORT_PY.write_text(new_text, encoding='utf-8')
    print(f'  ✓ import-flow-zip.py の VOL_TOPIC に {vol}: \'{topic}\' を追加')
    return True


def update_release_bat(vol, solution_name):
    """release-flow.bat の SOLUTION マッピング + ALL ループに追加"""
    text = RELEASE_BAT.read_text(encoding='utf-8')

    # 既に登録済みならスキップ
    if re.search(rf'if "%VOL%"=="{vol}" set SOLUTION=', text):
        print(f'  ⚠ release-flow.bat に Vol{vol} は既に登録済み')
        return False

    # 個別マッピング追加（最後の VOL=N の後に）
    last_vol_pattern = re.compile(
        r'(if "%VOL%"=="\d+" set SOLUTION=\w+)(\n\nif "%VOL%"=="all")', re.S
    )
    new_line = f'\nif "%VOL%"=="{vol}" set SOLUTION={solution_name}'
    text2, n1 = last_vol_pattern.subn(rf'\1{new_line}\2', text, count=1)
    if n1 == 0:
        # フォールバック：最後のマッピング行末尾に追加
        text2 = re.sub(
            r'(if "%VOL%"=="9" set SOLUTION=\w+)',
            rf'\1\nif "%VOL%"=="{vol}" set SOLUTION={solution_name}',
            text
        )

    # ALL ループの for %%S in (...) にも追加
    for_pattern = re.compile(r'(for %%S in \()([^)]+)(\) do)')
    m = for_pattern.search(text2)
    if m:
        existing = m.group(2).strip()
        if solution_name not in existing:
            new_for = m.group(1) + existing + ' ' + solution_name + m.group(3)
            text2 = text2[:m.start()] + new_for + text2[m.end():]

    RELEASE_BAT.write_text(text2, encoding='utf-8')
    print(f'  ✓ release-flow.bat に Vol{vol} ({solution_name}) を追加')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vol', type=int, required=True, help='Vol番号（10, 11, ...）')
    ap.add_argument('--topic', required=True, help='トピック識別子（例: FormsTeams）')
    ap.add_argument('--title', required=True, help='カード表示タイトル（例: Forms→Teams通知）')
    ap.add_argument('--date', required=True, help='開催日（例: 2026-05-14）')
    ap.add_argument('--participants', type=int, default=0, help='参加者数')
    ap.add_argument('--pptx', required=True, help='PPTXファイル名（assets/pa45/配下）')
    ap.add_argument('--solution-name', required=True, help='Solution UniqueName（例: PA45No10FormsTeams）')
    ap.add_argument('--blog-slug', default='', help='ブログslug（例: pa45-vol10-forms-teams）')
    ap.add_argument('--youtube', default='', help='YouTube URL')
    args = ap.parse_args()

    print(f'=== PA45 Vol.{args.vol} カード追加 ===')

    insert_card(args.vol, args.topic, args.title, args.date, args.participants,
                args.pptx, args.blog_slug, args.youtube)
    update_import_py(args.vol, args.topic)
    update_release_bat(args.vol, args.solution_name)

    print()
    print('完了！次のステップ:')
    print(f'  1. PA で Solution {args.solution_name} を作成しフローを追加')
    print(f'  2. .\\scripts\\release-flow.bat {args.vol} で初回エクスポート＋反映')
    print(f'  3. git commit & push')


if __name__ == '__main__':
    main()
