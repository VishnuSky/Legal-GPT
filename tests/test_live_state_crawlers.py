import hashlib
from pathlib import Path
from unittest.mock import patch

from ingestion.pipeline import IngestionPipeline
from ingestion.state_crawlers.california import CaliforniaLegConnector
from ingestion.state_crawlers.florida import FloridaLegConnector
from ingestion.state_crawlers.new_york import NewYorkLegConnector
from ingestion.state_crawlers.texas import TexasLegConnector


def test_california_parser_handles_leginfo_structure_and_url_path():
    crawler = CaliforniaLegConnector()
    fixture_html = """
    <html><body>
      <div class="codeSection">
        <h6>Section 300 - Persons subject to jurisdiction of juvenile court</h6>
        <div class="lawText">
          <p>(a) Any child who has suffered serious physical harm.</p>
          <p>(b) Any child at substantial risk of neglect &amp; abuse.</p>
        </div>
      </div>
    </body></html>
    """

    doc = crawler.parse_wic_html("300", "Fallback title", fixture_html)
    assert doc.citation == "Cal. Welf. & Inst. Code § 300"
    assert "serious physical harm" in doc.full_text
    assert "&" in doc.full_text
    assert "division=2." in doc.source_url
    assert "chapter=2." in doc.source_url


def test_california_offline_fallback_returns_complete_document():
    crawler = CaliforniaLegConnector()
    with patch.object(crawler, "fetch_url", side_effect=RuntimeError("offline")):
        doc = crawler.fetch_wic_section("315", "Detention hearing; setting; time limits")

    assert doc.citation
    assert doc.full_text
    assert doc.jurisdiction == "US-CA"


def test_california_cache_key_is_url_sha256(tmp_path):
    crawler = CaliforniaLegConnector()
    crawler.cache_dir = Path(tmp_path)
    crawler.cache_dir.mkdir(parents=True, exist_ok=True)

    class DummyResponse:
        text = "same body"

        @staticmethod
        def raise_for_status():
            return None

    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return None

        def get(self, *args, **kwargs):
            return DummyResponse()

    with patch("ingestion.base.httpx.Client", DummyClient):
        crawler.fetch_url("https://example.org/a", use_cache=True)
        crawler.fetch_url("https://example.org/b", use_cache=True)

    expected_a = hashlib.sha256("https://example.org/a".encode("utf-8")).hexdigest()
    expected_b = hashlib.sha256("https://example.org/b".encode("utf-8")).hexdigest()
    assert (crawler.cache_dir / f"{expected_a}.cache").exists()
    assert (crawler.cache_dir / f"{expected_b}.cache").exists()


def test_texas_parser_isolates_section_and_subsection_without_bleed():
    crawler = TexasLegConnector()
    chapter_html = """
    <html><body>
      <h3>Sec. 262.104. TAKING POSSESSION OF CHILD IN EMERGENCY.</h3>
      <p>(a) A governmental entity may take possession of a child without a court order.</p>
      <p>(b) Possession must be followed by notice to the court.</p>
      <h3>Sec. 262.105. NOTICE TO COURT.</h3>
      <p>(a) The entity shall file a sworn statement.</p>
    </body></html>
    """

    doc = crawler.parse_chapter_html("262.104", "Fallback", chapter_html)
    assert "TAKING POSSESSION" in doc.title
    assert "262.105" not in doc.full_text

    subsection = crawler._extract_section_block("262.104(a)", chapter_html)
    assert "without a court order" in subsection


def test_texas_offline_fallback_returns_complete_document():
    crawler = TexasLegConnector()
    with patch.object(crawler, "fetch_url", side_effect=RuntimeError("offline")):
        docs = crawler.ingest()

    assert docs
    first = docs[0]
    assert first.citation
    assert first.full_text
    assert first.jurisdiction == "US-TX"


def test_new_york_parser_handles_article_block_and_dual_source_ids():
    crawler = NewYorkLegConnector()
    fixture_html = """
    <html><body>
      <h2>ARTICLE 10 - Child Protective Proceedings</h2>
      <h3>§ 1024 Emergency removal without court order</h3>
      <p>(a) A child may be removed where life or health is in imminent danger.</p>
      <h3>§ 1027 Initial hearing</h3>
      <p>(a) The court shall hold a hearing.</p>
    </body></html>
    """

    fca_doc = crawler.parse_statute_html("NY_FCA", "1024", "Fallback", fixture_html)
    ssl_doc = crawler._build_document("NY_SSL", "384-B", "Guardianship", "Text")

    assert fca_doc.source_id == "NY_FCA"
    assert ssl_doc.source_id == "NY_SSL"
    assert fca_doc.document_id != ssl_doc.document_id
    assert "1027" not in fca_doc.full_text


def test_new_york_ssl_url_uses_article_path():
    crawler = NewYorkLegConnector()
    url = crawler._build_section_url("NY_SSL", "384-B")
    assert "/SOS/A6/384-B" in url


def test_new_york_offline_fallback_returns_complete_document():
    crawler = NewYorkLegConnector()
    with patch.object(crawler, "fetch_url", side_effect=RuntimeError("offline")):
        doc = crawler.fetch_statute("NY_FCA", "1028", "Application to return child temporarily removed")

    assert doc.citation
    assert doc.full_text
    assert doc.jurisdiction == "US-NY"


def test_florida_parser_extracts_catchline_and_decodes_entities():
    crawler = FloridaLegConnector()
    fixture_html = """
    <html><body>
      <h2>CHAPTER 39 PROCEEDINGS RELATING TO CHILDREN</h2>
      <div id="statuteText">
        <span class="Catchline">39.401 Taking a child alleged to be dependent into custody</span>
        <p>(1) If probable cause exists, a child may be taken into custody.</p>
        <p>(2) Counsel must explain rights under &sect; 39.013 and safety &amp; welfare standards.</p>
      </div>
    </body></html>
    """

    doc = crawler.parse_statute_html("39.401", "Fallback", fixture_html)
    assert "Taking a child alleged to be dependent into custody" in doc.title
    assert "§ 39.013" in doc.full_text
    assert "&" in doc.full_text
    assert "CHAPTER 39" not in doc.title


def test_florida_url_uses_online_sunshine_path_format():
    crawler = FloridaLegConnector()
    url = crawler._build_section_url("39.401")
    assert "App_mode=Display_Statute" in url
    assert "0000-0099/0039/Sections/0039.401.html" in url


def test_florida_offline_fallback_returns_complete_document():
    crawler = FloridaLegConnector()
    with patch.object(crawler, "fetch_url", side_effect=RuntimeError("offline")):
        doc = crawler.fetch_statute("39.507", "Adjudicatory hearings; orders")

    assert doc.citation
    assert doc.full_text
    assert doc.jurisdiction == "US-FL"


def test_rate_limit_delay_applies_between_fetches_for_all_live_crawlers(tmp_path):
    crawlers = [
        CaliforniaLegConnector(),
        TexasLegConnector(),
        NewYorkLegConnector(),
        FloridaLegConnector(),
    ]

    class DummyResponse:
        text = "ok"

        @staticmethod
        def raise_for_status():
            return None

    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return None

        def get(self, *args, **kwargs):
            return DummyResponse()

    for idx, crawler in enumerate(crawlers):
        crawler.cache_dir = tmp_path / f"cache_{idx}"
        crawler.cache_dir.mkdir(parents=True, exist_ok=True)
        crawler.rate_limit_delay = 1.0

        with patch("ingestion.base.httpx.Client", DummyClient), patch(
            "ingestion.base.time.time",
            side_effect=[10.0, 10.1, 10.2, 11.3],
        ), patch("ingestion.base.time.sleep") as sleep_mock:
            crawler.fetch_url(f"https://example.org/{idx}/a", use_cache=False)
            crawler.fetch_url(f"https://example.org/{idx}/b", use_cache=False)

        sleep_mock.assert_called()
        assert sleep_mock.call_args[0][0] > 0


def test_pipeline_registers_florida_crawler_and_has_no_state_import_gaps():
    pipeline = IngestionPipeline()
    assert "FL" in pipeline.state_crawlers
    expected = {"WA", "IL", "OH", "CA", "TX", "NY", "FL"}
    assert expected.issubset(set(pipeline.state_crawlers.keys()))
