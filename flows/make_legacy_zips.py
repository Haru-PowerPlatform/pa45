#!/usr/bin/env python3
"""
ソリューションZIPをレガシーパッケージZIPに変換する
レガシー形式 = マイフロー→インポートで直接マイフローに入る形式
"""
import zipfile, json, io, sys, os
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

flows = [
    {
        "vol": "vol-01",
        "solution_zip": "vol-01/PA45-Vol01-InitializeVariable.zip",
        "out_zip":      "vol-01/PA45-Vol01-InitializeVariable.zip",
        "json_file":    "Workflows/PA45_P001_InitializeVariable-C3A95FA2-DA15-F111-8341-002248F08C86.json",
        "flow_id":      "c3a95fa2-da15-f111-8341-002248f08c86",
        "display_name": "PA45 第1回 変数の初期化",
    },
    {
        "vol": "vol-02",
        "solution_zip": "vol-02/PA45-Vol02-SetVariable.zip",
        "out_zip":      "vol-02/PA45-Vol02-SetVariable.zip",
        "json_file":    "Workflows/PA45_P002__-2CF1DC51-7F1B-F111-8341-002248F08C86.json",
        "flow_id":      "2cf1dc51-7f1b-f111-8341-002248f08c86",
        "display_name": "PA45 第2回 変数を操作しよう",
    },
    {
        "vol": "vol-03",
        "solution_zip": "vol-03/PA45-Vol03-Condition.zip",
        "out_zip":      "vol-03/PA45-Vol03-Condition.zip",
        "json_file":    "Workflows/PA45-P003--5B54E6CF-E628-F111-88B3-002248F08C86.json",
        "flow_id":      "5b54e6cf-e628-f111-88b3-002248f08c86",
        "display_name": "PA45 第3回 条件分岐",
    },
    {
        "vol": "vol-04",
        "solution_zip": "vol-04/PA45-Vol04-ApplyToEach.zip",
        "out_zip":      "vol-04/PA45-Vol04-ApplyToEach.zip",
        "json_file":    "Workflows/PA45_P004_ApplyToEach_-066DDF38-CD2D-F111-88B4-002248F08C86.json",
        "flow_id":      "066ddf38-cd2d-f111-88b4-002248f08c86",
        "display_name": "PA45 第4回 Apply to each",
    },
    {
        "vol": "vol-05",
        "solution_zip": "vol-05/PA45-Vol05-Review.zip",
        "out_zip":      "vol-05/PA45-Vol05-Review.zip",
        "json_file":    "Workflows/PA45_No5-349DAC4F-C833-F111-88B4-002248F08C86.json",
        "flow_id":      "349dac4f-c833-f111-88b4-002248f08c86",
        "display_name": "PA45 第5回 基礎固めWeek",
    },
    {
        "vol": "vol-06",
        "solution_zip": "vol-06/PA45-Vol06-FormsMail.zip",
        "out_zip":      "vol-06/PA45-Vol06-FormsMail.zip",
        "json_file":    "Workflows/PA45-P006-Formsteams-23911156-F136-F111-88B4-002248F08C86.json",
        "flow_id":      "23911156-f136-f111-88b4-002248f08c86",
        "display_name": "PA45 第6回 Forms→メール",
    },
]

def make_legacy_zip(flow_def_json: bytes, flow_id: str, display_name: str) -> bytes:
    """レガシーパッケージZIPを生成して bytesで返す"""
    flow_def = json.loads(flow_def_json)

    # definition.json：フロー定義本体
    definition = {
        "properties": {
            "connectionReferences": flow_def.get("properties", {}).get("connectionReferences", {}),
            "definition": flow_def.get("properties", {}).get("definition", {}),
            "displayName": display_name,
            "description": ""
        }
    }

    # manifest.json：パッケージのメタ情報
    manifest = {
        "schema": "1.0",
        "details": {
            "displayName": display_name,
            "description": "",
            "author": "Haru (PA45)",
            "source": "ProcessSimple",
            "sourceLogicalName": "ProcessSimple",
            "sourceId": flow_id
        },
        "resources": {
            flow_id: {
                "type": "Microsoft.Flow/flows",
                "designerVersion": "2",
                "id": f"/providers/Microsoft.ProcessSimple/flows/{flow_id}",
                "name": flow_id,
                "properties": {
                    "displayName": display_name,
                    "state": "Started",
                    "connectionReferences": flow_def.get("properties", {}).get("connectionReferences", {})
                },
                "apiVersion": "2016-10-01",
                "dependsOn": []
            }
        }
    }

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        zout.writestr("manifest.json",
                      json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"))
        zout.writestr(f"Microsoft.Flow/flows/{flow_id}/definition.json",
                      json.dumps(definition, ensure_ascii=False, indent=2).encode("utf-8"))
    return buf.getvalue()


for f in flows:
    sol_path = os.path.join(SCRIPT_DIR, f["solution_zip"])
    out_path = os.path.join(SCRIPT_DIR, f["out_zip"])

    with zipfile.ZipFile(sol_path) as zsrc:
        flow_json_bytes = zsrc.read(f["json_file"])

    legacy_bytes = make_legacy_zip(flow_json_bytes, f["flow_id"], f["display_name"])

    with open(out_path, "wb") as fp:
        fp.write(legacy_bytes)

    print(f"OK {f['vol']}: {f['display_name']} ({len(legacy_bytes)} bytes)")

print("完了")
