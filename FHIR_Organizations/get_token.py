#!/usr/bin/env python3
# issue_token.py

import jwt  # pip install PyJWT
import datetime
import os
import json

# Config
JWT_SECRET = os.getenv("JWT_SECRET", "asdfasdf")
JWT_ALGORITHM = "HS256"
JWT_CLAIMS_TYPE = os.getenv("JWT_PG_TYPE_IDENTIFIER", "public.jwt_claims")

# Default claims — adjust these as needed for your RLS policies
claims = {
    "role": "web_user",
    "user_id": 1,
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    "iat": datetime.datetime.utcnow(),
}

# Encode token
token = jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)
print(token)
