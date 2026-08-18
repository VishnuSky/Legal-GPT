"""Unified loader for Legal Source Registries, 50-State Matrix, Territories, Tribal Codes, and Court Registries."""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from legal_registry.schemas.registry_entry import LegalSourceEntry
from legal_registry.schemas.cps_source_entry import CPSSourceEntry
from legal_registry.schemas.court_entry import CourtEntry

logger = logging.getLogger("legal_gpt.registry")


class RegistryLoader:
    def __init__(self, registry_dir: Optional[str] = None):
        if registry_dir:
            self.base_dir = Path(registry_dir)
        else:
            self.base_dir = Path(__file__).parent

        self.federal_sources: Dict[str, LegalSourceEntry] = {}
        self.state_matrix: Dict[str, dict] = {}
        self.state_sources: Dict[str, List[LegalSourceEntry]] = {}
        self.cps_sources: Dict[str, CPSSourceEntry] = {}
        self.territories: Dict[str, dict] = {}
        self.tribal_sources: Dict[str, LegalSourceEntry] = {}
        self.courts: Dict[str, CourtEntry] = {}
        self.load_errors: List[str] = []
        self.load_all()

    def load_all(self):
        self.load_errors.clear()
        self._load_federal()
        self._load_state_matrix()
        self._load_state_sources()
        self._load_cps_sources()
        self._load_territories()
        self._load_tribal_sources()
        self._load_courts()

    def _load_federal(self):
        fed_file = self.base_dir / "federal" / "federal_sources.yaml"
        if not fed_file.exists():
            msg = f"Warning: Federal sources file not found at {fed_file}"
            logger.warning(msg)
            self.load_errors.append(msg)
            return
        try:
            with open(fed_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                for item in data.get("sources", []):
                    entry = LegalSourceEntry(**item)
                    self.federal_sources[entry.source_id] = entry
        except Exception as e:
            msg = f"Error loading federal sources from {fed_file}: {e}"
            logger.error(msg)
            self.load_errors.append(msg)

    def _load_state_matrix(self):
        matrix_file = self.base_dir / "states" / "matrix.yaml"
        if not matrix_file.exists():
            msg = f"Warning: State matrix file not found at {matrix_file}"
            logger.warning(msg)
            self.load_errors.append(msg)
            return
        try:
            with open(matrix_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                self.state_matrix = data.get("states", {})
        except Exception as e:
            msg = f"Error loading state matrix from {matrix_file}: {e}"
            logger.error(msg)
            self.load_errors.append(msg)

    def _load_state_sources(self):
        states_dir = self.base_dir / "states"
        if not states_dir.exists():
            msg = f"Warning: States directory not found at {states_dir}"
            logger.warning(msg)
            self.load_errors.append(msg)
            return
        for fpath in states_dir.glob("*.yaml"):
            if fpath.name == "matrix.yaml":
                continue
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    state_id = data.get("state_id")
                    entries = []
                    for item in data.get("sources", []):
                        entry = LegalSourceEntry(**item)
                        entries.append(entry)
                    if state_id:
                        self.state_sources[state_id] = entries
            except Exception as e:
                msg = f"Error loading state source {fpath}: {e}"
                logger.error(msg)
                self.load_errors.append(msg)

    def _load_cps_sources(self):
        cps_dir = self.base_dir / "cps"
        if not cps_dir.exists():
            msg = f"Warning: CPS directory not found at {cps_dir}"
            logger.warning(msg)
            self.load_errors.append(msg)
            return
        for fpath in cps_dir.glob("*.yaml"):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    for item in data.get("sources", []):
                        entry = CPSSourceEntry(**item)
                        self.cps_sources[entry.source_id] = entry
            except Exception as e:
                msg = f"Error loading CPS source {fpath}: {e}"
                logger.error(msg)
                self.load_errors.append(msg)

    def _load_territories(self):
        terr_file = self.base_dir / "territories" / "territories.yaml"
        if terr_file.exists():
            try:
                with open(terr_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    self.territories = data.get("territories", {})
            except Exception as e:
                msg = f"Error loading territories from {terr_file}: {e}"
                logger.error(msg)
                self.load_errors.append(msg)

    def _load_tribal_sources(self):
        tribal_file = self.base_dir / "tribal" / "tribal_sources.yaml"
        if tribal_file.exists():
            try:
                with open(tribal_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    for item in data.get("tribal_sources", []):
                        entry = LegalSourceEntry(**item)
                        self.tribal_sources[entry.source_id] = entry
            except Exception as e:
                msg = f"Error loading tribal sources from {tribal_file}: {e}"
                logger.error(msg)
                self.load_errors.append(msg)

    def _load_courts(self):
        court_file = self.base_dir / "courts" / "court_registry.yaml"
        if not court_file.exists():
            msg = f"Warning: Court registry file not found at {court_file}"
            logger.warning(msg)
            self.load_errors.append(msg)
            return
        try:
            with open(court_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                for item in data.get("courts", []):
                    entry = CourtEntry(**item)
                    self.courts[entry.court_id] = entry
        except Exception as e:
            msg = f"Error loading courts from {court_file}: {e}"
            logger.error(msg)
            self.load_errors.append(msg)

    def get_source(self, source_id: str) -> Optional[LegalSourceEntry]:
        if source_id in self.federal_sources:
            return self.federal_sources[source_id]
        if source_id in self.cps_sources:
            return self.cps_sources[source_id]
        if source_id in self.tribal_sources:
            return self.tribal_sources[source_id]
        for entries in self.state_sources.values():
            for entry in entries:
                if entry.source_id == source_id:
                    return entry
        return None

    def get_cps_sources_for_jurisdiction(self, jurisdiction: str) -> List[CPSSourceEntry]:
        """Returns all CPS sources relevant for a given jurisdiction e.g. US, US-WA, US-IL, US-OH, US-CA, US-TX, US-NY."""
        results = []
        for entry in self.cps_sources.values():
            if entry.jurisdiction in (jurisdiction, "US", "TRIBAL"):
                results.append(entry)
        return results

    def get_courts_for_jurisdiction(self, state: str, county: Optional[str] = None) -> List[CourtEntry]:
        """Returns relevant courts for a given state and optional county."""
        results = []
        for court in self.courts.values():
            if court.state == state:
                if county is None or court.county is None or court.county.lower() == county.lower():
                    results.append(court)
            elif court.jurisdiction == "US":  # Federal
                results.append(court)
        return results


# Global singleton instance
default_registry = RegistryLoader()
