#!/usr/bin/env python3
"""Build Offline Data Package for Legal-GPT (Mission 2).

Generates:
- offline_packages/legal_gpt_offline_{date}.json (Full package)
- offline_packages/states/{STATE}_offline.json (Per-state packages)
"""

import os
import json
import yaml
import hashlib
from datetime import datetime, timezone, date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REGISTRY_DIR = BASE_DIR / "legal_registry"
STATES_DIR = REGISTRY_DIR / "states"
CONCEPTS_DIR = REGISTRY_DIR / "literacy" / "concepts"
OFFLINE_DIR = BASE_DIR / "offline_packages"
OFFLINE_STATES_DIR = OFFLINE_DIR / "states"

CRISIS_CHECKLIST = {
    "cps_removal": [
        "Write down exact removal date/time and worker name",
        "Ask for copies of all removal paperwork",
        "Request appointed counsel immediately",
        "Name relatives for placement in writing",
        "Note hearing date/time from notice"
    ]
}

DEFAULT_LEGAL_AID = {
    "WA": {
        "CLEAR": "1-888-201-1014",
        "OPD_parents": "https://opd.wa.gov/parents",
        "LawHelp": "https://www.washingtonlawhelp.org"
    },
    "CA": {
        "LawHelpCA": "https://www.lawhelpca.org",
        "JudicialBranchSelfHelp": "https://selfhelp.courts.ca.gov"
    },
    "TX": {
        "TexasLawHelp": "https://texaslawhelp.org",
        "LegalAidNW": "1-888-529-5277"
    },
    "NY": {
        "LawHelpNY": "https://www.lawhelpny.org",
        "LegalAidSociety": "212-577-3300"
    },
    "IL": {
        "IllinoisLegalAid": "https://www.illinoislegalaid.org",
        "CARPLS": "312-738-9200"
    },
    "OH": {
        "OhioLegalHelp": "https://www.ohiolegalhelp.org",
        "OhioLegalAid": "1-866-529-6446"
    },
    "FL": {
        "FloridaLegalAid": "https://www.floridalawhelp.org",
        "FloridaBarFoundation": "1-800-282-9781"
    },
    "AZ": {
        "AZLawHelp": "https://www.azlawhelp.org",
        "CommunityLegalServices": "1-800-852-9075"
    },
    "CO": {
        "ColoradoLegalServices": "https://www.coloradolegalservices.org",
        "DenverBarHelp": "303-837-1313"
    },
    "WI": {
        "WisconsinJudicare": "https://www.judicare.org",
        "LegalActionWisconsin": "1-855-947-2529"
    },
    "MN": {
        "LawHelpMN": "https://www.lawhelpmn.org",
        "MidMinnesotaLegalAid": "612-334-5970"
    },
    "MO": {
        "LegalServicesMissouri": "https://www.lsmo.org",
        "LegalAidWesternMissouri": "816-474-6750"
    },
    "IN": {
        "IndianaLegalHelp": "https://indianalegalhelp.org",
        "IndianaLegalServices": "1-844-243-8570"
    },
    "TN": {
        "HELP4TN": "https://www.help4tn.org",
        "LegalAidSocietyMiddleTN": "1-800-238-1443"
    },
    "MD": {
        "MarylandLegalAid": "https://www.mdlab.org",
        "MarylandCourtHelp": "https://mdcourts.gov/courthelp"
    },
    "OR": {
        "OregonLawHelp": "https://oregonlawhelp.org",
        "LegalAidServicesOregon": "503-224-4086"
    },
    "NM": {
        "NewMexicoLegalAid": "https://newmexicolegalaid.org",
        "LawHelpNM": "1-833-545-4357"
    },
    "WA_TRIBAL": {
        "NorthwestJusticeProjectTribal": "https://nwjustice.org/native-american-unit",
        "NationalIndianChildWelfareAssociation": "https://www.nicwa.org"
    }
}


def load_concepts():
    """Load all concepts from legal_registry/literacy/concepts/ into standard offline dict."""
    concepts_dict = {}
    if not CONCEPTS_DIR.exists():
        return concepts_dict

    for yfile in sorted(CONCEPTS_DIR.glob("*.yaml")):
        with open(yfile, "r", encoding="utf-8") as f:
            cdata = yaml.safe_load(f) or {}

        cid = cdata.get("id", yfile.stem)
        auths = []
        for a in cdata.get("level_4_primary_authority", []):
            auths.append({
                "citation": a.get("citation", ""),
                "jurisdiction": a.get("jurisdiction", "US"),
                "official_url": a.get("official_portal_url", ""),
                "key_text": a.get("key_holding_or_text", ""),
                "verification_status": a.get("verification_status", "VERIFIED")
            })

        drill_downs = {}
        for action, ddata in cdata.get("drill_downs", {}).items():
            if isinstance(ddata, dict):
                drill_downs[action] = {
                    "title": ddata.get("title", ""),
                    "content": ddata.get("content", ""),
                    "citations": ddata.get("citations", []),
                    "official_sources": ddata.get("official_sources", [])
                }
            else:
                drill_downs[action] = ddata

        concepts_dict[cid] = {
            "name": cdata.get("canonical_name", cid),
            "level_1": cdata.get("level_1_plain_english", ""),
            "level_2": cdata.get("level_2_practical", ""),
            "level_3": cdata.get("level_3_terminology", ""),
            "level_4_citations": auths,
            "level_5": cdata.get("level_5_advanced_analysis", ""),
            "drill_downs": drill_downs,
            "related_concepts": cdata.get("related_concepts", [])
        }

    return concepts_dict


def load_states():
    """Load states from legal_registry/states/."""
    states_dict = {}
    if not STATES_DIR.exists():
        return states_dict

    for yfile in sorted(STATES_DIR.glob("*.yaml")):
        if yfile.name == "matrix.yaml":
            continue
        with open(yfile, "r", encoding="utf-8") as f:
            sdata = yaml.safe_load(f) or {}

        scode = sdata.get("state_code") or sdata.get("state_id") or yfile.stem

        sh_hours = sdata.get("shelter_hearing_hours", 72)
        rem_hours = 72
        if isinstance(sh_hours, int):
            rem_hours = sh_hours

        states_dict[scode] = {
            "state_name": sdata.get("state_name", scode),
            "emergency_removal_hours": rem_hours,
            "shelter_hearing_hours": sh_hours,
            "shelter_hearing_citation": sdata.get("shelter_hearing_citation", "UNVERIFIED"),
            "counsel_citation": sdata.get("counsel_citation", "UNVERIFIED"),
            "tpr_citation": sdata.get("tpr_citation", "UNVERIFIED"),
            "icwa_inquiry": sdata.get("icwa_inquiry", "not_specified"),
            "official_portal": sdata.get("statutes_url") or sdata.get("legislature_url") or "",
            "legislature_url": sdata.get("legislature_url", ""),
            "verification_status": sdata.get("verification_status", "PARTIAL")
        }

    return states_dict


def build_offline_package():
    """Builds and writes full package and state packages."""
    OFFLINE_STATES_DIR.mkdir(parents=True, exist_ok=True)

    today_str = date.today().isoformat()
    now_iso = datetime.now(timezone.utc).isoformat()

    concepts = load_concepts()
    states = load_states()

    full_package = {
        "package_version": "0.3.2",
        "generated_at": now_iso,
        "jurisdiction_count": len(states),
        "concept_count": len(concepts),
        "concepts": concepts,
        "states": states,
        "crisis_checklist": CRISIS_CHECKLIST,
        "legal_aid": DEFAULT_LEGAL_AID,
        "disclaimer": "Legal information only. Not legal advice. Not a lawyer. Verify with qualified counsel.",
        "staleness_warning_days": 90,
        "abstention_note": "Where verification_status is PARTIAL or UNVERIFIED, consult the official_url for current law."
    }

    full_filename = f"legal_gpt_offline_{today_str}.json"
    full_path = OFFLINE_DIR / full_filename
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(full_package, f, indent=2)

    # Also maintain a symlink / pointer or copy as latest
    latest_path = OFFLINE_DIR / "legal_gpt_offline_latest.json"
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(full_package, f, indent=2)

    full_size_kb = round(full_path.stat().st_size / 1024, 2)
    print(f"Generated full package: {full_path.name} ({full_size_kb} KB)")

    # Per-state packages
    wa_size_kb = 0.0
    for scode, sinfo in states.items():
        state_aid = DEFAULT_LEGAL_AID.get(scode, {
            "statewide_legal_aid": sinfo.get("official_portal", "")
        })

        state_pkg = {
            "package_version": "0.3.2",
            "generated_at": now_iso,
            "state_code": scode,
            "state_info": sinfo,
            "concepts": concepts,
            "crisis_checklist": CRISIS_CHECKLIST,
            "legal_aid": {scode: state_aid},
            "disclaimer": "Legal information only. Not legal advice. Not a lawyer. Verify with qualified counsel.",
            "staleness_warning_days": 90,
            "abstention_note": "Where verification_status is PARTIAL or UNVERIFIED, consult the official_url for current law."
        }
        state_path = OFFLINE_STATES_DIR / f"{scode}_offline.json"
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(state_pkg, f, indent=2)

        if scode == "WA":
            wa_size_kb = round(state_path.stat().st_size / 1024, 2)

    print(f"Generated {len(states)} state offline packages in {OFFLINE_STATES_DIR}")
    print(f"WA offline package size: {wa_size_kb} KB")

    # Generate sha256 checksums file
    checksums = {}
    for p in OFFLINE_DIR.glob("*.json"):
        checksums[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    for p in OFFLINE_STATES_DIR.glob("*.json"):
        checksums[f"states/{p.name}"] = hashlib.sha256(p.read_bytes()).hexdigest()

    checksum_path = OFFLINE_DIR / "checksums.sha256"
    with open(checksum_path, "w", encoding="utf-8") as f:
        for fname, chk in sorted(checksums.items()):
            f.write(f"{chk}  {fname}\n")
    print("Generated checksums.sha256")

    return full_size_kb, wa_size_kb


if __name__ == "__main__":
    build_offline_package()
