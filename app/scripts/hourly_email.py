import requests
import sys

# Call your own API to trigger email
try:
    response = requests.post(
        "https://my-folio-api.onrender.com/email/send-poc",
        json={
            "subject": "Hourly Update",
            "body": "<p>This is the scheduled hourly mail.</p>",
            "to": ["poc@myfolio.catalytix.in"],
            "cc": []
        },
        timeout=75
    )
    print("Response:", response.json())
    sys.exit(0)
except Exception as e:
    print("Error:", str(e))
    sys.exit(1)