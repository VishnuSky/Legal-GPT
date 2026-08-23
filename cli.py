"""Interactive Command Line Interface for Legal-GPT."""

import sys
from datetime import date
from typing import Optional, List
import typer
from rich.console import Console
from rich.table import Table
from agents.legal_orchestrator import LegalGPTOrchestrator
from legal_registry.loader import default_registry
from storage.vector_store import SimpleHybridStore
from ingestion.pipeline import IngestionPipeline

# Reconfigure stdout for utf-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

app = typer.Typer(
    name="legal-gpt",
    help="Legal-GPT: Jurisdiction-Aware, Temporal, Citation-Verified Legal Intelligence CLI"
)
console = Console(highlight=False)
orchestrator = LegalGPTOrchestrator()


@app.command()
def query(
    prompt: str = typer.Argument(..., help="Legal question or case fact pattern"),
    state: Optional[str] = typer.Option(None, "--state", "-s", help="Jurisdiction state code e.g. WA, IL, OH, CA, TX, NY"),
    county: Optional[str] = typer.Option(None, "--county", "-c", help="County e.g. Skagit, Cook, Cuyahoga"),
    event_date: Optional[str] = typer.Option(None, "--event-date", "-d", help="Date event occurred (YYYY-MM-DD) for temporal validity"),
    mode: str = typer.Option("standard", "--mode", "-m", help="Persona mode: standard, self_represented, investigator, attorney, court"),
):
    """Analyze a legal question or case situation with jurisdiction locking, temporal checks, and citation verification."""
    if not prompt.strip():
        console.print("[bold red]Error:[/bold red] Prompt cannot be empty.")
        raise typer.Exit(code=1)

    parsed_date = None
    if event_date:
        try:
            parsed_date = date.fromisoformat(event_date)
        except ValueError:
            console.print(f"[bold red]Error:[/bold red] Invalid date format '{event_date}'. Use YYYY-MM-DD.")
            raise typer.Exit(code=1)

    console.print(f"[bold cyan]Analyzing query:[/bold cyan] {prompt}")
    if state:
        console.print(f"[bold yellow]Jurisdiction Locked to:[/bold yellow] {state}" + (f" ({county})" if county else ""))
    if parsed_date:
        console.print(f"[bold magenta]Temporal Evaluation Date:[/bold magenta] {parsed_date.isoformat()}")
    if mode != "standard":
        console.print(f"[bold green]Persona Review Mode:[/bold green] {mode}")

    try:
        resp = orchestrator.process_query(
            query=prompt,
            override_state=state,
            override_county=county,
            event_date=parsed_date,
            persona_mode=mode # type: ignore
        )
        console.print("\n" + resp.render_markdown() + "\n")
    except Exception as e:
        console.print(f"[bold red]Execution Error:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def ingest(
    category: str = typer.Option("all", "--category", "-c", help="Category to ingest: all, federal, caselaw, states, policies"),
):
    """Run data ingestion pipeline across authoritative statutes, precedents, and agency policy manuals."""
    console.print(f"[bold cyan]Running Legal-GPT Ingestion Pipeline (Category: {category})...[/bold cyan]")
    pipeline = IngestionPipeline()
    categories = [category] if category != "all" else ["federal", "caselaw", "states", "policies"]
    manifest = pipeline.run_sync(categories=categories)

    table = Table(title="Ingestion Pipeline Manifest")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Status", manifest.status)
    table.add_row("Duration", f"{manifest.duration_seconds:.2f} seconds")
    table.add_row("Total Ingested Documents", str(manifest.total_documents))
    table.add_row("Total Chunked Units", str(manifest.total_chunks))
    for cat, count in manifest.by_category.items():
        table.add_row(f"Category: {cat.capitalize()}", str(count))
    console.print(table)


@app.command()
def search(
    query_text: str = typer.Argument(..., help="Search query or keyword terms"),
    jurisdiction: Optional[str] = typer.Option(None, "--jurisdiction", "-j", help="Jurisdiction filter e.g. US, US-WA, US-IL, US-OH, US-CA, US-TX, US-NY"),
    top_k: int = typer.Option(5, "--top-k", "-k", help="Number of results to return"),
):
    """Search authoritative statutes, precedent cases, and policy chunks using hybrid BM25 search."""
    store = SimpleHybridStore()
    store.load_from_database("legal_gpt.db")
    results = store.search(query=query_text, jurisdiction=jurisdiction, top_k=top_k)

    if not results:
        console.print(f"[yellow]No matching authorities found for:[/yellow] '{query_text}'")
        return

    table = Table(title=f"Search Results for '{query_text}' (Jurisdiction: {jurisdiction or 'All'})")
    table.add_column("Citation / Heading", style="cyan", width=30)
    table.add_column("Jurisdiction", style="yellow", width=12)
    table.add_column("Score", style="green", width=8)
    table.add_column("Text Excerpt", style="white")

    for res in results:
        table.add_row(
            res.heading or res.citation or "Authority",
            res.jurisdiction or "Federal/General",
            f"{res.score:.2f}",
            res.text[:140] + ("..." if len(res.text) > 140 else "")
        )
    console.print(table)


@app.command()
def registry_summary():
    """Display a summary of the machine-readable legal source registry."""
    table = Table(title="Legal Source Registry Summary")
    table.add_column("Category", style="cyan")
    table.add_column("Count / Details", style="green")

    table.add_row("Federal Primary Sources", str(len(default_registry.federal_sources)))
    table.add_row("States & Territories in Matrix", str(len(default_registry.state_matrix)))
    table.add_row("CPS Specialized Sources", str(len(default_registry.cps_sources)))
    table.add_row("Registered Courts", str(len(default_registry.courts)))

    if default_registry.load_errors:
        table.add_row("Load Warnings/Errors", str(len(default_registry.load_errors)), style="red")

    console.print(table)


@app.command()
def verify_citation(citation: str = typer.Argument(..., help="Legal citation to verify e.g. 'RCW 13.34.050'")):
    """Verify whether a legal citation resolves to an official authority."""
    from core.citation_verifier import CitationVerifier
    if not citation.strip():
        console.print("[bold red]Error:[/bold red] Citation cannot be empty.")
        raise typer.Exit(code=1)

    res = CitationVerifier.verify_citation(citation)
    if res.verified:
        console.print(f"[bold green][VERIFIED][/bold green] {res.normalized_citation} -> Tier: {res.authority_tier} ({res.publisher_name})")
    else:
        console.print(f"[bold red][FAILED][/bold red] {res.raw_citation} -> Reason: {res.rejection_reason}")


if __name__ == "__main__":
    app()
