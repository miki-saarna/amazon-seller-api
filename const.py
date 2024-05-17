import os
from dotenv import load_dotenv

load_dotenv()

REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]
LWA_APP_ID = os.environ["LWA_APP_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_KEY_ID = os.environ["AWS_SECRET_KEY_ID"]
ROLE_ARN = os.environ["ROLE_ARN"]
REGION_NAME = os.environ["REGION_NAME"]

# GOOGLE_SHEETS_EMAIL = os.environ["GOOGLE_SHEETS_EMAIL"]
GS_INVENTORY_ID = os.environ["GS_INVENTORY_ID"]
GS_INVENTORY_NAME = os.environ["GS_INVENTORY_NAME"]

GS_COMMISSION_URL = os.environ["GS_COMMISSION_URL"]
GS_COMMISSION_ID = os.environ["GS_COMMISSION_ID"]
GS_COMMISSION_NAME = os.environ["GS_COMMISSION_NAME"]


OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
