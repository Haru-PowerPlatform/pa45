#!/usr/bin/env python3
"""
全14本のフローを1つの「PA45Handson」ソリューションに統合したまとめパックZIPを作る。
- Vol.1〜6 : 既存バンドル PA45Handson_1_0_0_4.zip から Workflow ブロック+JSON を流用
- Vol.7〜14: 各 vol-NN の個別ソリューションZIP から Workflow ブロック+JSON を抽出
出力: PA45Handson_1_0_0_5.zip（Version 1.0.0.5・全14フロー収録）
"""
import zipfile, re, io, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SOURCES = [
    ("PA45Handson_1_0_0_4.zip", "Vol.1-6 (既存バンドル)"),
    ("vol-07/PA45-Vol07-FormsSPTeams.zip", "Vol.7"),
    ("vol-08/PA45-Vol08-ApprovalFlow.zip", "Vol.8"),
    ("vol-09/PA45-Vol09-SharePointUpdate.zip", "Vol.9"),
    ("vol-10/PA45-Vol10-BizReview.zip", "Vol.10"),
    ("vol-11/PA45-Vol11-RunHistory.zip", "Vol.11"),
    ("vol-12/PA45-Vol12-Expression.zip", "Vol.12"),
    ("vol-13/PA45-Vol13-TryCatch.zip", "Vol.13"),
    ("vol-14/PA45-Vol14-JsonReading.zip", "Vol.14"),
]

WF_RE = re.compile(r'<Workflow\s+WorkflowId="\{([0-9a-fA-F-]+)\}".*?</Workflow>', re.DOTALL)
JSONNAME_RE = re.compile(r'<JsonFileName>(.*?)</JsonFileName>', re.DOTALL)
MISSDEP_RE = re.compile(r'<MissingDependency>.*?</MissingDependency>', re.DOTALL)

workflow_blocks = []   # XML文字列
root_components = []    # <RootComponent .../>
json_files = {}         # path -> bytes
missing_deps = []       # XML文字列

for rel, label in SOURCES:
    path = os.path.join(SCRIPT_DIR, rel)
    with zipfile.ZipFile(path) as z:
        custom = z.read("customizations.xml").decode("utf-8")
        blocks = WF_RE.findall(custom)
        full_blocks = WF_RE.finditer(custom)
        cnt = 0
        for m in full_blocks:
            block = m.group(0)
            guid = m.group(1).lower()
            workflow_blocks.append(block)
            root_components.append(f'      <RootComponent type="29" id="{{{guid}}}" behavior="0" />')
            jn = JSONNAME_RE.search(block)
            if jn:
                jpath = jn.group(1).strip().lstrip("/")
                json_files[jpath] = z.read(jpath)
            cnt += 1
        # MissingDependencies（solution.xml がある個別ZIP）
        try:
            sol = z.read("solution.xml").decode("utf-8")
            for md in MISSDEP_RE.findall(sol):
                missing_deps.append("      " + md.strip())
        except KeyError:
            pass
    print(f"  {label}: {cnt} flow(s)")

print(f"合計フロー数: {len(workflow_blocks)}")

# ── customizations.xml ──
customizations = (
    '<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
    'OrganizationVersion="9.2.26043.159" OrganizationSchemaType="Standard" '
    'CRMServerServiceabilityVersion="9.2.26043.00159">\n'
    '  <Entities></Entities>\n  <Roles></Roles>\n  <Workflows>\n'
    + "\n".join("    " + b for b in workflow_blocks) +
    '\n  </Workflows>\n'
    '  <FieldSecurityProfiles></FieldSecurityProfiles>\n'
    '  <Templates />\n  <EntityMaps />\n  <EntityRelationships />\n'
    '  <OrganizationSettings />\n  <optionsets />\n  <CustomControls />\n'
    '  <EntityDataProviders />\n  <Languages>\n    <Language>1041</Language>\n  </Languages>\n'
    '</ImportExportXml>'
)

missing_block = ("<MissingDependencies>\n" + "\n".join(missing_deps) + "\n    </MissingDependencies>") if missing_deps else "<MissingDependencies />"

solution = f'''<ImportExportXml version="9.2.26043.159" SolutionPackageVersion="9.2" languagecode="1041" generatedBy="CrmLive" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" OrganizationVersion="9.2.26043.159" OrganizationSchemaType="Standard" CRMServerServiceabilityVersion="9.2.26043.00159">
  <SolutionManifest>
    <UniqueName>PA45Handson</UniqueName>
    <LocalizedNames>
      <LocalizedName description="PA45 Hands-on (Vol.1-14)" languagecode="1041" />
    </LocalizedNames>
    <Descriptions />
    <Version>1.0.0.5</Version>
    <Managed>0</Managed>
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
{chr(10).join(root_components)}
    </RootComponents>
    {missing_block}
  </SolutionManifest>
</ImportExportXml>'''

content_types = '<?xml version="1.0" encoding="utf-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="xml" ContentType="application/octet-stream" /><Default Extension="json" ContentType="application/octet-stream" /></Types>'

out_path = os.path.join(SCRIPT_DIR, "PA45Handson_1_0_0_5.zip")
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
    out.writestr("customizations.xml", customizations.encode("utf-8"))
    out.writestr("solution.xml", solution.encode("utf-8"))
    out.writestr("[Content_Types].xml", content_types.encode("utf-8"))
    for p, b in json_files.items():
        out.writestr(p, b)
with open(out_path, "wb") as fp:
    fp.write(buf.getvalue())

print(f"OK {out_path} ({len(buf.getvalue())} bytes, {len(json_files)} json files)")
