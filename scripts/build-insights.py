"""
PA45 インサイト集計スクリプト

data/surveys/vol-NN.json と data/activities/*-pa45-volN.json を集計して
data/insights.json を書き出します。achievements/insights/ 配下のページが読み込みます。

使い方:
  python scripts/build-insights.py
新しい回のアンケートを parse-survey.py で取り込んだあとに実行してください。
"""

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SURVEY_DIR = ROOT / "data" / "surveys"
ACT_DIR = ROOT / "data" / "activities"
OUT = ROOT / "data" / "insights.json"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def session_rows():
    """activities から回ごとの参加者数・テーマ・エビデンスを拾う"""
    rows = {}
    for p in ACT_DIR.glob("*-pa45-vol*.json"):
        m = re.search(r"pa45-vol(\d+)", p.name)
        if not m:
            continue
        d = load_json(p)
        vol = int(m.group(1))
        title = d.get("title", "")
        theme = title.split("：", 1)[1] if "：" in title else title
        # 「── 」以降の副題は落として短くする
        theme = re.split(r"\s*(?:──|—|―)\s*", theme)[0].strip()
        rows[vol] = {
            "vol": vol,
            "date": d.get("date"),
            "theme": theme,
            "participants": d.get("participants"),
            "connpass": (d.get("evidence") or {}).get("connpass", ""),
            "youtube": (d.get("evidence") or {}).get("youtube", ""),
            "blog": (d.get("evidence") or {}).get("blog", ""),
        }
    return rows


def main():
    acts = session_rows()
    sessions = []
    can_do = Counter()
    can_do_rounds = Counter()   # その選択肢が出題された回数
    can_do_base = Counter()     # その選択肢が出題された回の回答者合計（母数）
    understanding = Counter()
    usefulness = Counter()
    time_pref = Counter()
    total_responses = 0
    w_understanding = 0.0
    w_usefulness = 0.0

    for vol in sorted(acts):
        sp = SURVEY_DIR / f"vol-{vol:02d}.json"
        s = load_json(sp) if sp.exists() else {}
        n = s.get("total_responses", 0)
        total_responses += n
        w_understanding += (s.get("understanding_pct") or 0) * n
        w_usefulness += (s.get("usefulness_pct") or 0) * n
        for k, v in (s.get("can_do") or {}).items():
            can_do[k] += v
            can_do_rounds[k] += 1
            can_do_base[k] += n
        for k, v in (s.get("understanding") or {}).items():
            understanding[k] += v
        for k, v in (s.get("usefulness") or {}).items():
            usefulness[k] += v
        for k, v in (s.get("time_preference") or {}).items():
            time_pref[k] += v

        row = dict(acts[vol])
        row.update({
            "responses": n,
            "understanding_pct": s.get("understanding_pct"),
            "usefulness_pct": s.get("usefulness_pct"),
            "comments": len(s.get("comments") or []),
        })
        sessions.append(row)

    def pct(counter):
        tot = sum(counter.values()) or 1
        return {k: round(v / tot * 100, 1) for k, v in counter.items()}

    data = {
        "generated_from": "data/surveys/*.json + data/activities/*-pa45-vol*.json",
        "summary": {
            "sessions": len(sessions),
            "first_date": sessions[0]["date"] if sessions else None,
            "last_date": sessions[-1]["date"] if sessions else None,
            "participants_total": sum(r["participants"] or 0 for r in sessions),
            "participants_avg": round(
                sum(r["participants"] or 0 for r in sessions) / max(len(sessions), 1), 1),
            "participants_max": max((r["participants"] or 0 for r in sessions), default=0),
            "responses_total": total_responses,
            "understanding_avg": round(w_understanding / max(total_responses, 1), 1),
            "usefulness_avg": round(w_usefulness / max(total_responses, 1), 1),
            "archive_videos": sum(1 for r in sessions if r["youtube"]),
        },
        "sessions": sessions,
        "can_do": can_do.most_common(),
        # 選択肢は途中で入れ替わっているため、出題された回だけを母数にした選択率も持つ
        "can_do_detail": [
            {
                "label": k,
                "count": v,
                "rounds": can_do_rounds[k],
                "base": can_do_base[k],
                "rate": round(v / can_do_base[k] * 100, 1) if can_do_base[k] else 0,
            }
            for k, v in can_do.most_common()
        ],
        "understanding": understanding.most_common(),
        "understanding_pcts": pct(understanding),
        "usefulness": usefulness.most_common(),
        "usefulness_pcts": pct(usefulness),
        "time_preference": time_pref.most_common(),
        "time_preference_pcts": pct(time_pref),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    s = data["summary"]
    print(f"[OK] {OUT}")
    print(f"  {s['sessions']}回 / のべ{s['participants_total']}名 / 回答{s['responses_total']}件 "
          f"/ 理解{s['understanding_avg']}% / 役立ち{s['usefulness_avg']}%")


if __name__ == "__main__":
    main()
