from supabase import create_client

SUPABASE_URL = "https://beorvnttfbczhjfkorcp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlb3J2bnR0ZmJjemhqZmtvcmNwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg2NDYxMDUsImV4cCI6MjA5NDIyMjEwNX0.Uu7wdxO4dxUF2uOFKKnARB6A_mnHpVzYBIwV_7wNCUs"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_attack_log(ip, attack_type, mitre_id, action, params, explanation):
    return supabase.table("attack_logs").insert({
        "attacker_ip": ip,
        "attack_type": attack_type,
        "mitre_id": mitre_id,
        "action": action,
        "parameters": params,
        "explanation": explanation
    }).execute()