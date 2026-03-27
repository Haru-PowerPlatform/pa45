"""
PA45 バッジ自動送信スクリプト

使い方:
  python scripts/send-badges.py --session 4
  python scripts/send-badges.py --session 4 --dry-run   ← 送信せず確認だけ

必要な .env 設定:
  BADGE_FORMS_FILE_ID=<FormsのExcelファイルID（OneDrive上）>
  SMTP_USER=<送信元メールアドレス>
  SMTP_PASSWORD=<Outlookアプリパスワード>
  NEXT_CONNPASS_URL=<次回connpassのURL>
  MS_TENANT_ID=<既存設定>
  MS_CLIENT_ID=<既存設定>
  MS_CLIENT_SECRET=<既存設定>

安全装置:
  - assets/badges/session-XXX/badge.png が存在しない場合は即終了（送信しない）
  - data/badge-sent/session-XXX.json で送信済みを記録 → 重複送信防止
  - --dry-run で実際に送信せず確認可能
"""

import os, sys, json, base64, argparse, smtplib, io
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# ─── 設定 ────────────────────────────────────────
_env_path = Path(__file__).parent.parent / ".env"
if _env_path.exists():
    for _line in _env_path.read_text(encoding="utf-8").splitlines():
        if "=" in _line and not _line.startswith("#"):
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

ROOT = Path(__file__).parent.parent

SMTP_HOST = "smtp.office365.com"
SMTP_PORT = 587

# ─── グラフAPIトークン取得（既存と同じ） ────────
def get_token():
    import requests
    resp = requests.post(
        f"https://login.microsoftonline.com/{os.environ['MS_TENANT_ID']}/oauth2/v2.0/token",
        data={
            "grant_type":    "client_credentials",
            "client_id":     os.environ["MS_CLIENT_ID"],
            "client_secret": os.environ["MS_CLIENT_SECRET"],
            "scope":         "https://graph.microsoft.com/.default",
        }
    )
    resp.raise_for_status()
    return resp.json()["access_token"]

# ─── FormsのExcelからメールアドレスを取得 ────────
def get_emails_from_forms_excel(session_num: int, token: str) -> list[dict]:
    """
    FormsのExcel（OneDrive上）を読み込み、メールアドレス一覧を返す。
    Excelの構成を想定:
      列A: タイムスタンプ
      列B: メールアドレス（「メールアドレスを入力してください」列）
      （他の列は無視）
    """
    import requests
    try:
        import openpyxl
    except ImportError:
        print("ERROR: openpyxl が必要です → pip install openpyxl")
        sys.exit(1)

    file_id = os.environ.get("BADGE_FORMS_FILE_ID")
    file_owner = os.environ.get("BADGE_FORMS_FILE_OWNER",
                                os.environ.get("MS_FILE_OWNER", "ixa_mct@plug136.onmicrosoft.com"))

    if not file_id:
        print("ERROR: .env に BADGE_FORMS_FILE_ID が未設定です")
        print("  → Formsの「Excelで開く」でOneDriveに保存し、そのファイルIDを設定してください")
        sys.exit(1)

    url = f"https://graph.microsoft.com/v1.0/users/{file_owner}/drive/items/{file_id}/content"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()

    wb = openpyxl.load_workbook(io.BytesIO(resp.content))
    ws = wb.active

    # ヘッダー行を探す
    headers = [cell.value for cell in ws[1]]
    email_col = None
    for i, h in enumerate(headers):
        if h and ("メール" in str(h) or "mail" in str(h).lower() or "email" in str(h).lower()):
            email_col = i
            break

    if email_col is None:
        print(f"ERROR: メールアドレス列が見つかりません")
        print(f"  ヘッダー: {headers}")
        print("  → FormsにE-mail列を追加し、Excelを再リンクしてください")
        sys.exit(1)

    results = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        email = row[email_col] if len(row) > email_col else None
        if email and "@" in str(email):
            results.append({
                "email": str(email).strip(),
                "timestamp": str(row[0]) if row[0] else "",
            })

    print(f"  Forms回答: {len(results)}件のメールアドレスを取得")
    return results

# ─── 送信済みの記録 ──────────────────────────────
def load_sent_log(session_num: int) -> set:
    sent_file = ROOT / "data" / "badge-sent" / f"session-{session_num:03d}.json"
    if sent_file.exists():
        data = json.loads(sent_file.read_text(encoding="utf-8"))
        return set(data.get("sent", []))
    return set()

def save_sent_log(session_num: int, sent_emails: set):
    sent_dir = ROOT / "data" / "badge-sent"
    sent_dir.mkdir(parents=True, exist_ok=True)
    sent_file = sent_dir / f"session-{session_num:03d}.json"
    existing = load_sent_log(session_num)
    all_sent = sorted(existing | sent_emails)
    sent_file.write_text(
        json.dumps({"session": session_num, "sent": all_sent, "updated": datetime.now().isoformat()},
                   ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

# ─── メール送信 ──────────────────────────────────
def send_email(to_email: str, session_num: int, badge_path: Path, dry_run: bool = False):
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASSWORD", "")
    next_url  = os.environ.get("NEXT_CONNPASS_URL", "https://connpass.com/group/powerautomate-create/")

    subject = f"【PA45 第{session_num}回】ご参加ありがとうございました！"

    body_html = f"""
<p>こんにちは！</p>

<p>本日は <strong>PA45 第{session_num}回</strong> にご参加いただき、ありがとうございました！<br>
今日学んだことを、ぜひ明日の業務でひとつ試してみてください。</p>

<hr>

<p>🏅 <strong>参加バッジを添付しました</strong><br>
XなどのSNSでシェアしていただけると嬉しいです！<br>
ハッシュタグ: <strong>#PA45</strong></p>

<hr>

<p>📅 <strong>次回のPA45はこちら</strong><br>
<a href="{next_url}">{next_url}</a></p>

<p>またお会いしましょう！</p>
<p>— PA45 運営 Haru</p>
"""

    if dry_run:
        print(f"  [DRY-RUN] → {to_email} : {subject}")
        return

    msg = MIMEMultipart()
    msg["From"]    = smtp_user
    msg["To"]      = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body_html, "html", "utf-8"))

    # バッジ画像を添付
    with open(badge_path, "rb") as f:
        part = MIMEBase("image", "png")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition",
                        f'attachment; filename="PA45_badge_{session_num:03d}.png"')
        msg.attach(part)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(smtp_user, smtp_pass)
        smtp.sendmail(smtp_user, to_email, msg.as_string())

# ─── メイン ──────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="PA45 バッジ自動送信")
    parser.add_argument("--session", type=int, required=True, help="回数（例: 4）")
    parser.add_argument("--dry-run", action="store_true", help="送信せず確認だけ")
    args = parser.parse_args()

    session_num = args.session
    dry_run     = args.dry_run
    badge_dir   = ROOT / "assets" / "badges" / f"session-{session_num:03d}"

    print(f"\n=== PA45 第{session_num}回 バッジ送信 {'[DRY-RUN]' if dry_run else ''} ===")

    # ─── 安全装置：バッジ画像の存在確認 ──────────────
    badge_path = None
    for ext in ["png", "jpg", "jpeg"]:
        candidate = badge_dir / f"badge.{ext}"
        if candidate.exists():
            badge_path = candidate
            break

    if badge_path is None:
        print(f"\n❌ バッジ画像が見つかりません！送信を中止します。")
        print(f"   配置してください: {badge_dir}/badge.png")
        sys.exit(1)

    print(f"✅ バッジ画像確認: {badge_path}")

    # ─── 送信済み記録を読み込み ────────────────────
    already_sent = load_sent_log(session_num)
    print(f"   送信済み: {len(already_sent)}件")

    # ─── Formsからメールアドレス取得 ──────────────
    print("\n📋 Forms回答を取得中...")
    token   = get_token()
    entries = get_emails_from_forms_excel(session_num, token)

    # ─── 未送信の絞り込み ─────────────────────────
    to_send = [e for e in entries if e["email"].lower() not in {s.lower() for s in already_sent}]
    print(f"   未送信: {len(to_send)}件")

    if not to_send:
        print("\n✅ 全員に送信済みです。")
        return

    # ─── 送信 ────────────────────────────────────
    print(f"\n{'📤 送信プレビュー' if dry_run else '📤 送信中'}...")
    newly_sent = set()
    errors = []

    for i, entry in enumerate(to_send, 1):
        email = entry["email"]
        try:
            send_email(email, session_num, badge_path, dry_run)
            print(f"  [{i}/{len(to_send)}] ✅ {email}")
            newly_sent.add(email)
        except Exception as e:
            print(f"  [{i}/{len(to_send)}] ❌ {email} → {e}")
            errors.append(email)

    # ─── 送信済み記録を保存 ───────────────────────
    if newly_sent and not dry_run:
        save_sent_log(session_num, newly_sent)

    # ─── 結果サマリー ─────────────────────────────
    print(f"\n=== 完了 ===")
    print(f"  送信成功: {len(newly_sent)}件")
    if errors:
        print(f"  送信失敗: {len(errors)}件 → {errors}")
    if dry_run:
        print("  ※ DRY-RUNのため実際には送信していません")

if __name__ == "__main__":
    main()
