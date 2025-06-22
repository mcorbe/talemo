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

Based on market feedback, we're narrowing our initial release to three core capabilities with an exclusive focus on AI-generated content:

1. **AI Story Builder** - Intuitive interface for creating personalized audio stories with AI assistance
2. **Dark-Screen Playback** - Screen-free listening mode that addresses the "moins d'écrans" parental concern
3. **Record-Your-Own** - Ability for families to record their own narration for AI-generated stories

At launch, we will solely focus on AI-generated story content without any pre-existing catalog. This approach allows us to prove that AI-generated content works for parents and kids before potentially adding licensed content in the future.

This focused approach allows us to:
- Launch a compelling product within 4 months
- Validate core user behaviors and retention metrics
- Build a strong foundation with French families
- Control costs while building toward unit economic sustainability

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
8. Prepare for a **freemium subscription model** targeting parents.
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
| 🟢 **D30 Retention**                   | ≥ 35%                          | Key VC requirement showing product stickiness            |
| 🟢 **Stories Created Per Child/Week**  | ≥ 3                            | Key VC requirement showing engagement                    |
| 🟢 **Time-to-First-Play** (new user)   | < 30 s                         | Critical for parent satisfaction and quick adoption      |
| 🟢 **Story Generation Lead Time**      | ≤ 2 min (submit → audio ready) | User experience requirement for creation flow            |
| 🟢 **Mobile PWA Lighthouse Perf**      | ≥ 85                           | Technical performance requirement                         |
| 🟢 **Customer Acquisition Cost (CAC)** | ≤ €12                          | Adjusted based on VC feedback (up from €6)               |
| 🟢 **LTV / CAC Ratio**                 | ≥ 3.0 ×                        | Business sustainability metric                           |
| 🟢 **Cost Per Story Generation**       | ≤ €0.03 (roadmap)              | Key VC requirement for unit economics                    |
| 🟢 **Paying Subscribers**              | ≥ 5,000 in 6 months           | Demonstrates consumer willingness to pay                 |

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

## 6. Personas & Use Cases

| Persona                   | Description                                                                      |
| ------------------------- | -------------------------------------------------------------------------------- |
| **Family Administrator**  | Creates a household tenant, invites family members, manages profiles.            |
| **Parent (Amélie, 38)**   | Browses AI-generated bedtime stories on phone, filters by length/theme.          |
| **Child (Léo, 8)**        | Taps colourful card, plays AI-generated story, creates own stories with AI assistance. |
| **Grandparent (Michel, 65)** | Receives shared stories from family, listens with grandchildren during visits.  |
| **Story Creator (Lucas)** | Parent who writes text, triggers AI asset generation, records own narration.     |

### Core User Journeys (MVP)

1. **AI Story Discovery & Playback**
   - Parent browses AI-generated stories
   - Selects AI story based on theme/length
   - Activates dark-screen mode
   - Child listens to AI-generated story

2. **AI Story Creation**
   - Child/parent selects "Create Story"
   - Enters basic story elements (characters, setting)
   - AI generates complete story
   - Reviews and publishes to family's AI story collection

3. **Record-Your-Own Narration for AI Stories**
   - Select existing AI-generated story
   - Choose "Record My Voice"
   - Record narration following text prompts
   - Save as alternative audio track for the AI story

4. **Family Sharing Journey**
   - Parent selects story to share
   - Generates unique family sharing link
   - Sends link to grandparents or other family members
   - Family members listen without needing an account
   - Option to save story to their own account if they sign up

---

## 7. Functional Requirements

### 7.1 Core Experience (MVP Focus)

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

To achieve our target of €0.03 per story generation, we will implement the following optimizations, clearly distinguishing between pure engineering tasks and those requiring model R&D:

### 9.1 Model & Voice Caching

| Phase | Optimization | Impact | Timeline | Implementation Type | Risk Level |
|-------|--------------|--------|----------|---------------------|------------|
| 1 | Implement aggressive caching of TTS outputs for common phrases | 15-20% reduction in TTS costs | Month 1 | **Pure Engineering** | Low |
| 2 | Create a library of pre-generated voice clips for story templates | Additional 10-15% reduction | Month 2 | **Pure Engineering** | Low |
| 3 | Develop voice fingerprinting to avoid regenerating similar audio | Additional 10% reduction | Month 3 | **Hybrid** (70% Engineering, 30% R&D) | Medium |

### 9.2 Local Inference

| Phase | Optimization | Impact | Timeline | Implementation Type | Risk Level |
|-------|--------------|--------|----------|---------------------|------------|
| 1 | Research and select lightweight TTS models for on-device inference | Planning only | Month 1-2 | **Pure Engineering** | Low |
| 2 | Implement client-side TTS for select devices with sufficient capabilities | 30-40% reduction in cloud TTS costs | Month 3-4 | **Pure Engineering** | Medium |
| 3 | Develop hybrid approach with on-device generation for common content | Additional 10-15% reduction | Post-MVP | **Hybrid** (60% Engineering, 40% R&D) | Medium |

### 9.3 Model Optimization

| Phase | Optimization | Impact | Timeline | Implementation Type | Risk Level |
|-------|--------------|--------|----------|---------------------|------------|
| 1 | Fine-tune smaller LLMs specifically for children's story generation | 20-30% reduction in LLM costs | Month 2-3 | **Model R&D** | High |
| 2 | Implement prompt optimization techniques to reduce token usage | 10-15% reduction | Month 1 | **Pure Engineering** | Low |
| 3 | Create story templates that require minimal LLM customization | 15-20% reduction | Month 2 | **Pure Engineering** | Low |

### 9.4 Cost Reduction Projection

| Timeline | Cost Per Story | Optimization Methods | Engineering vs. R&D Dependency |
|----------|----------------|----------------------|--------------------------------|
| Launch | €0.09-0.12 | Baseline with standard cloud APIs | N/A |
| Month 1 | €0.07-0.09 | Prompt optimization + basic caching | **100% Engineering** (low risk) |
| Month 2 | €0.05-0.07 | Template system + voice clip library | **100% Engineering** (low risk) |
| Month 3 | €0.04-0.05 | Fine-tuned models + voice fingerprinting | **60% Engineering, 40% R&D** (medium risk) |
| Month 4-6 | €0.03 | Client-side inference + hybrid approach | **70% Engineering, 30% R&D** (medium risk) |

### 9.5 Risk Mitigation Strategy

For optimizations with R&D dependencies, we've developed fallback approaches:

1. **Fine-tuned LLM Risk Mitigation**: If model fine-tuning doesn't yield expected results, we'll implement more aggressive prompt engineering and caching strategies that can achieve 15-20% of the targeted savings through pure engineering.

2. **Voice Fingerprinting Risk Mitigation**: If voice fingerprinting R&D is delayed, we'll expand our pre-generated voice clip library and implement more sophisticated caching rules to recover approximately 70% of the expected savings.

This approach ensures we have engineering-only paths to significant cost reduction even if R&D-dependent optimizations face delays.

---

## 10. Go-To-Market Plan

### 10.1 France-First Strategy

Talemo will launch exclusively in the French market, leveraging our competitive analysis and addressing the specific needs of French families.

| Ref    | Stage     | Tactics                                                                                                                 |
| ------ | --------- | ----------------------------------------------------------------------------------------------------------------------- |
| GTM-01 | Beta      | 100 French families via parenting newsletters and Facebook groups. Referral loop: 1 free premium story for each signup. Focus on gathering retention and usage data. |
| GTM-02 | Launch    | App Store + Google Play + PWA with French-first UI/UX, French influencer storytelling packs, launch campaign with free 7-day premium. Highlight "audio-first, minimal-screen" messaging to address "Zéro écran" concerns. |
| GTM-03 | Expansion | Targeted campaigns for specific parent segments (new parents, parents of 4-6 year olds, etc.) with customized story packs and features. |

### 10.1.1 Customer Acquisition Budget & Assumptions

To achieve our target CAC of ≤ €12, we've developed a detailed acquisition model with the following components:

| Channel | Budget Allocation | Expected CAC | Conversion Rate | Notes |
|---------|-------------------|--------------|-----------------|-------|
| **Paid Social** | €15,000 (50%) | €14-16 | 2.5-3.0% | Facebook/Instagram targeting French parents 28-45 with children 4-12 |
| **Influencer Marketing** | €9,000 (30%) | €10-12 | 3.5-4.0% | 15-20 micro-influencers in French parenting/education space |
| **Content Marketing** | €3,000 (10%) | €8-10 | 2.0-2.5% | French blog content on "moins d'écrans" and creative storytelling |
| **Referral Program** | €3,000 (10%) | €5-7 | 15-20% | Incentivized sharing with premium content rewards |

**Referral Loop Assumptions:**
- Each new user will invite an average of 0.4 additional users
- 15% conversion rate on referral invitations
- Effective referral CAC: €5-7 per acquired user
- Referral incentive: 1 premium story credit (€0.50 value) for each successful referral
- Net effect: 25-30% of users acquired through referrals, reducing blended CAC to ≤ €12

### 10.2 Family Engagement Strategy

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
   - Free-to-premium conversion prompts at high-engagement moments
   - Family subscription options with multiple child profiles
   - Special offers for annual subscriptions
   - Premium content bundles for specific age groups or interests

---

## 11. Monetization & Business Model

| Ref    | Model                | Description                                                                           |
| ------ | -------------------- | ------------------------------------------------------------------------------------- |
| MON-01 | **Freemium**         | Free tier (access to 5 rotating AI-generated stories/week), Premium (€4.99/month) unlocks full access + unlimited AI story creation |
| MON-02 | **Family Plan**      | €7.99/month for up to 5 family members with shared story library and individual profiles |
| MON-03 | **Annual Subscription** | €49.99/year (≈€4.17/month) for individual Premium, €79.99/year for Family Plan |

### 11.1 Unit Economics

| Metric | Target | Strategy |
|--------|--------|----------|
| ARPU | €4.99 (individual) / €7.99 (family) | Tiered model with clear value proposition for premium features |
| CAC | ≤ €12 | Focused marketing in French parenting channels + referral program |
| LTV | ≥ €36 | Target 7+ month retention for premium subscribers |
| Gross Margin | > 50% after AI costs | Implement cost control roadmap to reach €0.03/story |

---

## 12. Exit Narratives

### 12.1 Strategic Acquisition Paths (3-5 Year Horizon)

| Potential Acquirer | Strategic Fit | Path to Acquisition |
|-------------------|---------------|---------------------|
| **Yoto** | - Talemo provides content creation capabilities Yoto lacks<br>- Our French market presence complements their UK/US strength<br>- Our software platform enhances their hardware ecosystem | 1. Establish content syndication partnership<br>2. Integrate Talemo stories with Yoto cards<br>3. Demonstrate strong French market traction<br>4. Position as their software/content arm |
| **Bayard** | - Major French children's publisher seeking digital transformation<br>- Our platform extends their IP to interactive audio<br>- Complements their existing family content offerings | 1. Secure content licensing deal<br>2. Co-develop exclusive French stories<br>3. Integrate with their parent-focused distribution channels<br>4. Demonstrate technology advantage over competitors |
| **Spotify Kids** | - Our creation tools fill gap in their consumption-only model<br>- French-first approach complements their global reach<br>- Our family-focused features enhance their consumer offering | 1. Build user base with strong retention metrics<br>2. Develop API for potential integration<br>3. Demonstrate unique engagement vs. passive listening<br>4. Position as their "creation studio" for kids content |

### 12.2 Key Metrics for Acquisition Attractiveness

| Metric | Target | Rationale |
|--------|--------|-----------|
| Monthly Active Users | 100,000+ | Demonstrates product-market fit and scalability |
| D30 Retention | > 35% | Shows strong user engagement and product stickiness |
| Stories Created | > 1M | Proves content generation capability and user adoption |
| Family Plan Subscribers | 10,000+ | Validates multi-user household model and premium offering |
| Premium Conversion Rate | > 8% | Shows willingness to pay for premium features |
| ARR | €1-2M | Shows revenue traction and business model validation |
| French Market Share | 15%+ | Establishes leadership in initial market |

---

## 13. Development Roadmap

### 13.1 4-Month MVP Timeline with Critical Path

| Week | Focus | Key Deliverables | Milestone |
|------|-------|------------------|-----------|
| **Weeks 1-4** | Core Infrastructure | - Multi-tenant architecture with RLS<br>- Basic authentication and profile system<br>- Initial story playback functionality | Architecture Review (Week 4) |
| **Weeks 5-8** | Story Creation | - AI story generation workflow<br>- French voice integration<br>- Basic moderation system<br>- **CNIL DPIA submission** | DPIA Approval (Week 8) |
| **Weeks 9-12** | Key Features | - Record-your-own functionality<br>- Dark-screen mode implementation<br>- Offline capabilities | Feature Complete (Week 12) |
| **Weeks 13-16** | QA & Launch Prep | - Performance optimization<br>- Final UI/UX refinement<br>- Security audit<br>- App store submission | **Beta Launch: October 15, 2025** |

### 13.2 Critical Path Gantt Chart

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

### 13.3 Post-MVP Priorities

1. Enhanced analytics for retention optimization
2. Advanced parental controls and family management features
3. Additional cost optimization implementations
4. Curated content catalog through partnerships with French publishers (expanding beyond AI-only content)
5. Expanded AI creation tools and templates
6. Family sharing and collaboration features
7. Premium voice packs with celebrity narrators
