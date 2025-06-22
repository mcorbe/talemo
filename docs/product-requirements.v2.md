# Product Requirements Document (PRD)

## 1. Document Control

| **Product**   | Talemo - French Audio-Stories Platform (MVP)     |
| ------------- | ------------------------------------------------- |
| **Author**    | Product Team / CTO                                |
| **Reviewers** | Engineering · Design · Marketing · Legal · SecOps |

---

## 2. Executive Summary

**Talemo turns screen-time into shared audio imagination.**  

It is a mobile-first platform where French families can **discover, listen to, and co-create short audio stories**—all inside a lightning-fast Progressive Web App that works on any phone or tablet.

### Focused MVP Scope (4-Month Delivery)

Our initial release focuses on three core capabilities with an exclusive focus on AI-generated content:

1. **AI Story Builder** - Intuitive interface for creating personalized audio stories with AI assistance
2. **Dark-Screen Playback** - Screen-free listening mode that addresses the "moins d'écrans" parental concern
3. **Record-Your-Own** - Ability for families to record their own narration for AI-generated stories

At launch, we will solely focus on AI-generated story content without any pre-existing catalog. This approach allows us to prove that AI-generated content works for parents and kids before potentially adding licensed content in the future.

We're targeting the 6-8 year old "creative kids" segment as our primary audience, as they can self-serve creation flows while still benefiting from parental guidance.

This focused approach allows us to:
- Launch a compelling product within 4 months
- Validate core user behaviors and retention metrics
- Build a strong foundation with French families with children under 10
- Control costs while building toward unit economic sustainability
- Pursue hardware partnerships rather than competing head-on

### What makes Talemo different

#### Where it delights
- **Instant joy** — three taps from home-screen to playback keep "time-to-first-play" under 30 seconds, so parents can calm a restless child fast.  
- **Kids become storytellers** — an intuitive composer plus AI agents (voice, illustration, story coaching) lets children craft narrated tales in minutes, turning them from passive consumers into creators.  
- **« Mode Conte »** — our screen-free listening mode supports the « moins d'écrans » movement, giving parents audio-only benefits without extra hardware.

#### How it wins
- **Multi-tenant privacy by design** — every household is its own secure silo, enforced down to row-level security and tenant-scoped storage (with architecture ready for future expansion).  
- **100% données hébergées en France** — all user data exclusively hosted in France with SecNumCloud certification, exceeding CNIL requirements for children's privacy.
- **Authentic French AI-generated content** — native French voice packs with regional accents for generating culturally relevant stories.

**The outcome:** Talemo delivers wholesome, interactive audio experiences that strengthen family bonds and empower young voices—while meeting the strict governance and compliance standards that modern digital privacy demands.

---

## 3. Goals & Non-Goals

### 3.1 Goals

1. Deliver an intuitive, mobile-first experience for families to **discover** and **listen** to audio stories.
2. Provide parents a workflow to **generate new stories** (text → audio + illustration) via CrewAI.
3. Implement **record-your-own narration** capability for personalized family storytelling.
4. Ensure **dark-screen playback mode** for screen-free listening experience.
5. Focus exclusively on **French language** content and UI for initial release.
6. Implement **authentication** with Google and Apple SSO for parents.
7. **Provide strict multi-tenant governance** with family-focused household silos (architecture ready for future expansion).
8. Prepare for a **freemium model with one-time purchases and subscriptions** targeting parents.
9. Achieve **€0.03 per story generation cost** through optimization roadmap.

### 3.2 Non-Goals for MVP

- **Institutional features** (schools, libraries) — not on direct roadmap, parent-first focus.
- Full public social features (likes, comments) — deferred.
- Native desktop app — focus is mobile PWA + optional wrappers.
- Multi-language support — French-only for initial release.
- Advanced gamification features — basic engagement only for MVP.
- Hardware export capabilities — focus on software experience first.
- Complex branching stories — linear narratives only for MVP.
- Voice commands — touch-based interface for initial release.

---

## 4. Success Metrics

| Metric                                 | Target                         | Rationale                                                |
| -------------------------------------- | ------------------------------ | -------------------------------------------------------- |
| 🟢 **D30 Retention**                   | ≥ 35%                          | Critical metric showing product stickiness                |
| 🟢 **Stories Created Per Child/Week**  | ≥ 3                            | Key engagement metric for user activity                   |
| 🟢 **Time-to-First-Play** (new user)   | < 30 s                         | Critical for parent satisfaction and quick adoption       |
| 🟢 **Story Generation Lead Time**      | ≤ 2 min (submit → audio ready) | User experience requirement for creation flow             |
| 🟢 **Mobile PWA Lighthouse Perf**      | ≥ 85                           | Technical performance requirement                         |
| 🟢 **Customer Acquisition Cost (CAC)** | ≤ €12                          | Target for sustainable user acquisition                   |
| 🟢 **LTV / CAC Ratio**                 | ≥ 3.0 ×                        | Business sustainability metric                            |
| 🟢 **Cost Per Story Generation**       | ≤ €0.03 (by Month 6)           | Target for unit economics viability (see §11.4 for progression) |
| 🟢 **Paying Subscribers**              | ≥ 5,000 in 6 months (interim); 27,000 for €1.4M ARR | Demonstrates consumer willingness to pay; aligns with §11.3 creator-led model |

---

## 5. Competitive Landscape — French Market Focus

### French Market Competitive Analysis

As France will be our exclusive initial market, we've conducted a detailed competitive analysis of the French audio storytelling landscape:

#### 1. Home-turf Frontrunners to Study—and Out-flank

| Player | Core Offer (FR market) | Why It's a Real Threat | Counters & Gaps Talemo Can Exploit |
| ------ | ---------------------- | ---------------------- | ---------------------------------- |
| **Lunii – Ma Fabrique à Histoires** | - 1.5 M+ devices sold, big retail footprint in FNAC, Boulanger.<br>- Kids "mix & match" story elements on a screen-free box; 450+ French audiobooks. | • Brand already shorthand for "conteuse" in France.<br>• €59-79 price point is a one-time purchase vs. subscription. | • Lunii is hardware-bound and single-profile; no cloud collaboration.<br>• Pitch Talemo as "tout-en-un app"—create, share, listen anywhere, no extra gadget. |
| **Sybel Kids** | Mobile app & web with hundreds of kids podcasts and audiobooks in French; strong licensing ties with Bayard, Radio France. | • Pure-software, freemium, already sits on parents' phones.<br>• Only €0.55M ARR after 5 years shows slow growth. | • Sybel is listen-only: zero story-creation capabilities.<br>• Lean on Talemo's AI composer + family-friendly features. |
| **Bookinou** | €69 NFC "badge" reader that lets families record their own voice per physical book. | • Deep emotional appeal ("Papa lit l'histoire").<br>• Strong brand recognition among French parents. | • Requires the printed book + tag; no original stories, no streaming catalogue.<br>• Talemo can match the "record-your-own" angle without extra hardware. |

#### 2. Regulatory & Perception Checkpoints Specific to France

| Concern | Why It Matters | Our Approach |
| ------- | -------------- | ------------ |
| **CNIL & RGPD for minors** | French watchdog CNIL applies a higher bar on transparency and parental consent for <15 y.o. users. | Implement SECNUMCLOUD hosting; make sure onboarding collects explicit parental consent and offers a closed local-processing option for voice recordings. |
| **"Zéro écran" narrative** | French parent groups and mainstream press often praise screen-free devices like Lunii, Bookinou, Mon Petit Morphée. | Talemo's PWA needs a clear "audio-first, minimal-screen" story with dark screen mode and lock-screen playback as core features. |
| **Parental Control Expectations** | French parents expect robust controls over children's digital experiences. | Implement comprehensive parental controls including content filters, usage limits, and activity reporting. |

### French Market Value Proposition

For our French launch, we will emphasize these three key angles in all press briefings, app-store copy, and sales decks:

| Key Angle | Why It Resonates in France | How We'll Integrate It |
| ------------------ | -------------------------- | ---------------------- |
| **1. « Moins d'écrans » pledge** | Screen-free devices like Lunii dominate retail because French parent groups and media push zéro écran for < 6-year-olds. | **« Mode Conte »** - A dark-screen/lock-mode that blanks the display after one tap and keeps audio controls on the lock-screen, allowing parents to enjoy audio-only benefits without buying hardware. |
| **2. 100% données hébergées en France** | Sovereign-cloud and data-localization concerns are louder in France; CNIL insists on explicit consent for < 15 y.o. users. | Make French hosting & SecNumCloud compliance a headline: **"Vos histoires, vos données, hébergées exclusivement en France."** Include a parental-consent wizard that explicitly references CNIL guidelines. |
| **3. Record-Your-Own Narration** | French families value the emotional connection of parent-narrated stories, as evidenced by Bookinou's success. | Highlight the ability to record personal narrations for any story, creating a digital equivalent to "Papa lit l'histoire" without requiring additional hardware. |

---

## 6. Addressable Market Analysis

> **Note:** This section presents an earlier model with higher MAU requirements (e.g., 700K French MAU) and is kept for reference. The current creator-led monetization strategy in §11 succeeds with significantly lower MAU (180K) due to higher ARPU from subscriptions.

### 6.1 Target Market: Families with Children Under 10

Our refined target audience is families with at least one child under 10 years old. This focus allows us to address the most relevant audience for children's audio stories while providing more accurate market sizing.

To calculate this market segment, we combined two official sources:
1. Population by five-year age-bands (0-4 and 5-9) from Eurostat/World-Bank
2. Average number of children per family with minors from Eurostat "Children and family" 2023 (≈1.7 children/household EU-wide)

Using the formula: Families<10 = (children(0-4) + children(5-9)) ÷ 1.7 kids/family

#### European Market Size by Country (Families with Child <10)

| Country | Families with Child <10 ('000) |
|---------|-------------------------------|
| 🇫🇷 France | 4,300 |
| 🇬🇧 UK | 4,700 |
| 🇩🇪 Germany | 5,000 |
| 🇪🇸 Spain | 2,650 |
| 🇮🇹 Italy | 3,050 |
| 🇳🇱 Netherlands | 1,160 |
| 🇸🇪 Sweden | 730 |
| 🇧🇪 Belgium | 800 |
| 🇦🇹 Austria | 540 |
| 🇵🇱 Poland | 2,380 |

For France specifically: 0-4 yrs = 3.45M, 5-9 yrs = 3.89M ⇒ 7.34M children < 10 ÷ 1.7 ≈ 4.3 million families with at least one child < 10.

### 6.2 Baseline Reach Required for €6M ARR (€2M France + €4M Rest of Europe)

Our business goal is to achieve €2M ARR in France plus an additional €4M ARR across the rest of Europe (EU-9). Using our pricing model (€5 one-time consumer tier + €1/mo creative tier) with the unchanged blended ARPU of €2.87:

#### 6.2.1 France (€2M ARR)

France still needs ≈700K active families:

| Country | Families < 10 yrs | Families needed | Penetration |
|---------|-------------------|----------------|-------------|
| 🇫🇷 France | ≈4.3M | ≈700K | 16% |

With our current conversion goals, we need to activate approximately one family in six with children under 10 in France to reach our €2M ARR target.

#### 6.2.2 How many families for €4M ARR in the rest of Europe?

If we naïvely used the French ARPU (€2.87) everywhere, we would need:
€4,000,000 ÷ €2.87 ≈ 1.39M families

However, by weighting each country's own blended ARPU (higher eCPM lifts ARPU, so fewer families are required):

| Country (EU-9) | Blended ARPU (€) | Families < 10 yrs ('000) | Families to hit plan | % of local families |
|----------------|------------------|--------------------------|----------------------|---------------------|
| 🇬🇧 UK | 4.11 | 4,700 | 308K | 6.6% |
| 🇩🇪 DE | 3.28 | 5,000 | 308K | 6.2% |
| 🇪🇸 ES | 2.70 | 2,650 | 194K | 7.3% |
| 🇮🇹 IT | 2.70 | 3,050 | 194K | 6.4% |
| 🇵🇱 PL | 2.28 | 2,380 | 106K | 4.4% |
| 🇳🇱 NL | 3.03 | 1,160 | 40K | 3.4% |
| 🇸🇪 SE | 3.61 | 730 | 40K | 5.4% |
| 🇧🇪 BE | 2.95 | 800 | 40K | 5.0% |
| 🇦🇹 AT | 3.03 | 540 | 18K | 3.3% |
| EU-9 subtotal | — | — | ≈1,248K | — |

Total families required outside France: ≈1.25 million (not 1.39M) — a 10% buffer kept in.

Penetration ask is ≤8% in every market, dramatically less than the 16% needed for France.

#### 6.2.3 Revenue check

Σ (Families × ARPU) = €4,000K (UK 1.27M€ + DE 1.01M€ + … + AT 0.05M€) ✓

We still clear the €4M goal with a ≈€10K head-room.

#### 6.2.4 How this rolls up to the full plan

| Region | Families active | ARR (€) | Share of total ARR |
|--------|----------------|---------|-------------------|
| 🇫🇷 France | 700K | 2M | 33% |
| 🇪🇺 EU-9 combined | 1,246K | 4M | 67% |
| 🇪🇺 Pan-EU total | 1.95M | €6M | 100% |

≈2 million monthly-active families → ≈6 million cumulative installs (assumes 35% D30 retention).

### 6.3 Market Viability Analysis

Based on the penetration rates required, we can categorize markets into three tiers:

#### Realistic Phase-1/2 Markets
**France, UK, Germany**: Need 10-16% of families with <10 y.o. kids ⇒ challenging but plausible with paid UA + virality.

#### Southern Europe & Poland
**Spain, Italy, Poland**: Viable only if you raise the paid-tier mix or secure low-CAC channels (telcos, partnerships).

#### Small/High-CPM Markets
**Netherlands, Sweden, Belgium, Austria**: Even excellent CPMs cannot offset tiny bases; you would need 50-80% household penetration — treat them as incremental revenue, not €2M pillars.

### 6.4 Penetration Hurdle Reduction Strategies

| Lever | Effect |
|-------|--------|
| Lift premium attach 5% → 8% | Required families ↓ ~12% across all countries |
| Lift creative attach 2.5% → 4% | Families ↓ ~14% |
| Upsell "unlimited creative" at €3.99 to 1% of actives | Adds €0.40 to blended ARPU → families target ↓ ~7% |
| Secure €2.5+ CPM (contextual video) in DE/NL/SE | Families target ↓ 5-10% in those markets |
| OEM or school bundles giving 10% no-CAC installs | Every 100K zero-CAC families saves ≈ €180K UA budget |

### 6.5 Operational Takeaways

#### 6.5.1 What changes operationally

**User-acquisition budget**
At €1.80 cost-per-install the extra 1.25M families abroad translate to ≈3.6M installs → ≈€6.5M gross UA over three years (net cost lower after organic/referrals).

**Penetration realism**
The highest single-country hurdle is UK/DE at ~6-7% of families < 10; Spain/Italy at below 8%.
➜ Still well inside typical kids-app reach benchmarks (Lunii box ≈9% after 8 years).

**Price-mix upside**
Any uptick (e.g., 8% premium attach or 4% creative) cuts the required families by ~15%.

#### 6.5.2 Sequencing stays intact

1. **Phase A – France**: prove 700K MAU & funnel
2. **Phase B – UK + DE**: 600K families → €2.3M ARR
3. **Phase C – ES + IT**: 390K families → +€1.1M
4. **Phase D – PL + NL + SE + BE + AT**: 250K families → +€0.6M

#### 6.5.3 Take-away

1. **France**: 700K monthly-active families (16% of the <10 market) still delivers €2M.

2. **Rest of Europe**: a further 1.25M actives spread over nine markets, each at <8% penetration, yields the additional €4M ARR.

3. **Total footprint**: ≈2M MAU across Europe, sustaining a lean, €6M high-margin business—before any upside from better conversion, higher eCPMs or premium creative tiers.

### 6.6 Reach Challenge: Realistic Penetration Goals

While an aggressive growth model would target 16% penetration in France and up to 8% in other European markets, we must also consider a more conservative scenario with more realistic penetration goals: 5% in France (our main market), 5% in major markets (UK, Germany), 3% in mid-sized markets (Spain, Italy, Poland), and 2% in smaller markets (Netherlands, Sweden, Belgium, Austria).

#### 6.6.1 Impact on Active Families and Revenue

With these penetration goals applied to the standard pricing and conversion mix parameters:

| Market | Families < 10 yrs | Penetration goal | Target MAU | Blended ARPU (€/yr) | ARR (€000) |
|--------|-------------------|-----------------|------------|---------------------|------------|
| 🇫🇷 France | 4,300K | 5% | 215,000 | 2.87 | 617 |
| 🇬🇧 United Kingdom | 4,700K | 5% | 235,000 | 4.11 | 966 |
| 🇩🇪 Germany | 5,000K | 5% | 250,000 | 3.28 | 820 |
| 🇪🇸 Spain | 2,650K | 3% | 79,500 | 2.70 | 215 |
| 🇮🇹 Italy | 3,050K | 3% | 91,500 | 2.70 | 247 |
| 🇵🇱 Poland | 2,380K | 3% | 71,400 | 2.28 | 163 |
| 🇳🇱 Netherlands | 1,160K | 2% | 23,200 | 3.03 | 70 |
| 🇸🇪 Sweden | 730K | 2% | 14,600 | 3.61 | 53 |
| 🇧🇪 Belgium | 800K | 2% | 16,000 | 2.95 | 47 |
| 🇦🇹 Austria | 540K | 2% | 10,800 | 3.03 | 33 |
| EU-9 subtotal | — | — | 792,000 | — | 2,614 |
| **Grand total** | — | — | **1,007,000 families** | — | **≈€3.23M ARR** |

#### 6.6.2 Key Implications

1. **France**: 215,000 monthly-active families = €0.62M ARR.
   This is only one-third of the initial €2M goal because penetration is set at 5% instead of 16%.

2. **Major Markets (UK, Germany)**: at 5% penetration, these markets contribute significantly with €0.97M + €0.82M = €1.79M ARR.

3. **Mid-sized Markets (Spain, Italy, Poland)**: at 3% penetration, these markets add €0.63M ARR.

4. **Smaller Markets**: at 2% penetration, the Netherlands, Sweden, Belgium, and Austria contribute €0.20M ARR.

5. **Pan-EU total**: ≈€3.23M ARR, which is a substantial revenue figure but still below the €6M ambition.

#### 6.6.3 Revenue Impact Analysis

1. **Penetration remains the primary lever**
   - Setting France at 5% instead of 16% still reduces the domestic run-rate by -70%.
   - However, increasing UK and Germany to 5% (from 2%) significantly improves their contribution.

2. **The ARPU impact varies by market**
   - High-CPM markets like UK (€4.11/yr) benefit substantially from increased penetration.
   - Mid-sized markets with 3% penetration show meaningful revenue contribution.

3. **Market tier strategy is effective**
   - Major markets (5%): Drive significant revenue (€2.4M combined)
   - Mid-sized markets (3%): Provide solid contribution (€0.63M)
   - Smaller markets (2%): Deliver incremental revenue (€0.20M)

#### 6.6.4 Options to Further Increase Revenue

| Lever | Δ to ARR (France + EU) |
|-------|-------------------------|
| Lift "consumer" attach 5% → 8% | +€0.40M |
| Lift "creative" attach 2.5% → 4% | +€0.45M |
| Introduce €3.99/mo "Unlimited Creative" for 1% of actives | +€0.22M |
| Increase engagement to 90 interactions/MAU/mo | +€0.16M |
| Secure +€0.50 revenue uplift per user in UK/DE/NL/SE | +€0.21M |

With these penetration goals, we achieve €3.23M ARR. By stacking two of these levers, we could approach or exceed €4M ARR. To reach the ambitious €6M target, we would still need to:

- Further increase penetration in key markets; or
- Add recurring value at a higher price point (e.g., €3–4 creative base).

#### 6.6.5 Bottom Line

With our tiered penetration approach (5% in France and major markets, 3% in mid-sized markets, and 2% in smaller markets), the current freemium model can support ≈€3.23M ARR. To reach our more ambitious €6M ARR target, we should focus on:

1. Further increasing household penetration in key markets,
2. Improving paid conversion rates and ARPU, or
3. A combination of both approaches.

This strategic framework should guide our market entry sequencing, pricing strategy, and growth-loop experiments.

---

## 7. Personas & Use Cases

### 7.1 Primary Persona: Creative Kids (6-8 years)

Our narrow wedge persona focus is the 6-8 year old "creative kids" segment. This age group:
- Can self-serve creation flows with minimal parental assistance
- Has developed reading skills but still enjoys being read to
- Is highly imaginative and enjoys storytelling
- Can navigate digital interfaces independently
- Benefits from screen-free audio experiences

| Persona                   | Description                                                                      |
| ------------------------- | -------------------------------------------------------------------------------- |
| **Creative Child (Emma, 7)**  | Our primary persona: Imaginative, tech-savvy child who enjoys creating and customizing stories. Can navigate the app independently but benefits from parental guidance. |
| **Family Administrator**  | Creates a household tenant, invites family members, manages profiles.            |
| **Parent (Amélie, 38)**   | Browses AI-generated bedtime stories on phone, filters by length/theme.          |
| **Grandparent (Michel, 65)** | Receives shared stories from family, listens with grandchildren during visits.  |

### 7.2 Core User Journeys (MVP)

1. **Creative Child Story Creation** (Primary Journey)
   - Child (6-8y) selects "Create Story" on their profile
   - Chooses characters, setting, and basic plot elements through visual interface
   - AI generates complete story with appropriate complexity for age
   - Child reviews, makes simple edits if desired
   - Publishes to family's AI story collection
   - Option to upgrade to Creator Premium if weekly limit reached

2. **AI Story Discovery & Playback**
   - Child or parent browses AI-generated stories
   - Selects AI story based on theme/length
   - Activates dark-screen mode
   - Child listens to AI-generated story

3. **Record-Your-Own Narration**
   - Child selects existing AI-generated story
   - Chooses "Record My Voice"
   - Records narration following text prompts with age-appropriate guidance
   - Save as alternative audio track for the AI story

4. **Hardware Connection Journey** (Post-MVP)
   - Parent connects Talemo account to compatible hardware (Lunii, Yoto, etc.)
   - Child's created stories sync to the device
   - Child can listen to their creations on screen-free hardware
   - Hardware-specific features (cards, figurines) trigger story playback

---

## 8. Functional Requirements

### 8.1 Core Experience (MVP Focus)

| Ref    | Feature                | Description                                                                        | Priority |
| ------ | ---------------------- | ---------------------------------------------------------------------------------- | -------- |
| COR-01 | **AI Story List**     | Browsable, filterable list of available AI-generated stories                       | P0       |
| COR-02 | **AI Story Detail**   | Individual AI story view with metadata and playback controls                        | P0       |
| COR-03 | **AI Story Creation** | Interface for creating and editing AI-generated stories                             | P0       |
| COR-04 | **Agentic Assistant**  | AI-powered assistant for AI story creation and generation                          | P0       |
| COR-05 | **Admin Dashboard**    | Basic management interface for AI-generated content and users                      | P0       |
| COR-06 | **SSO**                | Single sign-on integration with Google and Apple                                   | P0       |
| COR-07 | **Voice-Over Mode**    | Mobile mic recording, waveform trim, stored as alternate audio track               | P0       |
| COR-08 | **« Mode Conte »**     | Dark-screen/lock-mode that blanks display after one tap, keeps audio controls on lock-screen | P0 |
| COR-09 | **French Voices**      | Native French voice packs with Parisian and regional accents                       | P0       |
| COR-10 | **Data Residency Controls** | User-selectable data storage location with French hosting option; CNIL-compliant consent | P0 |
| COR-11 | **Offline AI Story Packs** | Downloadable AI-generated stories for offline use in cars, rural areas, and travel scenarios | P1 |
| COR-12 | **Family Sharing**      | Ability to share stories with extended family members via secure links            | P1       |

### 8.2 Governance & Multi-Tenancy

| Ref    | Requirement                                                                                                 | Priority |
| ------ | ----------------------------------------------------------------------------------------------------------- | -------- |
| GOV-01 | **Tenant bootstrap** – users are created only via invitation tokens embedding `tenant_id`; no orphan users. | P0       |
| GOV-02 | **Profile catalogue** – tenant admins create/clone/delete permission profiles (e.g., *Kids Listen-Only*).   | P0       |
| GOV-03 | **Identity uniqueness** – composite DB constraint `(idp_issuer, idp_subject)` is globally unique.           | P0       |
| GOV-04 | **Tenant-wide feature flags / quotas** – `TenantPolicy` KV store (e.g., `story_quota = 50`).               | P0       |
| GOV-05 | **Row-level security** – every tenant-bound table enforces `tenant_id = current_setting('app.tenant')`.     | P0       |

---

## 9. Agent Architecture (Streamlined for MVP)

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

## 10. Cost Control Roadmap

To achieve our target of €0.03 per story generation, we will implement the following optimizations, clearly distinguishing between pure engineering tasks and those requiring model R&D:

### 10.1 Model & Voice Caching

| Phase | Optimization | Impact | Timeline | Implementation Type | Risk Level |
|-------|--------------|--------|----------|---------------------|------------|
| 1 | Implement aggressive caching of TTS outputs for common phrases | 15-20% reduction in TTS costs | Month 1 | **Pure Engineering** | Low |
| 2 | Create a library of pre-generated voice clips for story templates | Additional 10-15% reduction | Month 2 | **Pure Engineering** | Low |
| 3 | Develop voice fingerprinting to avoid regenerating similar audio | Additional 10% reduction | Month 3 | **Hybrid** (70% Engineering, 30% R&D) | Medium |

### 10.2 Local Inference

| Phase | Optimization | Impact | Timeline | Implementation Type | Risk Level |
|-------|--------------|--------|----------|---------------------|------------|
| 1 | Research and select lightweight TTS models for on-device inference | Planning only | Month 1-2 | **Pure Engineering** | Low |
| 2 | Implement client-side TTS for select devices with sufficient capabilities | 30-40% reduction in cloud TTS costs | Month 3-4 | **Pure Engineering** | Medium |
| 3 | Develop hybrid approach with on-device generation for common content | Additional 10-15% reduction | Post-MVP | **Hybrid** (60% Engineering, 40% R&D) | Medium |

### 10.3 Model Optimization

| Phase | Optimization | Impact | Timeline | Implementation Type | Risk Level |
|-------|--------------|--------|----------|---------------------|------------|
| 1 | Fine-tune smaller LLMs specifically for children's story generation | 20-30% reduction in LLM costs | Month 2-3 | **Model R&D** | High |
| 2 | Implement prompt optimization techniques to reduce token usage | 10-15% reduction | Month 1 | **Pure Engineering** | Low |
| 3 | Create story templates that require minimal LLM customization | 15-20% reduction | Month 2 | **Pure Engineering** | Low |

### 10.4 Cost Reduction Projection

| Timeline | Cost Per Story | Optimization Methods | Engineering vs. R&D Dependency |
|----------|----------------|----------------------|--------------------------------|
| Launch | €0.09-0.12 | Baseline with standard cloud APIs | N/A |
| Month 1 | €0.07-0.09 | Prompt optimization + basic caching | **100% Engineering** (low risk) |
| Month 2 | €0.05-0.07 | Template system + voice clip library | **100% Engineering** (low risk) |
| Month 3 | €0.04-0.05 | Fine-tuned models + voice fingerprinting | **60% Engineering, 40% R&D** (medium risk) |
| Month 4-6 | €0.03 | Client-side inference + hybrid approach | **70% Engineering, 30% R&D** (medium risk) |

### 10.5 Risk Mitigation Strategy

For optimizations with R&D dependencies, we've developed fallback approaches:

1. **Fine-tuned LLM Risk Mitigation**: If model fine-tuning doesn't yield expected results, we'll implement more aggressive prompt engineering and caching strategies that can achieve 15-20% of the targeted savings through pure engineering.

2. **Voice Fingerprinting Risk Mitigation**: If voice fingerprinting R&D is delayed, we'll expand our pre-generated voice clip library and implement more sophisticated caching rules to recover approximately 70% of the expected savings.

This approach ensures we have engineering-only paths to significant cost reduction even if R&D-dependent optimizations face delays.

---

## 11. Go-To-Market Plan

### 11.1 France-First Strategy

Talemo will launch exclusively in the French market, leveraging our competitive analysis and addressing the specific needs of French families.

| Ref    | Stage     | Tactics                                                                                                                 |
| ------ | --------- | ----------------------------------------------------------------------------------------------------------------------- |
| GTM-01 | Beta      | 100 French families via parenting newsletters and Facebook groups. Referral loop: 1 free creative story credit for each signup. Focus on gathering retention and usage data. |
| GTM-02 | Launch    | App Store + Google Play + PWA with French-first UI/UX, French influencer storytelling packs, launch campaign with free ad-free trial. Highlight "audio-first, minimal-screen" messaging to address "Zéro écran" concerns. |
| GTM-03 | Expansion | Targeted campaigns for specific parent segments (new parents, parents of 4-6 year olds, etc.) with customized story packs and features. |

### 11.1.1 Customer Acquisition Budget & Assumptions

To achieve our target CAC of ≤ €12, we've developed a detailed acquisition model with the following components:

| Channel | Budget Allocation | Expected CAC | Conversion Rate | Notes |
|---------|-------------------|--------------|-----------------|-------|
| **Paid Social** | €15,000 (50%) | €14-16 | 2.5-3.0% | Facebook/Instagram targeting French parents 28-45 with children under 10 |
| **Influencer Marketing** | €9,000 (30%) | €10-12 | 3.5-4.0% | 15-20 micro-influencers in French parenting/education space |
| **Content Marketing** | €3,000 (10%) | €8-10 | 2.0-2.5% | French blog content on "moins d'écrans" and creative storytelling |
| **Referral Program** | €3,000 (10%) | €5-7 | 15-20% | Incentivized sharing with creative story credits |

**Referral Loop Assumptions:**
- Each new user will invite an average of 0.4 additional users
- 15% conversion rate on referral invitations
- Effective referral CAC: €5-7 per acquired user
- Referral incentive: 1 creative story credit (€0.50 value) for each successful referral
- Net effect: 25-30% of users acquired through referrals, reducing blended CAC to ≤ €12

### 11.2 Family Engagement Strategy

To maximize retention and drive organic growth among French families, we will:

1. **Segment Targeting**
   - Identify key parent segments (new parents, parents of 4-6 year olds, parents of 7-10 year olds)
   - Develop segment-specific story templates and themes
   - Create targeted marketing campaigns for each segment

2. **Engagement Program**
   - Weekly new story notifications based on child preferences
   - Monthly themed story challenges for families
   - Seasonal content tied to French holidays and traditions
   - Parent community forums for sharing story ideas

3. **Conversion to Paid**
   - Free-to-paid conversion prompts at high-engagement moments
   - Ad-free upgrade offers at moments of ad friction
   - Creative Suite subscription options for story creation
   - Special content bundles for specific age groups or interests

---

## 12. Monetization & Business Model

### 12.1 Creator-Led Revenue Model

Based on our analysis, we're shifting to a creator-focused subscription model as our primary revenue driver, with advertising as a minimal fallback:

| Ref    | Model                | Description                                                                           |
| ------ | -------------------- | ------------------------------------------------------------------------------------- |
| MON-01 | **Creator Premium**  | €3.99/month subscription for unlimited story creation and ad-free experience |
| MON-02 | **Free with Ads**    | Limited access with kid-safe contextual ads (5 rotating AI-generated stories/week) |
| MON-03 | **Hardware Bundles** | White-label or SDK deals with Lunii/Yoto/Tonies for co-creation on their devices |

### 12.2 Unit Economics

| Metric | Target | Strategy |
|--------|--------|----------|
| Creator Conversion | ≥ 15% of MAU (stretch 20%) | Pushes blended ARPU >€0.65 and improves revenue stability |
| Monthly Blended ARPU | €0.46 (vs. €0.07 previous model) | ≈6.6× improvement over previous model |
| ARPU (Creator Premium) | €47.88/year | €3.99 × 12 months |
| ARPU (Free with Ads) | €0.81/year | €0.90 CPM × 75 impressions/month/1000 × 12 months (conservative estimate) |
| CAC | ≤ €12 | Focused marketing in French parenting channels + referral program |
| D30 Retention | ≥ 35% | Benchmark for paid audio-learning apps; critical for LTV/CAC |
| Gross Margin | ≥ 70% | With on-device TTS or €0.03/story cost ceiling |
| CAC Payback | < 6 months on paid cohort | Keeps cash needs within the €0.8M pre-seed envelope |

This creator-led model dramatically reduces the MAU required to reach our revenue targets:

| Metric | Baseline (previous model) | Creator-led (15% convert @ €3.99) |
|--------|---------------------|-----------------------------------|
| Monthly blended ARPU | €0.07 | €0.65 (9.3× higher) |
| MAU needed for €1M ARR | 1.26M | 0.13M (10× fewer) |

### 12.3 Detailed Business Model (€1.4M ARR Pre-Seed Milestone)

Based on our creator-led revenue model and best-available AI-inference benchmarks, we've developed a comprehensive business model to reach €1.4M ARR with a capital-efficient approach, requiring significantly fewer users than the previous model would demand.

#### 12.3.1 Revenue Assumptions (FY2025)

| Revenue Stream | Assumptions | Source/Rationale |
|----------------|-------------|------------------|
| **Creator Premium** | €3.99/month subscription | Primary revenue driver with 15% conversion target |
| **Ad Revenue** | €0.90 net kids-safe eCPM | Post-DSA contextual-only ads to minors; conservative estimate |
| | 75 impressions/free MAU/month | 3 sessions × 4 ads each × ~6 fill-rate discount |
| **Hardware Partnerships** | White-label/SDK revenue | Potential to attach to 1% of Tonies + Yoto's 4M installed base |

#### 12.3.2 Cost Structure

| Cost Category | Assumptions | Details |
|---------------|-------------|---------|
| **TTS Cost** | €0.000016/character | ~€0.022 per 1,500-char story (Google Polyglot tier) |
| **Image Cost** | €0.0004 per SD-XL image | AWS Inferentia2 benchmark |
| **Moderation + Misc** | €0.01/story | Quality assurance and safety |
| **All-in AI Cost/Story** | €0.06 | Voice + image + moderation |
| **Hosting/Streaming** | €0.20/active user/year | Cloud infrastructure costs |
| **Variable Cost per Creator User** | €15.6/year | 5 stories/week × 52 × €0.06 |

#### 12.3.3 User Mix to Achieve €1M ARR (Pre-Seed Milestone)

With our creator-led model focusing on €3.99/month subscriptions, we can achieve €1M ARR with dramatically fewer users:

| Segment | Users | Monthly Revenue | Annual Revenue |
|---------|-------|----------------|----------------|
| Creator Premium (15%) | 27,000 subscribers | 27K × €3.99 ≈ €107.7K | €1,292K |
| Free with Ads (85%) | 153,000 MAU | 153K × €0.07/mo ≈ €10.7K | €128K |
| **Total** | **180,000 MAU** | **€118.4K MRR** | **€1.42M ARR** |

This represents a dramatic reduction from the 700,000 MAU that would be required in the previous model, making our growth targets much more achievable with limited marketing resources.

#### 12.3.4 Hardware Partnership Potential

By pursuing white-label or SDK deals with established hardware players, we can further accelerate growth:

| Partner | Installed Base (EU) | Potential Attachment | Annual Revenue Potential |
|---------|---------------------|----------------------|--------------------------|
| Tonies + Yoto | ~4M devices | 1% adoption | 40K users × €3.99 × 12 = €1.92M |
| Lunii | ~1.5M devices | 2% adoption | 30K users × €3.99 × 12 = €1.44M |

Even modest adoption rates of our creation tools by existing hardware users could generate substantial additional revenue without the CAC burden of direct acquisition.

#### 12.3.5 Gross Margin Analysis

| Cost Bucket | Amount | Notes |
|-------------|--------|-------|
| AI Variable (creator users) | €421K | €15.6 × 27K creator users |
| Hosting/Streaming | €36K | €0.20 × 180K total users |
| **Total Variable Costs** | **€457K** | |
| **Gross Profit** | **€963K** | **68% gross margin** |

This margin is healthy and sustainable, especially as we implement our cost optimization roadmap to bring AI costs down to €0.03 per story, which would improve margins to >80%.

#### 12.3.6 Operational Structure

A lean team of approximately 8 FTE can efficiently operate the platform during the pre-seed phase:
- 4 Engineering (focus on on-device TTS and creator tools)
- 1 Design (focus on 6-8y "creative kids" UX)
- 1 Partnership Manager (hardware & distribution deals)
- 1 Content (story templates & moderation)
- 1 Founder/Business Development

**Fixed Operational Costs:**
- Team: €480K/year (all-in cost)
- Tools & Legal: €120K/year
- Paid User Acquisition: €150K/year (reduced due to hardware partnerships)

This structure maintains capital efficiency while focusing on our core creator-led value proposition.

#### 12.3.7 Key Funnel Metrics

| Funnel KPI | Target | Rationale |
|------------|--------|-----------|
| 12-month cumulative installs | ≈515K | Assumes D30 retention 35% → 180K MAU |
| Free → Creator Premium conversion | 15% (stretch 20%) | Critical metric for revenue model success |
| D30 retention (creator kids) | ≥ 35% | Benchmark for paid audio-learning apps |
| CAC payback | < 6 months on paid cohort | Ensures sustainable unit economics |

With these conversion rates, approximately 85% of users remain on the ad-supported tier while 15% subscribe to the Creator Premium tier, generating the bulk of our revenue. This is a significant improvement over the typical 7.5% paid conversion rate seen in standard freemium apps.

#### 12.3.8 Business Model Sensitivity

| Lever | Effect on €1M ARR Business |
|-------|---------------------------|
| Lift Creator Premium conversion from 15% → 20% | MAU needed ↓ to 135K (25% fewer) |
| Increase subscription price to €4.99/month | Revenue ↑ by 25% with same user base |
| Improve D30 retention from 35% → 45% | Reduces 12-month CAC by ~22% |
| Cut AI cost to €0.03/story | Margin ↑ to 85% (from 70%) |
| Hardware partnership adoption at 2% | Additional €3.36M ARR potential |

### 12.4 Focused Market Strategy

With our creator-led model, we can achieve our €1M ARR milestone with a much more focused market approach, concentrating exclusively on France during the pre-seed phase:

| Country | Target MAU | Creator Premium (15%) | Monthly Revenue | Annual Revenue |
|---------|------------|----------------------|-----------------|----------------|
| 🇫🇷 France | 180K | 27K subscribers | €107.7K | €1.29M |

This represents just 4.2% of French families with children under 10 (4.3M total) - a much more achievable target than the 16% penetration that would be required in a high-volume, low-ARPU scenario.

#### 12.4.1 Post-Seed European Expansion

After proving our creator-led model in France and securing seed funding, we'll expand to select European markets with a similar approach:

| Country | Target MAU | Creator Conversion | Annual Revenue Potential |
|---------|------------|-------------------|--------------------------|
| 🇬🇧 UK | 150K | 15% (22.5K subs) | €1.08M |
| 🇩🇪 Germany | 150K | 15% (22.5K subs) | €1.08M |

This focused approach allows us to:
1. Validate our model in France with minimal capital (€0.5-0.8M pre-seed)
2. Prove creator conversion and retention metrics
3. Establish hardware partnerships to reduce CAC
4. Expand to key European markets with seed funding (€3-4M)

By focusing on creator conversion rather than massive scale, we can build a sustainable business with significantly less capital and marketing spend.

### 12.5 Regulatory Compliance & Risk De-Risking

We're proactively addressing regulatory concerns from day one, making compliance a competitive advantage rather than a burden:

#### 12.5.1 CNIL-Style Parental Dashboard

We'll build a comprehensive parental control dashboard that exceeds CNIL requirements:

| Feature | Description | Benefit |
|---------|-------------|---------|
| **Granular Consent Management** | Parents can approve/revoke permissions for specific features | Exceeds GDPR-K requirements |
| **Usage Monitoring** | Time spent, stories created/consumed, with weekly reports | Gives parents transparency |
| **Content Filtering** | Age-appropriate content controls with parent override | Builds trust with families |
| **Data Residency Controls** | All data hosted in France with SecNumCloud certification | Addresses sovereignty concerns |

#### 12.5.2 AI Content Transparency

| Feature | Description | Benefit |
|---------|-------------|---------|
| **AI-Generated Content Labeling** | Clear marking of AI-generated content per EU AI Act requirements | Regulatory compliance |
| **Contextual-Only Advertising** | No behavioral targeting, fully DSA-compliant | Future-proof revenue model |
| **CNIL Sandbox Submission** | Voluntary participation in CNIL's regulatory sandbox | Early feedback and trust badge |

#### 12.5.3 Business Risk Mitigation

| Risk | Mitigation Strategy |
|------|---------------------|
| **AI cost volatility** | On-device TTS implementation within 6 months; local model caching | Reduces cloud dependency |
| **Competitive response** | Hardware partnership strategy creates win-win with potential competitors | Turns threats into opportunities |
| **Regulatory changes** | Proactive compliance and participation in regulatory sandboxes | Builds relationships with regulators |

This approach not only creates a capital-efficient business but positions Talemo as a leader in responsible AI for children, making us attractive to both seed VCs and strategic buyers in ed-tech or kids hardware markets.

---

## 13. Exit Narratives

### 13.1 Strategic Acquisition Paths (3-5 Year Horizon)

| Potential Acquirer | Strategic Fit | Path to Acquisition |
|-------------------|---------------|---------------------|
| **Yoto** | - Talemo provides content creation capabilities Yoto lacks<br>- Our French market presence complements their UK/US strength<br>- Our software platform enhances their hardware ecosystem | 1. Establish content syndication partnership<br>2. Integrate Talemo stories with Yoto cards<br>3. Demonstrate strong French market traction<br>4. Position as their software/content arm |
| **Bayard** | - Major French children's publisher seeking digital transformation<br>- Our platform extends their IP to interactive audio<br>- Complements their existing family content offerings | 1. Secure content licensing deal<br>2. Co-develop exclusive French stories<br>3. Integrate with their parent-focused distribution channels<br>4. Demonstrate technology advantage over competitors |
| **Spotify Kids** | - Our creation tools fill gap in their consumption-only model<br>- French-first approach complements their global reach<br>- Our family-focused features enhance their consumer offering | 1. Build user base with strong retention metrics<br>2. Develop API for potential integration<br>3. Demonstrate unique engagement vs. passive listening<br>4. Position as their "creation studio" for kids content |

### 13.2 Key Metrics for Acquisition Attractiveness

| Metric | Target | Rationale |
|--------|--------|-----------|
| Monthly Active Users | 100,000+ | Demonstrates product-market fit and scalability |
| D30 Retention | > 35% | Shows strong user engagement and product stickiness |
| Stories Created | > 1M | Proves content generation capability and user adoption |
| Creative Suite Subscribers | 17,500+ | Validates recurring revenue model and creation features |
| Paid Conversion Rate | > 7.5% | Shows willingness to pay (5% ad-free, 2.5% creative) |
| ARR | €1-2M | Shows revenue traction and business model validation |
| French Market Share | 15%+ | Establishes leadership in initial market |

---

## 14. Development Roadmap

### 14.1 4-Month MVP Timeline with Critical Path

| Week | Focus | Key Deliverables | Milestone |
|------|-------|------------------|-----------|
| **Weeks 1-4** | Core Infrastructure | - Multi-tenant architecture with RLS<br>- Basic authentication and profile system<br>- Initial story playback functionality | Architecture Review (Week 4) |
| **Weeks 5-8** | Story Creation | - AI story generation workflow<br>- French voice integration<br>- Basic moderation system<br>- **CNIL DPIA submission** | DPIA Approval (Week 8) |
| **Weeks 9-12** | Key Features | - Record-your-own functionality<br>- Dark-screen mode implementation<br>- Offline capabilities | Feature Complete (Week 12) |
| **Weeks 13-16** | QA & Launch Prep | - Performance optimization<br>- Final UI/UX refinement<br>- Security audit<br>- App store submission | **Beta Launch: October 15, 2025** |

### 14.2 Critical Path Gantt Chart

```
                    Week: 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
Core Infrastructure     [==========]
  Multi-tenant RLS      [====]
  Authentication           [====]
  Playback                    [====]
Story Creation                   [==========]
  AI Generation                  [======]
  Voice Integration                 [====]
  CNIL DPIA                            [==]
Key Features                               [==========]
  Record-Your-Own                         [======]
  Dark-Screen Mode                           [====]
  Offline Support                                [====]
QA & Launch                                         [==========]
  Performance Opt.                                  [====]
  Security Audit                                       [====]
  Store Submission                                        [====]
BETA LAUNCH                                                    [X]
```

### 14.3 Post-MVP Priorities

1. Enhanced analytics for retention optimization
2. Advanced parental controls and family management features
3. Additional cost optimization implementations
4. Curated content catalog through partnerships with French publishers (expanding beyond AI-only content)
5. Expanded AI creation tools and templates
6. Family sharing and collaboration features
7. Premium voice packs with celebrity narrators
