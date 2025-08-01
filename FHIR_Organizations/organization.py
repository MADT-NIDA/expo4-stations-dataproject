#!/usr/bin/env python3
# organization.py

import os
import csv
from neo4j import GraphDatabase, basic_auth

# --- CONFIG ---
URI      = os.getenv("NEO4J_URI", "bolt://34.143.247.40:7687")
AUTH     = basic_auth("neo4j", "letmein123")
CSV_PATH = "FHIR_Organizations.csv"

driver = GraphDatabase.driver(URI, auth=AUTH)

def create_constraint(tx):
    tx.run(
        """
        CREATE CONSTRAINT organization_id IF NOT EXISTS
          FOR (o:Organization)
          REQUIRE o.id IS UNIQUE;
        """
    )

def import_orgs(tx, row):
    tx.run(
        """
        MERGE (o:Organization {id: $id})
        SET
          o.name         = $name,
          o.type         = $type,
          o.addressLine  = $address_line,
          o.city         = $city,
          o.state        = $state,
          o.postalCode   = $postalCode,
          o.country      = $country,
          o.phone        = $phone,
          o.email        = $email,
          o.active       = toBoolean($active)
        """,
        **row
    )

with driver.session() as session:
    # 1) Create uniqueness constraint in its own transaction
    session.execute_write(create_constraint)
    print("✔ Constraint ensured")

    # 2) Load CSV and import rows in a separate transaction per batch
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            session.execute_write(import_orgs, row)
            count += 1
    print(f"✔ Imported {count} organizations")

driver.close()
