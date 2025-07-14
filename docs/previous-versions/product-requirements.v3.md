# Product Requirements Document (PRD) - v3

## 1. Document Control

| **Product**   | Talemo - French Audio-Stories Platform (MVP)     |
| ------------- | ------------------------------------------------- |
| **Author**    | Product Team / CTO                                |
| **Reviewers** | Engineering · Design · Marketing · Legal · SecOps |
| **Version**   | 3.0                                               |

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
8. Prepare for a **creator-led subscription model** targeting parents.
9. Achieve **cost-efficient story generation** through optimization roadmap.

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
| **D30 Retention**                      | ≥ 35%                          | Critical metric showing product stickiness                |
| **Stories Created Per Child/Week**     | ≥ 3                            | Key engagement metric for user activity                   |
| **Time-to-First-Play** (new user)      | < 30 s                         | Critical for parent satisfaction and quick adoption       |
| **Story Generation Lead Time**         | ≤ 2 min (submit → audio ready) | User experience requirement for creation flow             |
| **Mobile PWA Lighthouse Perf**         | ≥ 85                           | Technical performance requirement                         |
| **Customer Acquisition Cost (CAC)**    | ≤ €12                          | Target for sustainable user acquisition                   |
| **LTV / CAC Ratio**                    | ≥ 3.0 ×                        | Business sustainability metric                            |
| **Creator Premium Conversion**         | ≥ 15%                          | Critical for creator-led business model                   |
| **Search-to-Play conversion rate**     | ≥ 55%                          | Measures effectiveness of semantic search                 |
| **Duplicate stories generated / 1k prompts** | ≤ 1.0                    | Measures effectiveness of duplication guard               |
| **Average TTS € per story**            | ≤ €0.062                       | Measures cost efficiency improvements                     |

---

## 5. Competitive Landscape — French Market Focus

### French Market Competitive Analysis

As France will be our exclusive initial market, we've conducted a detailed competitive analysis of the French audio storytelling landscape:

#### 1. Home-turf Frontrunners to Study—and Out-flank

| Player | Core Offer (FR market) | Why It's a Real Threat | Counters & Gaps Talemo Can Exploit |
| ------ | ---------------------- | ---------------------- | ---------------------------------- |
| **Lunii – Ma Fabrique à Histoires** | - Hardware device with screen-free experience<br>- Kids "mix & match" story elements on a screen-free box; French audiobooks. | • Brand already shorthand for "conteuse" in France.<br>• One-time purchase vs. subscription. | • Lunii is hardware-bound and single-profile; no cloud collaboration.<br>• Pitch Talemo as "tout-en-un app"—create, share, listen anywhere, no extra gadget. |
| **Sybel Kids** | Mobile app & web with kids podcasts and audiobooks in French; strong licensing ties with Bayard, Radio France. | • Pure-software, freemium, already sits on parents' phones.<br>• Slow growth after 5 years shows market challenges. | • Sybel is listen-only: zero story-creation capabilities.<br>• Lean on Talemo's AI composer + family-friendly features. |
| **Bookinou** | NFC "badge" reader that lets families record their own voice per physical book. | • Deep emotional appeal ("Papa lit l'histoire").<br>• Strong brand recognition among French parents. | • Requires the printed book + tag; no original stories, no streaming catalogue.<br>• Talemo can match the "record-your-own" angle without extra hardware. |

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

Our refined target audience is families with at least one child under 10 years old. This focus allows us to address the most relevant audience for children's audio stories while providing more accurate market sizing.

For France specifically, there are approximately 4.3 million families with at least one child under 10 years old.

With our creator-led business model, we can achieve meaningful revenue with a much smaller user base than traditional ad-supported or one-time purchase models. Our target is to reach 5% penetration in the French market (approximately 215,000 monthly active users), with 15% of those converting to our Creator Premium subscription.

This approach is significantly more realistic than attempting to reach 16% market penetration, which would be required under a lower ARPU model.

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

4. **Family Sharing Journey**
   - Parent shares child's created story with grandparents
   - Grandparent receives secure link to access the story
   - Grandparent listens to the story with or without the child
   - Option for grandparent to record their own narration as a gift back to the child

---

## 8. Functional Requirements

### 8.1 Core Experience (MVP Focus)

| Ref    | Feature                | Description                                                                        | Priority |
|--------| ---------------------- | ---------------------------------------------------------------------------------- | -------- |
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
| COR-11 | **Semantic Story Search** | Vector-powered search that ranks results by cosine similarity on embeddings, with full-text fallback | P0 |
| COR-12 | **Duplication Guard**   | Vector similarity check against existing library to prevent near-identical stories | P0       |
| COR-13 | **Offline AI Story Packs** | Downloadable AI-generated stories for offline use in cars, rural areas, and travel scenarios | P1 |
| COR-14 | **Family Sharing**      | Ability to share stories with extended family members via secure links            | P1       |

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
| AGT-05 | **EmbeddingAgent**       | Generates vector embeddings for semantic search and duplication detection.       | `story.draft` → `story.embedded` / `story.duplicate` |

### User-facing Agents

| Ref       | Agent                | Purpose                                                |
| --------- | -------------------- | ------------------------------------------------------ |
| AGT-UF-01 | **StoryCompanion**   | Co-creation chat assistant for families                |

---

## 10. Cost Control Roadmap

To achieve our target of cost-efficient story generation, we will implement the following optimizations, clearly distinguishing between pure engineering tasks and those requiring model R&D:

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
| GTM-02 | Launch    | App Store + Google Play + PWA with French-first UI/UX, French influencer storytelling packs, launch campaign with free trial. Highlight "audio-first, minimal-screen" messaging to address "Zéro écran" concerns. |
| GTM-03 | Expansion | Targeted campaigns for specific parent segments (new parents, parents of 4-6 year olds, etc.) with customized story packs and features. |

### 11.1.1 Customer Acquisition Budget & Assumptions

To achieve our target CAC of ≤ €12, we've developed a detailed acquisition model with the following components:

| Channel | Budget Allocation | Expected CAC | Conversion Rate | Notes |
|---------|-------------------|--------------|-----------------|-------|
| **Paid Social** | 50% | €14-16 | 2.5-3.0% | Facebook/Instagram targeting French parents 28-45 with children under 10 |
| **Influencer Marketing** | 30% | €10-12 | 3.5-4.0% | 15-20 micro-influencers in French parenting/education space |
| **Content Marketing** | 10% | €8-10 | 2.0-2.5% | French blog content on "moins d'écrans" and creative storytelling |
| **Referral Program** | 10% | €5-7 | 15-20% | Incentivized sharing with creative story credits |

**Referral Loop Assumptions:**
- Each new user will invite an average of 0.4 additional users
- 15% conversion rate on referral invitations
- Effective referral CAC: €5-7 per acquired user
- Referral incentive: 1 creative story credit for each successful referral
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
   - Creative Suite subscription options for story creation
   - Special content bundles for specific age groups or interests

---

## 12. Creator-Led Business Model

### 12.1 Creator-Led Revenue Model

Our primary revenue driver is a creator-focused subscription model, with a free tier to drive acquisition:

| Ref    | Model                | Description                                                                           |
| ------ | -------------------- | ------------------------------------------------------------------------------------- |
| MON-01 | **Creator Premium**  | €3.99/month subscription for unlimited story creation and ad-free experience |
| MON-02 | **Free Tier**        | Limited access (5 rotating AI-generated stories/week, 2 story creations/week) |
| MON-03 | **Hardware Partnerships** | White-label or SDK deals with Lunii/Yoto/Tonies for co-creation on their devices |

### 12.2 Unit Economics

| Metric | Target | Strategy                                                          |
|--------|--------|-------------------------------------------------------------------|
| Creator Conversion | ≥ 15% of MAU | Pushes blended ARPU higher and improves revenue stability         |
| ARPU (Creator Premium) | €47.88/year | €3.99 × 12 months                                                 |
| CAC | ≤ €12 | Focused marketing in French parenting channels + referral program |
| D30 Retention | ≥ 35% | Benchmark for paid audio-learning apps; critical for LTV/CAC      |
| Gross Margin | ≥ 70% | With optimized story generation costs                             |
| CAC Payback | < 6 months on paid cohort | Keeps cash needs low                                              |

This creator-led model dramatically reduces the MAU required to reach our revenue targets compared to ad-supported or one-time purchase models.

### 12.3 Creator-Led Business Model Benefits

The creator-led subscription model offers several key advantages:

1. **Higher ARPU**: At €3.99/month, subscribers generate significantly more revenue than ad-supported users.

2. **Lower User Acquisition Requirements**: With higher ARPU, we need fewer total users to reach revenue targets.

3. **Aligned Value Proposition**: Parents are willing to pay for creative tools that engage their children in active learning.

4. **Predictable Revenue**: Subscription model provides more stable, predictable revenue compared to one-time purchases or ad revenue.

5. **Cost Control**: By limiting free tier creation to 2 stories/week, we can manage AI generation costs while still providing value.

### 12.4 Path to Revenue

With our creator-led model focusing on €3.99/month subscriptions, we can achieve meaningful revenue with a realistic user base:

1. **Initial Target**: 5% penetration of French families with children under 10 (215,000 MAU)
2. **Creator Premium Conversion**: 15% of MAU (32,250 subscribers)
3. **Monthly Revenue**: 32,250 × €3.99 = €128,677 MRR
4. **Annual Revenue**: €1.54M ARR

This represents a realistic and achievable target that requires just 5% market penetration in France, compared to the 16% that would be required with a lower ARPU model.

### 12.5 Hardware Partnership Strategy

Rather than competing directly with hardware players, we'll pursue partnerships that create win-win opportunities:

1. **SDK Integration**: Provide our story creation technology to hardware manufacturers like Lunii, Yoto, and Tonies.

2. **Revenue Share**: Establish revenue-sharing agreements for stories created on our platform and played on partner devices.

3. **Co-Marketing**: Joint marketing campaigns that highlight the combined value of creative software + dedicated hardware.

4. **White-Label Solutions**: Offer white-label versions of our creation tools that hardware partners can integrate into their ecosystems.

This approach turns potential competitors into partners and creates additional revenue streams without the CAC burden of direct acquisition.

### 12.6 Regulatory Compliance & Trust

We're proactively addressing regulatory concerns from day one, making compliance a competitive advantage:

#### 12.6.1 CNIL-Style Parental Dashboard

We'll build a comprehensive parental control dashboard that exceeds CNIL requirements:

| Feature | Description | Benefit |
|---------|-------------|---------|
| **Granular Consent Management** | Parents can approve/revoke permissions for specific features | Exceeds GDPR-K requirements |
| **Usage Monitoring** | Time spent, stories created/consumed, with weekly reports | Gives parents transparency |
| **Content Filtering** | Age-appropriate content controls with parent override | Builds trust with families |
| **Data Residency Controls** | All data hosted in France with SecNumCloud certification | Addresses sovereignty concerns |

#### 12.6.2 AI Content Transparency

| Feature | Description | Benefit |
|---------|-------------|---------|
| **AI-Generated Content Labeling** | Clear marking of AI-generated content per EU AI Act requirements | Regulatory compliance |
| **CNIL Sandbox Submission** | Voluntary participation in CNIL's regulatory sandbox | Early feedback and trust badge |

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
| Creative Suite Subscribers | 15,000+ | Validates recurring revenue model and creation features |
| French Market Share | 5%+ | Establishes leadership in initial market |
| ARR | €1-2M | Shows revenue traction and business model validation |

---

## 14. Development Roadmap

### 14.1 4-Month MVP Timeline with Critical Path

| Week | Focus | Key Deliverables | Milestone |
|------|-------|------------------|-----------|
| **Weeks 1-4** | Core Infrastructure | - Multi-tenant architecture with RLS<br>- Basic authentication and profile system<br>- Initial story playback functionality | Architecture Review (Week 4) |
| **Weeks 5-8** | Story Creation | - AI story generation workflow<br>- French voice integration<br>- Basic moderation system<br>- **CNIL DPIA submission** | DPIA Approval (Week 8) |
| **Weeks 9-12** | Key Features | - Record-your-own functionality<br>- Dark-screen mode implementation<br>- Offline capabilities | Feature Complete (Week 12) |
| **Weeks 13-16** | QA & Launch Prep | - Performance optimization<br>- Final UI/UX refinement<br>- Security audit<br>- App store submission | **Beta Launch** |

### 14.2 Post-MVP Priorities

1. Enhanced analytics for retention optimization
2. Advanced parental controls and family management features
3. Additional cost optimization implementations
4. Curated content catalog through partnerships with French publishers (expanding beyond AI-only content)
5. Expanded AI creation tools and templates
6. Family sharing and collaboration features
7. Premium voice packs with celebrity narrators

---

## 15. Investment Case (Pre-Seed, France-first)

### 15.1 Elevator Thesis

> *"Talemo turns France's 'moins d'écrans' movement into a €1 B-plus exit play by letting kids **create**—not just consume—audio stories, wrapped in iron-clad CNIL compliance."*

A narrowly-scoped, four-month MVP proves that **creator-led engagement + €3.99 subscription** can reach break-even on < 300 k active families, then scales through hardware partnerships and EU expansion.

### 15.2 Market Opportunity

* **Target segment:** 4.3 million French households with children < 10 yrs.
* **Initial wedge:** 5 % penetration ⇒ **215 k MAU**.
* **Parental zeitgeist:** record sales of screen-free devices (Lunii, Tonies) signal enduring appetite for "audio-only" but none offer in-app creation.

### 15.3 Product & Moat

* **Differentiator:** mobile *creation-first* workflow (AI text→voice→illustration) unavailable on Lunii/Yoto.
* **Trust moat:** 100 % French SecNumCloud hosting + voluntary CNIL sandbox submission from Day 1.
* **Regulatory head-start:** built-in AI-labelling, parental dashboard and kid-safe moderation anticipated by EU AI Act.

### 15.4 Business Model & Unit Economics (Year 1)

| Driver                   | Target                   | Proof-Point                            |
| ------------------------ | ------------------------ | -------------------------------------- |
| Creator Premium price    | **€3.99 / month**        | Matches willingness-to-pay surveys     |
| Paid conversion          | **15 % of MAU**          | Benchmarked vs Roblox Edu templates    |
| ARR @ 5 % FR penetration | **€1.54 M** (€128 k MRR) | Profit pool large enough for seed KPIs |
| Gross margin             | **≥ 70 %**               | Story cost roadmap to €0.03 by Mo-6    |
| CAC (blended)            | **≤ €12**                | Paid-social + micro-influencer model   |
| CAC pay-back             | **< 6 months**           | LTV ≈ €48 vs CAC €12                   |

**Take-away:** With €12 CAC, 32 k subscribers generate €1.5 M ARR and €1.1 M gross profit—covering acquisition burn within Year 1.

### 15.5 Go-to-Market & Growth Loops

1. **100-family beta** to validate creation delight and D30 ≥ 35 %.
2. **France-only launch** leverages paid-social + referral loop bringing CAC to the €12 target.
3. **Hardware piggy-back:** SDK / revenue-share with Yoto, Tonies, Lunii turns potential competitors into zero-CAC funnels.

### 15.6 Execution Milestones

| Date         | Milestone                                    | Value Inflection                    |
| ------------ | -------------------------------------------- | ----------------------------------- |
| **Oct 2025** | 4-month MVP live; 100 families; D30 ≥ 35 %   | Team proves shipping cadence        |
| **Q1 2026**  | 5 k MAU soft-launch; CAC evidence ≤ €15      | Unlock seed round                   |
| **Q4 2026**  | 100 k MAU, 15 k subscribers; ARR ≈ €0.7 M    | Strategic interest triggers         |
| **2027**     | SDK live on first hardware; pan-EU expansion | Path to €4 M ARR (Series A trigger) |

### 15.7 Funding Plan & Returns

* **Raise now:** **€1.2 M** pre-seed at €4–5 M pre-money.
  * Runway 18 m: MVP build (€450 k), UA (€300 k), compliance & ops (€150 k), buffer (€300 k).
* **Exit paths (3–5 yr):** Yoto, Bayard, Spotify Kids, each identified with LOI sequencing.
* **Multiple:** strategic ed-tech / kids hardware deals clear 6–8× revenue; at €15 M ARR (EU roll-out) = **€90–120 M** exit.
* **Investor IRR:** pre-seed entry at €5 M → 20×-plus return within 5 yrs even at low-end €90 M outcome.

### 15.8 Key Risks & Mitigations

| Risk                               | Mitigation                                                                                      |
| ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| Creation usage lower than forecast | Run Wizard-of-Oz prototype before full build; narrow age band if needed.                        |
| CAC drifts > €18                   | Shift budget to hardware funnels & referral credits, lift price to €4.99 if retention supports. |
| AI generation costs stick at €0.06 | Margin still ≥ 55 %; maintain pay-back under 9 m.                                               |
| Regulatory delay                   | CNIL sandbox early, SecNumCloud chosen up-front.                                                |
| **Cold-start embeddings spike Postgres RAM** | Back-fill in 500-story batches; monitor `shared_buffers`, scale to 16 GB tier if cache miss > 5 %. |
| **False-positive duplicate blocks frustrate kids** | Log vetoes; auto-whitelist after parental override; tune cosine threshold weekly. |

### 15.9 Bottom Line

Talemo offers a **capital-efficient path to €1–2 M ARR inside 24 months**, a credible moat in regulatory compliance plus child-led creation, and multiple logical acquirers hungry for software IP in the booming screen-free audio space. A €1.2 M pre-seed today underwrites a realistic **10–20× return** on a five-year horizon.
