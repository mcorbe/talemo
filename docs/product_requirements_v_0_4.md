# Product Requirements Document (PRD)

## 1. Document Control

| Item | Value |
| ---- | ----- |
|      |       |

|   |
| - |

|   |
| - |

| **Product**   | Family Audio‑Stories Platform                     |
| ------------- | ------------------------------------------------- |
| **Version**   | **0.4** (Governance & SECNUMCLOUD alignment)      |
| **Author**    | Product Team / CTO                                |
| **Date**      | 22 Jun 2025                                       |
| **Reviewers** | Engineering · Design · Marketing · Legal · SecOps |

---

## 2. Executive Summary

A **mobile‑first** platform for families and institutions to **discover, listen to, and create** short audio stories. v0.4 introduces a **multi‑tenant governance layer** with tenant‑scoped **Profiles**, **UserIdentity** linking of multiple IDPs, and a **TenantPolicy** KV store. These changes hard‑enforce data isolation and map cleanly to the French **ANSSI SECNUMCLOUD** controls, while keeping the stack Django / PostgreSQL / Celery / MinIO and agent‑centric.

---

## 3. Goals & Non‑Goals

### 3.1 Goals (additions in **bold**)

1. Deliver an intuitive, mobile‑first experience for families to **discover** and **listen** to audio stories.
2. Provide creators/admins a workflow to **generate new stories** (text → audio + illustration) via CrewAI.
3. Implement **enterprise authentication & authorization** with Google and Apple SSO, extensible to SAML/OIDC.
4. Ensure the platform is **cloud‑agnostic** with S3‑compatible storage swap‑outs.
5. Offer an admin UI to manage stories, assets, and metadata.
6. Leverage **agent‑based architecture** for modular creation, moderation, search.
7. **Provide strict multi‑tenant governance** so each family or institution is a logical silo.
8. **Manage permissions through reusable Profiles; no per‑user role tweaking.**
9. **Guarantee one digital identity (IDP issuer+subject) = one tenant** across the platform.
10. Prepare for a **freemium subscription model**, B2B licensing, and future IP partnerships.

### 3.2 Non‑Goals (unchanged)

- Full public social features (likes, comments) — deferred.
- Native desktop app — focus is mobile PWA + optional wrappers.

---

## 4. Success Metrics (unchanged)

| Metric                                 | Target                         |
| -------------------------------------- | ------------------------------ |
| 🟢 **Time‑to‑First‑Play** (new user)   | < 30 s                         |
| 🟢 **Story Search Success**            | ≥ 90 % (search result clicked) |
| 🟢 **Story Generation Lead Time**      | ≤ 2 min (submit → audio ready) |
| 🟢 **Mobile PWA Lighthouse Perf**      | ≥ 85                           |
| 🟢 **Net Promoter Score (NPS)**        | ≥ 50                           |
| 🟢 **Customer Acquisition Cost (CAC)** | ≤ €6                           |
| 🟢 **LTV / CAC Ratio**                 | ≥ 3.5 ×                        |

---

## 5. Personas & Use Cases

- **Family Administrator** (new) – creates a household tenant, invites parents & children, manages profiles.
- **Institution Admin** (new) – librarian/teacher controlling an organisation tenant.
- **Parent (Amélie, 38)** – browses bedtime stories on phone, filters by length/theme.
- **Child (Léo, 8)** – taps colourful card, plays story.
- **Story Creator (Lucas, 30)** – writes text, triggers AI asset generation.
- **Admin** – moderates flagged content, manages quotas.
- **School/Day‑care Buyer** – explores institutional subscription with curriculum filters.

---

## 6. Functional Requirements

### 6.1 Core Experience (retained)

- Story List, Story Detail, Story Creation, Agentic Assistant, Admin Dashboard, SSO.

### 6.2 Governance & Multi‑Tenancy (new)

| Ref    | Requirement                                                                                                 |
| ------ | ----------------------------------------------------------------------------------------------------------- |
| GOV‑01 | **Tenant bootstrap** – users are created only via invitation tokens embedding `tenant_id`; no orphan users. |
| GOV‑02 | **Profile catalogue** – tenant admins create/clone/delete permission profiles (e.g., *Kids Listen‑Only*).   |
| GOV‑03 | **Bulk assignment** – admins can move multiple users between profiles in one action.                        |
| GOV‑04 | **Identity uniqueness** – composite DB constraint `(idp_issuer, idp_subject)` is globally unique.           |
| GOV‑05 | **Multiple IDPs per user** – allowed if they map to the same tenant, stored in `UserIdentity`.              |
| GOV‑06 | **Tenant‑wide feature flags / quotas** – `TenantPolicy` KV store (e.g., `story_quota = 50`).                |
| GOV‑07 | **Audit trail** – all profile/policy edits logged to immutable WORM storage ≥ 1 yr.                         |
| GOV‑08 | **Row‑level security** – every tenant‑bound table enforces `tenant_id = current_setting('app.tenant')`.     |

---

## 7. Agent Architecture

The platform runs a suite of stateless **CrewAI** agents orchestrated by Celery. Each agent receives a tenant‑scoped message, performs one atomic task, emits an event for the next stage, and writes an audit trace for SECNUMCLOUD.

| Agent                    | Purpose                                                                          | Consumes → Produces                                |
| ------------------------ | -------------------------------------------------------------------------------- | -------------------------------------------------- |
| **SearchAgent**          | Hybrid semantic + keyword search on `pgvector`; returns ordered `story_id` list. | `search.query` → `search.results`                  |
| **ModerationAgent**      | Runs GPT‑4 based moderation & keyword heuristics; flags disallowed content.      | `story.draft` → `story.approved` / `story.flagged` |
| **TTSAgent**             | Synthesises speech via tenant‑selected voice pack; stores `.mp3` in MinIO.       | `story.approved` → `asset.audio.ready`             |
| **IllustratorAgent**     | Generates cover art (Stable Diffusion XL); stores `.png` under tenant prefix.    | `story.approved` → `asset.image.ready`             |
| **MetadataAgent**        | Extracts language, tags, reading‑level; updates `story` row.                     | `story.draft`                                      |
| **QuotaAgent**           | Enforces `TenantPolicy.story_quota`; blocks over‑limit creations.                | `story.request`                                    |
| **PersonalizationAgent** | Updates per‑user embeddings for recommendations.                                 | `play.event`                                       |

> All agent logs stream to an immutable WORM bucket to satisfy traceability (IS‑5).

---

## 8. Information Architecture / Data Model

```
Tenant        id · name · type [family | institution]
Profile       id · tenant_id · name(unique) · permissions JSONB
User          id · tenant_id(!) · profile_id(!) · email · name · is_active · …
UserIdentity  id · user_id · idp_issuer · idp_subject   -- UNIQUE(issuer,subject)
TenantPolicy  id · tenant_id · key(unique) · value JSONB
Story         id · tenant_id · visibility [public | tenant_only | private] · …
Asset         id · tenant_id · type(image/audio) · file_path · …
AgentTask     id · agent_type · input · output · status · …
```

*All tenant‑bound tables share the same RLS predicate:* `USING (tenant_id = current_setting('app.tenant')::uuid)`

---

## 9. UX Flows

### 9.1 Invite & Onboarding (Admin → User)

1. Admin opens **Invite** screen, picks profile (e.g., *Kids Listen‑Only*), enters email.
2. System generates a single‑use link containing `tenant_id` + `invite_token`.
3. Recipient clicks link → SSO (Google / Apple).
4. Back‑end validates `(issuer, subject)` uniqueness; creates `User`, links `UserIdentity`.
5. New user lands on **Welcome** and completes a 3‑step tutorial.

### 9.2 Story Discovery & Playback

1. Home shows **Categories**, **Continue Listening**, **For You**.
2. User taps a card → Story Detail (cover, tags, length).
3. Taps **Play** → signed URL fetched, native `<audio>` element streams.
4. `play.event` posted; PersonalizationAgent updates embeddings.

### 9.3 Story Creation (Parent / Creator)

1. Tap **Create** → Composer opens.
2. Enter title + story text; optional prompt for illustration.
3. Draft saved; QuotaAgent checks `story_quota`.
4. Tap **Publish** → ModerationAgent; if approved, TTSAgent & IllustratorAgent run.
5. Assets ready → push notification; story visible in My Stories.

### 9.4 Profile Management (Admin)

1. Admin opens **Profiles** tab.
2. Tap **New Profile** → clone or blank.
3. Toggle permissions & quotas via JSON‑backed UI.
4. Save emits audit event; changes propagate instantly.
5. Drag‑select users → **Assign to profile** for bulk update.

> Detailed wireframes live in Figma (*UX‑Flows‑v4*).

---

## 10. Technical Architecture (minor additions)

- Backend: Django + Django REST + PostgreSQL **(RLS enabled)**
- Auth: `django‑allauth` SSO + IDP linking via `UserIdentity`.
- Permission evaluation: request loads `Profile.permissions` JSON once; quotas from `TenantPolicy`.
- Storage: MinIO/S3 prefixes per tenant.

Mobile‑app strategy and other subsections unchanged.

---

## 12. Security & Access Control (rewritten)

- **Authorization**: permissions flow strictly via Profiles; no per‑user toggles.
- **Identity binding**: `(issuer, subject)` uniqueness rule blocks cross‑tenant login.
- **Row‑level security**: single‑column predicate keeps queries cheap & auditable.
- **Audit**: profile/policy changes and break‑glass actions streamed to immutable log bucket.

---

## 16. Compliance & Safety (update)

- Target **GDPR, COPPA, and SECNUMCLOUD (ANSSI)** certification.
- Explicit mapping of IS‑1 → IS‑5 controls to backlog epics (see Engineering doc).
- Isolation + traceability proofs via identity uniqueness & RLS.

---

## 17. App‑Store Compliance Strategy (unchanged)

---

## 18. Open Strategic Questions (updated)

1. Which regional launch first: France‑only vs multilingual?
2. Minimum licensing required for branded IP?
3. **Should we open a profile marketplace for shared templates?**
4. **Do institutional tenants need data residency beyond EU‑wide hosting?**
5. Should we prioritise mobile app downloads over PWA adoption?

---

## 19. Next Steps (Pre‑Implementation) (unchanged except SECNUMCLOUD)

| Area                      | Action Item                                                                       | Owner          |
| ------------------------- | --------------------------------------------------------------------------------- | -------------- |
| 🔐 **Compliance Audit**   | Map PRD v0.4 controls to SECNUMCLOUD checklist; schedule external gap assessment. | SecOps + Legal |
| 📦 **MVP Tech Stack POC** | Validate Profile & RLS scaffold with sample load test.                            | Engineering    |
| … (other rows unchanged)  |                                                                                   |                |

---

*End of Document (v0.4)*

