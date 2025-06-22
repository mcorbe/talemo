# Product Requirements Document (PRD)

## 1. Document Control

| **Product**   | Family Audio‑Stories Platform                     |
| ------------- | ------------------------------------------------- |
| **Author**    | Product Team / CTO                                |
| **Date**      | 22 Jun 2025                                       |
| **Reviewers** | Engineering · Design · Marketing · Legal · SecOps |

---

## 2. Executive Summary

**Talemo turns screen-time into shared audio imagination.**  

It is a mobile-first platform where families, schools, and libraries can **discover, listen to, and co-create short audio stories**—all inside a lightning-fast Progressive Web App that works on any phone or tablet.

### What makes Talemo different

#### Where it delights
- **Instant joy** — three taps from home-screen to playback keep “time-to-first-play” under 30 seconds, so parents can calm a restless child fast.  
- **Kids become storytellers** — an intuitive composer plus AI agents (voice, illustration, story coaching) lets children craft narrated tales in minutes, turning them from passive consumers into creators.  
- **Free to start, easy to grow** — a generous freemium tier removes barriers; households upgrade for unlimited creation, while institutions license per seat or flat-fee.

#### How it wins
- **Multi-tenant privacy by design** — every household or institution is its own secure silo, enforced down to row-level security and tenant-scoped storage.  
- **Compliance baked-in** — governance, audit trails, and control mapping align with GDPR, COPPA, and France’s SECNUMCLOUD, giving schools enterprise-grade assurance with zero IT effort.  
- **Agent-centric architecture** — modular AI services run on a lean Django + PostgreSQL stack, keeping the product fast today and future-proof for new creative workflows.

**The outcome:** Talemo delivers wholesome, interactive audio experiences that strengthen family bonds, empower young voices, and give educators a safe, ready-made storytelling lab—while meeting the strict governance and compliance standards that modern digital learning demands.

---

## 3. Goals & Non‑Goals

### 3.1 Goals

1. Deliver an intuitive, mobile‑first experience for families to **discover** and **listen** to audio stories.
2. Provide creators/admins a workflow to **generate new stories** (text → audio + illustration) via CrewAI.
3. Implement **enterprise authentication & authorization** with Google and Apple SSO, extensible to SAML/OIDC.
4. Ensure the platform is **cloud‑agnostic** with S3‑compatible storage swap‑outs.
5. Offer an admin UI to manage stories, assets, and metadata.
6. Leverage **agent‑based architecture** for modular creation, moderation, search.
7. **Provide strict multi‑tenant governance** so each family or institution is a logical silo.
8. **Manage permissions through reusable Profiles; no per‑user role tweaking.**
9. **Guarantee one digital identity (IDP issuer+subject) = one tenant** across the platform.
10. Prepare for a **freemium subscription model**, B2B licensing, and future IP partnerships.

### 3.2 Non‑Goals

- Full public social features (likes, comments) — deferred.
- Native desktop app — focus is mobile PWA + optional wrappers.

---

## 4. Success Metrics

| Metric                                 | Target                         |
| -------------------------------------- | ------------------------------ |
| 🟢 **Time‑to‑First‑Play** (new user)   | < 30 s                         |
| 🟢 **Story Search Success**            | ≥ 90 % (search result clicked) |
| 🟢 **Story Generation Lead Time**      | ≤ 2 min (submit → audio ready) |
| 🟢 **Mobile PWA Lighthouse Perf**      | ≥ 85                           |
| 🟢 **Net Promoter Score (NPS)**        | ≥ 50                           |
| 🟢 **Customer Acquisition Cost (CAC)** | ≤ €6                           |
| 🟢 **LTV / CAC Ratio**                 | ≥ 3.5 ×                        |

---

## 5. Competitive Landscape — Looking Beyond Niche Players

Talemo competes on two fronts:

1. **Family-safe audio streaming & discovery**
2. **Generative-AI story creation**

### Global Platforms With Generative Muscle

| Platform               | Why It Matters                                                | Strategic Gap Talemo Exploits                                                                                |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| **OpenAI / ChatGPT** | ChatGPT’s voice mode can spin a bedtime story on demand, in any language, at near-zero marginal cost. Kids already use it through parents’ phones or smart speakers. | No multi-profile governance, no curated kid catalog, and no teacher admin controls for classrooms. :contentReference[oaicite:0]{index=0} |
| **Google Gemini** | “Audio Overview” converts documents and prompts into spoken summaries and is baked into Android and Chromebook ecosystems. Future Gemini Kid agents could extend that to stories. | Privacy and moderation for under-13 users remain an open question; no turnkey institutional tenancy. :contentReference[oaicite:1]{index=1} |
| **Amazon Alexa Kids+ / Stories with Alexa** | Alexa+ (Feb 2025) added “Stories with Alexa,” letting kids co-create tales by voice on tens of millions of Echo devices. | Hardware-bound experience; weak cross-institution admin tooling; limited visual art generation. :contentReference[oaicite:2]{index=2} |
| **Apple Intelligence** | Apple’s on-device generative stack can synthesize lifelike voices and will open APIs to any iOS developer; story apps can piggy-back quickly. | Apple keeps experiences siloed per device family; Talemo’s web-first PWA reaches every platform at once. :contentReference[oaicite:3]{index=3} |

### Mass-market Audio Hubs

| Platform | Current Kids Offering | Why It’s a Threat | Talemo Edge |
|----------|----------------------|-------------------|-------------|
| **Spotify (Kids, AI DJ, voice prompts)** | Spotify Kids app plus AI DJ that now takes spoken requests and generates mood-based playlists. :contentReference[oaicite:4]{index=4} | Could layer generative stories into its existing “Stories” rail and surface them to 600 M+ listeners. | Creation tools today focus on music, not narrative; no classroom compliance model. |
| **Apple / Google Podcasts, YouTube Kids, Audible** | Huge passive listening catalogs; some have exclusive kids podcasts (e.g., Cocomelon on Spotify). | Control the discovery funnel for audio. | None offer interactive, user-generated story creation. |

### Kid-Centric Hardware Ecosystems

| Device | Strengths | Weaknesses Relative to Talemo |
|--------|-----------|-------------------------------|
| **Yoto, Toniebox, Storypod** | Tangible, screen-free listening experience; strong retail presence. | Closed content pipelines; adding new stories is slow and often paid per item. Talemo can syndicate or white-label its catalog instead of building hardware. |

### Classroom & Ed-Tech Creators

Platforms like **Book Creator**, **Epic!**, and **Storytime AI** let teachers build multimedia books or students auto-generate tales, but they are print- or video-first and lack Talemo’s **audio-native**, **governance-by-tenant** approach.

---

### Positioning Take-aways

1. **Platform Risk, Feature Opportunity**  
   Big tech can (and will) generate bedtime stories, but none pair that with Talemo’s *multi-tenant privacy, age gates, and teacher dashboards*.

2. **Audio Is Still Fragmented**  
   Spotify owns music; Audible owns audiobooks; Alexa owns smart-speaker moments. **Nobody owns interactive, kid-safe audio storytelling.**

3. **Hardware Players Need Content**  
   Rather than fight Yoto or Toniebox, Talemo can syndicate select stories to their NFC cards while upselling creation features in-app.

4. **Defensible Wedge**  
   By focusing on **“kids become creators” + “institutions stay compliant,”** Talemo builds a moat that pure streaming services and raw LLM tools haven’t addressed.

Talemo’s blend of *AI-assisted creation*, *governance-grade privacy*, and *cross-platform PWA delivery* remains uniquely positioned—even when viewed against the largest tech incumbents.


---

## 6. Personas & Use Cases

| Persona                   | Description                                                                      |
| ------------------------- | -------------------------------------------------------------------------------- |
| **Family Administrator**  | Creates a household tenant, invites parents & children, manages profiles.        |
| **Institution Admin**     | Librarian/teacher controlling an organisation tenant.                            |
| **Parent (Amélie, 38)**   | Browses bedtime stories on phone, filters by length/theme.                       |
| **Child (Léo, 8)**        | Taps colourful card, plays story.                                                |
| **Story Creator (Lucas)** | Writes text, triggers AI asset generation.                                       |
| **Admin**                 | Moderates flagged content, manages quotas.                                       |
| **Story Assistant User**  | Chats with a story-building AI to co-create new adventures.                      |
| **School/Day‑care Buyer** | Explores institutional subscription with curriculum filters.                     |

---

## 7. Functional Requirements

### 7.1 Core Experience

| Ref    | Feature                | Description                                                                        |
| ------ | ---------------------- | ---------------------------------------------------------------------------------- |
| COR‑01 | **Story List**         | Browsable, filterable list of available stories                                    |
| COR‑02 | **Story Detail**       | Individual story view with metadata and playback controls                          |
| COR‑03 | **Story Creation**     | Interface for creating and editing stories                                         |
| COR‑04 | **Agentic Assistant**  | AI-powered assistant for story creation and discovery                              |
| COR‑05 | **Admin Dashboard**    | Management interface for content and users                                         |
| COR‑06 | **SSO**                | Single sign-on integration with Google and Apple                                   |
| COR‑07 | **Branching Engine**   | JSON graph model, simple choice UI (<4 options/junction), TTS/illustration per branch |
| COR‑08 | **Voice-Over Mode**    | Mobile mic recording, waveform trim, optional AI clean-up, stored as alternate audio track |
| COR‑09 | **Quiz Module**        | After playback, serve 3-5 auto-generated questions & word-lists; results feed Analytics dashboard |
| COR‑10 | **Accessibility Layer**| Auto-generate text transcript, toggle dyslexia-friendly typeface, WCAG AA colour palette |
| COR‑11 | **Multi-Author Drafts**| Shared edit rights inside a tenant, comments sidebar, version history              |

### 7.2 Governance & Multi‑Tenancy

| Ref    | Requirement                                                                                                 |
| ------ | ----------------------------------------------------------------------------------------------------------- |
| GOV‑01 | **Tenant bootstrap** – users are created only via invitation tokens embedding `tenant_id`; no orphan users. |
| GOV‑02 | **Profile catalogue** – tenant admins create/clone/delete permission profiles (e.g., *Kids Listen‑Only*).   |
| GOV‑03 | **Bulk assignment** – admins can move multiple users between profiles in one action.                        |
| GOV‑04 | **Identity uniqueness** – composite DB constraint `(idp_issuer, idp_subject)` is globally unique.           |
| GOV‑05 | **Multiple IDPs per user** – allowed if they map to the same tenant, stored in `UserIdentity`.              |
| GOV‑06 | **Tenant‑wide feature flags / quotas** – `TenantPolicy` KV store (e.g., `story_quota = 50`, `daily_time_limit`, `quiet_hours`). |
| GOV‑07 | **Audit trail** – all profile/policy edits logged to immutable WORM storage ≥ 1 yr.                         |
| GOV‑08 | **Row‑level security** – every tenant‑bound table enforces `tenant_id = current_setting('app.tenant')`.     |

---

## 8. Agent Architecture

The platform runs a suite of stateless **CrewAI** agents orchestrated by Celery. Each agent receives a tenant‑scoped message, performs one atomic task, emits an event for the next stage, and writes an audit trace for SECNUMCLOUD.

| Ref    | Agent                    | Purpose                                                                          | Consumes → Produces                                |
| ------ | ------------------------ | -------------------------------------------------------------------------------- | -------------------------------------------------- |
| AGT‑01 | **SearchAgent**          | Hybrid semantic + keyword search on `pgvector`; returns ordered `story_id` list. | `search.query` → `search.results`                  |
| AGT‑02 | **ModerationAgent**      | Runs GPT‑4 based moderation & keyword heuristics; flags disallowed content.      | `story.draft` → `story.approved` / `story.flagged` |
| AGT‑03 | **TTSAgent**             | Synthesises speech via tenant‑selected voice pack; stores `.mp3` in MinIO.       | `story.approved` → `asset.audio.ready`             |
| AGT‑04 | **IllustratorAgent**     | Generates cover art (Stable Diffusion XL); stores `.png` under tenant prefix.    | `story.approved` → `asset.image.ready`             |
| AGT‑05 | **MetadataAgent**        | Extracts language, tags, reading‑level; updates `story` row.                     | `story.draft`                                      |
| AGT‑06 | **QuotaAgent**           | Enforces `TenantPolicy.story_quota`; blocks over‑limit creations.                | `story.request`                                    |
| AGT‑07 | **PersonalizationAgent** | Updates per‑user embeddings for recommendations.                                 | `play.event`                                       |
| AGT‑08 | **TranslationAgent**     | Re-voices and re-illustrates approved stories for localization.                  | `story.translate` → `story.translated`             |

> All agent logs stream to an immutable WORM bucket to satisfy traceability (IS‑5).

### User-facing Agents

| Ref       | Agent                | Purpose                                                |
| --------- | -------------------- | ------------------------------------------------------ |
| AGT‑UF‑01 | **StoryCompanion**   | Co-creation chat assistant for families                |
| AGT‑UF‑02 | **SearchAssistant**  | Conversational assistant to surface content            |

---

## 9. Information Architecture / Data Model

```
Tenant        id · name · type [family | institution]
Profile       id · tenant_id · name(unique) · permissions JSONB
User          id · tenant_id(!) · profile_id(!) · email · name · is_active · …
UserIdentity  id · user_id · idp_issuer · idp_subject   -- UNIQUE(issuer,subject)
UserAchievement id · user_id · badge_type · earned_at · streak_count · …
TenantPolicy  id · tenant_id · key(unique) · value JSONB
Story         id · tenant_id · visibility [public | tenant_only | private] · …
Asset         id · tenant_id · type(image/audio) · file_path · …
AgentTask     id · agent_type · input · output · status · …
```

*All tenant‑bound tables share the same RLS predicate:* `USING (tenant_id = current_setting('app.tenant')::uuid)`

---

## 10. UX Flows

### 10.1 Invite & Onboarding (Admin → User)

| Ref      | Step | Description                                                                                      |
| -------- | ---- | ------------------------------------------------------------------------------------------------ |
| UXF‑01‑01 | 1    | Admin opens **Invite** screen, picks profile (e.g., *Kids Listen‑Only*), enters email.           |
| UXF‑01‑02 | 2    | System generates a single‑use link containing `tenant_id` + `invite_token`.                      |
| UXF‑01‑03 | 3    | Recipient clicks link → SSO (Google / Apple).                                                    |
| UXF‑01‑04 | 4    | Back‑end validates `(issuer, subject)` uniqueness; creates `User`, links `UserIdentity`.         |
| UXF‑01‑05 | 5    | New user lands on **Welcome** and completes a 3‑step tutorial.                                   |

### 10.2 Story Discovery & Playback

| Ref      | Step | Description                                                                                      |
| -------- | ---- | ------------------------------------------------------------------------------------------------ |
| UXF‑02‑01 | 1    | Home shows **Categories**, **Continue Listening**, **For You**.                                  |
| UXF‑02‑02 | 2    | User taps a card → Story Detail (cover, tags, length).                                           |
| UXF‑02‑03 | 3    | Taps **Play** → signed URL fetched, native `<audio>` element streams.                            |
| UXF‑02‑04 | 4    | `play.event` posted; PersonalizationAgent updates embeddings.                                    |

### 10.3 Story Creation (Parent / Creator)

| Ref      | Step | Description                                                                                      |
| -------- | ---- | ------------------------------------------------------------------------------------------------ |
| UXF‑03‑01 | 1    | Tap **Create** → Composer opens.                                                                 |
| UXF‑03‑02 | 2    | Enter title + story text; optional prompt for illustration.                                      |
| UXF‑03‑03 | 3    | Draft saved; QuotaAgent checks `story_quota`.                                                    |
| UXF‑03‑04 | 4    | Tap **Publish** → ModerationAgent; if approved, TTSAgent & IllustratorAgent run.                 |
| UXF‑03‑05 | 5    | Assets ready → push notification; story visible in My Stories.                                   |

### 10.4 Profile Management (Admin)

| Ref      | Step | Description                                                                                      |
| -------- | ---- | ------------------------------------------------------------------------------------------------ |
| UXF‑04‑01 | 1    | Admin opens **Profiles** tab.                                                                    |
| UXF‑04‑02 | 2    | Tap **New Profile** → clone or blank.                                                            |
| UXF‑04‑03 | 3    | Toggle permissions & quotas via JSON‑backed UI.                                                  |
| UXF‑04‑04 | 4    | Save emits audit event; changes propagate instantly.                                             |
| UXF‑04‑05 | 5    | Drag‑select users → **Assign to profile** for bulk update.                                       |


### 10.5 Story Assistant Flow

| Ref      | Step | Description                                                                                      |
| -------- | ---- | ------------------------------------------------------------------------------------------------ |
| UXF‑05‑01 | 1    | User taps **Story Assistant** → StoryCompanion chat interface opens.                             |
| UXF‑05‑02 | 2    | User chats with AI about story ideas; StoryCompanion suggests themes and characters.             |
| UXF‑05‑03 | 3    | Tap **Fill Details** → AI populates a structured form with title, plot, characters from chat.    |
| UXF‑05‑04 | 4    | Tap **Generate** → QuotaAgent checks limits; if approved, ModerationAgent, TTSAgent & IllustratorAgent run. |
| UXF‑05‑05 | 5    | Preview screen shows story with audio and images; user can **Edit** or **Save to Library**.      |

---

## 11. Technical Architecture

| Ref    | Component               | Implementation                                                                      |
| ------ | ----------------------- | ----------------------------------------------------------------------------------- |
| TEC‑01 | **Backend**             | Django + Django REST + PostgreSQL **(RLS enabled)**                                 |
| TEC‑02 | **Authentication**      | `django‑allauth` SSO + IDP linking via `UserIdentity`                              |
| TEC‑03 | **Permission System**   | Request loads `Profile.permissions` JSON once; quotas from `TenantPolicy`           |
| TEC‑04 | **Storage**             | MinIO/S3 prefixes per tenant                                                        |
| TEC‑05 | **Internationalization**| i18n library + Story.translate() agent; language selector in footer                 |

## 11.1 Mobile App Architecture & Strategy

To ensure an optimal experience across platforms, the application will follow a **PWA-first strategy** with the option to deliver **store-ready native wrappers**.

### Architecture Considerations

- **Progressive Web App (PWA)**: Core experience delivered as a responsive web app using Django templates + Bootstrap 5 + HTMX, designed to function offline via a service worker and manifest.
- **Capacitor Wrapping (Optional)**: Enables packaging the web app into installable native iOS and Android apps. This approach supports native APIs such as push notifications, media playback, and native sign-in dialogs.
- **SSO Integration**: Web-based SSO (Google, Apple) will be integrated using `django-allauth`. In Capacitor wrappers, native SSO flows may be embedded using Capacitor plugins.
- **Mobile Responsiveness**: Achieved through Bootstrap 5, ensuring family-friendly mobile UX with scalable text, tappable buttons, and low-load times.
- **Interactivity with HTMX**: Enables AJAX-style dynamic updates for search, filtering, and story playback, avoiding full page reloads.
- **Store Compliance**:

  - Offline functionality via service worker (Apple/Google requirement)
  - Avoids external browser redirections
  - GDPR and COPPA-compliant UX flows

### Developer Tools & Distribution

- **Build Tools**: Django for backend, Docker for deployment, Celery for background jobs
- **Distribution**: PWA install prompts + optional App Store / Play Store deployment through Capacitor build pipelines
- **Monitoring & Analytics**: Add PWA analytics compatible with privacy standards (e.g., Plausible or Matomo)

All frontends will follow a **single source of truth** using Django’s templating system and shared CSS/JS assets, reducing maintenance overhead and allowing synchronized feature releases between web and mobile.

---

## 12. APIs & Interfaces

| Ref    | Interface Type | Endpoints/Description                                      |
| ------ | -------------- | ---------------------------------------------------------- |
| API‑01 | **REST APIs**  | `/api/stories/`, `/api/stories/<id>/`                      |
| API‑02 |                | `/api/assets/`, `/api/agents/trigger/`                     |
| API‑03 | **Webhooks**   | For Celery job completion (story ready)                    |
| API‑04 | **Agent Bridge**| Internal API between Django + CrewAI layer                |
| API‑05 | **Story Export**| One-click MP3 + cover PNG bundle with YAML metadata; webhooks to third-party card manufacturers or Alexa skill |

---

## 13. Security & Access Control

| Ref    | Category               | Implementation                                                                      |
| ------ | ---------------------- | ----------------------------------------------------------------------------------- |
| SEC‑01 | **RBAC**               | Roles: Guest, Registered, Creator, Admin                                            |
| SEC‑02 | **Authentication**     | SSO via Google / Apple + token fallback                                             |
| SEC‑03 | **File Access**        | Signed URL for asset delivery                                                       |
| SEC‑04 | **Compliance**         | GDPR, COPPA; opt-in for data collection                                             |
| SEC‑05 | **Authorization**      | Permissions flow strictly via Profiles; no per‑user toggles                         |
| SEC‑06 | **Identity binding**   | `(issuer, subject)` uniqueness rule blocks cross‑tenant login                       |
| SEC‑07 | **Row‑level security** | Single‑column predicate keeps queries cheap & auditable                             |
| SEC‑08 | **Audit**              | Profile/policy changes and break‑glass actions streamed to immutable log bucket     |

---

## 14. AI Observability & Monitoring

| Ref    | Category                | Implementation                                                                      |
| ------ | ----------------------- | ----------------------------------------------------------------------------------- |
| OBS‑01 | **OpenTelemetry**       | Expose agent runs, tool calls, and LLM invocations as OpenTelemetry spans           |
| OBS‑02 | **Token Usage Tracking**| Monitor and log token consumption per model, tenant, and request                    |
| OBS‑03 | **Cost Monitoring**     | Track AI service costs with dashboards and alerts for budget thresholds             |
| OBS‑04 | **Performance Metrics** | Latency tracking for AI operations with percentile breakdowns                       |
| OBS‑05 | **Observability UI**    | Integration with Arize Phoenix for local development and testing                    |
| OBS‑06 | **Production Telemetry**| Langfuse integration for production environments with cost & latency charts         |
| OBS‑07 | **Agent Runs Analysis** | Session replays and side-by-side diffing of agent runs via AgentOps                 |
| OBS‑08 | **Fallback Monitoring** | Track fallback service usage and success rates                                      |
| OBS‑09 | **Audit Compliance**    | Ensure all AI operations are logged to immutable WORM storage for compliance        |

### 14.1 Observability Platform Integration

| Platform               | Use Case                                                          | Implementation Effort |
| ---------------------- | ----------------------------------------------------------------- | --------------------- |
| **Arize Phoenix**      | Local development, testing, embeddings visualization              | Low                   |
| **Langfuse + OpenLIT** | Production monitoring, cost tracking, prompt versioning           | Low-Medium            |
| **AgentOps**           | Agent run comparisons during development iterations               | Low                   |
| **Langtrace**          | Lightweight OSS-only tracing for environments with minimal overhead | Low                 |
| **OpenLIT**            | Stand-alone OTel backend with Grafana/Tempo integration           | Medium                |
| **MLflow**             | Integration with existing ML lifecycle management                 | Medium                |

All observability solutions will be implemented with privacy-first design, ensuring no PII or sensitive data is included in telemetry.

---

## 15. Admin Features

| Ref    | Feature                   | Description                                                |
| ------ | ------------------------- | ---------------------------------------------------------- |
| ADM‑01 | **Content Management**    | Admin CRUD on stories, users, tags, assets                 |
| ADM‑02 | **Task Monitoring**       | Status dashboard for Celery tasks + agent jobs             |
| ADM‑03 | **Moderation Tools**      | Manual moderation & content flagging tools                 |
| ADM‑04 | **Publishing Controls**   | Content preview & scheduling                               |
| ADM‑05 | **Insights**              | Per-profile & per-user charts: minutes played, stories finished, creations, comprehension quiz scores |

---

## 16. Go-To-Market Plan

| Ref    | Stage     | Tactics                                                                                                                 |
| ------ | --------- | ----------------------------------------------------------------------------------------------------------------------- |
| GTM‑01 | Beta      | 500 families via parenting newsletters, teachers, Facebook groups. Referral loop: 1 free premium story for each signup. |
| GTM‑02 | Launch    | App Store + Google Play + PWA, influencer storytelling packs, launch campaign with free 7-day premium.                  |
| GTM‑03 | B2B       | Outreach to daycare networks, family apps, and educational resellers. Embed IP licensing into discovery stories.        |
| GTM‑04 | Expansion | Localized editions (FR, ES, DE). Stories generated or curated per language.                                             |

---

## 17. Monetization & Business Model

| Ref    | Model                | Description                                                                           |
| ------ | -------------------- | ------------------------------------------------------------------------------------- |
| MON‑01 | **Freemium**         | Free tier (access to 5 rotating stories/week), Premium (€4.99/month) unlocks full access + unlimited creation |
| MON‑02 | **À-la-carte**       | Purchase option for special packs (e.g., bedtime, adventure, licensed IP)             |
| MON‑03 | **B2B licensing**    | Institutions pay per seat (€1–2/student/month) or flat fee                            |
| MON‑04 | **Future Revenue**   | Voice merchandising, branded stories, parental gifting                                |

---

## 18. Compliance & Safety

| Ref    | Area                    | Implementation                                                                      |
| ------ | ----------------------- | ----------------------------------------------------------------------------------- |
| CMP‑01 | **Certifications**      | Target GDPR, COPPA, and SECNUMCLOUD (ANSSI) certification                           |
| CMP‑02 | **Control Mapping**     | Explicit mapping of IS‑1 → IS‑5 controls to backlog epics (see Engineering doc)     |
| CMP‑03 | **Data Isolation**      | Isolation + traceability proofs via identity uniqueness & RLS                       |
| CMP‑04 | **Privacy & Safety**    | Full compliance with GDPR and COPPA. Parental consent flows. No child data stored   |
| CMP‑05 | **Content moderation**  | AI moderation agent + manual review fallback. Age-appropriate filters               |
| CMP‑06 | **Usage analytics**     | Anonymized tracking only. Explicit opt-in for suggestions                           |

---

## 19. App Store Compliance Strategy

| Ref    | Requirement                | Implementation                                                |
| ------ | -------------------------- | ------------------------------------------------------------ |
| ASC‑01 | **Offline Support**        | Service worker implementation for offline functionality       |
| ASC‑02 | **Mobile UI**              | Touch-optimized, responsive Bootstrap 5 UI                    |
| ASC‑03 | **Navigation**             | Native-like navigation with HTMX                              |
| ASC‑04 | **Native Features**        | Optional use of Capacitor plugins for notifications and media |
| ASC‑05 | **Browser Handling**       | No redirection to external browser                            |
| ASC‑06 | **Privacy Compliance**     | GDPR/COPPA consent and privacy policies embedded              |

---

## 20. Open Strategic Questions

1. Which regional launch first: France‑only vs multilingual?
2. Minimum licensing required for branded IP?
3. **Should we open a profile marketplace for shared templates?**
4. **Do institutional tenants need data residency beyond EU‑wide hosting?**
5. Should we prioritise mobile app downloads over PWA adoption?
6. Should we enable public sharing of user-created stories in Phase 1?

---

## 21. Next Steps (Pre‑Implementation)

| Area                       | Action Item                                                                         | Owner             |
| -------------------------- |-------------------------------------------------------------------------------------|-------------------|
| 🎯 **Market Sizing**       | TAM/SAM/SOM validation (family audio market)                                        | Strategy Lead     |
| 💸 **Pricing Simulation**  | Model CAC, conversion, LTV; test premium tiers                                      | Product + Finance |
| 📢 **GTM Assets**          | Prepare launch website, teaser video, social ads                                    | Marketing         |
| 🔐 **Compliance Audit**    | External review for GDPR/COPPA adherence; map PRD v0.4 controls to SECNUMCLOUD checklist; schedule external gap assessment | Legal + SecOps    |
| 🎨 **Voice Licensing**     | Secure license or verify open use for voice/music assets                            | BizDev            |
| 📦 **MVP Tech Stack POC**  | Validate Celery + CrewAI orchestration + fallback; validate Profile & RLS scaffold with sample load test | Engineering       |
| 📱 **Mobile UX Prototype** | Test story discovery + generation with real families                                | Engineering       |
