"""Legal Domain and Issue Spotting Classifier for Public Legal Navigator."""

import re
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class LegalDomain(str, Enum):
    CONSTITUTIONAL = "CONSTITUTIONAL"              # Due process, 4th Amendment search & seizure, Equal protection
    CPS_CHILD_WELFARE = "CPS_CHILD_WELFARE"        # Child dependency, emergency removal, shelter care, CPS investigations
    FAMILY_LAW = "FAMILY_LAW"                      # Custody, dissolution, parenting plans, guardianship, domestic violence
    HOUSING_TENANT = "HOUSING_TENANT"              # Eviction, lease violations, habitability, security deposits
    CONSUMER_DEBT = "CONSUMER_DEBT"                # Debt collection, credit reporting, unfair trade practices, loans
    EMPLOYMENT = "EMPLOYMENT"                      # Wage theft, wrongful termination, workplace safety, discrimination
    EDUCATION = "EDUCATION"                        # Special education, IEP, school discipline, student rights
    HEALTH_LAW = "HEALTH_LAW"                      # Medical consent, patient rights, Medicaid/Medicare disputes
    MENTAL_HEALTH = "MENTAL_HEALTH"                # Involuntary commitment, mental health treatment rights, conservatorship
    DISABILITY_RIGHTS = "DISABILITY_RIGHTS"        # ADA accommodations, public accessibility, service animals
    CIVIL_RIGHTS = "CIVIL_RIGHTS"                  # Police misconduct, discrimination, freedom of speech/religion
    ADMINISTRATIVE = "ADMINISTRATIVE"              # Agency licensing, benefits denial (SNAP, TANF), central registry appeals
    CRIMINAL_DEFENSE = "CRIMINAL_DEFENSE"          # Arrest, criminal charges, bail, public defender eligibility
    IMMIGRATION = "IMMIGRATION"                    # Public immigration processes, citizenship, asylum informational rights


class DomainClassification(BaseModel):
    domain: LegalDomain
    confidence: float
    trigger_keywords: List[str] = Field(default_factory=list)
    summary: str


class LegalIssueClassificationResult(BaseModel):
    primary_domain: LegalDomain
    secondary_domains: List[LegalDomain] = Field(default_factory=list)
    domain_scores: Dict[str, float] = Field(default_factory=dict)
    all_classifications: List[DomainClassification] = Field(default_factory=list)
    spotted_issues: List[str] = Field(default_factory=list)
    routed_concepts: List[str] = Field(default_factory=list)


class IssueClassifier:
    """Classifies user situations across 14 substantive legal domains and spots potential issues."""

    CONCEPT_ROUTES = {
        "police entered my home": "fourth_amendment_home_entry",
        "disability discrimination": "ada_section_504_dependency",
        "violated my civil rights": "civil_rights_section_1983",
    }

    @classmethod
    def route_concept(cls, narrative: str) -> Optional[str]:
        """Routes specific trigger phrases to verified legal literacy concepts."""
        text_lower = narrative.lower()
        for phrase, concept_id in cls.CONCEPT_ROUTES.items():
            if phrase in text_lower:
                return concept_id
        return None

    DOMAIN_KEYWORDS = {
        LegalDomain.CPS_CHILD_WELFARE: [
            "cps", "caseworker", "child protective services", "dcyf", "dcfs", "dfps", "acs",
            "shelter care", "dependency", "removed my child", "took my child", "foster care",
            "child abuse", "neglect", "safety plan", "kinship", "visitation", "family time",
            "tpr", "termination of parental rights", "adjudication", "icwa", "indian child"
        ],
        LegalDomain.CONSTITUTIONAL: [
            "constitutional", "due process", "fourth amendment", "search and seizure",
            "warrantless", "unreasonable search", "without a warrant", "fourteenth amendment",
            "equal protection", "substantive due process", "procedural due process",
            "civil rights", "fundamental right", "liberty interest", "santosky", "troxel"
        ],
        LegalDomain.HOUSING_TENANT: [
            "landlord", "tenant", "evict", "eviction", "notice to vacate", "pay or quit",
            "lease", "rent", "habitability", "mold", "broken heater", "security deposit",
            "unlawful detainer", "housing authority", "section 8", "squatter", "lockout"
        ],
        LegalDomain.CONSUMER_DEBT: [
            "debt", "debt collector", "collection agency", "creditor", "lawsuit for money",
            "garnishment", "bank levy", "credit card", "medical bill", "fdcpa",
            "scam", "fraudulent charge", "repo", "repossession", "credit score", "dispute debt"
        ],
        LegalDomain.FAMILY_LAW: [
            "custody", "parenting plan", "visitation schedule", "child support", "divorce",
            "dissolution", "paternity", "restraining order", "domestic violence", "protection order",
            "guardianship", "alimony", "spousal maintenance"
        ],
        LegalDomain.EMPLOYMENT: [
            "employer", "fired", "terminated", "wrongful termination", "unpaid wages",
            "overtime", "minimum wage", "retaliation", "whistleblower", "harassment at work",
            "eeoc", "fmla", "sick leave", "workplace safety", "osha"
        ],
        LegalDomain.EDUCATION: [
            "school", "iep", "special education", "504 plan", "suspension", "expulsion",
            "truancy", "school district", "bullying", "accommodations in school", "idea act"
        ],
        LegalDomain.DISABILITY_RIGHTS: [
            "disability", "disabled", "ada", "accommodation", "service dog", "wheelchair",
            "accessible", "physical limitation", "blind", "deaf", "reasonable accommodation"
        ],
        LegalDomain.MENTAL_HEALTH: [
            "involuntary commitment", "psychiatric", "mental health hold", "baker act",
            "5150", "psychiatric facility", "forced medication", "conservatorship", "mental capacity"
        ],
        LegalDomain.ADMINISTRATIVE: [
            "administrative hearing", "central registry", "founded finding", "substantiated finding",
            "snap", "food stamps", "medicaid denial", "tanf", "social security denial",
            "ssi", "ssdi", "driver license suspended", "professional license"
        ],
        LegalDomain.CRIMINAL_DEFENSE: [
            "arrest", "arrested", "charged", "misdemeanor", "felony", "bail", "jail",
            "police custody", "public defender", "arraignment", "plea", "miranda", "probation"
        ],
        LegalDomain.IMMIGRATION: [
            "immigration", "visa", "green card", "uscis", "deportation", "asylum",
            "undocumented", "naturalization", "work authorization", "ice", "border"
        ]
    }

    @classmethod
    def classify_issues(cls, narrative: str) -> LegalIssueClassificationResult:
        """Evaluates narrative text, computes keyword frequency and weights, and identifies primary/secondary domains."""
        text_lower = narrative.lower()
        domain_counts: Dict[LegalDomain, int] = {}
        domain_triggers: Dict[LegalDomain, List[str]] = {}

        for domain, keywords in cls.DOMAIN_KEYWORDS.items():
            matched = []
            for kw in keywords:
                if re.search(rf'\b{re.escape(kw)}\b', text_lower):
                    matched.append(kw)
            if matched:
                domain_counts[domain] = len(matched)
                domain_triggers[domain] = matched

        # If constitutional keywords appear alongside CPS or Housing, give appropriate weighting
        if LegalDomain.CONSTITUTIONAL in domain_counts and LegalDomain.CPS_CHILD_WELFARE in domain_counts:
            domain_counts[LegalDomain.CPS_CHILD_WELFARE] += 2

        # Sort domains by count
        sorted_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)

        if not sorted_domains:
            # Fallback general civil
            primary = LegalDomain.CPS_CHILD_WELFARE
            secondary = []
            classifications = [
                DomainClassification(
                    domain=primary,
                    confidence=0.5,
                    trigger_keywords=[],
                    summary="General civil / child welfare context by default."
                )
            ]
            scores = {primary.value: 0.5}
        else:
            primary = sorted_domains[0][0]
            secondary = [d[0] for d in sorted_domains[1:4]]
            total_hits = sum(d[1] for d in sorted_domains)
            scores = {d[0].value: round(d[1] / max(1, total_hits), 2) for d in sorted_domains}
            classifications = []
            for d, cnt in sorted_domains[:4]:
                classifications.append(DomainClassification(
                    domain=d,
                    confidence=round(cnt / max(1, total_hits), 2),
                    trigger_keywords=domain_triggers.get(d, []),
                    summary=f"Identified {cnt} concept matches for {d.value}."
                ))

        # Concept routing check
        routed_concepts = []
        for phrase, cid in cls.CONCEPT_ROUTES.items():
            if phrase in text_lower and cid not in routed_concepts:
                routed_concepts.append(cid)

        # Spot specific legal issues based on top domains and keywords
        spotted_issues = cls._generate_spotted_issues(primary, secondary, text_lower)

        return LegalIssueClassificationResult(
            primary_domain=primary,
            secondary_domains=secondary,
            domain_scores=scores,
            all_classifications=classifications,
            spotted_issues=spotted_issues,
            routed_concepts=routed_concepts
        )

    @classmethod
    def _generate_spotted_issues(
        cls,
        primary: LegalDomain,
        secondary: List[LegalDomain],
        text_lower: str
    ) -> List[str]:
        """Generates concrete legal issues based on domain and factual trigger terms."""
        issues = []

        # Civil rights concept routes
        if "police entered my home" in text_lower:
            issues.append("Fourth Amendment protection against warrantless home entry (fourth_amendment_home_entry)")
        if "disability discrimination" in text_lower:
            issues.append("ADA Title II / Section 504 reasonable accommodation duty (ada_section_504_dependency)")
        if "violated my civil rights" in text_lower:
            issues.append("Civil rights claim under 42 U.S.C. § 1983 (Note: user claim, not an established judicial fact; civil_rights_section_1983)")

        # CPS Issues
        if primary == LegalDomain.CPS_CHILD_WELFARE or LegalDomain.CPS_CHILD_WELFARE in secondary:
            if any(term in text_lower for term in ["removed", "took my", "seized", "hospital"]):
                issues.append("Threshold validity of emergency protective custody / warrantless removal")
            if any(term in text_lower for term in ["hearing", "court date", "72 hour", "shelter"]):
                issues.append("Statutory timeline compliance for shelter care / temporary custody hearing")
            if any(term in text_lower for term in ["notice", "papers", "served", "tell me"]):
                issues.append("Procedural due process notice requirements prior to detention hearing")
            if any(term in term for term in ["counsel", "attorney", "lawyer", "afford"]):
                issues.append("Statutory and constitutional right to court-appointed indigent counsel")
            if any(term in text_lower for term in ["relative", "grandma", "grandparent", "aunt"]):
                issues.append("Statutory preference for relative kinship placement over foster care")
            if any(term in text_lower for term in ["indian", "tribe", "tribal", "native", "icwa"]):
                issues.append("Indian Child Welfare Act (ICWA) tribal notice and heightened active efforts")
            if any(term in text_lower for term in ["visit", "visitation", "see my"]):
                issues.append("Parental right to regular, ongoing family time and visitation")

        # Constitutional Search & Seizure Issues
        if LegalDomain.CONSTITUTIONAL in secondary or primary == LegalDomain.CONSTITUTIONAL:
            if "warrant" in text_lower or "door" in text_lower or "enter" in text_lower:
                issues.append("Fourth Amendment limits on warrantless entry into a private residence")
            if "process" in text_lower or "notice" in text_lower or "hearing" in text_lower:
                issues.append("Fourteenth Amendment procedural due process notice and opportunity to be heard")

        # Housing Issues
        if primary == LegalDomain.HOUSING_TENANT or LegalDomain.HOUSING_TENANT in secondary:
            if "notice" in text_lower or "days" in text_lower:
                issues.append("Validity of landlord statutory notice period (e.g. 3-day, 14-day, 30-day)")
            if "habitability" in text_lower or "repair" in text_lower or "mold" in text_lower:
                issues.append("Implied warranty of habitability and defense of rent withholding")
            if "lock" in text_lower or "shut off" in text_lower:
                issues.append("Unlawful constructive eviction / illegal self-help lockout")

        # Consumer Debt Issues
        if primary == LegalDomain.CONSUMER_DEBT or LegalDomain.CONSUMER_DEBT in secondary:
            if "collector" in text_lower or "harass" in text_lower:
                issues.append("Fair Debt Collection Practices Act (FDCPA) prohibited communication practices")
            if "dispute" in text_lower or "validate" in text_lower:
                issues.append("Statutory debt validation request rights within 30-day notice window")

        if not issues:
            issues.append(f"General inquiry regarding statutory rules and rights under {primary.value}")

        return issues
