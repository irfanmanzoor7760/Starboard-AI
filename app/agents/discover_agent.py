import requests
from typing import List, Dict, Optional
from urllib.parse import urljoin
from collections import defaultdict


class APIDiscoveryAgent:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def test_connection(self) -> bool:
        try:
            response = requests.get(self.base_url, timeout=10)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def discover_endpoints(self) -> List[str]:
        """Basic: Try to list sub-endpoints from common paths."""
        candidates = ["data", "datasets", "properties", "api", "records", "public"]
        discovered = []

        for path in candidates:
            full_url = urljoin(self.base_url + "/", path)
            try:
                r = requests.get(full_url, timeout=5)
                if r.ok and r.headers.get("Content-Type", "").startswith("application/json"):
                    discovered.append(full_url)
            except requests.RequestException:
                continue

        return discovered

    def sample_fields(self, endpoint: str) -> Dict:
        """Attempt to extract sample field names from a JSON endpoint."""
        try:
            r = requests.get(endpoint, timeout=5)
            data = r.json()
            if isinstance(data, list) and data:
                return {"fields": list(data[0].keys())}
            elif isinstance(data, dict):
                return {"fields": list(data.keys())}
        except Exception as e:
            return {"error": str(e)}
        return {}

    def full_discovery(self) -> Dict:
        if not self.test_connection():
            return {"error": "Unable to connect to base URL"}

        endpoints = self.discover_endpoints()
        output = defaultdict(dict)

        for ep in endpoints:
            result = self.sample_fields(ep)
            output[ep] = result

        return {
            "base_url": self.base_url,
            "endpoints": output
        }
