"""
x402 Scraper & Intelligence Client (Python)
Zero-credit card, HTTP 402 micro-settled scraping for autonomous AI agents on Base L2.
"""

import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

DEFAULT_ENDPOINT = "https://x402-scraper-engine.gejoe-tt.workers.dev"

class X402Scraper:
    def __init__(self, endpoint: str = DEFAULT_ENDPOINT, session_key: Optional[str] = None, internal_key: Optional[str] = None):
        self.endpoint = endpoint.rstrip("/")
        self.session_key = session_key
        self.internal_key = internal_key

    def _headers(self, receipt: Optional[str] = None) -> Dict[str, str]:
        headers = {
            "User-Agent": "x402-Python-Client/1.5",
            "Content-Type": "application/json"
        }
        if self.session_key:
            headers["X-Session-Key"] = self.session_key
        if self.internal_key:
            headers["X-ASOT-Internal-Key"] = self.internal_key
        if receipt:
            headers["X-Payment-Receipt"] = receipt
        return headers

    def read(self, url: str, receipt: Optional[str] = None) -> str:
        """Instant 1-tap proxy read returning clean Markdown."""
        clean_url = url if url.startswith("http") else f"https://{url}"
        req_url = f"{self.endpoint}/read/{clean_url}"
        req = urllib.request.Request(req_url, headers=self._headers(receipt))
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode("utf-8")

    def scrape(self, url: str, receipt: Optional[str] = None) -> Dict[str, Any]:
        """Scrape webpage and return structured Markdown payload ($0.005 USDC)."""
        req_url = f"{self.endpoint}/v1/scrape"
        payload = json.dumps({"url": url}).encode("utf-8")
        req = urllib.request.Request(req_url, data=payload, headers=self._headers(receipt))
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def extract(self, url: str, schema: Optional[Dict[str, Any]] = None, prompt: Optional[str] = None, receipt: Optional[str] = None) -> Dict[str, Any]:
        """Extract structured JSON adhering strictly to a schema via Edge Llama-3 ($0.030 USDC)."""
        req_url = f"{self.endpoint}/v1/extract"
        body = {"url": url}
        if schema:
            body["schema"] = schema
        if prompt:
            body["prompt"] = prompt
        payload = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(req_url, data=payload, headers=self._headers(receipt))
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
