import httpx
import asyncio
import time
import sys
import os

# Base URL of the example app
BASE_URL = "http://localhost:8000"

async def run_shannon():
    print("🚀 [SHANNON] Initializing AI Pentest Agent...")
    async with httpx.AsyncClient() as client:
        
        # 1. Reconnaissance Phase
        print("\n🔍 [SHANNON] Phase 1: Reconnaissance")
        print("Checking homepage for vulnerabilities and metadata...")
        resp = await client.get(BASE_URL)
        if "<!--" in resp.text:
            print("Found comments in HTML. Analyzing for leaks...")
        
        # 2. Scanning / Probe Phase
        print("\n🧪 [SHANNON] Phase 2: Vulnerability Probing")
        probes = [
            "/?q=' UNION SELECT 1,2,3--",
            "/?redirect=javascript:alert(1)",
            "/?path=../../etc/passwd"
        ]
        for p in probes:
            print(f"Testing: {p}")
            try:
                r = await client.get(BASE_URL + p)
                print(f"Status: {r.status_code}")
                if r.status_code == 500:
                    print("Exploit triggered server error (Potential vulnerability!)")
            except Exception as e:
                print(f"Request failed: {e}")

        # 3. Hidden Path Discovery
        print("\n📂 [SHANNON] Phase 3: Hidden Path Discovery")
        paths = ["/admin", "/api/v1/users", "/admin/debug"]
        for path in paths:
            print(f"Attempting access to {path}...")
            r = await client.get(BASE_URL + path)
            print(f"Status: {r.status_code}")
            if r.status_code == 200:
                 print(f"Success! Data exfiltrated from {path}")

        # 4. Honeytoken Trap (Exfiltration)
        print("\n🍯 [SHANNON] Phase 4: Credential Exfiltration")
        # Simulate finding a leaked token in source code (Honeytoken)
        fake_token = "wukong_tk_test_trap_123" # This is our honeytoken
        print(f"Using discovered credential: {fake_token[:8]}...")
        auth_headers = {"Authorization": f"Bearer {fake_token}"}
        r = await client.get(BASE_URL + "/", headers=auth_headers)
        print(f"Status: {r.status_code}")
        if r.status_code == 401:
            print("Access denied. Token invalid or trapped.")

        # 5. Resource Exhaustion / Persistence (Tar Pitting Test)
        print("\n⌛ [SHANNON] Phase 5: Persistence & Resource Exhaustion")
        print("Repeating attacks to check for defensive adaptation...")
        for i in range(5):
            start = time.time()
            r = await client.get(BASE_URL + "/")
            elapsed = time.time() - start
            print(f"Request {i+1} took {elapsed:.2f}s | Status: {r.status_code}")
            if elapsed > 1.0:
                 print("!!! Server side delay detected. Wukong Tar-Pit active.")
            if r.status_code == 403:
                 print("!!! Access Blocked. Vulnerability Vacuum has banned us.")
                 break

    print("\n🏁 [SHANNON] Pentest complete.")

if __name__ == "__main__":
    asyncio.run(run_shannon())
