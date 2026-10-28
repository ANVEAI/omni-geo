"""
Platform End-to-End Verification Test
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def run_tests():
    print("[*] Testing Dashboard GET / ...")
    r1 = client.get("/")
    assert r1.status_code == 200, f"Dashboard failed: {r1.status_code}"
    assert "OmniGEO" in r1.text
    print(" -> Dashboard OK (200)")

    print("[*] Testing Sample Report GET /report/audit_linear_sample ...")
    r2 = client.get("/report/audit_linear_sample")
    assert r2.status_code == 200, f"Sample report failed: {r2.status_code}"
    assert "Generative AI Search Audit" in r2.text
    assert "Linear" in r2.text
    print(" -> Sample Report OK (200)")

    print("[*] Testing GTM Sales Machine GET /gtm-kit ...")
    r3 = client.get("/gtm-kit")
    assert r3.status_code == 200, f"GTM Kit failed: {r3.status_code}"
    assert "GTM Sales Machine" in r3.text
    print(" -> GTM Kit OK (200)")

    print("[*] Testing Live Audit API POST /api/audit ...")
    payload = {
        "brand_name": "Supabase",
        "domain": "https://supabase.com",
        "niche": "Backend as a Service & Database",
        "competitors": ["Firebase", "AWS Amplify"],
        "custom_queries": ["What is the best open source alternative to Firebase?"]
    }
    r4 = client.post("/api/audit", json=payload)
    assert r4.status_code == 200, f"Live audit failed: {r4.status_code} - {r4.text}"
    data = r4.json()
    assert data.get("status") == "success"
    audit_id = data.get("audit_id")
    print(f" -> Live Audit Succeeded! Generated Audit ID: {audit_id}")

    print(f"[*] Testing Generated Report GET /report/{audit_id} ...")
    r5 = client.get(f"/report/{audit_id}")
    assert r5.status_code == 200
    assert "Supabase" in r5.text
    assert "Firebase" in r5.text
    print(" -> Generated Report OK (200)")

    print("[*] Testing Workspace Dashboard GET /dashboard ...")
    r_dash = client.get("/dashboard")
    assert r_dash.status_code == 200, f"Dashboard failed: {r_dash.status_code}"
    assert "Active Brand Intelligence" in r_dash.text
    print(" -> Workspace Dashboard OK (200)")

    print("[*] Testing /llms.txt Tool GET /tools/llms-txt-generator ...")
    r_llms = client.get("/tools/llms-txt-generator")
    assert r_llms.status_code == 200
    assert "llms.txt" in r_llms.text
    print(" -> /llms.txt Tool OK (200)")

    print("[*] Testing AI Bot Tester GET /tools/robots-txt-tester ...")
    r_rob = client.get("/tools/robots-txt-tester")
    assert r_rob.status_code == 200
    assert "robots.txt" in r_rob.text
    print(" -> AI Bot Tester OK (200)")

    print("[*] Testing AI Bot API POST /api/tools/check-robots ...")
    r_rob_api = client.post("/api/tools/check-robots", json={"url": "https://linear.app"})
    assert r_rob_api.status_code == 200
    rob_data = r_rob_api.json()
    assert "bot_permissions" in rob_data
    print(" -> AI Bot API OK (200)")

    print("[*] Testing Pricing GET /pricing ...")
    r_price = client.get("/pricing")
    assert r_price.status_code == 200
    assert "Pricing" in r_price.text
    print(" -> Pricing Page OK (200)")

    print("\n[SUCCESS] ALL END-TO-END TESTS PASSED FLACID-FREE!")

if __name__ == "__main__":
    run_tests()
