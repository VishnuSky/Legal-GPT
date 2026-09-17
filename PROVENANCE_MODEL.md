# Legal-GPT Provenance Graph Model

To guarantee tamper-proof integrity and complete auditability, all community submissions and authoritative law in Legal-GPT are structured as a **Directed Acyclic Graph (DAG) of Provenance**.

---

## 1. Provenance Graph Architecture

```
                  ┌─────────────────────────────────┐
                  │      OFFICIAL LEGAL ENTITY      │
                  │ (e.g. Washington State Legis.)  │
                  └────────────────┬────────────────┘
                                   │ PUBLISHED_BY
                                   ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    SUBMITTER    ├──────►│  CONTRIBUTION   │◄──────┤    REVIEWER     │
│ (JaneDoe / Org) │       │   (CONTRIB-001) │       │ (Licensed Atty) │
└─────────────────┘       └────────┬────────┘       └─────────────────┘
     SUBMITTED_BY                  │                         VERIFIED_BY
                                   │ SUPERSEDED_BY
                                   ▼
                          ┌─────────────────┐
                          │  CONTRIBUTION   │
                          │   (CONTRIB-002) │
                          └─────────────────┘
```

---

## 2. Graph Node Types

1. **`ContributionNode`**: Represents the submitted legal item (Statute, Case, Resource, Benchmark, etc.).
   - `id`: Unique identifier (e.g. `CONTRIB-A9F21804`).
   - `content_hash`: SHA-256 hash of the submitted text and metadata.
   - `authority_tier`: Formal authority level.
   - `verification_state`: One of `PROPOSED`, `UNDER_REVIEW`, `VERIFIED`, `REJECTED`, `SUPERSEDED`, `ARCHIVED`.
2. **`SubmitterNode`**: Represents the contributing entity.
   - `submitter_id`: Handle, name, or public signing key.
   - `organization`: Sponsoring organization, legal aid clinic, or independent researcher.
3. **`ReviewerNode`**: Represents the auditing individual or team.
   - `reviewer_id`: Auditing attorney, maintainer, or verification specialist.
   - `credentials`: Bar affiliation, institutional position, or verification role.
4. **`OfficialSourceNode`**: Represents the authentic originating publisher.
   - `official_portal_url`: Direct URL to the government repository or court reporter.
   - `publisher_name`: Official body (e.g. "Supreme Court of the United States", "Illinois General Assembly").

---

## 3. Graph Edge Types

| Edge Type | Source Node | Target Node | Meaning |
| :--- | :--- | :--- | :--- |
| **`SUBMITTED_BY`** | `ContributionNode` | `SubmitterNode` | Connects the contribution to the author who submitted it. |
| **`ORIGINATES_FROM`**| `ContributionNode` | `OfficialSourceNode` | Binds the contribution to its primary government publication source. |
| **`REVIEWED_BY`** | `ContributionNode` | `ReviewerNode` | Records that a qualified reviewer audited the submission. |
| **`VERIFIED_BY`** | `ContributionNode` | `ReviewerNode` | Records the final certification promoting the item to `VERIFIED`. |
| **`REJECTED_BY`** | `ContributionNode` | `ReviewerNode` | Records the rejection action with an immutable explanatory rationale. |
| **`SUPERSEDES`** | `ContributionNode` | `ContributionNode` | Connects a newer legislative amendment to the prior version it replaced. |
| **`CITES`** | `ContributionNode` | `ContributionNode` | Documents citation relationships between authorities. |

---

## 4. Cryptographic Tamper-Proofing

Each node incorporates a cryptographic checksum:

$$\text{NodeHash} = \text{SHA256}(\text{source} \parallel \text{jurisdiction} \parallel \text{effective\_date} \parallel \text{payload} \parallel \text{parent\_hash})$$

This creates a verifiable chain of custody:
- Modifications to any statute or interpretation alter the node's hash.
- History cannot be rewritten retroactively.
- Point-in-time legal validity can be proven by tracing the graph state at any historic commit timestamp.

---

## 5. Audit Trail & Verification Ledger

Every state transition logs an immutable event:
```json
{
  "event_id": "EVT-88F102B9",
  "timestamp": "2026-09-17T11:15:00Z",
  "contribution_id": "CONTRIB-A9F21804",
  "previous_state": "UNDER_REVIEW",
  "new_state": "VERIFIED",
  "actor_id": "Reviewer-Atty-WA",
  "action": "PROMOTE_TO_VERIFIED",
  "verification_details": {
    "official_url_matched": true,
    "citator_signal": "GOOD_LAW",
    "temporal_effective_confirmed": "2021-07-01",
    "reason": "Statute matches official Washington State Code Reviser text exactly."
  }
}
```
