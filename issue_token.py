#!/usr/bin/env python3
# issue_token.py

import os
import sys
import datetime
import jwt  # pip install PyJWT

# Load secret (defaults to your compose file value)
JWT_SECRET = os.getenv("JWT_SECRET", "asdfasdf")
# Algorithm must match what PostGraphile expects (HS256 by default)
ALGORITHM = "HS256"

def make_token(claims: dict, expires_in_hours: int = 100) -> str:
    now = datetime.datetime.utcnow()
    payload = {
        **claims,
        "iat": now,
        "exp": now + datetime.timedelta(hours=expires_in_hours),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

if __name__ == "__main__":
    # Example default claims – replace or extend as needed
    default_claims = {
        "role": "web_user",
        # add any other fields your RLS setup requires, e.g.:
        # "user_id": 42,
    }

    # Allow overriding via command-line JSON
    if len(sys.argv) > 1:
        import json
        try:
            default_claims = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            print("Failed to parse JSON claims; using defaults.", file=sys.stderr)

    token = make_token(default_claims, expires_in_hours=24)
    print(token)
