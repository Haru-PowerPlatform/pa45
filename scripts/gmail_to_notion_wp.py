#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail[自己検証] → Notion ネタ帳 → Claude下書き → WordPress

毎朝 JST 07:00 に実行（GitHub Actions cron: UTC 22:00 前日）
件名に [自己検証] を含むメールを処理する。
"""

import sys, io, os, json, re, base64, tempfile
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── 設定 ─────────────────────────────────────────────────────────────────────
NOTION_TOKEN  = os.environ["NOTION_TOKEN"]
NOTION_DB_ID  = os.environ.get("NOTION_DB_ID", "13656c494f674c83b63d7b8d543da5d3")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
WP_URL        = os.environ.get("WP_URL", "")
WP_USER       = os.environ.get("WP_USER", "")
WP_PASS       = os.environ.get("WP_APP_PASSWORD", "")

GMAIL_LABEL   = "自己検証"   # Gmailのラベル名
SUBJECT_PREFIX = "[自己検証]"

JST = timezone(timedelta(hours=9))

# ── Gmail認証 ────────────────────────────────────────────────────────────────
def get_gmail_service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    creds_json  = os.environ["GMAIL_CREDENTIALS"]
    token_json  = os.environ["GMAIL_TOKEN"]

    creds_data  = json.loads(creds_json)
    token_data  = json.loads(token_json)

    creds = Credentials(
        token         = token_data["token"],
        refresh_token = token_data["refresh_token"],
        token_uri     = token_data["token_uri"],
        client_id     = creds_data["installed"]["client_id"],
        client_secret = creds_data["installed"]["client_secret"],
        scopes        = token_data["scopes"],
    )
    return build("gmail", "v1", credentials=creds)

# ── Gmail: 未処理メール取得 ───────────────────────────────────────────────────
def fetch_new_emails(service):
    """[自己検証]ラベルがついた未読メールを取得"""
    query = f"label:{GMAIL_LABEL} is:unread"
    result = service.users().messages().list(userId="me", q=query).execute()
    messages = result.get("messages", [])
    print(f"未処理メール数: {len(messages)}")

    emails = []
    for msg_ref in messages:
        msg = service.users().messages().get(
            userId="me", id=msg_ref["id"], format="full"
        ).execute()

        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        subject = headers.get("Subject", "（件名なし）")
        date    = headers.get("Date", "")
        body    = extract_body(msg["payload"])

        emails.append({
            "id":      msg_ref["id"],
            "subject": subject,
            "date":    date,
            "body":    body,
        })
    return emails

def extract_body(payload):
    """メール本文（text/plain）を取得"""
    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")

    for part in payload.get("parts", []):
        if part["mimeType"] == "text/plain":
            data = part.get("body", {}).get("data", "")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
        if part.get("parts"):
            result = extract_body(part)
            if result:
                return result
    return ""

def mark_as_read(service, msg_id):
    service.users().messages().modify(
        userId="me", id=msg_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()

# ── Notion: ネタ帳に追加 ──────────────────────────────────────────────────────
def add_to_notion(subject, body, source="Gmailから"):
    """ネタ帳DBにページを追加し、作成したページIDを返す"""
    # 件名から[自己検証]プレフィックスを除去してカテゴリを推測
    clean_subject = re.sub(r'^\[自己検証\]\s*', '', subject).strip()
    category = guess_category(clean_subject)

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type":  "application/json",
        "Notion-Version": "2022-06-28",
    }
    payload = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "メモ": {
                "title": [{"text": {"content": clean_subject}}]
            },
            "カテゴリ": {
                "select": {"name": category}
            },
            "ソース": {
                "select": {"name": source}
            },
            "下書き済み": {
                "checkbox": False
            },
            "メモ詳細": {
                "rich_text": [{"text": {"content": body[:2000]}}]  # Notion上限
            },
        }
    }

    resp = requests.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json=payload,
    )
    resp.raise_for_status()
    page_id = resp.json()["id"]
    print(f"  Notion追加完了: {clean_subject} (ID: {page_id})")
    return page_id

def guess_category(subject: str) -> str:
    """件名からカテゴリを推測"""
    kws = {
        "PA45":    ["PA45", "pa45"],
        "フロー":   ["フロー", "Power Automate", "Automate", "自動化"],
        "PLUG":    ["PLUG", "プラグ"],
        "ふみだせTV": ["ふみだせ", "登壇", "LT"],
        "生成AI×PA":  ["生成AI", "ChatGPT", "GPT", "Claude", "AI"],
        "社内講座":  ["社内", "講座", "研修"],
    }
    for cat, words in kws.items():
        if any(w in subject for w in words):
            return cat
    return "気づき・考察"

# ── Notion: 下書きURL更新 ─────────────────────────────────────────────────────
def update_notion_draft(page_id, wp_url):
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type":  "application/json",
        "Notion-Version": "2022-06-28",
    }
    payload = {
        "properties": {
            "下書きURL": {"url": wp_url},
            "下書き済み": {"checkbox": True},
        }
    }
    resp = requests.patch(
        f"https://api.notion.com/v1/pages/{page_id}",
        headers=headers,
        json=payload,
    )
    resp.raise_for_status()
    print(f"  NotionURL更新完了: {wp_url}")

# ── Claude API: ブログ下書き生成 ──────────────────────────────────────────────
def generate_blog_draft(subject, memo_body):
    """Claude APIでブログ記事の下書きを生成（HTMLブロック形式）"""
    import anthropic

    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

    prompt = f"""以下の自己検証メモをもとに、Power Automateユーザー向けブログ記事の下書きをWordPress Gutenbergブロック形式で書いてください。

【件名】{subject}
【メモ内容】
{memo_body}

【執筆ルール】
- 対象読者: Power Automateを使い始めた社会人
- 文体: 体験ベース、話しかけるような口語体（ですます調）
- 構成: 導入→課題→解決策→手順→まとめ
- 文字数: 800〜1200字
- コードや設定値は <code> タグで囲む
- 見出しはh2/h3を使う
- WordPressブロック記法（<!-- wp:paragraph -->等）で出力

タイトル候補も3つ提案してください。"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

# ── WordPress: 下書き保存 ──────────────────────────────────────────────────────
def save_to_wordpress(title, content):
    """WordPressに下書きとして保存し、編集URLを返す"""
    url  = f"{WP_URL}/wp-json/wp/v2/posts"
    auth = (WP_USER, WP_PASS)

    payload = {
        "title":   title,
        "content": content,
        "status":  "draft",
    }
    resp = requests.post(url, auth=auth, json=payload)
    resp.raise_for_status()

    post_id  = resp.json()["id"]
    edit_url = f"{WP_URL}/wp-admin/post.php?post={post_id}&action=edit"
    print(f"  WordPress下書き保存完了: post_id={post_id}")
    return edit_url

# ── メイン ────────────────────────────────────────────────────────────────────
def main():
    service = get_gmail_service()
    emails  = fetch_new_emails(service)

    if not emails:
        print("新しいメールはありません")
        return

    for email in emails:
        subject = email["subject"]
        body    = email["body"].strip()
        print(f"\n処理中: {subject}")

        # 1. Notionに追加
        page_id = add_to_notion(subject, body)

        # 2. Claude APIで下書き生成（APIキーがある場合のみ）
        if ANTHROPIC_KEY and WP_URL:
            try:
                clean_title = re.sub(r'^\[自己検証\]\s*', '', subject).strip()
                blog_content = generate_blog_draft(clean_title, body)

                # タイトル候補の1番目を抽出（簡易）
                title_match = re.search(r'【タイトル[^】]*】[^\n]*\n(.+)', blog_content)
                title = title_match.group(1).strip() if title_match else clean_title

                # 3. WordPressに下書き保存
                wp_edit_url = save_to_wordpress(title, blog_content)

                # 4. NotionのURL更新
                update_notion_draft(page_id, wp_edit_url)

            except Exception as e:
                print(f"  ブログ生成エラー（スキップ）: {e}")
        else:
            print("  ANTHROPIC_API_KEY or WP_URL 未設定 → Notionのみ保存")

        # 5. Gmailを既読にする
        mark_as_read(service, email["id"])
        print(f"  既読化完了: {subject}")

    print(f"\n処理完了: {len(emails)}件")

if __name__ == "__main__":
    main()
