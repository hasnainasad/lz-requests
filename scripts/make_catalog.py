import os, sys, yaml

repo = os.environ.get("GITHUB_REPOSITORY", "hasnainasad/lz-requests")
for path in sys.argv[1:]:
    req = yaml.safe_load(open(path))
    name, spec = req["metadata"]["name"], req["spec"]
    bu = spec["businessUnit"].lower().replace(" & ", "-").replace(" ", "-")
    card = {
        "apiVersion": "backstage.io/v1alpha1",
        "kind": "Resource",
        "metadata": {
            "name": f"sub-{name}",
            "title": f"Azure subscription sub-{name}",
            "description": spec["justification"],
            "tags": ["azure-subscription", spec["environment"]],
            "annotations": {
                "lz.platform/status": "vended (dry run)",
                "lz.platform/management-group": spec["targetManagementGroup"],
                "lz.platform/region": spec["region"],
                "lz.platform/cost-centre": spec["costCentre"],
                "lz.platform/owner-email": spec["ownerEmail"],
            },
            "links": [{"url": f"https://github.com/{repo}/blob/main/{path}", "title": "Request file"}],
        },
        "spec": {"type": "azure-subscription", "owner": f"group:default/{bu}"},
    }
    out = os.path.join(os.path.dirname(path), "catalog-info.yaml")
    yaml.safe_dump(card, open(out, "w"), sort_keys=False)
    print(f"Wrote {out}")