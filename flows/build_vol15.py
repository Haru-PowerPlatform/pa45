#!/usr/bin/env python3
"""
Vol.15「共有フォルダ監視 → リンク付き自動メール通知」ソリューションZIPを生成する。
題材: 共有フォルダ（SharePoint ドキュメント）にファイルが作成されたら、
      担当者へ「ファイルを開くリンク付き」のメールを自動送信する。
配布ZIPはインポートして動く完成版（接続参照は取り込み時にユーザーが割り当て、
トリガーのサイト/フォルダと宛先は各自の環境に合わせて設定する）。
vol-10/11 と同じソリューションフォーマット（solution.xml + customizations.xml + Workflows/*.json）。
"""
import zipfile, json, io, os, uuid, sys
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

FLOW_NAME    = "PA45-No15-FolderWatchMail"
UNIQUE_NAME  = "PA45No15FolderWatchMail"
DISPLAY_NAME = "PA45 No.15 FolderWatchMail"
OUT_ZIP      = os.path.join(SCRIPT_DIR, "vol-15", "PA45-Vol15-FolderWatchMail.zip")

flow_guid  = str(uuid.uuid4())
GUID_UPPER = flow_guid.upper()
JSON_PATH  = f"Workflows/{FLOW_NAME}-{GUID_UPPER}.json"

# このソリューション内で一意な接続参照 論理名
CONN_SP   = "new_sharedsharepointonline_pa45no15"
CONN_MAIL = "new_sharedoffice365_pa45no15"

flow_def = {
    "properties": {
        "connectionReferences": {
            "shared_sharepointonline": {
                "runtimeSource": "embedded",
                "connection": {"connectionReferenceLogicalName": CONN_SP},
                "api": {"name": "shared_sharepointonline"}
            },
            "shared_office365": {
                "runtimeSource": "embedded",
                "connection": {"connectionReferenceLogicalName": CONN_MAIL},
                "api": {"name": "shared_office365"}
            }
        },
        "definition": {
            "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
            "contentVersion": "1.0.0.0",
            "parameters": {
                "$authentication": {"defaultValue": {}, "type": "SecureObject"},
                "$connections": {"defaultValue": {}, "type": "Object"}
            },
            "triggers": {
                "ファイルが作成されたとき_プロパティのみ": {
                    "recurrence": {"interval": 1, "frequency": "Minute"},
                    "splitOn": "@triggerOutputs()?['body/value']",
                    "metadata": {"operationMetadataId": str(uuid.uuid4())},
                    "type": "OpenApiConnection",
                    "inputs": {
                        "parameters": {
                            "dataset": "",
                            "table": "",
                            "folderPath": "/Shared Documents"
                        },
                        "host": {
                            "apiId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
                            "operationId": "GetOnNewFileItems",
                            "connectionName": "shared_sharepointonline"
                        }
                    }
                }
            },
            "actions": {
                "メールを送信する_リンク付き": {
                    "runAfter": {},
                    "metadata": {"operationMetadataId": str(uuid.uuid4())},
                    "type": "OpenApiConnection",
                    "inputs": {
                        "parameters": {
                            "emailMessage/To": "",
                            "emailMessage/Subject": "【共有フォルダ】新しいファイルが届きました：@{triggerOutputs()?['body/{FilenameWithExtension}']}",
                            "emailMessage/Body": "<p>共有フォルダに新しいファイルが追加されました。</p><p><b>ファイル名：</b>@{triggerOutputs()?['body/{FilenameWithExtension}']}</p><p><a href=\"@{triggerOutputs()?['body/{Link}']}\">▶ ファイルを開く</a></p>",
                            "emailMessage/Importance": "Normal"
                        },
                        "host": {
                            "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
                            "operationId": "SendEmailV2",
                            "connectionName": "shared_office365"
                        }
                    }
                }
            },
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
    <Workflow WorkflowId="{{{flow_guid}}}" Name="{FLOW_NAME}">
      <JsonFileName>/{JSON_PATH}</JsonFileName>
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
        <LocalizedName languagecode="1041" description="{FLOW_NAME}" />
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

solution = f'''<ImportExportXml version="9.2.26043.159" SolutionPackageVersion="9.2" languagecode="1041" generatedBy="CrmLive" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" OrganizationVersion="9.2.26043.159" OrganizationSchemaType="Standard" CRMServerServiceabilityVersion="9.2.26043.00159">
  <SolutionManifest>
    <UniqueName>{UNIQUE_NAME}</UniqueName>
    <LocalizedNames>
      <LocalizedName description="{DISPLAY_NAME}" languagecode="1041" />
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
    <MissingDependencies>
      <MissingDependency>
        <Required type="connectionreference" displayName="{CONN_SP}" solution="Active" id.connectionreferencelogicalname="{CONN_SP}" />
        <Dependent type="29" displayName="{FLOW_NAME}" id="{{{flow_guid}}}" />
      </MissingDependency>
      <MissingDependency>
        <Required type="connectionreference" displayName="{CONN_MAIL}" solution="Active" id.connectionreferencelogicalname="{CONN_MAIL}" />
        <Dependent type="29" displayName="{FLOW_NAME}" id="{{{flow_guid}}}" />
      </MissingDependency>
    </MissingDependencies>
  </SolutionManifest>
</ImportExportXml>'''

content_types = '<?xml version="1.0" encoding="utf-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="xml" ContentType="application/octet-stream" /><Default Extension="json" ContentType="application/octet-stream" /></Types>'

os.makedirs(os.path.dirname(OUT_ZIP), exist_ok=True)
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
    out.writestr("customizations.xml", customizations.encode("utf-8"))
    out.writestr("solution.xml", solution.encode("utf-8"))
    out.writestr("[Content_Types].xml", content_types.encode("utf-8"))
    out.writestr(JSON_PATH, json.dumps(flow_def, ensure_ascii=False, indent=2).encode("utf-8"))

with open(OUT_ZIP, "wb") as fp:
    fp.write(buf.getvalue())

print(f"OK {OUT_ZIP} ({len(buf.getvalue())} bytes)")
print(f"   WorkflowId: {flow_guid}")
print(f"   JSON: {JSON_PATH}")
