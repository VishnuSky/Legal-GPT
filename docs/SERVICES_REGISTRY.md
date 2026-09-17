# Official Civil Legal Aid & Public Services Registry

## 1. Overview & Purpose

The `services/` module provides a verified, structured directory of official civil legal aid organizations, court self-help facilitators, bar association pro bono referral networks, and government ombuds offices across federal, state, and tribal jurisdictions.

When a user or autonomous agent queries Legal-GPT via the Public Scout Bridge (`POST /api/v1/public/resolve` or `GET /api/v1/public/services`), the engine pairs controlling legal citations with direct, actionable contact information for verified public institutional support.

---

## 2. Public-Source Provenance & Strict Data Isolation

In strict adherence to `PUBLIC_DATA_POLICY.md`:
- **100% Official Public Sourcing**: All service records are curated from publicly accessible state government directories, official court websites, Legal Services Corporation (LSC) grantee portals, and federally recognized tribal registries.
- **Zero Scraped Private Data**: The registry contains no private attorney rosters, paid directory listings, individual case worker personal information, or proprietary commercial databases.
- **Cryptographic Integrity**: Every service record computes an immutable SHA-256 integrity hash (`content_sha256`) over its canonical identifiers, ensuring seed data has not been modified or corrupted.

---

## 3. Supported Service Types & Taxonomies

### Service Classifications (`ServiceType`)
1. `LEGAL_AID`: LSC-funded or state IOLTA-funded non-profit civil legal aid providers (e.g., Northwest Justice Project, Legal Aid Chicago, Ohio Legal Help).
2. `COURT_SELF_HELP`: Official court facilitator offices, self-help centers, and clerk assistance desks (e.g., Skagit County Family Law Facilitator, Cook County Help Desk).
3. `BAR_REFERRAL`: State and county bar association lawyer referral services and modest-means panels.
4. `AG_CONSUMER`: State Attorney General consumer protection, civil rights, and public advocacy bureaus.
5. `TRIBAL_ICWA`: Federally recognized tribal courts, tribal ICWA designated liaisons, and tribal legal departments.
6. `PUBLIC_CONTACT`: Official state agency ombudsman offices and family advocacy hotlines (e.g., Washington Office of the Family and Children's Ombuds - OFCO).

### Civil Matter Taxonomies (`CivilMatterType`)
- `FAMILY_CPS`: Dependency, child removal defense, shelter care hearings, custody, domestic violence.
- `HOUSING`: Unlawful detainer, tenant rights, habitability, foreclosure prevention.
- `CONSUMER_DEBT`: Debt defense, FDCPA violations, predatory lending, credit protection.
- `EMPLOYMENT`: Wage theft, worker misclassification, workplace rights.
- `BENEFITS`: SNAP, Medicaid, SSI/SSDI appeals, TANF, unemployment.
- `EDUCATION`: Special education due process, IEP enforcement, disciplinary hearings.
- `DISABILITY`: ADA Title II/III public accommodations, disability rights advocacy.
- `IMMIGRATION`: Public immigration forms, naturalization assistance, fee waiver information.
- `SMALL_CLAIMS`: Security deposit disputes, breach of contract, small claims court self-help.
- `PUBLIC_RECORDS`: State Public Records Acts, FOIA, government transparency requests.

---

## 4. Seed Files & Registry Structure

Seed definitions reside under `services/seeds/`:
- `federal_services.yaml`: National Legal Services Corporation (LSC), DOJ Access to Justice, HHS Children's Bureau, National ICWA directory.
- `wa_services.yaml`: Northwest Justice Project (CLEAR hotline), Skagit/King County Court Facilitators, Washington OFCO Ombuds, Puyallup Tribal Court.
- `il_services.yaml`: Legal Aid Chicago, Illinois Legal Aid Online (ILAO), Cook County Early Resolution Program (ERP), Illinois DCFS Advocacy Office.
- `oh_services.yaml`: Ohio Legal Help, Legal Aid Society of Cleveland, Cuyahoga County Juvenile Court Self-Help Center.

---

## 5. Programmatic Usage

```python
from services.registry import default_service_registry
from services.models import CivilMatterType, ServiceType

# 1. Query legal aid for CPS matters in Skagit County, WA
hits = default_service_registry.query_services(
    state="WA",
    county="Skagit",
    matter=CivilMatterType.FAMILY_CPS,
    service_type=ServiceType.LEGAL_AID
)

for service in hits:
    print(f"Service: {service.name}")
    print(f"Phone: {service.contact.phone}")
    print(f"Website: {service.contact.website}")
    print(f"Eligibility: {service.eligibility_summary}")
```
