#!/usr/bin/env python3
# organization_dep.py

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
CSV_PATH = "FHIR_Organization_Departments.csv"

driver = GraphDatabase.driver(URI, auth=AUTH)

def create_department_constraint(tx):
    tx.run("""
    CREATE CONSTRAINT department_id IF NOT EXISTS
      FOR (d:Department)
      REQUIRE d.id IS UNIQUE;
    """)

def import_department(tx, params):
    tx.run("""
    MERGE (o:Organization {id: $organization_id})
    MERGE (d:Department   {id: $id})
      SET d.name  = $name,
          d.head  = $head,
          d.phone = $phone,
          d.email = $email
    MERGE (o)-[:HAS_DEPARTMENT]->(d)
    """, **params)

def main():
    # 1) Ensure constraint
    with driver.session() as session:
        session.execute_write(create_department_constraint)
        print("✔ Department constraint ensured")

    # 2) Open CSV and inspect headers
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        print("CSV headers detected:", headers)

        # Verify expected columns
        required = {"id", "organization_id", "department_name", "head", "phone", "email"}
        missing = required - set(headers)
        if missing:
            print(f"❗️ Missing expected columns in CSV: {missing}", file=sys.stderr)
            sys.exit(1)

        # 3) Import rows
        count = 0
        with driver.session() as session:
            for row in reader:
                params = {
                    "id":               row["id"].strip(),
                    "organization_id":  row["organization_id"].strip(),
                    "name":             row["department_name"].strip(),  # mapped correctly
                    "head":             row["head"].strip(),
                    "phone":            row["phone"].strip(),
                    "email":            row["email"].strip(),
                }
                try:
                    session.execute_write(import_department, params)
                    count += 1
                except Exception as e:
                    print(f"⚠️ Skipped row {row.get('id','<no-id>')}: {e}", file=sys.stderr)

        print(f"✔ Imported {count} department records")

    driver.close()

if __name__ == "__main__":
    main()
