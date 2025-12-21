import os
from dotenv import load_dotenv

load_dotenv()

gms_key = os.getenv("GMS_KEY")
print(f"GMS_KEY exists: {gms_key is not None}")
print(f"GMS_KEY length: {len(gms_key) if gms_key else 0}")
print(f"GMS_KEY value: {gms_key[:10]}..." if gms_key and len(gms_key) > 10 else f"GMS_KEY value: {gms_key}")
