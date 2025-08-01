#!/usr/bin/env python3
# import_patients.py

import os
import csv
import sys
from neo4j import GraphDatabase, basic_auth

# --- CONFIG ---
URI      = os.getenv("NEO4J_URI", "bolt://34.143.247.40:7687")
AUTH     = basic_auth(
    os.getenv("NEO4J_USER", "neo4j"),
    os.getenv("NEO4J_PASSWORD", "letmein123")
)
CSV_PATH = "FHIR_Patients.csv"

driver = GraphDatabase.driver(URI, auth=AUTH)

def create_patient_constraint(tx):
    tx.run("""
    CREATE CONSTRAINT patient_id IF NOT EXISTS
      FOR (p:Patient)
      REQUIRE p.id IS UNIQUE;
    """)

def import_patient(tx, params):
    tx.run("""
    MERGE (o:Organization {id: $organization_id})
    MERGE (p:Patient      {id: $id})
      SET p.name        = $name,
          p.gender      = $gender,
          p.birthDate   = date($birth_date),
          p.phone       = $phone,
          p.email       = $email,
          p.address     = $address,
          p.active      = toBoolean($active)
    MERGE (o)-[:HAS_PATIENT]->(p)
    """, **params)

def main():
    # 1) Ensure constraint
    with driver.session() as session:
        session.execute_write(create_patient_constraint)
        print("✔ Patient constraint ensured")

    # 2) Open CSV and inspect headers
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        print("CSV headers detected:", headers)

        # Expected columns
        required = {
            "id", "organization_id", "name",
            "gender", "birth_date", "phone",
            "email", "address", "active"
        }
        missing = required - set(headers)
        if missing:
            print(f"❗️ Missing expected columns in CSV: {missing}", file=sys.stderr)
            sys.exit(1)

        # 3) Import rows
        count = 0
        with driver.session() as session:
            for row in reader:
                params = {
                    "id":                row["id"].strip(),
                    "organization_id":   row["organization_id"].strip(),
                    "name":              row["name"].strip(),
                    "gender":            row["gender"].strip(),
                    "birth_date":        row["birth_date"].strip(),
                    "phone":             row["phone"].strip(),
                    "email":             row["email"].strip(),
                    "address":           row["address"].strip(),
                    "active":            row["active"].strip(),
                }
                try:
                    session.execute_write(import_patient, params)
                    count += 1
                except Exception as e:
                    print(f"⚠️ Skipped patient {params['id']}: {e}", file=sys.stderr)
        print(f"✔ Imported {count} patient records")

    driver.close()

if __name__ == "__main__":
    main()
