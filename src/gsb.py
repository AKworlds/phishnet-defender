import requests

def check_url_gsb(url, api_key):
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"

    payload = {
        "client": {
            "clientId": "phishnet-defender",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE", 
                "SOCIAL_ENGINEERING", 
                "UNWANTED_SOFTWARE"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    response = requests.post(endpoint, json=payload)
    if response.status_code == 200:
        matches = response.json().get("matches")
        return True if matches else False
    else:
        print("❌ Google Safe Browsing API error:", response.text)
        return False
