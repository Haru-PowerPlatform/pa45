#!/usr/bin/env python3
"""
Vol.12/13/14 のソリューションZIPを生成する（vol-10 と同じソリューション形式）。
配布ZIPはインポートして動く完成版。
- Vol.12 Expression : Forms→3営業日後を Do until で計算→Teams通知（addDays/dayOfWeek/formatDateTime）
- Vol.13 TryCatch   : 手動トリガー→Try(div(1,0)で失敗)→Catch(失敗時Teams)→Finally(常にTeams)
- Vol.14 JsonReading: 手動トリガー→サンプルJSONをCompose→キー/配列添字で値を取り出す
"""
import zipfile, json, io, os, uuid, sys
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEAMS_RECIPIENT = "ixa_mct@plug136.onmicrosoft.com"


def teams_post(name, message_html, run_after=None):
    return name, {
        "runAfter": run_after or {},
        "metadata": {"operationMetadataId": str(uuid.uuid4())},
        "type": "OpenApiConnection",
        "inputs": {
            "parameters": {
                "poster": "Flow bot",
                "location": "Chat with Flow bot",
                "body/recipient": TEAMS_RECIPIENT,
                "body/messageBody": message_html
            },
            "host": {
                "apiId": "/providers/Microsoft.PowerApps/apis/shared_teams",
                "operationId": "PostMessageToConversation",
                "connectionName": "shared_teams"
            }
        }
    }


def compose(name, inputs, run_after=None):
    return name, {
        "runAfter": run_after or {},
        "metadata": {"operationMetadataId": str(uuid.uuid4())},
        "type": "Compose",
        "inputs": inputs
    }


def build_zip(out_rel, flow_name, unique_name, display_name, conn_refs, triggers, actions):
    flow_guid = str(uuid.uuid4())
    guid_upper = flow_guid.upper()
    json_path = f"Workflows/{flow_name}-{guid_upper}.json"

    flow_def = {
        "properties": {
            "connectionReferences": conn_refs,
            "definition": {
                "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
                "contentVersion": "1.0.0.0",
                "parameters": {
                    "$authentication": {"defaultValue": {}, "type": "SecureObject"},
                    "$connections": {"defaultValue": {}, "type": "Object"}
                },
                "triggers": triggers,
                "actions": actions,
                "outputs": {}
            },
            "templateName": None
        },
        "schemaVersion": "1.0.0.0"
    }

    customizations = f'''<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" OrganizationVersion="9.2.26043.159" OrganizationSchemaType="Standard" CRMServerServiceabilityVersion="9.2.26043.00159">
  <Entities></Entities>
  <Roles></Roles>
  <Workflows>
    <Workflow WorkflowId="{{{flow_guid}}}" Name="{flow_name}">
      <JsonFileName>/{json_path}</JsonFileName>
      <Type>1</Type>
      <Subprocess>0</Subprocess>
      <Category>5</Category>
      <Mode>0</Mode>
      <Scope>4</Scope>
      <OnDemand>0</OnDemand>
      <TriggerOnCreate>0</TriggerOnCreate>
      <TriggerOnDelete>0</TriggerOnDelete>
      <AsyncAutodelete>0</AsyncAutodelete>
      <SyncWorkflowLogOnFailure>0</SyncWorkflowLogOnFailure>
      <StateCode>1</StateCode>
      <StatusCode>2</StatusCode>
      <RunAs>1</RunAs>
      <IsTransacted>1</IsTransacted>
      <IntroducedVersion>1.0</IntroducedVersion>
      <IsCustomizable>1</IsCustomizable>
      <BusinessProcessType>0</BusinessProcessType>
      <IsCustomProcessingStepAllowedForOtherPublishers>1</IsCustomProcessingStepAllowedForOtherPublishers>
      <ModernFlowType>0</ModernFlowType>
      <PrimaryEntity>none</PrimaryEntity>
      <LocalizedNames>
        <LocalizedName languagecode="1041" description="{flow_name}" />
      </LocalizedNames>
    </Workflow>
  </Workflows>
  <FieldSecurityProfiles></FieldSecurityProfiles>
  <Templates />
  <EntityMaps />
  <EntityRelationships />
  <OrganizationSettings />
  <optionsets />
  <CustomControls />
  <EntityDataProviders />
  <Languages>
    <Language>1041</Language>
  </Languages>
</ImportExportXml>'''

    # MissingDependencies（接続参照ごと）
    deps = ""
    for ref_logical in conn_refs_logical(conn_refs):
        deps += f'''
      <MissingDependency>
        <Required type="connectionreference" displayName="{ref_logical}" solution="Active" id.connectionreferencelogicalname="{ref_logical}" />
        <Dependent type="29" displayName="{flow_name}" id="{{{flow_guid}}}" />
      </MissingDependency>'''
    missing = f"<MissingDependencies>{deps}\n    </MissingDependencies>" if deps else "<MissingDependencies />"

    solution = f'''<ImportExportXml version="9.2.26043.159" SolutionPackageVersion="9.2" languagecode="1041" generatedBy="CrmLive" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" OrganizationVersion="9.2.26043.159" OrganizationSchemaType="Standard" CRMServerServiceabilityVersion="9.2.26043.00159">
  <SolutionManifest>
    <UniqueName>{unique_name}</UniqueName>
    <LocalizedNames>
      <LocalizedName description="{display_name}" languagecode="1041" />
    </LocalizedNames>
    <Descriptions />
    <Version>1.0.0.0</Version>
    <Managed>1</Managed>
    <Publisher>
      <UniqueName>pa45</UniqueName>
      <LocalizedNames>
        <LocalizedName description="PA45" languagecode="1041" />
      </LocalizedNames>
      <Descriptions>
        <Description description="PA45 Hands-on Training Publisher" languagecode="1041" />
      </Descriptions>
      <EMailAddress xsi:nil="true"></EMailAddress>
      <SupportingWebsiteUrl xsi:nil="true"></SupportingWebsiteUrl>
      <CustomizationPrefix>pa45</CustomizationPrefix>
      <CustomizationOptionValuePrefix>27410</CustomizationOptionValuePrefix>
      <Addresses />
    </Publisher>
    <RootComponents>
      <RootComponent type="29" id="{{{flow_guid}}}" behavior="0" />
    </RootComponents>
    {missing}
  </SolutionManifest>
</ImportExportXml>'''

    content_types = '<?xml version="1.0" encoding="utf-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="xml" ContentType="application/octet-stream" /><Default Extension="json" ContentType="application/octet-stream" /></Types>'

    out_path = os.path.join(SCRIPT_DIR, out_rel)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        out.writestr("customizations.xml", customizations.encode("utf-8"))
        out.writestr("solution.xml", solution.encode("utf-8"))
        out.writestr("[Content_Types].xml", content_types.encode("utf-8"))
        out.writestr(json_path, json.dumps(flow_def, ensure_ascii=False, indent=2).encode("utf-8"))
    with open(out_path, "wb") as fp:
        fp.write(buf.getvalue())
    print(f"OK {out_rel} ({len(buf.getvalue())} bytes)  guid={flow_guid}")


def conn_refs_logical(conn_refs):
    return [v["connection"]["connectionReferenceLogicalName"] for v in conn_refs.values()]


def cref(api_name, logical):
    return {
        "runtimeSource": "embedded",
        "connection": {"connectionReferenceLogicalName": logical},
        "api": {"name": api_name}
    }


# ───────────────────────── Vol.12 Expression ─────────────────────────
v12_conns = {
    "shared_microsoftforms": cref("shared_microsoftforms", "new_sharedmicrosoftforms_pa45no12"),
    "shared_teams": cref("shared_teams", "new_sharedteams_pa45no12"),
}
v12_triggers = {
    "新しい応答が送信されるとき": {
        "splitOn": "@triggerOutputs()?['body/value']",
        "metadata": {"operationMetadataId": str(uuid.uuid4())},
        "type": "OpenApiConnectionWebhook",
        "inputs": {
            "parameters": {"form_id": ""},
            "host": {
                "apiId": "/providers/Microsoft.PowerApps/apis/shared_microsoftforms",
                "operationId": "CreateFormWebhook",
                "connectionName": "shared_microsoftforms"
            }
        }
    }
}
v12_actions = dict([
    ("応答の詳細を取得する", {
        "runAfter": {},
        "metadata": {"operationMetadataId": str(uuid.uuid4())},
        "type": "OpenApiConnection",
        "inputs": {
            "parameters": {
                "form_id": "",
                "response_id": "@triggerOutputs()?['body/resourceData/responseId']"
            },
            "host": {
                "apiId": "/providers/Microsoft.PowerApps/apis/shared_microsoftforms",
                "operationId": "GetFormResponseById",
                "connectionName": "shared_microsoftforms"
            }
        }
    }),
    ("変数を初期化する_カウント", {
        "runAfter": {"応答の詳細を取得する": ["Succeeded"]},
        "metadata": {"operationMetadataId": str(uuid.uuid4())},
        "type": "InitializeVariable",
        "inputs": {"variables": [{"name": "count", "type": "integer", "value": 0}]}
    }),
    ("変数を初期化する_処理日", {
        "runAfter": {"変数を初期化する_カウント": ["Succeeded"]},
        "metadata": {"operationMetadataId": str(uuid.uuid4())},
        "type": "InitializeVariable",
        "inputs": {"variables": [{"name": "currentDate", "type": "string", "value": "@utcNow()"}]}
    }),
    ("Do_until_平日を3日数える", {
        "runAfter": {"変数を初期化する_処理日": ["Succeeded"]},
        "metadata": {"operationMetadataId": str(uuid.uuid4())},
        "type": "Until",
        "expression": "@greaterOrEquals(variables('count'), 3)",
        "limit": {"count": 60, "timeout": "PT1H"},
        "actions": dict([
            compose("作成_1日進める", "@addDays(variables('currentDate'), 1)"),
            ("変数の設定_処理日を1日後に", {
                "runAfter": {"作成_1日進める": ["Succeeded"]},
                "metadata": {"operationMetadataId": str(uuid.uuid4())},
                "type": "SetVariable",
                "inputs": {"name": "currentDate", "value": "@outputs('作成_1日進める')"}
            }),
            ("条件_平日かどうか判定", {
                "runAfter": {"変数の設定_処理日を1日後に": ["Succeeded"]},
                "metadata": {"operationMetadataId": str(uuid.uuid4())},
                "type": "If",
                "expression": {
                    "and": [
                        {"greater": ["@dayOfWeek(variables('currentDate'))", 0]},
                        {"less": ["@dayOfWeek(variables('currentDate'))", 6]}
                    ]
                },
                "actions": {
                    "変数の値を増やす_count_プラス1": {
                        "runAfter": {},
                        "metadata": {"operationMetadataId": str(uuid.uuid4())},
                        "type": "IncrementVariable",
                        "inputs": {"name": "count", "value": 1}
                    }
                },
                "else": {"actions": {}}
            })
        ])
    }),
    compose("作成_JST日付に整える",
            "@formatDateTime(convertFromUtc(variables('currentDate'),'Tokyo Standard Time'),'yyyy-MM-dd')",
            {"Do_until_平日を3日数える": ["Succeeded"]}),
    teams_post("チャットまたはチャネルでメッセージを投稿する_期日通知",
               "<p class=\"editor-paragraph\">この申請は <b><strong class=\"editor-text-bold\">@{outputs('作成_JST日付に整える')}</strong></b> までに対応してください（申請日から3営業日後）。</p>",
               {"作成_JST日付に整える": ["Succeeded"]}),
])

build_zip("vol-12/PA45-Vol12-Expression.zip", "PA45-No12-Expression",
          "PA45No12Expression", "PA45 No.12 Expression",
          v12_conns, v12_triggers, v12_actions)


# ───────────────────────── Vol.13 TryCatch ─────────────────────────
v13_conns = {"shared_teams": cref("shared_teams", "new_sharedteams_pa45no13")}
v13_triggers = {
    "手動でフローをトリガーします": {
        "metadata": {"operationMetadataId": str(uuid.uuid4())},
        "type": "Request",
        "kind": "Button",
        "inputs": {}
    }
}
v13_actions = dict([
    ("スコープ_Try", {
        "runAfter": {},
        "metadata": {"operationMetadataId": str(uuid.uuid4())},
        "type": "Scope",
        "actions": dict([
            compose("作成_わざと失敗_div_1_0", "@div(1,0)")
        ])
    }),
    ("スコープ_Catch", {
        "runAfter": {"スコープ_Try": ["Failed", "TimedOut"]},
        "metadata": {"operationMetadataId": str(uuid.uuid4())},
        "type": "Scope",
        "actions": dict([
            teams_post("チャットまたはチャネルでメッセージを投稿する_失敗通知",
                       "<p class=\"editor-paragraph\"><b><strong class=\"editor-text-bold\">⚠️ 処理が失敗しました</strong></b>（担当者に確認してください）</p>")
        ])
    }),
    ("スコープ_Finally", {
        "runAfter": {"スコープ_Catch": ["Succeeded", "Failed", "Skipped", "TimedOut"]},
        "metadata": {"operationMetadataId": str(uuid.uuid4())},
        "type": "Scope",
        "actions": dict([
            teams_post("チャットまたはチャネルでメッセージを投稿する_完了記録",
                       "<p class=\"editor-paragraph\">処理が完了しました（成功でも失敗でも必ず記録されます）</p>")
        ])
    }),
])

build_zip("vol-13/PA45-Vol13-TryCatch.zip", "PA45-No13-TryCatch",
          "PA45No13TryCatch", "PA45 No.13 TryCatch",
          v13_conns, v13_triggers, v13_actions)


# ───────────────────────── Vol.14 JsonReading ─────────────────────────
v14_conns = {}
v14_triggers = {
    "手動でフローをトリガーします": {
        "metadata": {"operationMetadataId": str(uuid.uuid4())},
        "type": "Request",
        "kind": "Button",
        "inputs": {}
    }
}
sample_json = {
    "申請者": "山田 太郎",
    "金額": 12000,
    "明細": [
        {"品目": "書籍", "金額": 5000},
        {"品目": "備品", "金額": 7000}
    ]
}
v14_actions = dict([
    compose("作成_サンプルJSON", sample_json),
    compose("作成_申請者名を取り出す", "@outputs('作成_サンプルJSON')?['申請者']",
            {"作成_サンプルJSON": ["Succeeded"]}),
    compose("作成_1件目の品目を取り出す", "@outputs('作成_サンプルJSON')?['明細'][0]['品目']",
            {"作成_申請者名を取り出す": ["Succeeded"]}),
])

build_zip("vol-14/PA45-Vol14-JsonReading.zip", "PA45-No14-JsonReading",
          "PA45No14JsonReading", "PA45 No.14 JsonReading",
          v14_conns, v14_triggers, v14_actions)

print("完了")
