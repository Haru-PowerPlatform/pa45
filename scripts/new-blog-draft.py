"""
PA45 ブログ下書き自動生成スクリプト

使い方:
  python scripts/new-blog-draft.py --vol 4 --date 2026-04-02 --theme "Apply to each"

WordPressに下書きを作成します。
骨格だけ生成されるので、あとは管理画面で肉付けしてください。
"""

import sys
import io
import json
import argparse
import base64
from pathlib import Path
from urllib.request import urlopen, Request
import urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
AVATAR = "https://www.automate136.com/wp-content/uploads/2025/07/u9429395585_side_profile_portrait_of_a_man_in_his_30s_with_me_e4cca787-50fc-42ba-8f64-d0185bce97e5_1.png"


def load_env():
    env = {}
    with open(ROOT / ".env", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, val = line.partition("=")
            env[key.strip()] = val.strip()
    return env


def wp_post(env, payload):
    url = f"{env['WP_URL']}/wp-json/wp/v2/posts"
    creds = base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()
    req = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Basic {creds}", "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req) as resp:
        return json.loads(resp.read())


def build_content(vol, date, theme, slide_url):
    def bubble(text):
        return f"""<!-- wp:html -->
<div class="speech-wrap sb-id-14 sbs-stn sbp-l sbis-cb cf">
<div class="speech-person">
<figure class="speech-icon"><img class="speech-icon-image" src="{AVATAR}" alt="" width="1024" height="1024" /></figure>
</div>
<div class="speech-balloon">
{text}
</div>
</div>
<!-- /wp:html -->"""

    connpass_url = f"https://powerautomate-create.connpass.com/event/"

    return f"""<!-- wp:paragraph -->
<p>PA45 第{vol}回、テーマは「<span style="color: #0000ff;"><strong>{theme}</strong></span>」です。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>今回も45分間、手を動かしながら進めました。</p>
<!-- /wp:paragraph -->

&nbsp;

<!-- wp:heading -->
<h2 class="wp-block-heading">今回のテーマ：{theme}</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>（ここに内容を書く）</p>
<!-- /wp:paragraph -->

{bubble(f'「{theme}」は〇〇みたいなイメージです。（ここに一言コメントを書く）')}

&nbsp;

<!-- wp:heading -->
<h2 class="wp-block-heading">ハンズオンの流れ</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list"><li>（ステップ1）</li><li>（ステップ2）</li><li>（ステップ3）</li></ul>
<!-- /wp:list -->

&nbsp;

<!-- wp:heading -->
<h2 class="wp-block-heading">参加者の声</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>（ここにアンケートや感想を書く）</p>
<!-- /wp:paragraph -->

&nbsp;

<!-- wp:heading -->
<h2 class="wp-block-heading">スライド資料</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>当日使用したスライドはこちらです。↓</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><a href="{slide_url}" target="_blank" rel="noopener">{slide_url}</a></p>
<!-- /wp:paragraph -->

&nbsp;

<!-- wp:heading -->
<h2 class="wp-block-heading">次回予告</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>次回は（テーマ未定）の予定です。connpassで参加登録をお待ちしています！</p>
<!-- /wp:paragraph -->

{bubble('毎週木曜夜に開催しています。初めての方も気軽にどうぞ。')}
"""


def main():
    parser = argparse.ArgumentParser(description="PA45 ブログ下書き自動生成")
    parser.add_argument("--vol", required=True, type=int)
    parser.add_argument("--date", required=True, help="開催日 YYYY-MM-DD")
    parser.add_argument("--theme", required=True, help="テーマ名")
    parser.add_argument("--slide", default="", help="スライドURL（省略時は自動生成）")
    args = parser.parse_args()

    slide_url = args.slide or (
        f"https://haru-powerplatform.github.io/pa45/assets/pa45/"
        f"P{args.vol:03d}_PA45_{args.theme}_{args.date.replace('-', '')}.pptx"
    )

    title = f"【PA45 第{args.vol}回】{args.theme}"
    content = build_content(args.vol, args.date, args.theme, slide_url)

    print(f"▶ WordPress に下書きを作成中...")
    env = load_env()
    result = wp_post(env, {"title": title, "content": content, "status": "draft"})
    post_id = result["id"]

    print(f"  完了！投稿ID: {post_id}")
    print(f"  編集URL: {env['WP_URL']}/wp-admin/post.php?post={post_id}&action=edit")
    print()
    print(f"  タイトル: {title}")
    print(f"  ステータス: 下書き")
    print(f"  あとは管理画面で内容を肉付けして公開してください。")


if __name__ == "__main__":
    main()
