import requests
from requests.adapters import HTTPAdapter, Retry
from .conf import API_KEY

# Create the session with retries
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=0.1,
    status_forcelist=[500, 501, 502, 504],
)
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))
session.headers.update(
    {"Accept": "application/json", "Authorization": f"Bearer {API_KEY}"}
)
