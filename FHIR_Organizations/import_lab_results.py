#!/usr/bin/env python3
# import_lab_results.py

import os
import csv
import sys
from neo4j import GraphDatabase, basic_auth

# --- CONFIG ---
URI = os.getenv("NEO4J_URI", "bolt://34.143.247.40:7687")
AUTH = basic_auth(
    os.getenv("NEO4J_USER", "neo4j"),
    os.getenv("NEO4J_PASSWORD", "letmein123")
)
CSV_PATH = "FHIR_Lab_Results.csv"

driver = GraphDatabase.driver(URI, auth=AUTH)

def create_lab_result_constraint(tx):
    tx.run("""
    CREATE CONSTRAINT lab_result_id IF NOT EXISTS
    FOR (l:LabResult)
    REQUIRE l.id IS UNIQUE;
    """)

def insert_lab_result(tx, row):
    tx.run("""
    MERGE (p:Patient      {id: $patient_id})
    MERGE (e:Encounter    {id: $encounter_id})
    MERGE (o:Organization {id: $organization_id})
    MERGE (d:Department   {id: $department_id})
    MERGE (l:LabResult    {id: $id})
      SET l.test_code     = $test_code,
          l.test_display  = $test_display,
          l.value         = $value,
          l.unit          = $unit,
          l.status        = $status,
          l.issued        = datetime($issued)
    MERGE (p)-[:HAS_LAB_RESULT]->(l)
    MERGE (l)-[:RECORDED_DURING]->(e)
    MERGE (l)-[:IN_DEPARTMENT]->(d)
    MERGE (l)-[:AT_ORGANIZATION]->(o)
    """, row)

def main():
    with driver.session() as session:
        session.execute_write(create_lab_result_constraint)
        print("✔ LabResult constraint ensured")

    count = 0
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        required = {
            "id", "encounter_id", "patient_id", "organization_id", "department_id",
            "test_code", "test_display", "value", "unit", "status", "issued"
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
                        "id":               row["id"].strip(),
                        "encounter_id":     row["encounter_id"].strip(),
                        "patient_id":       row["patient_id"].strip(),
                        "organization_id":  row["organization_id"].strip(),
                        "department_id":    row["department_id"].strip(),
                        "test_code":        row["test_code"].strip(),
                        "test_display":     row["test_display"].strip(),
                        "value":            row["value"].strip(),
                        "unit":             row["unit"].strip(),
                        "status":           row["status"].strip(),
                        "issued":           row["issued"].strip(),
                    }
                    session.execute_write(insert_lab_result, params)
                    count += 1
                except Exception as e:
                    print(f"⚠️ Failed to insert lab result {row.get('id')}: {e}", file=sys.stderr)

    print(f"✔ Imported {count} lab results")
    driver.close()

if __name__ == "__main__":
    main()
