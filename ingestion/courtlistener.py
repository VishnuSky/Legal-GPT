"""CourtListener API Connector for Court Opinions, Dockets, and Citation Graphs."""

import os
import json
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from ingestion.base import BaseLegalConnector
from normalization.models import LegalDocument, TemporalMetadata, AuthorityScore
from normalization.chunkers import StatuteChunker

logger = logging.getLogger("legal_gpt.courtlistener")


class CourtListenerConnector(BaseLegalConnector):
    BASE_URL = "https://www.courtlistener.com/api/rest/v4"

    def __init__(self, api_token: Optional[str] = None):
        super().__init__(source_id="FED_COURTLISTENER", rate_limit_delay_seconds=1.0)
        self.api_token = api_token or os.getenv("COURTLISTENER_API_TOKEN")

    def search_opinions(self, query: str, jurisdiction: Optional[str] = None, page_size: int = 5) -> Dict[str, Any]:
        """Searches CourtListener opinions with optional jurisdiction filter."""
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Token {self.api_token}"

        params = f"q={query}&type=o&order_by=score%20desc"
        if jurisdiction:
            params += f"&court={jurisdiction}"

        url = f"{self.BASE_URL}/search/?{params}"
        try:
            content = self.fetch_url(url, headers=headers)
            return json.loads(content)
        except Exception as e:
            logger.warning(f"CourtListener search failed: {e}")
            return {"count": 0, "results": []}

    def ingest(self, **kwargs) -> List[LegalDocument]:
        return []
