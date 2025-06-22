# Product Requirements Document (PRD)

## 1. Document Control

| Item          | Value                                           |
| ------------- | ----------------------------------------------- |
| **Product**   | Family Audio-Stories Platform                   |
| **Version**   | 0.3 (Validated with GTM/VC Lens)                |
| **Author**    | Product Team / CTO                              |
| **Date**      | 22 Jun 2025                                     |
| **Reviewers** | Engineering, Design, Marketing, Legal, Strategy |

---

## 2. Executive Summary

A **mobile-first** web and companion mobile application enabling families to browse, search, listen to, and create short audio stories. The platform uses **Django (MVT)**, **PostgreSQL**, **Celery**, **MinIO**, and an **agentic framework (CrewAI)** for content-generation workflows. Enterprise-grade **SSO (Google & Apple Sign-In)** and role-based access control (RBAC) are required. Assets (audio, images) are stored locally via MinIO but the stack must remain cloud-portable. Agentic design extends to internal workflows and public-facing AI assistants.

The platform targets a growing segment of families seeking high-quality screen-light entertainment. It combines AI creativity, safety, and mobile-first convenience.

---

## 3. Goals & Non-Goals

### Goals

1. Deliver an intuitive, mobile-first experience for families to **discover** and **listen** to audio stories.
2. Provide creators/admins a workflow to **generate new stories** (text → audio + illustration) via CrewAI, with asynchronous processing.
3. Implement **enterprise authentication & authorization** with Google SSO and Apple Sign-In, extensible to SAML/OIDC.
4. Ensure the platform is **cloud-agnostic**: local MinIO for development/on-prem, quick swap to S3/GCS/Azure.
5. Offer an admin UI to manage stories, assets, and metadata.
6. Leverage **agent-based architecture** for modular content generation, moderation, and story discovery.
7. Prepare for **freemium subscription model**, **B2B licensing**, and potential **IP partnerships**.

### Non-Goals

* Full public social network features (likes, comments, etc.) — deferred.
* Native desktop experience — focus is mobile & responsive web plus future mobile app wrappers.

---

## 4. Success Metrics

| Metric                                 | Target                             |
| -------------------------------------- | ---------------------------------- |
| 🟢 **Time-to-First-Play** (new user)   | < 30 s                             |
| 🟢 **Story Search Success**            | ≥ 90 % (search results clicked)    |
| 🟢 **Story Generation Lead Time**      | ≤ 2 min (submission → audio ready) |
| 🟢 **Mobile PWA Lighthouse Perf**      | ≥ 85                               |
| 🟢 **Net Promoter Score (NPS)**        | ≥ 50                               |
| 🟢 **Customer Acquisition Cost (CAC)** | ≤ €6                               |
| 🟢 **LTV / CAC Ratio**                 | ≥ 3.5x                             |

---

## 5. Personas & Use Cases

* **Parent (Amélie, 38)** – finds bedtime stories quickly on phone, filters by length (<10 min) or theme.
* **Child (Léo, 8)** – selects story by colourful card, taps play.
* **Story Creator (Lucas, 30)** – writes text, triggers AI to generate assets; revises metadata.
* **Admin** – bulk-edits stories, reviews flagged content.
* **Story Assistant User** – chats with a story-building AI to co-create new adventures.
* **School/Daycare Buyer** – explores institutional subscription with curriculum-safe filtering.

---

## 6. Functional Requirements

* Story Listing Page with filters, search, and creation link
* Story Detail Page with image, audio player, and metadata
* Story Creation Page (form + agentic generation trigger)
* Admin Dashboard with CRUD access to stories, metadata, user management
* User Authentication with SSO (Google & Apple)
* Agentic Assistant Interface (for story co-creation)

---

## 7. Agent Architecture

* **Internal Agents**:

  * `StoryBuilderAgent`: orchestrates text to image + audio + metadata
  * `TTSAgent`: handles voice synthesis via local/3rd-party model
  * `ImageGenAgent`: generates illustrations from story text
  * `MetadataAgent`: auto-tags stories with category, length, age range
  * `ModerationAgent`: flags NSFW or age-inappropriate content

* **User-facing Agents**:

  * `StoryCompanion`: co-creation chat assistant for families
  * `SearchAssistant`: conversational assistant to surface content

---

## 8. Information Architecture / Data Model

### Key Entities:

* **Story**: id, title, description, image, audio, tags, language, age\_range, duration, created\_by, is\_published
* **User**: id, name, email, role, auth\_provider
* **AgentTask**: id, agent\_type, input, output, status, created\_at, executed\_at
* **Asset**: id, type (image/audio), file\_path, source\_task

---

## 9. UX Flows (Outline)

* **Discover Story** → Search > Filter > Click > Play
* **Create Story** → New > Form > Trigger Agent > Preview > Save
* **Edit Story (Admin)** → List > Edit > Save
* **Story Assistant Flow** → Chat > Fill > Generate > Review

---

## 10. Technical Architecture

* Backend: Django + Django REST + PostgreSQL
* Async: Celery + Redis
* Agentic Framework: CrewAI
* Storage: MinIO (local/dev), S3-compatible
* SSO: Google, Apple; extensible to SAML/OIDC
* Frontend: HTMX / Bootstrap 5
* Mobile App Packaging: CapacitorJS (for native PWA bundling on iOS/Android)
* Hosting: cloud-agnostic (Docker/Kubernetes-ready)

## 10.1 Mobile App Architecture & Strategy

To ensure an optimal experience across platforms, the application will follow a **PWA-first strategy** with the option to deliver **store-ready native wrappers**.

### Architecture Considerations

* **Progressive Web App (PWA)**: Core experience delivered as a responsive web app using Django templates + Bootstrap 5 + HTMX, designed to function offline via a service worker and manifest.
* **Capacitor Wrapping (Optional)**: Enables packaging the web app into installable native iOS and Android apps. This approach supports native APIs such as push notifications, media playback, and native sign-in dialogs.
* **SSO Integration**: Web-based SSO (Google, Apple) will be integrated using `django-allauth`. In Capacitor wrappers, native SSO flows may be embedded using Capacitor plugins.
* **Mobile Responsiveness**: Achieved through Bootstrap 5, ensuring family-friendly mobile UX with scalable text, tappable buttons, and low-load times.
* **Interactivity with HTMX**: Enables AJAX-style dynamic updates for search, filtering, and story playback, avoiding full page reloads.
* **Store Compliance**:

  * Offline functionality via service worker (Apple/Google requirement)
  * Avoids external browser redirections
  * GDPR and COPPA-compliant UX flows

### Developer Tools & Distribution

* **Build Tools**: Django for backend, Docker for deployment, Celery for background jobs
* **Distribution**: PWA install prompts + optional App Store / Play Store deployment through Capacitor build pipelines
* **Monitoring & Analytics**: Add PWA analytics compatible with privacy standards (e.g., Plausible or Matomo)

All frontends will follow a **single source of truth** using Django’s templating system and shared CSS/JS assets, reducing maintenance overhead and allowing synchronized feature releases between web and mobile.

---

## 11. APIs & Interfaces

* REST APIs:

  * `/api/stories/`, `/api/stories/<id>/`
  * `/api/assets/`, `/api/agents/trigger/`
* Webhooks:

  * For Celery job completion (story ready)
* Agent Bridge:

  * Internal API between Django + CrewAI layer

---

## 12. Security & Access Control

* RBAC:

  * Roles: Guest, Registered, Creator, Admin
* Authentication:

  * SSO via Google / Apple + token fallback
* File Access:

  * Signed URL for asset delivery
* Compliance:

  * GDPR, COPPA; opt-in for data collection

---

## 13. Admin Features

* Admin CRUD on stories, users, tags, assets
* Status dashboard for Celery tasks + agent jobs
* Manual moderation & content flagging tools
* Content preview & scheduling

---

## 14. Go-To-Market Plan

| Stage     | Tactics                                                                                                                 |
| --------- | ----------------------------------------------------------------------------------------------------------------------- |
| Beta      | 500 families via parenting newsletters, teachers, Facebook groups. Referral loop: 1 free premium story for each signup. |
| Launch    | App Store + Google Play + PWA, influencer storytelling packs, launch campaign with free 7-day premium.                  |
| B2B       | Outreach to daycare networks, family apps, and educational resellers. Embed IP licensing into discovery stories.        |
| Expansion | Localized editions (FR, ES, DE). Stories generated or curated per language.                                             |

---

## 15. Monetization & Business Model

* **Freemium** model: free tier (access to 5 rotating stories/week), Premium (€4.99/month) unlocks full access + unlimited creation.
* **À-la-carte** purchase option for special packs (e.g., bedtime, adventure, licensed IP).
* **B2B licensing**: institutions pay per seat (€1–2/student/month) or flat fee.
* Future: voice merchandising, branded stories, parental gifting.

---

## 16. Compliance & Safety

* **Privacy & Safety**: Full compliance with GDPR and COPPA. Parental consent flows. No child data stored.
* **Content moderation**: AI moderation agent + manual review fallback. Age-appropriate filters.
* **Usage analytics**: Anonymized tracking only. Explicit opt-in for suggestions.

---

## 17. App Store Compliance Strategy

* The mobile app (PWA or Capacitor-wrapped) will meet Apple and Google guidelines:

  * Offline support (service worker)
  * Touch-optimized, responsive Bootstrap 5 UI
  * Native-like navigation with HTMX
  * Optional use of Capacitor plugins for notifications and media
  * No redirection to external browser
  * GDPR/COPPA consent and privacy policies embedded

---

## 18. Open Strategic Questions

1. Which regional market do we launch in first: France or multilingual (EN)?
2. What minimum licensing must we secure before adding well-known characters/IPs?
3. Should we prioritize mobile app downloads over PWA adoption in initial GTM?
4. Should we enable public sharing of user-created stories in Phase 1?

---

## 19. Next Steps (Pre-Implementation)

| Area                       | Action Item                                              | Owner             |
| -------------------------- | -------------------------------------------------------- | ----------------- |
| 🎯 **Market Sizing**       | TAM/SAM/SOM validation (family audio market)             | Strategy Lead     |
| 💸 **Pricing Simulation**  | Model CAC, conversion, LTV; test premium tiers           | Product + Finance |
| 📢 **GTM Assets**          | Prepare launch website, teaser video, social ads         | Marketing         |
| 🔐 **Compliance Audit**    | External review for GDPR/COPPA adherence                 | Legal             |
| 🎨 **Voice Licensing**     | Secure license or verify open use for voice/music assets | BizDev            |
| 📦 **MVP Tech Stack POC**  | Validate Celery + CrewAI orchestration + fallback        | Engineering       |
| 📱 **Mobile UX Prototype** | Test story discovery + generation with real families     | Product/UX        |
