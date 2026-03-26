"""
PA45アンケート自動取得・集計スクリプト

使い方:
  # Graph API経由（GitHub Actions用）
  python scripts/parse-survey.py

  # ローカルファイル指定
  python scripts/parse-survey.py --file "C:/path/to/アンケート.xlsx"

出力: data/surveys/vol-NN.json
"""

import os, sys, io, json, re, argparse
from pathlib import Path
from datetime import date

# ローカル実行時に .env を読み込む
_env_path = Path(__file__).parent.parent / ".env"
if _env_path.exists():
    for _line in _env_path.read_text(encoding="utf-8").splitlines():
        if "=" in _line and not _line.startswith("#"):
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

ROOT       = Path(__file__).parent.parent
OUTPUT_DIR = ROOT / "data" / "surveys"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FILE_OWNER = "ixa_mct@plug136.onmicrosoft.com"
FILE_ID    = "47E8E22E-7B13-4D0C-9181-31D6B9BF9150"

Q_UNDERSTAND = "今日の内容は理解しやすかったですか？"
Q_USEFUL     = "今日の学びは、あなたの業務や生活に役立ちそうですか？\n"
Q_TIME       = "参加しやすい時間帯を教えてください"
Q_CAN        = "今日のPA45で\u201cできるようになったこと\u201dはありますか？（複数選択可）"
Q_COMMENT    = "今回のPA45について感想・コメントを記入お願いします。（運営の励みになります）"


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


def download_excel(token):
    import requests
    url  = f"https://graph.microsoft.com/v1.0/users/{FILE_OWNER}/drive/items/{FILE_ID}/content"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    return io.BytesIO(resp.content)


def count_choices(series):
    counts = {}
    for val in series.dropna():
        for item in str(val).split(";"):
            item = item.strip()
            if item:
                counts[item] = counts.get(item, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


def analyze_session(df_session, vol_num, session_date):
    total    = len(df_session)
    can_do   = count_choices(df_session[Q_CAN])
    comments = [
        str(c).strip() for c in df_session[Q_COMMENT].dropna()
        if len(str(c).strip()) > 5 and str(c).strip().lower() != "nan"
        and "テスト" not in str(c)
    ]

    understand  = df_session[Q_UNDERSTAND].value_counts().to_dict()
    useful      = df_session[Q_USEFUL].value_counts().to_dict()
    time_pref   = df_session[Q_TIME].value_counts().to_dict()

    # 理解度：5択スコア（とても=100, 理解=75, 普通=50, 少し難=25, 難=0）
    U = {
        "とても理解できた": 100,
        "理解できた":       75,
        "普通":             50,
        "少し難しかった":   25,
        "難しかった":        0,
    }
    understand_pct = round(
        sum(understand.get(k, 0) * v for k, v in U.items()) / (total * 100) * 100, 1
    ) if total else 0
    understand_pcts = {k: round(understand.get(k, 0) / total * 100, 1) for k in U} if total else {k: 0 for k in U}

    # 役立ち度：3択スコア（役立ちそう=100, 少し役立ちそう=50, まだイメージがついていない=0）
    F = {
        "役立ちそう":               100,
        "少し役立ちそう":            50,
        "まだイメージがついていない":  0,
    }
    useful_pct  = round(
        sum(useful.get(k, 0) * v for k, v in F.items()) / (total * 100) * 100, 1
    ) if total else 0
    useful_pcts = {k: round(useful.get(k, 0) / total * 100, 1) for k in F} if total else {k: 0 for k in F}

    return {
        "vol":                  vol_num,
        "date":                 str(session_date),
        "total_responses":      total,
        "understanding":        understand,
        "understanding_pct":    understand_pct,
        "understanding_pcts":   understand_pcts,
        "usefulness":           useful,
        "usefulness_pct":       useful_pct,
        "usefulness_pcts":      useful_pcts,
        "time_preference":      time_pref,
        "can_do":               can_do,
        "comments":             comments,
    }


def load_existing_mapping():
    mapping = {}
    for f in sorted(OUTPUT_DIR.glob("vol-*.json")):
        m = re.search(r"vol-(\d+)", f.name)
        if m:
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                date_val = data.get("date")
                if date_val:
                    mapping[str(date_val)] = int(m.group(1))
            except Exception:
                pass
    return mapping


def process(excel_source):
    import pandas as pd

    if isinstance(excel_source, (str, Path)):
        df = pd.read_excel(excel_source)
    else:
        df = pd.read_excel(excel_source)

    df["日付"] = pd.to_datetime(df["開始時刻"]).dt.date

    # 5件以上の日をイベント日とみなす
    date_counts  = df["日付"].value_counts()
    event_dates  = sorted([d for d, c in date_counts.items() if c >= 5])
    print(f"イベント日: {event_dates}")

    existing = load_existing_mapping()
    next_vol = max(existing.values(), default=0) + 1
    updated  = []

    for event_date in event_dates:
        date_str = str(event_date)
        if date_str in existing:
            vol_num = existing[date_str]
            print(f"  Vol.{vol_num} ({date_str}) - 更新")
        else:
            vol_num = next_vol
            next_vol += 1
            print(f"  Vol.{vol_num} ({date_str}) - 新規")

        df_session = df[df["日付"] == event_date].copy()
        result     = analyze_session(df_session, vol_num, event_date)

        out_path = OUTPUT_DIR / f"vol-{vol_num:02d}.json"
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"    → {out_path} ({result['total_responses']}件, 理解度{result['understanding_pct']}%, 役立ち{result['usefulness_pct']}%)")
        updated.append(vol_num)

    print(f"\n完了: Vol.{updated} を更新しました")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default=None, help="ローカルExcelファイルパス（省略時はGraph API使用）")
    args = parser.parse_args()

    if args.file:
        print(f"ローカルファイル読み込み: {args.file}")
        process(args.file)
    else:
        print("Graph API経由でダウンロード中...")
        token      = get_token()
        excel_bytes = download_excel(token)
        process(excel_bytes)


if __name__ == "__main__":
    main()
