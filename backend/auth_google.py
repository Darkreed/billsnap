from google_auth_oauthlib.flow import InstalledAppFlow
from app.calendar.client import SCOPES, CREDENTIALS_FILE, TOKEN_FILE

flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
creds = flow.run_local_server(port=0)

with open(TOKEN_FILE, 'w') as f:
    f.write(creds.to_json())

print(f"Token saved to {TOKEN_FILE}")
