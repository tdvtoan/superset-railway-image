#!/usr/bin/env python3
"""
Diagnose Superset API connectivity
"""

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SUPERSET_URL = "https://superset-railway-image-production-6d86.up.railway.app"

print("\n=== Superset API Diagnostics ===\n")

# Test 1: Basic connectivity
print("[1] Testing basic connectivity...")
try:
    response = requests.get(f"{SUPERSET_URL}/", verify=False, timeout=5)
    print(f"✓ Main page accessible: Status {response.status_code}")
except Exception as e:
    print(f"✗ Main page not accessible: {e}")

# Test 2: API root
print("\n[2] Testing API endpoint...")
try:
    response = requests.get(f"{SUPERSET_URL}/api/v1/", verify=False, timeout=5)
    print(f"✓ API root accessible: Status {response.status_code}")
except Exception as e:
    print(f"✗ API root not accessible: {e}")

# Test 3: Health endpoint
print("\n[3] Testing health endpoint...")
try:
    response = requests.get(
        f"{SUPERSET_URL}/api/v1/health", verify=False, timeout=5
    )
    print(f"✓ Health check: Status {response.status_code}")
    if response.status_code == 200:
        print(f"  Response: {response.json()}")
except Exception as e:
    print(f"✗ Health check failed: {e}")

# Test 4: Login endpoint (OPTIONS request to check if endpoint exists)
print("\n[4] Testing login endpoint...")
try:
    response = requests.options(
        f"{SUPERSET_URL}/api/v1/security/login", verify=False, timeout=5
    )
    print(f"✓ Login endpoint exists: Status {response.status_code}")
except Exception as e:
    print(f"✗ Login endpoint check failed: {e}")

# Test 5: Try login with JSON
print("\n[5] Attempting login...")
try:
    response = requests.post(
        f"{SUPERSET_URL}/api/v1/security/login",
        json={"username": "admin", "password": "#Stayahead88"},
        verify=False,
        timeout=5,
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    if response.status_code == 200:
        print("✓ Login successful!")
    else:
        print(f"✗ Login failed")
except requests.exceptions.Timeout:
    print("✗ Login request timed out (5s)")
except Exception as e:
    print(f"✗ Login request failed: {e}")

print("\n=== Diagnostics Complete ===\n")
print("Next steps:")
print("1. If API is not accessible, check Railway deployment logs")
print("2. If login fails, verify credentials in .env.local")
print("3. Consider manual dashboard creation via UI")
