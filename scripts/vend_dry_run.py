import sys, yaml

for path in sys.argv[1:]:
    spec = yaml.safe_load(open(path))["spec"]
    name = path.split("/")[1]
    print(f"=== DRY RUN: {name} ===")
    print(f"1. Create subscription  sub-{name}")
    print(f"2. Move it under        {spec['targetManagementGroup']}")
    print(f"3. Tag it               BU={spec['businessUnit']} env={spec['environment']} costCentre={spec['costCentre']} owner={spec['ownerEmail']}")
    print(f"4. Budget alert         {spec['estimatedMonthlySpend']} per month, email {spec['ownerEmail']}")
    print(f"5. Allowed region       {spec['region']}")
    print(f"6. Network              {spec['connectivity']} (internal = peer spoke to hub)")
    print("SKIPPED live creation: free trial returns AccountNeedsUpgrade (needs EA/MCA billing scope).")