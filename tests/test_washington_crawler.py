"""Unit tests for Washington State Legislature Crawler and Regulation Chunking."""

from datetime import date
from normalization.chunkers import RegulationChunker
from ingestion.state_crawlers.washington import (
    WashingtonLegConnector,
    WA_RCW_TARGET_SECTIONS,
    WA_WAC_TARGET_SECTIONS,
)


def test_regulation_chunker_basic():
    rule_text = (
        "General rule requirements.\n"
        "(1) First subsection regarding licensing criteria.\n"
        "(2) Second subsection regarding background investigations."
    )
    chunks = RegulationChunker.chunk_regulation(
        document_id="WA-WAC-110_30_0010",
        title="WAC 110-30-0010: DCYF Authority",
        full_text=rule_text,
    )
    assert len(chunks) == 3
    assert chunks[0].chunk_type == "regulation_rule"
    assert "Overview" in chunks[0].hierarchy_path
    assert chunks[1].chunk_type == "regulation_subsection"
    assert "(1)" in chunks[1].heading
    assert chunks[2].chunk_type == "regulation_subsection"
    assert "(2)" in chunks[2].heading


def test_regulation_chunker_single_chunk():
    rule_text = "Brief administrative requirement without subsections."
    chunks = RegulationChunker.chunk_regulation(
        document_id="WA-WAC-110_300_0010",
        title="WAC 110-300-0010",
        full_text=rule_text,
    )
    assert len(chunks) == 1
    assert chunks[0].chunk_type == "regulation_rule"
    assert chunks[0].text == rule_text


def test_washington_rcw_html_parsing():
    connector = WashingtonLegConnector()
    html_sample = """
    <html>
      <head>
        <script>var x = 123;</script>
        <style>.hide { display:none; }</style>
      </head>
      <body>
        <span id="ContentPlaceHolder1_lblTitle">13.34.050 - Court order to take child into custody</span>
        <div id="ContentPlaceHolder1_divContent">
          <p>(1) The court may enter an order directing a law enforcement officer to take a child into custody.</p>
          <p>(2) The petition must contain a statement of facts.</p>
          [ 2021 c 211 &sect; 9; ]
        </div>
        <div id="ContentPlaceHolder1_divBottomContent">Footer</div>
      </body>
    </html>
    """
    doc = connector.parse_rcw_html("13.34.050", "Court order to take child into custody", html_sample)
    assert doc.document_id == "WA-RCW-13_34_050"
    assert doc.citation == "RCW 13.34.050"
    assert doc.jurisdiction == "US-WA"
    assert doc.authority.tier == "TIER_0"
    assert doc.authority.official_source is True
    assert doc.temporal.effective_date is None
    assert len(doc.chunks) >= 2
    assert "var x = 123" not in doc.full_text


def test_washington_rcw_short_html_fixture_fallback():
    connector = WashingtonLegConnector()
    short_html = "<html><body><div>Empty or short error page</div></body></html>"
    doc = connector.parse_rcw_html("13.34.050", "Court order to take child into custody", short_html)
    assert doc.citation == "RCW 13.34.050"
    # Should fall back to synthetic fixture text instead of empty/short title
    assert len(doc.full_text) > 100
    assert "(1) The court may enter an order" in doc.full_text


def test_washington_wac_html_parsing():
    connector = WashingtonLegConnector()
    html_sample = """
    <html>
      <body>
        <span id="ContentPlaceHolder1_lblTitle">110-30-0010 - DCYF Authority and Purpose</span>
        <div id="ContentPlaceHolder1_divContent">
          (1) The department was established under Title 43 RCW.
          <br />
          (2) These administrative rules govern juvenile justice operations.
        </div>
      </body>
    </html>
    """
    doc = connector.parse_wac_html("110-30-0010", "DCYF Authority", html_sample)
    assert doc.document_id == "WA-WAC-110_30_0010"
    assert doc.citation == "WAC 110-30-0010"
    assert doc.document_type == "regulation"
    assert len(doc.chunks) >= 2
    assert doc.chunks[1].chunk_type == "regulation_subsection"


def test_washington_canonical_statutes_offline():
    connector = WashingtonLegConnector()
    docs = connector.get_canonical_statutes()
    assert len(docs) == len(WA_RCW_TARGET_SECTIONS)
    for doc in docs:
        assert doc.citation.startswith("RCW ")
        assert doc.jurisdiction == "US-WA"
        assert len(doc.full_text) > 50
        assert doc.content_hash != ""
        assert len(doc.chunks) >= 1
