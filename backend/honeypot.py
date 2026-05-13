def engage(ip):
    return {"status": "engaged", "decoy": "Fake Nginx 1.23.4"}

def isolate(ip):
    return {"status": "isolated", "sandbox": True}

def spawn(service="http"):
    return {"status": "spawned", "service": service, "id": "honeypot_new"}