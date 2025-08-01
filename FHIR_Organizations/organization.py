# insert_via_graphile.py
import os
import csv
import requests

# --- CONFIG ---
GRAPHILE_URL = os.getenv("GRAPHILE_URL", "http://expo4.madt.pro:5000/graphql")
TOKEN        = os.getenv("JWT_TOKEN", "asdfasdf")  # from issue_token.py
CSV_FILE     = "FHIR_Organizations.csv"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}",
}

mutation = """
mutation CreateOrg($input: CreatePublicOrganizationInput!) {
  createPublicOrganization(input: $input) {
    organization {
      id
    }
  }
}
"""

def row_to_input(row):
    return {
        "organization": {
            "id":           row["id"],
            "name":         row["name"],
            "type":         row["type"],
            "addressLine":  row["address_line"],
            "city":         row["city"],
            "state":        row["state"],
            "postalCode":   row["postalCode"],
            "country":      row["country"],
            "phone":        row["phone"],
            "email":        row["email"],
            "active":       row["active"].lower() in ("true", "1", "t"),
        }
    }

with open(CSV_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        payload = {
            "query": mutation,
            "variables": {"input": row_to_input(row)}
        }
        resp = requests.post(GRAPHILE_URL, json=payload, headers=headers)
        data = resp.json()
        if resp.status_code != 200 or data.get("errors"):
            print("❌ Error inserting", row["id"], data.get("errors"))
        else:
            print("✅ Inserted", data["data"]["createPublicOrganization"]["organization"]["id"])
