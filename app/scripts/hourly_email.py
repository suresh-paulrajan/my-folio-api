import requests

# Call your own API to trigger email
response = requests.post(
    "https://my-folio-api.onrender.com/email/send-poc",
    json={
        "subject": "Hourly Update",
        "body": "<p>This is the scheduled hourly mail.</p>",
        "to": ["sureshpaulrajan@gmail.com"],
        "cc": ["sureshkanna.ece@gmail.com","poc@myfolio.catalytix.in"]
    }
)
print("Response:", response.json())