import sys
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Optional
from agents.legal_orchestrator import LegalGPTOrchestrator
from legal_registry.loader import default_registry

# Reconfigure stdout for utf-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

app = typer.Typer(help="Legal-GPT: Jurisdiction-Aware Legal Intelligence CLI")
console = Console(highlight=False)
orchestrator = LegalGPTOrchestrator()


@app.command()
def query(
    prompt: str = typer.Argument(..., help="Legal question or case fact pattern"),
    state: Optional[str] = typer.Option(None, "--state", "-s", help="Jurisdiction state code e.g. WA, IL, OH"),
    county: Optional[str] = typer.Option(None, "--county", "-c", help="County e.g. Skagit, Cook, Cuyahoga"),
):
    """Analyze a legal question or case situation with jurisdiction locking and citation verification."""
    console.print(f"[bold cyan]Analyzing query:[/bold cyan] {prompt}")
    if state:
        console.print(f"[bold yellow]Jurisdiction Locked to:[/bold yellow] {state}" + (f" ({county})" if county else ""))

    resp = orchestrator.process_query(prompt, override_state=state, override_county=county)
    console.print("\n" + resp.render_markdown() + "\n")


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

    console.print(table)


@app.command()
def verify_citation(citation: str = typer.Argument(..., help="Legal citation to verify e.g. 'RCW 13.34.050'")):
    """Verify whether a legal citation resolves to an official authority."""
    from core.citation_verifier import CitationVerifier
    res = CitationVerifier.verify_citation(citation)
    if res.verified:
        console.print(f"[bold green][VERIFIED][/bold green] {res.normalized_citation} -> Tier: {res.authority_tier} ({res.publisher_name})")
    else:
        console.print(f"[bold red][FAILED][/bold red] {res.raw_citation} -> Reason: {res.rejection_reason}")


if __name__ == "__main__":
    app()
