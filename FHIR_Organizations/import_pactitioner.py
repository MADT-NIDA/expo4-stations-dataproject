#!/usr/bin/env python3
# import_participants.py

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
CSV_PATH = "FHIR_Department_Participants.csv"

driver = GraphDatabase.driver(URI, auth=AUTH)

def create_participant_constraint(tx):
    tx.run("""
    CREATE CONSTRAINT participant_id IF NOT EXISTS
    FOR (p:Participant)
    REQUIRE p.id IS UNIQUE;
    """)

def insert_participant(tx, row):
    tx.run("""
    MERGE (o:Organization {id: $organization_id})
    MERGE (d:Department   {id: $department_id})
    MERGE (p:Participant  {id: $id})
      SET p.name   = $name,
          p.role   = $role,
          p.phone  = $phone,
          p.email  = $email,
          p.active = toBoolean($active)
    MERGE (p)-[:WORKS_IN]->(d)
    MERGE (p)-[:BELONGS_TO]->(o)
    """, row)

def main():
    with driver.session() as session:
        session.execute_write(create_participant_constraint)
        print("✔ Participant constraint ensured")

    count = 0
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        required = {
            "id", "department_id", "organization_id",
            "name", "role", "phone", "email", "active"
        }
        headers = set(reader.fieldnames or [])
        missing = required - headers
        if missing:
            print(f"❗️ Missing columns in CSV: {missing}")
            sys.exit(1)

        with driver.session() as session:
            for row in reader:
                try:
                    params = {
                        "id":              row["id"].strip(),
                        "department_id":   row["department_id"].strip(),
                        "organization_id": row["organization_id"].strip(),
                        "name":            row["name"].strip(),
                        "role":            row["role"].strip(),
                        "phone":           row["phone"].strip(),
                        "email":           row["email"].strip(),
                        "active":          row["active"].strip(),
                    }
                    session.execute_write(insert_participant, params)
                    count += 1
                except Exception as e:
                    print(f"⚠️ Failed to insert participant {row.get('id')}: {e}", file=sys.stderr)

    print(f"✔ Imported {count} participants")
    driver.close()

if __name__ == "__main__":
    main()
