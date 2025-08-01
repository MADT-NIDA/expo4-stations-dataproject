#!/usr/bin/env python3
# import_encounters.py

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
CSV_PATH = "FHIR_Encounters_With_Department.csv"

driver = GraphDatabase.driver(URI, auth=AUTH)

def create_encounter_constraint(tx):
    tx.run("""
    CREATE CONSTRAINT encounter_id IF NOT EXISTS
    FOR (e:Encounter)
    REQUIRE e.id IS UNIQUE;
    """)

def insert_encounter(tx, row):
    tx.run("""
    MERGE (p:Patient      {id: $patient_id})
    MERGE (o:Organization {id: $organization_id})
    MERGE (d:Department   {id: $department_id})
    MERGE (e:Encounter    {id: $id})
      SET e.status         = $status,
          e.encounterClass = $encounter_class,
          e.start          = datetime($start_date),
          e.end            = datetime($end_date),
          e.reason         = $reason
    MERGE (p)-[:HAS_ENCOUNTER]->(e)
    MERGE (e)-[:AT_ORGANIZATION]->(o)
    MERGE (e)-[:IN_DEPARTMENT]->(d)
    """, row)

def main():
    with driver.session() as session:
        session.execute_write(create_encounter_constraint)
        print("✔ Encounter constraint ensured")

    count = 0
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        required = {
            "id", "patient_id", "organization_id", "department_id",
            "encounter_class", "start_date", "end_date", "status", "reason"
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
                        "id": row["id"].strip(),
                        "patient_id": row["patient_id"].strip(),
                        "organization_id": row["organization_id"].strip(),
                        "department_id": row["department_id"].strip(),
                        "encounter_class": row["encounter_class"].strip(),
                        "start_date": row["start_date"].strip(),
                        "end_date": row["end_date"].strip(),
                        "status": row["status"].strip(),
                        "reason": row["reason"].strip(),
                    }
                    session.execute_write(insert_encounter, params)
                    count += 1
                except Exception as e:
                    print(f"⚠️ Failed to insert encounter {row.get('id')}: {e}", file=sys.stderr)

    print(f"✔ Imported {count} encounters")
    driver.close()

if __name__ == "__main__":
    main()
