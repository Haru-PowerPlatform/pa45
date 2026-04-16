import zipfile, re, io, sys
sys.stdout.reconfigure(encoding='utf-8')

flows = [
    {"vol":"vol-01","json":"Workflows/PA45_P001_InitializeVariable-C3A95FA2-DA15-F111-8341-002248F08C86.json","id":"c3a95fa2-da15-f111-8341-002248f08c86","name":"PA45_P001_InitializeVariable"},
    {"vol":"vol-02","json":"Workflows/PA45_P002__-2CF1DC51-7F1B-F111-8341-002248F08C86.json","id":"2cf1dc51-7f1b-f111-8341-002248f08c86","name":"PA45_P002_SetVariable"},
    {"vol":"vol-03","json":"Workflows/PA45-P003--5B54E6CF-E628-F111-88B3-002248F08C86.json","id":"5b54e6cf-e628-f111-88b3-002248f08c86","name":"PA45_P003_Condition"},
    {"vol":"vol-04","json":"Workflows/PA45_P004_ApplyToEach_-066DDF38-CD2D-F111-88B4-002248F08C86.json","id":"066ddf38-cd2d-f111-88b4-002248f08c86","name":"PA45_P004_ApplyToEach"},
    {"vol":"vol-05","json":"Workflows/PA45_No5-349DAC4F-C833-F111-88B4-002248F08C86.json","id":"349dac4f-c833-f111-88b4-002248f08c86","name":"PA45_No5_Review"},
    {"vol":"vol-06","json":"Workflows/PA45-P006-Formsteams-23911156-F136-F111-88B4-002248F08C86.json","id":"23911156-f136-f111-88b4-002248f08c86","name":"PA45_P006_FormsMail"},
]

with zipfile.ZipFile("PA45Handson_1_0_0_4.zip") as src:
    full_custom = src.read("customizations.xml").decode("utf-8")
    content_types = src.read("[Content_Types].xml")

    for f in flows:
        wf_pat = re.compile(
            r'<Workflow WorkflowId="\{' + re.escape(f["id"]) + r'\}".*?</Workflow>',
            re.DOTALL | re.IGNORECASE
        )
        wf_match = wf_pat.search(full_custom)
        if not wf_match:
            print(f"WARNING: {f['vol']} not found")
            continue

        custom_xml = f'''<ImportExportXml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" OrganizationVersion="9.2.26034.167">
  <Entities></Entities><Roles></Roles>
  <Workflows>
    {wf_match.group(0)}
  </Workflows>
</ImportExportXml>'''

        solution_xml = f'''<ImportExportXml version="9.2.26034.167" SolutionPackageVersion="9.2" languagecode="1041" generatedBy="CrmLive" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <SolutionManifest>
    <UniqueName>PA45_{f["name"]}</UniqueName>
    <LocalizedNames><LocalizedName description="PA45 {f["name"]}" languagecode="1041" /></LocalizedNames>
    <Descriptions />
    <Version>1.0.0.1</Version>
    <Managed>0</Managed>
    <Publisher>
      <UniqueName>pa45</UniqueName>
      <LocalizedNames><LocalizedName description="PA45" languagecode="1041" /></LocalizedNames>
      <CustomizationPrefix>pa45</CustomizationPrefix>
    </Publisher>
    <RootComponents>
      <RootComponent type="29" id="{{{f["id"]}}}" behavior="0" />
    </RootComponents>
    <MissingDependencies />
  </SolutionManifest>
</ImportExportXml>'''

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
            out.writestr("solution.xml",        solution_xml.encode("utf-8"))
            out.writestr("customizations.xml",  custom_xml.encode("utf-8"))
            out.writestr("[Content_Types].xml",  content_types)
            out.writestr(f["json"],              src.read(f["json"]))
        with open(f"{f['vol']}/flow.zip", "wb") as fp:
            fp.write(buf.getvalue())
        print(f"OK {f['vol']}/flow.zip  ({len(buf.getvalue())} bytes)")

print("done")
