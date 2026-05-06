import requests
import time
import json

GOPHISH_API = "https://localhost:3333/api"
GOPHISH_KEY = "e93b6b4b08157c8a9df964fc1433be3d18be0903b28fb7848123fe3c1fba4066"
SPLUNK_HEC  = "http://localhost:8088/services/collector/event"
SPLUNK_TOK  = "18bc99a6-100e-4219-a4c8-8b50ef2c1421"

def forward_events():
    campaigns = requests.get(
        f"{GOPHISH_API}/campaigns/",
        headers={"Authorization": f"Bearer {GOPHISH_KEY}"},
        verify=False
    ).json()

    for campaign in campaigns:
        for event in campaign.get("timeline", []):
            payload = {
                "event": event,
                "sourcetype": "_json",
                "source": "gophish",
                "index": "main"
            }
            requests.post(
                SPLUNK_HEC,
                json=payload,
                headers={"Authorization": f"Splunk {SPLUNK_TOK}"},
                verify=False
            )
            print(f"Forwarded event: {event.get('message')}")

while True:
    print("Polling GoPhish...")
    forward_events()
    time.sleep(60)
