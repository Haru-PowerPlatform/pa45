"""
PA45 アンケートExcelファイルを解析してJSONに変換するスクリプト

使い方:
  python scripts/parse-survey.py --vol 1 --date 2026-03-05 --file "C:/path/to/アンケート.xlsx"
  python scripts/parse-survey.py --vol 2 --date 2026-03-12 --file "C:/path/to/アンケート.xlsx"
  # --date 省略時は全行を対象にする

出力: data/surveys/vol-N.json
"""
import sys
import io
import json
import argparse
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
SURVEYS_DIR = ROOT / "data" / "surveys"
SURVEYS_DIR.mkdir(parents=True, exist_ok=True)

# テスト回答を除外するキーワード
TEST_KEYWORDS = ["テスト", "test", "dummy"]


def is_test_response(row):
    comment_col = next((c for c in row.index if "感想" in str(c) or "コメント" in str(c)), None)
    if comment_col:
        val = str(row.get(comment_col, "")).strip().lower()
        if any(kw in val for kw in TEST_KEYWORDS):
            return True
    return False


def count_choices(series):
    """複数選択肢の集計（セミコロン区切り）"""
    counts = {}
    for val in series.dropna():
        for choice in str(val).split(";"):
            choice = choice.strip()
            if choice:
                counts[choice] = counts.get(choice, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


def pick_highlight_comments(series, n=3):
    """コメントからハイライトを選ぶ（50文字以上・テスト除外・短めに）"""
    comments = []
    for val in series.dropna():
        val = str(val).strip()
        if len(val) >= 20 and not any(kw in val.lower() for kw in TEST_KEYWORDS):
            comments.append(val)
    # 文字数が適度なものを優先（長すぎず短すぎず 30〜120文字）
    preferred = [c for c in comments if 30 <= len(c) <= 120]
    result = preferred[:n] if len(preferred) >= n else comments[:n]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vol", required=True, type=int)
    parser.add_argument("--file", required=True, help="アンケートExcelファイルのパス")
    parser.add_argument("--date", default=None, help="開催日でフィルタ YYYY-MM-DD（省略時は全行）")
    parser.add_argument("--comments", type=int, default=3, help="ハイライトコメント数")
    args = parser.parse_args()

    try:
        import pandas as pd
    except ImportError:
        print("pandas が必要です: pip install pandas openpyxl")
        sys.exit(1)

    df = pd.read_excel(args.file)
    print(f"読み込み: {len(df)}件")

    # 日付フィルタ
    if args.date:
        df['_date'] = pd.to_datetime(df['開始時刻']).dt.date.astype(str)
        df = df[df['_date'] == args.date].reset_index(drop=True)
        print(f"日付フィルタ({args.date})後: {len(df)}件")

    # テスト回答を除外
    df = df[~df.apply(is_test_response, axis=1)].reset_index(drop=True)
    print(f"テスト除外後: {len(df)}件")

    total = len(df)

    # 列名マッピング
    col_understanding = next((c for c in df.columns if "理解しやすかった" in str(c) and "点数" not in str(c) and "フィードバック" not in str(c)), None)
    col_usefulness    = next((c for c in df.columns if "役立ちそう" in str(c) and "点数" not in str(c) and "フィードバック" not in str(c)), None)
    col_time          = next((c for c in df.columns if "時間帯" in str(c) and "点数" not in str(c) and "フィードバック" not in str(c)), None)
    col_learned       = next((c for c in df.columns if "できるようになった" in str(c) and "点数" not in str(c) and "フィードバック" not in str(c)), None)
    col_comment       = next((c for c in df.columns if "感想" in str(c) and "点数" not in str(c) and "フィードバック" not in str(c)), None)

    result = {
        "vol": args.vol,
        "total_responses": total,
        "understanding": {},
        "usefulness": {},
        "time_preference": {},
        "learned": {},
        "highlight_comments": []
    }

    if col_understanding:
        result["understanding"] = df[col_understanding].value_counts().to_dict()

    if col_usefulness:
        result["usefulness"] = df[col_usefulness].value_counts().to_dict()

    if col_time:
        result["time_preference"] = df[col_time].value_counts().to_dict()

    if col_learned:
        result["learned"] = count_choices(df[col_learned])

    if col_comment:
        result["highlight_comments"] = pick_highlight_comments(df[col_comment], args.comments)

    # パーセンテージ追加
    if result["understanding"]:
        top = max(result["understanding"], key=result["understanding"].get)
        result["understanding_pct"] = round(result["understanding"].get(top, 0) / total * 100, 1)
        result["understanding_top"] = top

    if result["usefulness"]:
        useful_count = result["usefulness"].get("役立ちそう", 0)
        result["usefulness_pct"] = round(useful_count / total * 100, 1)

    # 保存
    out_path = SURVEYS_DIR / f"vol-{args.vol}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n✅ 保存: {out_path}")
    print(f"  回答数: {total}")
    print(f"  理解度トップ: {result.get('understanding_top')} ({result.get('understanding_pct')}%)")
    print(f"  役立ち度: {result.get('usefulness_pct')}%")
    print(f"  ハイライトコメント: {len(result['highlight_comments'])}件")


if __name__ == "__main__":
    main()
