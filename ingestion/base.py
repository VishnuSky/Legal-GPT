"""Abstract Base Connector for Legal Source Ingestion."""

import abc
import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import httpx
from normalization.models import LegalDocument

logger = logging.getLogger("legal_gpt.ingestion")


class BaseLegalConnector(abc.ABC):
    """Abstract base class for all authoritative legal connectors."""

    def __init__(
        self,
        source_id: str,
        cache_dir: str = ".cache/ingestion",
        rate_limit_delay_seconds: float = 1.0,
        timeout_seconds: float = 30.0
    ):
        self.source_id = source_id
        self.cache_dir = Path(cache_dir) / source_id
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.rate_limit_delay = rate_limit_delay_seconds
        self.timeout = timeout_seconds
        self.last_request_time: float = 0.0

    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    def fetch_url(self, url: str, headers: Optional[Dict[str, str]] = None, use_cache: bool = True) -> str:
        """Fetches URL content with local disk caching and rate limiting."""
        url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
        cache_file = self.cache_dir / f"{url_hash}.cache"

        if use_cache and cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                logger.warning(f"Cache read error for {url}: {e}")

        self._rate_limit()
        req_headers = headers or {}
        if "User-Agent" not in req_headers:
            req_headers["User-Agent"] = "Legal-GPT-Bot/0.1.1 (Research & Educational Legal Ingestion)"

        with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
            response = client.get(url, headers=req_headers)
            response.raise_for_status()
            content = response.text

            try:
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception as e:
                logger.warning(f"Cache write error for {url}: {e}")

            return content

    @abc.abstractmethod
    def ingest(self, **kwargs) -> List[LegalDocument]:
        """Performs extraction and returns standardized LegalDocuments."""
        pass
