"""
Power Automate ブログ記事 下書き4本を WordPress(automate136.com) に作成する。
status=draft で作成。公開はしない。
"""
import sys, io, json, base64
from pathlib import Path
from urllib.request import urlopen, Request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = Path(__file__).parent.parent
AVATAR = "https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png"


def load_env():
    env = {}
    with open(ROOT / ".env", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env


def wp_post(env, payload):
    url = f"{env['WP_URL']}/wp-json/wp/v2/posts"
    creds = base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()
    req = Request(url, data=json.dumps(payload).encode("utf-8"),
                  headers={"Authorization": f"Basic {creds}", "Content-Type": "application/json"},
                  method="POST")
    with urlopen(req) as resp:
        return json.loads(resp.read())


# ---- HTML ヘルパー（Gutenbergブロック） ----
def P(t):  return f"<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->\n\n"
def H2(t): return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{t}</h2>\n<!-- /wp:heading -->\n\n'
def H3(t): return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{t}</h3>\n<!-- /wp:heading -->\n\n'
def SP():  return "&nbsp;\n\n"
def UL(items):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'<!-- wp:list -->\n<ul class="wp-block-list">{li}</ul>\n<!-- /wp:list -->\n\n'
def OL(items):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'<!-- wp:list {{"ordered":true}} -->\n<ol class="wp-block-list">{li}</ol>\n<!-- /wp:list -->\n\n'
def CODE(t):
    return f'<!-- wp:code -->\n<pre class="wp-block-code"><code>{t}</code></pre>\n<!-- /wp:code -->\n\n'
def BLUE(t): return f'<span style="color: #0000ff;"><strong>{t}</strong></span>'
def TODO(t): return f'<!-- wp:paragraph -->\n<p style="background:#fff8e1;border-left:4px solid #f0ad4e;padding:10px 14px;">✍️ <strong>あとで書く</strong>：{t}</p>\n<!-- /wp:paragraph -->\n\n'
def bubble(text):
    return ('<!-- wp:html -->\n'
            '<div class="speech-wrap sb-id-14 sbs-stn sbp-l sbis-cb cf">\n'
            '<div class="speech-person">\n'
            f'<figure class="speech-icon"><img class="speech-icon-image" src="{AVATAR}" alt="" width="1024" height="1024" /></figure>\n'
            '</div>\n'
            f'<div class="speech-balloon">\n{text}\n</div>\n</div>\n'
            '<!-- /wp:html -->\n\n')


# =========================================================
# 記事1：Viva Engage → Teams 通知フロー
# =========================================================
def article1():
    c = ""
    c += P("社内でせっかく Viva Engage（旧 Yammer）を導入しても、「投稿しても誰も見ていない気がする」「気づいたら止まっている」——そんな声をよく聞きます。原因のひとつは、<strong>みんなが Viva Engage を毎日は開かない</strong>こと。逆に Teams は一日中開いています。")
    c += P(f"そこで今回は、{BLUE('Viva Engage に新しい投稿があったら、その本文ごと指定の Teams チャンネルに自動で通知する')}フローを Power Automate で作ります。投稿が Teams に流れてくれば、自然と目に入って反応が増え、結果として Viva Engage の活用も回り始めます。")
    c += bubble("「見てもらえない」を仕組みで解決する回です。社内の活性化担当の方にこそ作ってほしいフローです。")
    c += SP()

    c += H2("このフローでできること")
    c += UL([
        "Viva Engage のコミュニティに投稿が入ると即座に検知",
        "投稿者名・本文・元投稿へのリンクをまとめて Teams に通知",
        "「通知を見て Teams から元投稿に飛ぶ」導線ができる",
    ])
    c += SP()

    c += H2("使うもの")
    c += UL([
        "コネクタ：<strong>Viva Engage</strong>（旧 Yammer）／<strong>Microsoft Teams</strong>",
        "事前準備：通知を流したい Teams のチームとチャンネル／対象の Viva Engage コミュニティ",
    ])
    c += SP()

    c += H2("作り方（4ステップ）")
    c += H3("① トリガー：Viva Engage に投稿が入ったら")
    c += P("「自動化したクラウド フロー」で新規作成し、トリガーに <strong>Viva Engage（Yammer）→「新しいメッセージがグループに投稿されたとき（When there is a new message in a group）」</strong>を選びます。<strong>グループ ID</strong> で監視したいコミュニティを指定します。")
    c += bubble("コネクタ名は環境により「Viva Engage」「Yammer」と表記が分かれます。中身は同じです。")

    c += H3("② 投稿本文を取り出す")
    c += P("トリガーの動的コンテンツに、投稿の <strong>本文（Body）</strong>・<strong>投稿者（Sender / Posted By）</strong>・<strong>Web URL（元投稿へのリンク）</strong> が入っています。次の通知でそのまま差し込みます。")

    c += H3("③ アクション：Teams に投稿する")
    c += P("アクションで <strong>Microsoft Teams →「チャットまたはチャネルでメッセージを投稿する（Post message in a chat or channel）</strong>」を追加します。")
    c += UL([
        "投稿先：<strong>Channel</strong>",
        "チーム／チャネル：通知したい場所を選択",
        "Message：下のテンプレートを貼り、動的コンテンツを差し込む",
    ])
    c += CODE("📣 Viva Engage に新しい投稿があります\n\n投稿者：@{投稿者}\n──────────────\n@{本文}\n──────────────\n▶ 元の投稿を見る：@{Web URL}")
    c += P("（<code>@{ }</code> の部分はキーボード入力ではなく、動的コンテンツから選んで入れてください）")

    c += H3("④ テスト")
    c += P("保存して「テスト」→ 対象コミュニティに試し投稿 → 指定の Teams チャンネルに通知が届けば完成です。")
    c += SP()

    c += H2("うまくいかない時のチェックポイント")
    c += UL([
        "トリガーが動かない：<strong>グループ ID</strong> が正しいか／そのコミュニティに投稿する権限があるか",
        "本文が空：返信ではなく「新規投稿」でテストしているか",
        "Teams に届かない：投稿先が「Channel」になっているか・チーム／チャネルの選択ミスがないか",
    ])
    c += SP()

    c += H2("まとめ")
    c += P("「見てもらえないから盛り上がらない」は、通知の置き場所を変えるだけで大きく変わります。Viva Engage の投稿を Teams に流すこの一本で、社内コミュニケーションの“気づき”を仕組み化できます。")
    c += bubble("PA45 では、こういう“実務でそのまま使える”フローを毎週45分で一緒に作っています。")
    return "【Power Automate】Viva Engageの投稿をTeamsに自動通知して社内を活性化する", c, [76, 78]


# =========================================================
# 記事2：リアクション数ランキング自動発表
# =========================================================
def article2():
    c = ""
    c += P("社内のチャットやコミュニティって、結局のところ <strong>「いいね」やリアクションが付くかどうか</strong>で盛り上がりが決まりますよね。リアクションがないと、投稿した人もだんだん書かなくなる。これは“あるある”です。")
    c += P(f"そこで私が作ったのが、{BLUE('Teams のリアクションを自動でカウントして、週明け月曜にランキングを発表するフロー')}です。一番リアクションを集めた人へ「今週のMVPです！おめでとうございます🎉」と自動でメッセージが届く。これだけで、投稿にもリアクションにも前向きな空気が生まれます。")
    c += bubble("「数えて、たたえる」を自動化する回です。盛り上げ役を人間がやり続けるのは大変なので、仕組みに任せます。")
    c += SP()

    c += H2("このフローの全体像")
    c += OL([
        "毎日（または毎週）対象チャンネルの投稿とリアクションを取得する",
        "投稿者ごとに、集めたリアクション数を合計する",
        "1週間ぶんを集計してランキングを作る",
        "月曜の朝、1位の人へ「おめでとう」メッセージを自動送信する",
    ])
    c += SP()

    c += H2("使うもの")
    c += UL([
        "<strong>スケジュール</strong>（繰り返しトリガー）",
        "<strong>Microsoft Teams</strong>（メッセージ取得・通知）",
        "リアクション数の取得には <strong>Microsoft Graph（HTTP アクション）</strong> を併用すると確実です",
        "週次の集計値をためる場所として <strong>SharePoint リスト</strong> か <strong>Excel/Dataverse</strong>",
    ])
    c += bubble("標準コネクタだけだとリアクション数は取りにくいので、Graph を一度だけ通すのがコツです。ここは少し中級者向けです。")
    c += SP()

    c += H2("作り方の流れ")
    c += H3("① 毎日の集計フロー")
    c += UL([
        "トリガー：<strong>スケジュール（例：毎日 18:00）</strong>",
        "対象チャンネルのメッセージ一覧を取得",
        "各メッセージのリアクション（いいね等）を取得し、<strong>投稿者ごとに件数を加算</strong>",
        "その日の集計を SharePoint リスト等に「氏名・日付・リアクション数」で記録",
    ])
    c += TODO("実際に使っている Graph のエンドポイント（/teams/{id}/channels/{id}/messages など）と、集計ロジックの具体ステップをここに貼る。はる本人の実装画面のスクショも入れると分かりやすい。")

    c += H3("② 月曜のランキング発表フロー")
    c += UL([
        "トリガー：<strong>スケジュール（毎週月曜 9:00）</strong>",
        "直近1週間ぶんの記録を取得し、<strong>氏名ごとに合計</strong>",
        "合計が最大の人（＝今週のMVP）を特定",
        "その人へ Teams で「おめでとう」メッセージを送信＋チャンネルにもランキングを投稿",
    ])
    c += CODE("🏆 今週のリアクションMVP発表！\n\n🥇 1位：@{1位の人}（@{合計数} リアクション）\n🥈 2位：…\n🥉 3位：…\n\n今週もたくさんの反応をありがとうございました！\n来週もお気軽に投稿・リアクションしてくださいね😊")
    c += SP()

    c += H2("作ってみて感じた効果")
    c += UL([
        "「リアクションすること」自体が前向きな行動として可視化される",
        "発表が楽しみになり、投稿のハードルが下がる",
        "盛り上げ役を人がやり続けなくても、空気が自走しはじめる",
    ])
    c += TODO("実際にこのフローを回してみての社内の反応・変化を、ここに正直に書く（盛らずに）。")
    c += SP()

    c += H2("まとめ")
    c += P("リアクションは「気持ち」ですが、集計して発表するのは「仕組み」でできます。Power Automate に“盛り上げ役”を一部任せることで、コミュニティは続きやすくなります。")
    c += bubble("少し背伸びするフローですが、効果は抜群。詰まったら PA45 で一緒に分解しましょう。")
    return "【Power Automate】Teamsのリアクションを自動集計して「今週のMVP」を発表する仕組み", c, [76, 78]


# =========================================================
# 記事3：書籍レビュー（PAD × Copilot 新刊）
# =========================================================
def article3():
    c = ""
    c += P("インプレスさんから発売された Power Automate for Desktop × Copilot の新刊を、ご縁あって献本いただきました。読んでみて「これは良いな」と感じたポイントを、自分なりの視点で20個に絞って紹介します。")
    c += TODO("書籍の正式タイトル・著者名（あーちゃんさん）・出版社（インプレス）・発売日・Amazon等のリンクを正確に記入する。表紙画像も差し込む。")
    c += bubble("献本いただいた一冊を、忖度なしで「自分が良いと思ったところ」だけ挙げていきます。")
    c += SP()

    c += H2("この本がおすすめな人")
    c += UL([
        "Power Automate for Desktop（PAD）をこれから始めたい人",
        "PAD は触っているけど Copilot をまだ活かせていない人",
        "デスクトップ自動化を社内に広げたい推進担当者",
    ])
    c += TODO("上記3つは仮。読んだ感触で書き換える。")
    c += SP()

    c += H2("自分的に良かったポイント20")
    c += P("（※各見出しに、本のどこが・なぜ良かったかを2〜4行で。引用は最小限・自分の言葉で）")
    for i in range(1, 21):
        c += H3(f"{i}. （良かったポイント{i}）")
        c += TODO("ここに具体的に何が良かったか／どんな場面で効くかを書く。")
    c += SP()

    c += H2("まとめ")
    c += TODO("20個を振り返って、一番刺さった点・どんな人に勧めたいかで締める。")
    c += bubble("あーちゃんさん、素敵な一冊をありがとうございました。")
    return "【書評】あーちゃんさんの新刊『Power Automate for Desktop × Copilot』を読んで良かった20のポイント", c, [76]


# =========================================================
# 記事4：なんでもCopilot大阪 登壇記（感謝の日記）
# =========================================================
def article4():
    c = ""
    c += P("「なんでもCopilot 大阪会」で登壇させていただきました。終わってからも余韻が続いていて、とにかく良いことがたくさんあった一日でした。うまくまとめるというより、感じたこと・やったことを日記のように残しておきます。そして何より、運営のみなさんへの感謝を伝えたくて書いています。")
    c += bubble("きれいな登壇レポートというより、正直な気持ちの記録です。")
    c += SP()

    c += H2("登壇したこと")
    c += TODO("当日のセッションタイトル・話した内容・持ち時間をここに。スライドや写真があれば差し込む。")
    c += SP()

    c += H2("当日うれしかったこと")
    c += TODO("会場の雰囲気・声をかけてもらったこと・印象に残った会話など、実際にあった出来事を時系列か箇条書きで。盛らずに、覚えている範囲で。")
    c += SP()

    c += H2("学んだこと・刺激を受けたこと")
    c += TODO("他の登壇者・参加者から受けた刺激、自分の中で言語化できた気づきを書く。")
    c += SP()

    c += H2("運営のみなさんへ")
    c += P("こうした場は、当たり前に存在しているわけではなくて、準備・告知・当日運営まで、たくさんの方の手で支えられて初めて成り立っています。登壇者として呼んでいただけたこと、そして安心して話せる空気を作ってくださったことに、心から感謝しています。")
    c += TODO("運営者のお名前（出してよい方のみ）や、特に助けられた具体的な場面を添えると感謝がより伝わる。")
    c += bubble("声をかけてくださったみなさん、運営のみなさん、本当にありがとうございました。また会いに行きます。")
    c += SP()

    c += H2("これからのこと")
    c += TODO("この登壇を受けて次にやりたいこと・つながりたい気持ちを一言で締める。")
    return "「なんでもCopilot 大阪」で登壇してきました ― 感謝をこめた登壇日記", c, [77]


def main():
    env = load_env()
    builders = [article1, article2, article3, article4]
    print("▶ WordPress(automate136.com) に下書き4本を作成します\n")
    for b in builders:
        title, content, cats = b()
        payload = {"title": title, "content": content, "status": "draft", "categories": cats}
        res = wp_post(env, payload)
        pid = res["id"]
        print(f"  ✅ [{pid}] {title}")
        print(f"     編集: {env['WP_URL']}/wp-admin/post.php?post={pid}&action=edit\n")
    print("完了。すべて下書き(draft)です。公開はしていません。")


if __name__ == "__main__":
    main()
