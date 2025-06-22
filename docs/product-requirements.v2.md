# Product Requirements Document (PRD) - V2

## 1. Document Control

| **Product**   | Talemo - French Audio-Stories Platform (MVP)     |
| ------------- | ------------------------------------------------- |
| **Author**    | Product Team / CTO                                |
| **Date**      | Updated based on VC feedback                      |
| **Reviewers** | Engineering · Design · Marketing · Legal · SecOps |

---

## 2. Executive Summary

**Talemo turns screen-time into shared audio imagination.**  

It is a mobile-first platform where French families can **discover, listen to, and co-create short audio stories**—all inside a lightning-fast Progressive Web App that works on any phone or tablet.

### Focused MVP Scope (4-Month Delivery)

Based on market feedback, we're narrowing our initial release to three core capabilities:

1. **AI Story Builder** - Intuitive interface for creating personalized audio stories with AI assistance
2. **Dark-Screen Playback** - Screen-free listening mode that addresses the "moins d'écrans" parental concern
3. **Record-Your-Own** - Ability for families to record their own narration, creating an emotional connection

This focused approach allows us to:
- Launch a compelling product within 4 months
- Validate core user behaviors and retention metrics
- Establish an institutional foothold with French schools
- Control costs while building toward unit economic sustainability

### What makes Talemo different

#### Where it delights
- **Instant joy** — three taps from home-screen to playback keep "time-to-first-play" under 30 seconds, so parents can calm a restless child fast.  
- **Kids become storytellers** — an intuitive composer plus AI agents (voice, illustration, story coaching) lets children craft narrated tales in minutes, turning them from passive consumers into creators.  
- **« Mode Conte »** — our screen-free listening mode supports the « moins d'écrans » movement, giving parents audio-only benefits without extra hardware.

#### How it wins
- **Multi-tenant privacy by design** — every household or institution is its own secure silo, enforced down to row-level security and tenant-scoped storage.  
- **100% données hébergées en France** — all user data exclusively hosted in France with SecNumCloud certification, exceeding CNIL requirements for children's privacy.
- **Authentic French content** — native French voice packs with regional accents and focus on culturally relevant stories.

**The outcome:** Talemo delivers wholesome, interactive audio experiences that strengthen family bonds, empower young voices, and give educators a safe, ready-made storytelling lab—while meeting the strict governance and compliance standards that modern digital learning demands.

---

## 3. Goals & Non-Goals

### 3.1 Goals

1. Deliver an intuitive, mobile-first experience for families to **discover** and **listen** to audio stories.
2. Provide creators/admins a workflow to **generate new stories** (text → audio + illustration) via CrewAI.
3. Implement **record-your-own narration** capability for personalized storytelling.
4. Ensure **dark-screen playback mode** for screen-free listening experience.
5. Focus exclusively on **French language** content and UI for initial release.
6. Implement **enterprise authentication** with Google and Apple SSO.
7. **Provide strict multi-tenant governance** so each family or institution is a logical silo.
8. Prepare for a **freemium subscription model**, B2B licensing, and future IP partnerships.
9. Achieve **€0.03 per story generation cost** through optimization roadmap.
10. Secure at least one **institutional pilot** with a French académie or UGAP-eligible reseller.

### 3.2 Non-Goals for MVP

- Full public social features (likes, comments) — deferred.
- Native desktop app — focus is mobile PWA + optional wrappers.
- Multi-language support — French-only for initial release.
- Advanced gamification features — basic engagement only for MVP.
- Hardware export capabilities — focus on software experience first.
- Complex branching stories — linear narratives only for MVP.
- Teacher analytics dashboard — basic usage stats only for MVP.
- Voice commands — touch-based interface for initial release.

---

## 4. Success Metrics

| Metric                                 | Target                         | Rationale                                                |
| -------------------------------------- | ------------------------------ | -------------------------------------------------------- |
| 🟢 **D30 Retention**                   | ≥ 35%                          | Key VC requirement showing product stickiness            |
| 🟢 **Stories Created Per Child/Week**  | ≥ 3                            | Key VC requirement showing engagement                    |
| 🟢 **Time-to-First-Play** (new user)   | < 30 s                         | Critical for parent satisfaction and quick adoption      |
| 🟢 **Story Generation Lead Time**      | ≤ 2 min (submit → audio ready) | User experience requirement for creation flow            |
| 🟢 **Mobile PWA Lighthouse Perf**      | ≥ 85                           | Technical performance requirement                         |
| 🟢 **Customer Acquisition Cost (CAC)** | ≤ €12                          | Adjusted based on VC feedback (up from €6)               |
| 🟢 **LTV / CAC Ratio**                 | ≥ 3.0 ×                        | Business sustainability metric                           |
| 🟢 **Cost Per Story Generation**       | ≤ €0.03 (roadmap)              | Key VC requirement for unit economics                    |
| 🟢 **Institutional ARR**               | ≥ €50k (signed LOI)            | Key VC requirement for anchor pilot                      |

---

## 5. Competitive Landscape — French Market Focus

### French Market Competitive Analysis

As France will be our exclusive initial market, we've conducted a detailed competitive analysis of the French audio storytelling landscape:

#### 1. Home-turf Frontrunners to Study—and Out-flank

| Player | Core Offer (FR market) | Why It's a Real Threat | Counters & Gaps Talemo Can Exploit |
| ------ | ---------------------- | ---------------------- | ---------------------------------- |
| **Lunii – Ma Fabrique à Histoires** | - 1.5 M+ devices sold, big retail footprint in FNAC, Boulanger.<br>- Kids "mix & match" story elements on a screen-free box; 450+ French audiobooks. | • Brand already shorthand for "conteuse" in France.<br>• €59-79 price point is a one-time purchase vs. subscription. | • Lunii is hardware-bound and single-profile; no cloud collaboration.<br>• Pitch Talemo as "tout-en-un app"—create, share, listen anywhere, no extra gadget. |
| **Sybel Kids** | Mobile app & web with hundreds of kids podcasts and audiobooks in French; strong licensing ties with Bayard, Radio France. | • Pure-software, freemium, already sits on parents' phones.<br>• Only €0.55M ARR after 5 years shows slow growth. | • Sybel is listen-only: zero story-creation or classroom tenancy.<br>• Lean on Talemo's AI composer + institution dashboards. |
| **Bookinou** | €69 NFC "badge" reader that lets families record their own voice per physical book; endorsed by Éducation Nationale pilots. | • Deep emotional appeal ("Papa lit l'histoire").<br>• School partnerships give them early-childhood mind-share. | • Requires the printed book + tag; no original stories, no streaming catalogue.<br>• Talemo can match the "record-your-own" angle without extra hardware. |

#### 2. Regulatory & Perception Checkpoints Specific to France

| Concern | Why It Matters | Our Approach |
| ------- | -------------- | ------------ |
| **CNIL & RGPD for minors** | French watchdog CNIL applies a higher bar on transparency and parental consent for <15 y.o. users. | Implement SECNUMCLOUD hosting; make sure onboarding collects explicit parental consent and offers a closed local-processing option for voice recordings. |
| **"Zéro écran" narrative** | French parent groups and mainstream press often praise screen-free devices like Lunii, Bookinou, Mon Petit Morphée. | Talemo's PWA needs a clear "audio-first, minimal-screen" story with dark screen mode and lock-screen playback as core features. |
| **Education procurement** | Many primary schools buy via UGAP and look for tools déjà labellisés by Éduthèque or La Maison de la Pédagogie Numérique. | Early pilots with two or three académies will help establish credibility. |

### French Market Value Proposition

For our French launch, we will emphasize these three key angles in all press briefings, app-store copy, and sales decks:

| Key Angle | Why It Resonates in France | How We'll Integrate It |
| ------------------ | -------------------------- | ---------------------- |
| **1. « Moins d'écrans » pledge** | Screen-free devices like Lunii dominate retail because French parent groups and media push zéro écran for < 6-year-olds. | **« Mode Conte »** - A dark-screen/lock-mode that blanks the display after one tap and keeps audio controls on the lock-screen, allowing parents to enjoy audio-only benefits without buying hardware. |
| **2. 100% données hébergées en France** | Sovereign-cloud and data-localization concerns are louder in France; CNIL insists on explicit consent for < 15 y.o. users. | Make French hosting & SecNumCloud compliance a headline: **"Vos histoires, vos données, hébergées exclusivement en France."** Include a parental-consent wizard that explicitly references CNIL guidelines. |
| **3. Record-Your-Own Narration** | French families value the emotional connection of parent-narrated stories, as evidenced by Bookinou's success. | Highlight the ability to record personal narrations for any story, creating a digital equivalent to "Papa lit l'histoire" without requiring additional hardware. |

---

## 6. Personas & Use Cases

| Persona                   | Description                                                                      |
| ------------------------- | -------------------------------------------------------------------------------- |
| **Family Administrator**  | Creates a household tenant, invites parents & children, manages profiles.        |
| **Institution Admin**     | Librarian/teacher controlling an organisation tenant.                            |
| **Parent (Amélie, 38)**   | Browses bedtime stories on phone, filters by length/theme.                       |
| **Child (Léo, 8)**        | Taps colourful card, plays story, creates own stories with assistance.           |
| **Story Creator (Lucas)** | Writes text, triggers AI asset generation, records own narration.                |

### Core User Journeys (MVP)

1. **Story Discovery & Playback**
   - Parent browses story library
   - Selects story based on theme/length
   - Activates dark-screen mode
   - Child listens to story

2. **Story Creation**
   - Child/parent selects "Create Story"
   - Enters basic story elements (characters, setting)
   - AI generates complete story
   - Reviews and publishes to family library

3. **Record-Your-Own Narration**
   - Select existing story
   - Choose "Record My Voice"
   - Record narration following text prompts
   - Save as alternative audio track

4. **Institutional Setup**
   - Teacher creates institution account
   - Sets up class profiles
   - Invites students
   - Manages story access

---

## 7. Functional Requirements

### 7.1 Core Experience (MVP Focus)

| Ref    | Feature                | Description                                                                        | Priority |
| ------ | ---------------------- | ---------------------------------------------------------------------------------- | -------- |
| COR-01 | **Story List**         | Browsable, filterable list of available stories                                    | P0       |
| COR-02 | **Story Detail**       | Individual story view with metadata and playback controls                          | P0       |
| COR-03 | **Story Creation**     | Interface for creating and editing stories                                         | P0       |
| COR-04 | **Agentic Assistant**  | AI-powered assistant for story creation                                            | P0       |
| COR-05 | **Admin Dashboard**    | Basic management interface for content and users                                   | P0       |
| COR-06 | **SSO**                | Single sign-on integration with Google and Apple                                   | P0       |
| COR-07 | **Voice-Over Mode**    | Mobile mic recording, waveform trim, stored as alternate audio track               | P0       |
| COR-08 | **« Mode Conte »**     | Dark-screen/lock-mode that blanks display after one tap, keeps audio controls on lock-screen | P0 |
| COR-09 | **French Voices**      | Native French voice packs with Parisian and regional accents                       | P0       |
| COR-10 | **Data Residency Controls** | User-selectable data storage location with French hosting option; CNIL-compliant consent | P0 |
| COR-11 | **Offline Story Packs** | Downloadable content for offline use in cars, rural areas, and travel scenarios    | P1       |
| COR-12 | **ENT/Pronote SSO**    | CAS/SAML single sign-on integration with French school platforms                   | P1       |

### 7.2 Governance & Multi-Tenancy

| Ref    | Requirement                                                                                                 | Priority |
| ------ | ----------------------------------------------------------------------------------------------------------- | -------- |
| GOV-01 | **Tenant bootstrap** – users are created only via invitation tokens embedding `tenant_id`; no orphan users. | P0       |
| GOV-02 | **Profile catalogue** – tenant admins create/clone/delete permission profiles (e.g., *Kids Listen-Only*).   | P0       |
| GOV-03 | **Identity uniqueness** – composite DB constraint `(idp_issuer, idp_subject)` is globally unique.           | P0       |
| GOV-04 | **Tenant-wide feature flags / quotas** – `TenantPolicy` KV store (e.g., `story_quota = 50`).               | P0       |
| GOV-05 | **Row-level security** – every tenant-bound table enforces `tenant_id = current_setting('app.tenant')`.     | P0       |

---

## 8. Agent Architecture (Streamlined for MVP)

The platform runs a focused suite of stateless **CrewAI** agents orchestrated by Celery. Each agent receives a tenant-scoped message, performs one atomic task, emits an event for the next stage, and writes an audit trace for SECNUMCLOUD.

| Ref    | Agent                    | Purpose                                                                          | Consumes → Produces                                |
| ------ | ------------------------ | -------------------------------------------------------------------------------- | -------------------------------------------------- |
| AGT-01 | **ModerationAgent**      | Runs GPT-4 based moderation & keyword heuristics; flags disallowed content.      | `story.draft` → `story.approved` / `story.flagged` |
| AGT-02 | **TTSAgent**             | Synthesises speech via tenant-selected voice pack; stores `.mp3` in MinIO.       | `story.approved` → `asset.audio.ready`             |
| AGT-03 | **IllustratorAgent**     | Generates cover art (Stable Diffusion XL); stores `.png` under tenant prefix.    | `story.approved` → `asset.image.ready`             |
| AGT-04 | **QuotaAgent**           | Enforces `TenantPolicy.story_quota`; blocks over-limit creations.                | `story.request`                                    |

### User-facing Agents

| Ref       | Agent                | Purpose                                                |
| --------- | -------------------- | ------------------------------------------------------ |
| AGT-UF-01 | **StoryCompanion**   | Co-creation chat assistant for families                |

---

## 9. Cost Control Roadmap

To achieve our target of €0.03 per story generation, we will implement the following optimizations:

### 9.1 Model & Voice Caching

| Phase | Optimization | Impact | Timeline |
|-------|--------------|--------|----------|
| 1 | Implement aggressive caching of TTS outputs for common phrases | 15-20% reduction in TTS costs | Month 1 |
| 2 | Create a library of pre-generated voice clips for story templates | Additional 10-15% reduction | Month 2 |
| 3 | Develop voice fingerprinting to avoid regenerating similar audio | Additional 10% reduction | Month 3 |

### 9.2 Local Inference

| Phase | Optimization | Impact | Timeline |
|-------|--------------|--------|----------|
| 1 | Research and select lightweight TTS models for on-device inference | Planning only | Month 1-2 |
| 2 | Implement client-side TTS for select devices with sufficient capabilities | 30-40% reduction in cloud TTS costs | Month 3-4 |
| 3 | Develop hybrid approach with on-device generation for common content | Additional 10-15% reduction | Post-MVP |

### 9.3 Model Optimization

| Phase | Optimization | Impact | Timeline |
|-------|--------------|--------|----------|
| 1 | Fine-tune smaller LLMs specifically for children's story generation | 20-30% reduction in LLM costs | Month 2-3 |
| 2 | Implement prompt optimization techniques to reduce token usage | 10-15% reduction | Month 1 |
| 3 | Create story templates that require minimal LLM customization | 15-20% reduction | Month 2 |

### 9.4 Cost Reduction Projection

| Timeline | Cost Per Story | Optimization Methods |
|----------|----------------|----------------------|
| Launch | €0.09-0.12 | Baseline with standard cloud APIs |
| Month 1 | €0.07-0.09 | Prompt optimization + basic caching |
| Month 2 | €0.05-0.07 | Template system + voice clip library |
| Month 3 | €0.04-0.05 | Fine-tuned models + voice fingerprinting |
| Month 4-6 | €0.03 | Client-side inference + hybrid approach |

---

## 10. Go-To-Market Plan

### 10.1 France-First Strategy

Talemo will launch exclusively in the French market, leveraging our competitive analysis and addressing the specific needs of French families and educational institutions.

| Ref    | Stage     | Tactics                                                                                                                 |
| ------ | --------- | ----------------------------------------------------------------------------------------------------------------------- |
| GTM-01 | Beta      | 100 French families via parenting newsletters and Facebook groups. Referral loop: 1 free premium story for each signup. Focus on gathering retention and usage data. |
| GTM-02 | Launch    | App Store + Google Play + PWA with French-first UI/UX, French influencer storytelling packs, launch campaign with free 7-day premium. Highlight "audio-first, minimal-screen" messaging to address "Zéro écran" concerns. |
| GTM-03 | B2B       | Outreach to 3-5 académies for pilot programs. Target signing at least one UGAP-eligible reseller worth ≥ €50k ARR. |

### 10.2 Institutional Pilot Strategy

To secure our anchor pilot worth ≥ €50k ARR, we will:

1. **Target Selection**
   - Identify 3-5 académies with existing digital initiatives
   - Research UGAP-eligible resellers with education focus
   - Prioritize institutions with "moins d'écrans" initiatives

2. **Pilot Program Structure**
   - 3-month free pilot with 2-3 classrooms per institution
   - Provide teacher training and support materials
   - Collect usage data and testimonials
   - Present clear ROI for full implementation

3. **Conversion to Paid**
   - Develop case studies from pilot data
   - Create tiered pricing model for institutions
   - Secure Letter of Intent (LOI) for full deployment
   - Establish path to UGAP catalog inclusion

---

## 11. Monetization & Business Model

| Ref    | Model                | Description                                                                           |
| ------ | -------------------- | ------------------------------------------------------------------------------------- |
| MON-01 | **Freemium**         | Free tier (access to 5 rotating stories/week), Premium (€4.99/month) unlocks full access + unlimited creation |
| MON-02 | **B2B licensing**    | Institutions pay per seat (€1–2/student/month) or flat fee                            |

### 11.1 Unit Economics

| Metric | Target | Strategy |
|--------|--------|----------|
| ARPU | €4.99 (consumer) / €1-2 (B2B per seat) | Freemium model with clear value proposition for premium features |
| CAC | ≤ €12 | Focused marketing in French parenting channels + referral program |
| LTV | ≥ €36 | Target 7+ month retention for premium subscribers |
| Gross Margin | > 50% after AI costs | Implement cost control roadmap to reach €0.03/story |

---

## 12. Exit Narratives

### 12.1 Strategic Acquisition Paths (3-5 Year Horizon)

| Potential Acquirer | Strategic Fit | Path to Acquisition |
|-------------------|---------------|---------------------|
| **Yoto** | - Talemo provides content creation capabilities Yoto lacks<br>- Our French market presence complements their UK/US strength<br>- Our software platform enhances their hardware ecosystem | 1. Establish content syndication partnership<br>2. Integrate Talemo stories with Yoto cards<br>3. Demonstrate strong French market traction<br>4. Position as their software/content arm |
| **Bayard** | - Major French children's publisher seeking digital transformation<br>- Our platform extends their IP to interactive audio<br>- Complements their existing educational offerings | 1. Secure content licensing deal<br>2. Co-develop exclusive French stories<br>3. Integrate with their school distribution channels<br>4. Demonstrate technology advantage over competitors |
| **Spotify Kids** | - Our creation tools fill gap in their consumption-only model<br>- French-first approach complements their global reach<br>- Our education features extend their consumer focus | 1. Build user base with strong retention metrics<br>2. Develop API for potential integration<br>3. Demonstrate unique engagement vs. passive listening<br>4. Position as their "creation studio" for kids content |

### 12.2 Key Metrics for Acquisition Attractiveness

| Metric | Target | Rationale |
|--------|--------|-----------|
| Monthly Active Users | 100,000+ | Demonstrates product-market fit and scalability |
| D30 Retention | > 35% | Shows strong user engagement and product stickiness |
| Stories Created | > 1M | Proves content generation capability and user adoption |
| Institutional Customers | 50+ | Validates B2B model and education market fit |
| ARR | €1-2M | Shows revenue traction and business model validation |
| French Market Share | 15%+ | Establishes leadership in initial market |

---

## 13. Development Roadmap

### 13.1 4-Month MVP Timeline

| Month | Focus | Key Deliverables |
|-------|-------|------------------|
| **Month 1** | Core Infrastructure | - Multi-tenant architecture with RLS<br>- Basic authentication and profile system<br>- Initial story playback functionality |
| **Month 2** | Story Creation | - AI story generation workflow<br>- French voice integration<br>- Basic moderation system |
| **Month 3** | Key Features | - Record-your-own functionality<br>- Dark-screen mode implementation<br>- Offline capabilities |
| **Month 4** | Polish & Launch | - Performance optimization<br>- Final UI/UX refinement<br>- App store submission<br>- Beta testing with initial users |

### 13.2 Post-MVP Priorities

1. Enhanced analytics for retention optimization
2. Institutional dashboard for schools
3. Additional cost optimization implementations
4. Content partnerships with French publishers
5. Expanded creation tools and templates
