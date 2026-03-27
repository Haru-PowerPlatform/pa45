"""
PA45 バッジ自動送信スクリプト

使い方:
  python scripts/send-badges.py --session 4
  python scripts/send-badges.py --session 4 --date 2026-04-02        ← 開催日を明示
  python scripts/send-badges.py --session 4 --dry-run                ← 送信せず確認

必要な .env 設定:
  BADGE_FORMS_FILE_ID=<FormsのExcelファイルID（OneDrive上）>
  BADGE_FORMS_FILE_OWNER=ixa_mct@plug136.onmicrosoft.com
  SMTP_USER=<送信元メールアドレス>
  SMTP_PASSWORD=<Outlookアプリパスワード>
  NEXT_CONNPASS_URL=<次回connpassのURL>
  MS_TENANT_ID=<既存設定>
  MS_CLIENT_ID=<既存設定>
  MS_CLIENT_SECRET=<既存設定>

安全装置:
  - assets/badges/session-XXX/badge.png が存在しない場合は即終了
  - 指定した日付（--date）の回答のみを対象にする
  - data/badge-sent/session-XXX.json で送信済みを記録 → 重複送信防止
  - --dry-run で実際に送信せず確認可能
"""

import os, sys, json, argparse, smtplib, io
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, date

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

# ─── グラフAPIトークン取得 ───────────────────────
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
def get_emails_from_forms_excel(token: str, target_date: date) -> list[dict]:
    """
    FormsのExcel（OneDrive上）を読み込み、
    target_dateの日付に回答したメールアドレス一覧を返す。

    Excelの列構成（Formsの自動生成）:
      列0: 開始時刻（タイムスタンプ）
      列1: 完了時刻
      列2: メール（名前）
      列3以降: 各質問の回答
    ※ メールアドレス列の列名はFormsの設定によって異なる
    """
    import requests
    try:
        import openpyxl
    except ImportError:
        print("ERROR: openpyxl が必要です → pip install openpyxl")
        sys.exit(1)

    file_id    = os.environ.get("BADGE_FORMS_FILE_ID", "").strip()
    file_owner = os.environ.get("BADGE_FORMS_FILE_OWNER", "ixa_mct@plug136.onmicrosoft.com").strip()

    if not file_id or file_id.startswith("←"):
        print("ERROR: .env に BADGE_FORMS_FILE_ID が設定されていません")
        print("  → Formsの「Excelで開く」でOneDriveに保存し、そのファイルIDを設定してください")
        sys.exit(1)

    url  = f"https://graph.microsoft.com/v1.0/users/{file_owner}/drive/items/{file_id}/content"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()

    wb = openpyxl.load_workbook(io.BytesIO(resp.content))
    ws = wb.active

    # ヘッダー行でメールアドレス列を探す
    headers = [str(cell.value or "").strip() for cell in ws[1]]
    email_col   = None
    ts_col      = 0   # タイムスタンプは通常0列目（開始時刻）

    for i, h in enumerate(headers):
        if any(kw in h.lower() for kw in ["メール", "mail", "email", "e-mail"]):
            email_col = i
            break

    if email_col is None:
        print("ERROR: メールアドレス列が見つかりません")
        print(f"  ヘッダー: {headers}")
        print("  → FormsにE-mailアドレスの質問を追加し、Excelを再リンクしてください")
        sys.exit(1)

    print(f"  列構成: タイムスタンプ=[{headers[ts_col]}] メール=[{headers[email_col]}]")
    print(f"  絞り込み日: {target_date}")

    all_count   = 0
    date_matched = []

    for row in ws.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue
        all_count += 1

        # タイムスタンプから日付を抽出
        ts = row[ts_col] if len(row) > ts_col else None
        if isinstance(ts, datetime):
            row_date = ts.date()
        elif isinstance(ts, date):
            row_date = ts
        elif ts and str(ts):
            # 文字列の場合、日付部分をパース
            try:
                row_date = datetime.fromisoformat(str(ts)[:10]).date()
            except ValueError:
                row_date = None
        else:
            row_date = None

        # ── 日付フィルター（開催日の回答のみ） ──
        if row_date != target_date:
            continue

        email = row[email_col] if len(row) > email_col else None
        if email and "@" in str(email):
            date_matched.append({
                "email":     str(email).strip(),
                "timestamp": str(ts) if ts else "",
            })

    print(f"  Forms回答: 全{all_count}件 → {target_date}の回答: {len(date_matched)}件")
    return date_matched

# ─── 送信済みの記録 ──────────────────────────────
def load_sent_log(session_num: int) -> set:
    sent_file = ROOT / "data" / "badge-sent" / f"session-{session_num:03d}.json"
    if sent_file.exists():
        data = json.loads(sent_file.read_text(encoding="utf-8"))
        return set(data.get("sent", []))
    return set()

def save_sent_log(session_num: int, sent_emails: set):
    sent_dir  = ROOT / "data" / "badge-sent"
    sent_dir.mkdir(parents=True, exist_ok=True)
    sent_file = sent_dir / f"session-{session_num:03d}.json"
    existing  = load_sent_log(session_num)
    all_sent  = sorted(existing | sent_emails)
    sent_file.write_text(
        json.dumps(
            {"session": session_num, "sent": all_sent, "updated": datetime.now().isoformat()},
            ensure_ascii=False, indent=2
        ),
        encoding="utf-8"
    )

# ─── メール送信 ──────────────────────────────────
def send_email(to_email: str, session_num: int, badge_path: Path, dry_run: bool = False):
    smtp_user = os.environ.get("SMTP_USER", "").strip()
    smtp_pass = os.environ.get("SMTP_PASSWORD", "").strip()
    next_url  = os.environ.get("NEXT_CONNPASS_URL",
                               "https://connpass.com/group/powerautomate-create/").strip()

    if not smtp_user or smtp_user.startswith("←"):
        print("ERROR: .env に SMTP_USER が設定されていません")
        sys.exit(1)

    subject = f"【PA45 第{session_num}回】ご参加ありがとうございました！"

    body_html = f"""\
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
        print(f"  [DRY-RUN] → {to_email}")
        return

    msg = MIMEMultipart()
    msg["From"]    = smtp_user
    msg["To"]      = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body_html, "html", "utf-8"))

    # バッジ画像を添付
    ext = badge_path.suffix.lstrip(".")
    with open(badge_path, "rb") as f:
        part = MIMEBase("image", ext)
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition",
                        f'attachment; filename="PA45_badge_{session_num:03d}.{ext}"')
        msg.attach(part)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(smtp_user, smtp_pass)
        smtp.sendmail(smtp_user, to_email, msg.as_string())

# ─── メイン ──────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="PA45 バッジ自動送信")
    parser.add_argument("--session", type=int, required=True,
                        help="回数（例: 4）")
    parser.add_argument("--date", type=str, default=None,
                        help="開催日 YYYY-MM-DD（省略時は今日）")
    parser.add_argument("--dry-run", action="store_true",
                        help="送信せず確認だけ")
    args = parser.parse_args()

    session_num = args.session
    dry_run     = args.dry_run
    badge_dir   = ROOT / "assets" / "badges" / f"session-{session_num:03d}"

    # 開催日の解決
    if args.date:
        try:
            target_date = date.fromisoformat(args.date)
        except ValueError:
            print(f"ERROR: 日付の形式が不正です（例: 2026-04-02）")
            sys.exit(1)
    else:
        target_date = date.today()

    print(f"\n=== PA45 第{session_num}回 バッジ送信 {'[DRY-RUN]' if dry_run else ''} ===")
    print(f"  対象開催日: {target_date}")

    # ─── 安全装置①：バッジ画像の存在確認 ────────
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

    print(f"✅ バッジ画像: {badge_path}")

    # ─── 送信済み記録を読み込み ────────────────────
    already_sent = load_sent_log(session_num)
    print(f"✅ 送信済み記録: {len(already_sent)}件")

    # ─── Formsから開催日の回答を取得 ──────────────
    print("\n📋 Forms回答を取得中...")
    token   = get_token()
    entries = get_emails_from_forms_excel(token, target_date)

    if not entries:
        print(f"\n⚠️  {target_date} のアンケート回答が0件です。")
        print("   日付が合っているか確認してください（--date YYYY-MM-DD で指定）")
        return

    # ─── 安全装置②：重複送信チェック ──────────────
    to_send = [e for e in entries
               if e["email"].lower() not in {s.lower() for s in already_sent}]

    skipped = len(entries) - len(to_send)
    if skipped:
        print(f"   ※ 送信済みのためスキップ: {skipped}件")
    print(f"   送信予定: {len(to_send)}件")

    if not to_send:
        print("\n✅ 全員に送信済みです。")
        return

    # ─── 送信 ────────────────────────────────────
    print(f"\n{'📤 送信プレビュー' if dry_run else '📤 送信中'}...")
    newly_sent = set()
    errors     = []

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
        print(f"  送信失敗: {len(errors)}件")
        for e in errors:
            print(f"    - {e}")
    if dry_run:
        print("  ※ DRY-RUNのため実際には送信していません")

if __name__ == "__main__":
    main()
