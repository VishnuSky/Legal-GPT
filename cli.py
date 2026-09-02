"""Command Line Interface for Legal-GPT."""

import os
import sys
import json
from datetime import date
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table

# Reconfigure console output on Windows to support UTF-8 formatting
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from agents.legal_orchestrator import LegalGPTOrchestrator
from legal_registry.loader import default_registry
from storage.vector_store import SimpleHybridStore
from ingestion.pipeline import IngestionPipeline
from knowledge_graph.relational_graph import citator_graph, CitatorSignal
from knowledge_graph.point_in_time_diff import PointInTimeDiffEngine
from core.temporal_graph import temporal_graph
from cps.evidence_matrix import EvidenceMatrixEngine, CaseEvidenceItem, EvidenceType
from cps.evidence_bridge import ExternalEvidenceContract, EvidenceBridgeEngine
from cps.pleading_generator import PleadingGenerator, PleadingDraftRequest
from cps.due_process_audit import DueProcessAuditor

app = typer.Typer(help="Legal-GPT: Jurisdiction-Aware, Temporal, Citation-Verified Legal Intelligence Platform")
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
def generate_motion(
    state: str = typer.Option("WA", "--state", "-s", help="State code: WA, IL, OH, CA, TX, NY, ICWA"),
    motion: str = typer.Option("shelter_rehearing", "--motion", "-m", help="Motion type: shelter_rehearing, return_child, section_1028, icwa_intervention, section_388"),
    county: str = typer.Option("District 1", "--county", "-c", help="County or Judicial District"),
    facts: str = typer.Option("Lack of timely statutory notice and availability of verified relative placement.", "--facts", "-f", help="Summary factual basis")
):
    """Generate a formal court motion and pleading template customized to state court rules."""
    req = PleadingDraftRequest(
        state=state,
        motion_type=motion,
        county=county,
        factual_basis=facts
    )
    draft = PleadingGenerator.generate_pleading(req)

    console.print(f"\n[bold green]=== GENERATED COURT PLEADING: {draft.title} ===[/bold green]")
    console.print(f"[bold cyan]Governing Authority:[/bold cyan] {draft.governing_rule_and_statute}")
    console.print(f"[bold yellow]Jurisdiction:[/bold yellow] {draft.jurisdiction}\n")
    console.print(f"```\n{draft.caption}\n```\n")
    console.print(draft.body_markdown)
    console.print(f"\n[dim]{draft.certificate_of_service}[/dim]\n")


@app.command()
def due_process_audit(
    state: str = typer.Option("WA", "--state", "-s", help="State code: WA, IL, OH, CA, TX, NY"),
    stage: str = typer.Option("EMERGENCY_REMOVAL", "--stage", help="CPS stage: EMERGENCY_REMOVAL, SHELTER_CARE, ADJUDICATION"),
    notice: bool = typer.Option(True, "--notice/--no-notice", help="Whether formal personal service was provided"),
    counsel: bool = typer.Option(True, "--counsel/--no-counsel", help="Whether parent had appointed counsel present"),
    services: bool = typer.Option(True, "--services/--no-services", help="Whether active/reasonable services were offered"),
    visitation: bool = typer.Option(True, "--visitation/--no-visitation", help="Whether parent-child visitation was ordered"),
    icwa: bool = typer.Option(False, "--icwa/--no-icwa", help="Whether child is ICWA eligible"),
    tribal_notice: bool = typer.Option(True, "--tribal-notice/--no-tribal-notice", help="Whether registered mail tribal notice was sent")
):
    """Perform a comprehensive multi-pillar due process audit for child welfare proceedings."""
    report = DueProcessAuditor.audit_case(
        state=state,
        stage=stage,
        notice_served_personally=notice,
        counsel_appointed=counsel,
        counsel_present_at_hearing=counsel,
        services_tailored_and_offered=services,
        family_visitation_ordered=visitation,
        is_icwa_eligible=icwa,
        tribal_notice_registered_mail=tribal_notice
    )

    console.print(f"\n[bold cyan]=== DUE PROCESS HEALTH AUDIT REPORT ===[/bold cyan]")
    console.print(f"[bold]Summary:[/bold] {report.summary_narrative}\n")

    table = Table(title=f"Due Process Compliance Matrix ({state} - {stage})")
    table.add_column("Due Process Pillar", style="cyan", width=30)
    table.add_column("Status", style="yellow", width=20)
    table.add_column("Authority & Recommended Remedy", style="white")

    for chk in report.checks:
        status_style = "green" if chk.status == "COMPLIANT" else "bold red"
        table.add_row(
            chk.right_name,
            f"[{status_style}]{chk.status}[/{status_style}]",
            f"{chk.guaranteeing_authority}\n[dim]Remedy: {chk.recommended_remedy}[/dim]"
        )

    console.print(table)


@app.command()
def evaluate_evidence(
    jurisdiction: str = typer.Option("US-WA", "--jurisdiction", "-j", help="Jurisdiction code e.g. US-WA"),
    stage: str = typer.Option("EMERGENCY_REMOVAL", "--stage", help="CPS lifecycle stage")
):
    """Analyze a synthetic evidentiary matrix to separate unverified allegations from documented exhibits."""
    sample_contract = ExternalEvidenceContract(
        external_case_id="SYNTHETIC-CASE-001",
        jurisdiction=jurisdiction,
        cps_stage=stage,
        items=[
            {
                "id": "EV-001",
                "description": "Anonymous referral alleging untidy home and potential substance use.",
                "type": "UNVERIFIED_ALLEGATION",
                "statutory_element": "Imminent Physical Harm",
                "source": "Caseworker Intake Report"
            },
            {
                "id": "EV-002",
                "description": "Verified negative 10-panel urinalysis toxicology laboratory report.",
                "type": "DOCUMENTED_EXHIBIT",
                "statutory_element": "Substance Impairment",
                "source": "Certified Lab Exhibit A"
            },
            {
                "id": "EV-003",
                "description": "Maternal Grandparent approved relative home assessment.",
                "type": "DOCUMENTED_EXHIBIT",
                "statutory_element": "Kinship Placement Viability",
                "source": "Relative Home Study Exhibit B"
            }
        ]
    )

    evaluation = EvidenceBridgeEngine.ingest_and_evaluate_contract(sample_contract)

    console.print(f"\n[bold cyan]=== EVIDENTIARY MATRIX SUFFICIENCY EVALUATION ===[/bold cyan]")
    console.print(f"[bold]Summary:[/bold] {evaluation.case_summary}\n")

    table = Table(title=f"Evidentiary Balance ({evaluation.jurisdiction})")
    table.add_column("Category", style="cyan")
    table.add_column("Count", style="green")

    table.add_row("Total Items Analyzed", str(evaluation.total_items_analyzed))
    table.add_row("Documented Exhibits", str(evaluation.documented_exhibits_count))
    table.add_row("Disputed Facts", str(evaluation.disputed_facts_count))
    table.add_row("Unverified Allegations", str(evaluation.unverified_allegations_count), style="red" if evaluation.unverified_allegations_count > 0 else "green")
    table.add_row("Sufficiency Rating", evaluation.sufficiency_rating.value, style="bold magenta")

    console.print(table)

    if evaluation.evidentiary_gaps:
        console.print("\n[bold yellow]Evidentiary Proof Gaps Identified:[/bold yellow]")
        for gap in evaluation.evidentiary_gaps:
            console.print(f"- [bold red]{gap.statutory_element}[/bold red]: {gap.missing_evidence_description}")
            console.print(f"  [dim]Rebuttal: {gap.rebuttal_strategy}[/dim]")


@app.command()
def ingest(
    category: str = typer.Option("all", "--category", "-c", help="Category to ingest: all, federal, caselaw, states, policies")
):
    """Run data ingestion across Federal statutory, landmark appellate caselaw, state codes, and CPS policies."""
    console.print(f"[bold cyan]Running Legal-GPT Ingestion Pipeline (Category: {category})...[/bold cyan]")
    pipeline = IngestionPipeline()
    manifest = pipeline.run_sync(categories=[category])

    table = Table(title="Ingestion Pipeline Manifest")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Status", manifest.status)
    table.add_row("Duration", f"{manifest.duration_seconds:.2f} seconds")
    table.add_row("Total Ingested Documents", str(manifest.total_documents))
    table.add_row("Total Chunked Units", str(manifest.total_chunks))

    for cat_name, cnt in manifest.by_category.items():
        table.add_row(f"Category: {cat_name.capitalize()}", str(cnt))

    console.print(table)


@app.command()
def search(
    query_text: str = typer.Argument(..., help="Search query or keywords"),
    jurisdiction: Optional[str] = typer.Option(None, "--jurisdiction", "-j", help="e.g. US, US-WA, US-IL, US-OH, US-CA, US-TX, US-NY"),
    top_k: int = typer.Option(5, "--top-k", "-k", help="Number of results to retrieve")
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
def citator(
    citation: str = typer.Argument(..., help="Citation or case name to analyze in Citator (e.g. 'Haaland v. Brackeen' or 'RCW 13.34.065')")
):
    """Inspect subsequent treatment, citing references, and Shepard's/KeyCite-style signals for a legal authority."""
    report = citator_graph.evaluate_citator_status(citation)

    color = "green" if report.overall_signal == CitatorSignal.GOOD_LAW else ("yellow" if report.overall_signal == CitatorSignal.CAUTION else "red")
    console.print(f"\n[bold {color}]Citator Treatment Status:[/bold {color}] [{report.overall_signal.value}] {citation}")
    console.print(f"[bold]Summary:[/bold] {report.treatment_summary}\n")

    if report.citing_references:
        table = Table(title=f"Citing Authorities & Historical Graph ({len(report.citing_references)} References)")
        table.add_column("Citing Authority", style="cyan")
        table.add_column("Relation", style="yellow")
        table.add_column("Signal", style="magenta")
        table.add_column("Context Snippet", style="white")

        for ref in report.citing_references:
            table.add_row(
                ref.get("source_citation", "Unknown"),
                ref.get("relation_type", "CITES"),
                ref.get("treatment_signal", "NEUTRAL"),
                ref.get("context_snippet", "")[:120]
            )
        console.print(table)


@app.command()
def law_at_date(
    citation: str = typer.Argument(..., help="Statute citation e.g. 'RCW 13.34.065'"),
    target_date: str = typer.Option(..., "--date", "-d", help="Calendar date to evaluate (YYYY-MM-DD)"),
    diff_with: Optional[str] = typer.Option(None, "--diff-with", help="Secondary date (YYYY-MM-DD) to compare text diff")
):
    """Resolve point-in-time statutory text on a specific date, or compute a line-by-line diff between two dates."""
    parsed_date = date.fromisoformat(target_date)
    eval_res = temporal_graph.evaluate_law_at_date(citation, "US-WA", parsed_date)

    console.print(f"\n[bold cyan]Point-in-Time Resolution for {citation} on {parsed_date.isoformat()}:[/bold cyan]")
    console.print(f"- **Valid on Date**: {'[green]YES[/green]' if eval_res.valid_on_date else '[red]NO[/red]'}")
    console.print(f"- **Superseded**: {'[yellow]YES[/yellow]' if eval_res.superseded else '[green]NO[/green]'}")
    console.print(f"- **Operative Version**: {eval_res.active_version.version_id if eval_res.active_version else 'None'}")
    console.print(f"- **Analysis**: {eval_res.analysis}\n")

    if eval_res.active_version:
        console.print(f"[dim]Operative Statutory Text:[/dim]\n> \"{eval_res.active_version.text}\"\n")

    if diff_with:
        diff_date = date.fromisoformat(diff_with)
        diff_res = PointInTimeDiffEngine.diff_statute_at_dates(citation, parsed_date, diff_date)
        console.print(f"[bold yellow]Statutory Text Diff ({parsed_date.isoformat()} -> {diff_date.isoformat()}):[/bold yellow]")
        console.print(diff_res.diff_unified_text)


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


@app.command()
def mcp():
    """Start the Model Context Protocol (MCP) JSON-RPC 2.0 stdio server for LM Studio & OpenWebUI."""
    from api.mcp_server import run_stdio_server
    run_stdio_server()


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host IP to bind"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind")
):
    """Start the FastAPI local REST server."""
    import uvicorn
    console.print(f"[bold green]Starting Legal-GPT REST Server on http://{host}:{port}...[/bold green]")
    uvicorn.run("api.server:app", host=host, port=port, reload=False)


@app.command()
def benchmark(
    category: str = typer.Option("all", "--category", "-c", help="Category: all, cps_emergency, icwa, uccjea, parent_rights, temporal, procedural, due_process")
):
    """Run the comprehensive 50-scenario multi-jurisdiction benchmark suite."""
    from benchmarks.scenarios import BenchmarkEvaluator
    console.print(f"[bold cyan]Running Comprehensive 50-Scenario Benchmark Suite (Category: {category.upper()})...[/bold cyan]\n")
    report = BenchmarkEvaluator.run_benchmark(category=category)

    table = Table(title=f"Benchmark Evaluation Results ({report.accuracy_rate * 100:.1f}% Pass Rate)")
    table.add_column("Category", style="cyan")
    table.add_column("Passed / Total", style="green")
    table.add_column("Accuracy Rate", style="yellow")

    for cat_name, stats in report.category_breakdown.items():
        rate = (stats["passed"] / max(1, stats["total"])) * 100
        table.add_row(cat_name, f"{stats['passed']}/{stats['total']}", f"{rate:.1f}%")

    table.add_row("OVERALL TOTAL", f"{report.scenarios_passed}/{report.total_scenarios}", f"{report.accuracy_rate * 100:.1f}%", style="bold magenta")
    console.print(table)

    if report.failed_scenario_details:
        console.print("\n[bold red]Failed Scenarios Details:[/bold red]")
        for f in report.failed_scenario_details:
            console.print(f"- [{f['scenario_id']}] {f['title']}: {f['reason']}")
    else:
        console.print("\n[bold green]✅ All benchmark scenarios passed with 100% precision & jurisdiction integrity![/bold green]\n")


if __name__ == "__main__":
    app()
