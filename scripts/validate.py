import glob, re, sys, yaml

REQUIRED = ["applicationName", "businessUnit", "environment", "ownerEmail", "costCentre",
            "justification", "targetManagementGroup", "region", "dataClassification",
            "connectivity", "estimatedMonthlySpend"]
BUSINESS_UNITS = ["Range", "Supply Chain", "Retail Concept", "Operations"]
ENVIRONMENTS = ["sandbox", "dev", "test", "prod"]

failed = False
for path in glob.glob("requests/*/request.yaml"):
    doc = yaml.safe_load(open(path))
    spec = doc.get("spec", {})
    errors = [f"missing field: {f}" for f in REQUIRED if f not in spec]
    if doc.get("kind") != "AzureSubscriptionRequest":
        errors.append("kind must be AzureSubscriptionRequest")
    if doc.get("metadata", {}).get("name") != path.split("/")[1]:
        errors.append("metadata.name must match the folder name")
    if spec.get("businessUnit") not in BUSINESS_UNITS:
        errors.append(f"businessUnit must be one of {BUSINESS_UNITS}")
    if spec.get("environment") not in ENVIRONMENTS:
        errors.append(f"environment must be one of {ENVIRONMENTS}")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", str(spec.get("ownerEmail", ""))):
        errors.append("ownerEmail is not a valid email")
    if not re.fullmatch(r"CC-\d{4}", str(spec.get("costCentre", ""))):
        errors.append("costCentre must look like CC-1234")
    if errors:
        failed = True
        print(f"FAIL {path}")
        for e in errors:
            print(f"   - {e}")
    else:
        print(f"PASS {path}")

sys.exit(1 if failed else 0)
