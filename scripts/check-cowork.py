#!/usr/bin/env python3
"""
Copilot Cowork (Frontier) 可用性チェックスクリプト
毎日実行してCoworkがテナントに届いたらGmailで通知する
"""

import os
import sys
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_access_token(tenant_id, client_id, client_secret):
    """Microsoft Graph API アクセストークンを取得"""
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
    }
    resp = requests.post(url, data=data, timeout=30)
    resp.raise_for_status()
    return resp.json()["access_token"]


def check_cowork_available(token):
    """
    Teams アプリカタログでCowork (Frontier)を検索する
    Returns: True if found, False otherwise
    """
    headers = {"Authorization": f"Bearer {token}"}

    # テナントのエージェントレジストリを検索
    url = (
        "https://graph.microsoft.com/v1.0/appCatalogs/teamsApps"
        "?$filter=contains(displayName,'Cowork')"
        "&$select=id,displayName,distributionMethod"
    )
    resp = requests.get(url, headers=headers, timeout=30)

    if resp.status_code == 200:
        apps = resp.json().get("value", [])
        for app in apps:
            name = app.get("displayName", "")
            if "Cowork" in name and "Frontier" in name:
                print(f"✅ 発見: {name} (ID: {app.get('id')})")
                return True, app
        print(f"❌ Coworkは見つかりませんでした（検索結果: {len(apps)}件）")
        return False, None
    else:
        print(f"⚠️ API呼び出し失敗: {resp.status_code} - {resp.text[:200]}")
        # 権限不足の場合はNoneを返してスキップ
        return None, None


def send_gmail(subject, body):
    """Gmail SMTPでメール送信"""
    email_from = os.environ["EMAIL_FROM"]
    email_password = os.environ["EMAIL_PASSWORD"]
    email_to = os.environ["EMAIL_TO"]

    msg = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = email_to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_from, email_password)
        server.send_message(msg)
    print(f"📧 メール送信完了: {email_to}")


def main():
    tenant_id = os.environ.get("MS_TENANT_ID")
    client_id = os.environ.get("MS_CLIENT_ID")
    client_secret = os.environ.get("MS_CLIENT_SECRET")

    if not all([tenant_id, client_id, client_secret]):
        print("❌ MS_TENANT_ID / MS_CLIENT_ID / MS_CLIENT_SECRET が設定されていません")
        sys.exit(1)

    print("🔍 Microsoft Graph API でCowork (Frontier)を検索中...")
    token = get_access_token(tenant_id, client_id, client_secret)
    found, app_info = check_cowork_available(token)

    if found is True:
        print("🎉 Cowork (Frontier) がテナントに届きました！")
        subject = "🎉 Copilot Cowork (Frontier) が使えるようになりました！"
        body = f"""はるさん、

Copilot Cowork (Frontier) がテナントに届きました！

▼ 有効化の手順（あと2ステップ）：
1. 管理センター → エージェント → すべてのエージェント
   https://admin.cloud.microsoft/#/agents/all

2. 「Cowork (Frontier)」をクリック → 展開ウィザード
   → 「すべてのユーザー」を選択 → 次へ → Review & finish

アプリ情報:
- 名前: {app_info.get('displayName')}
- ID: {app_info.get('id')}

設定完了後、M365 CopilotアプリのエージェントストアでCoworkが使えます。

（このメールはGitHub Actionsの自動チェックによって送信されました）
"""
        send_gmail(subject, body)

    elif found is False:
        print("Coworkはまだ届いていません。明日また確認します。")
        # 見つからない場合はメール送信しない（毎日届くと邪魔なので）

    else:
        # API権限不足などのエラー
        print("⚠️ チェック結果が不明です。手動で確認してください。")


if __name__ == "__main__":
    main()
