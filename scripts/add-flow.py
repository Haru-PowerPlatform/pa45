#!/usr/bin/env python3
"""
PA45 フローダウンロードページ更新スクリプト
使い方:
  python scripts/add-flow.py \
    --zip "C:/Users/isamu/Downloads/PA45Handson_X_X_X_X.zip" \
    --vol 7 \
    --title "Switch で複数条件分岐" \
    --desc "Switch アクションで3つ以上の分岐を作り、選択肢に応じて処理を切り替えるフロー。" \
    --trigger "手動トリガー" \
    --tags "Switch,条件分岐,メール送信" \
    --blog "https://www.automate136.com/?p=XXXX"

実行すると:
  1. ZIPを回ごとに分割（既存含む全フローを再生成）
  2. data/flows.json に新しいエントリを追加
  3. git add & commit & push
"""
import argparse, json, zipfile, re, io, sys, os, subprocess
sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLOWS_DIR = os.path.join(REPO, "flows")
DATA_JSON = os.path.join(REPO, "data", "flows.json")

# カラーマッピング（vol番号 → CSSクラス）
COLOR_MAP = ["vol1","vol2","vol3","vol4","vol5","vol6","vol7","vol8","vol9","vol10"]

def split_solution(zip_path):
    """ソリューションZIPを回ごとの個別ZIPに分割して flows/vol-XX/ に配置"""
    with zipfile.ZipFile(zip_path) as src:
        full_custom = src.read("customizations.xml").decode("utf-8")
        content_types = src.read("[Content_Types].xml")
        solution_xml_base = src.read("solution.xml").decode("utf-8")

        # 全Workflowブロックを抽出
        wf_blocks = re.findall(
            r'<Workflow WorkflowId="\{([^}]+)\}" Name="([^"]*)".*?</Workflow>',
            full_custom, re.DOTALL | re.IGNORECASE
        )
        results = []
        for wf_id, wf_name in wf_blocks:
            # JSONファイルを特定
            json_files = [n for n in src.namelist()
                          if n.startswith("Workflows/") and wf_id.upper().replace("-","") in n.upper().replace("-","")]
            if not json_files:
                print(f"  WARN: {wf_id} のJSONが見つかりません")
                continue
            json_file = json_files[0]

            wf_pat = re.compile(
                r'<Workflow WorkflowId="\{' + re.escape(wf_id) + r'\}".*?</Workflow>',
                re.DOTALL | re.IGNORECASE
            )
            wf_match = wf_pat.search(full_custom)
            if not wf_match:
                continue

            custom_xml = f'''<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" OrganizationVersion="9.2.26034.167">
  <Entities></Entities><Roles></Roles>
  <Workflows>
    {wf_match.group(0)}
  </Workflows>
</ImportExportXml>'''

            solution_xml = f'''<ImportExportXml version="9.2.26034.167" SolutionPackageVersion="9.2" languagecode="1041" generatedBy="CrmLive" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <SolutionManifest>
    <UniqueName>PA45_{wf_name}</UniqueName>
    <LocalizedNames><LocalizedName description="PA45 {wf_name}" languagecode="1041" /></LocalizedNames>
    <Descriptions />
    <Version>1.0.0.1</Version>
    <Managed>0</Managed>
    <Publisher>
      <UniqueName>pa45</UniqueName>
      <LocalizedNames><LocalizedName description="PA45" languagecode="1041" /></LocalizedNames>
      <CustomizationPrefix>pa45</CustomizationPrefix>
    </Publisher>
    <RootComponents>
      <RootComponent type="29" id="{{{wf_id.lower()}}}" behavior="0" />
    </RootComponents>
    <MissingDependencies />
  </SolutionManifest>
</ImportExportXml>'''

            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
                out.writestr("solution.xml",        solution_xml.encode("utf-8"))
                out.writestr("customizations.xml",  custom_xml.encode("utf-8"))
                out.writestr("[Content_Types].xml",  content_types)
                out.writestr(json_file,              src.read(json_file))
            results.append({"id": wf_id.lower(), "name": wf_name, "data": buf.getvalue()})

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip",     required=True,  help="新しいソリューションZIPのパス")
    parser.add_argument("--vol",     required=True,  type=int, help="追加する回番号（例: 7）")
    parser.add_argument("--title",   required=True,  help="フローのタイトル")
    parser.add_argument("--desc",    required=True,  help="フローの説明")
    parser.add_argument("--trigger", default="手動トリガー", help="トリガー名")
    parser.add_argument("--tags",    required=True,  help="タグ（カンマ区切り）")
    parser.add_argument("--blog",    default="",     help="ブログURL（任意）")
    args = parser.parse_args()

    vol_str = f"{args.vol:02d}"
    vol_dir = os.path.join(FLOWS_DIR, f"vol-{vol_str}")
    os.makedirs(vol_dir, exist_ok=True)

    print(f"[1/4] ZIPを分割中: {args.zip}")
    flows_data = split_solution(args.zip)
    print(f"  {len(flows_data)} 件のフローを検出")

    # 既存のflows.jsonを読み込み
    with open(DATA_JSON, encoding="utf-8") as f:
        existing = json.load(f)
    existing_vols = {e["vol"] for e in existing}

    print(f"[2/4] 個別ZIPを flows/ に配置中")
    # 全フローのZIPを更新（番号順にvol割り当て）
    # 新規フロー用のIDを特定するため、既存ZIPに対応するIDを収集
    existing_ids = set()
    for e in existing:
        zip_path_rel = e.get("zip", "")
        # vol-XX/PA45-VolXX-Name.zip から既存フローを把握
        existing_ids.add(zip_path_rel.split("/")[0] if "/" in zip_path_rel else "")

    # 新フロー（最後に追加されたもの = existing_vols に存在しない）
    # ソリューション内のフロー数 vs 既存JSON数で判断
    new_flow_data = None
    if len(flows_data) > len(existing):
        # 一番最後のフローが新規
        new_flow_data = flows_data[-1]

    # 全フローをvol番号順に保存
    for i, fd in enumerate(flows_data):
        v = f"{i+1:02d}"
        # 対応するexistingエントリを探す
        if i < len(existing):
            existing_zip = existing[i]["zip"]
            out_path = os.path.join(FLOWS_DIR, existing_zip)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "wb") as fp:
                fp.write(fd["data"])
            print(f"  更新: {existing_zip}")
        else:
            # 新規フロー
            fname = f"PA45-Vol{vol_str}-{args.title.replace(' ','')[:20]}.zip"
            out_path = os.path.join(vol_dir, fname)
            with open(out_path, "wb") as fp:
                fp.write(fd["data"])
            new_zip_rel = f"vol-{vol_str}/{fname}"
            print(f"  新規: {new_zip_rel}")

    print(f"[3/4] data/flows.json を更新中")
    if vol_str not in existing_vols:
        fname = f"PA45-Vol{vol_str}-{args.title.replace(' ','')[:20]}.zip"
        color_idx = min(args.vol - 1, len(COLOR_MAP) - 1)
        new_entry = {
            "vol":     vol_str,
            "title":   args.title,
            "desc":    args.desc,
            "trigger": args.trigger,
            "tags":    [t.strip() for t in args.tags.split(",")],
            "zip":     f"vol-{vol_str}/{fname}",
            "blog":    args.blog,
            "color":   COLOR_MAP[color_idx]
        }
        existing.append(new_entry)
        with open(DATA_JSON, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        print(f"  追加: 第{args.vol}回 '{args.title}'")
    else:
        print(f"  Vol.{vol_str} は既に存在します（スキップ）")

    print(f"[4/4] git commit & push")
    os.chdir(REPO)
    subprocess.run(["git", "add", "flows/", "data/flows.json"], check=True)
    subprocess.run(["git", "commit", "-m",
        f"add: 第{args.vol}回フロー追加 ({args.title})\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"],
        check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print(f"\n完了！ https://haru-powerplatform.github.io/pa45/flows/")


if __name__ == "__main__":
    main()
