import os

NOPS_API_URL = "https://app.nops.io/"
environment = os.environ.get("NOPS_ENV")
if environment == "UAT":
    NOPS_API_URL = "https://uat.nops.io/"
elif environment == "DEBUG":
    NOPS_API_URL = "http://127.0.0.1:8080/"
