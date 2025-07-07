# Talemo – MVP Specifications

“A good MVP spec is like a Lego instruction booklet: enough structure that every team snaps pieces together the same way, but flexible enough that we can still add a new wing without tearing the whole castle apart.”

## Introduction 

### What is Talemo?
Talemo is a voice-first storytelling companion for children, with an optional parent dashboard for supervision, limits and insight. Children speak a few creative prompts; Talemo’s AI imagines and narrates an original audio story on the spot. The experience is deliberately progressive-disclosure: anyone can try it as a guest (“Copilot”), then families can unlock richer “Child-Solo” and “Parent Dashboard” features by creating an account.

### Why this MVP spec exists
One living document lets product, design, engineering, QA and legal stay aligned on:

Aspect	Where to look
Boundaries between layers	Domain Package Diagram
Exact user-facing screens & flows	Information Architecture tree
Non-negotiable data & safety rules	Telemetry Event Spec, QuotaService, ModerationService
“Definition of Done” quality gates	Accessibility Checklist, User Journey Smoke Tests

By freezing these slices early we de-risk infinite scope creep and unblock parallel work streams (API, UI kit, TTS pipeline) without waiting for fully-fleshed hi-fi mocks.

### Scope of the MVP
Included	Excluded / later phase
Guest storytelling with quota	Web text stories; comic export
Child-Solo voice wizard & playback	Multi-child profiles
Parent Dashboard with limits & history	In-app purchases / monetisation
English & French locale packs	Third-party story marketplace
Offline resilience & sync	Teacher / classroom multi-seat mode

### Success criteria
Time-to-first-story < 60 s on low-end Android tablets.

Story completion rate ≥ 70 % across guest users (Copilot).

≤ 1 % moderation false positives on curated prompt set.

Zero P0 accessibility bugs (all a11y checklist items ticked).

SyncManager exactly-once guarantee verified in offline smoke test #2.

### Guiding principles
Kids first – copy, visuals and flows assume an under-10 primary user.

Parent trust through transparency – limits, history and data export are obvious and friction-free.

Resilience over gracefulness – the product must work when bandwidth is poor; animation polish can come later.

Guardrails > perfect detection – quota, moderation and parental gate err on the side of safety.

Instrumentation from day one – every key action emits a deterministic, duplicate-safe telemetry event.



## Domain Package Diagram

```txt
[core/story-engine]  ← pure functions, no UI
[services]            ↳ QuotaService, ModerationService, OfflineQueue
[platform]            ↳ AuthRouter, RoleContext, Telemetry
[ui]                  ↳ StoryWizard, Playback, Dashboard
```
*Keeping UI free of business rules (= testable logic) limits regressions later.*

## Telemetry Event Specification

| Event | Required props |
|-------|---------------|
| story_started | mode, topic, hero, place, tool |
| story_completed | duration_sec, rating, quota_remaining |
| quota_exhausted | mode, quota_limit |
| moderation_blocked | stage, reason_code |

*Writing this now saves weeks of "hmm, which team logs what?" later.*

## Information Architecture 

```txt
🏠 Root Shell
├─ Global Components
│   ├─ ErrorBoundary     (component bugs → mascot fallback)
│   ├─ OperationalErrors (TTS fails, moderation blocked, network down → contextual toast/voice prompt)
│   ├─ OfflineQueueMgr   (persist jobs, retry on reconnection)
│   ├─ SyncManager       (orchestrates: batch outbound calls, exponential back-off, sync-in-progress flag)
│   ├─ ModeBanner        (mode status + switch CTA)
│   ├─ HelpDrawer        (tour • FAQ • contact)
│   ├─ AuthRouter        (guarded routes + RoleContext)
│   ├─ ModerationService (check prompt & story pre‑TTS)
│   ├─ NetworkAlert      (offline / retry toast + "Process when back online")
│   ├─ QuotaService      (useQuota() hooks, local persistence, backend sync)
│   └─ Telemetry         (events • perf traces)
│
├─ Resources
│   └─ i18nPrompts.json  (wizard voice strings, easy locale add‑ons)
│
├─ StoryLifecycle        (Idle → CollectingPrompts → Generating → Playing → Feedback → Done)
│
├─ Accessibility Checklist (Definition of Done items in Jira/Linear)
│   ├─ Voice equivalents for every ring / progress indicator
│   ├─ Text alternatives for icons ("Play", "Pause")
│   ├─ Focus order predictable when keyboard or switch-access is used
│   └─ Colour-blind-safe palette for quota rings
│   *Note: Devs can't move a ticket unless every a11y row is checked*
│
├─ Copilot Mode  (no login)
│   ├─ HomeCopilot       – "Start Story" CTA + quota ring
│   ├─ StoryWizard (shared, variant="touch")
│   │   ├─ Step1  Topic
│   │   ├─ Step2  Hero  (2 suggestions + free answer)
│   │   ├─ Step3  Place (2 suggestions + free answer)
│   │   └─ Step4  Tool  (2 suggestions + free answer)
│   ├─ StoryGenerating   – "J'imagine ton histoire…" + subtle spinner
│   ├─ StoryPlayback
│   │   ├─ PlayPause (big circle)
│   │   ├─ ProgressRing (time remaining)
│   │   ├─ ChangeStory
│   │   └─ StartNew
│   └─ EndOfStory        – FeedbackOnly
│       ├─ 👍 / 👎 rating buttons
│       ├─ "Dis‑le nous !" voice note capture (optional)
│       └─ Banner invite to create account (unobtrusive)
│
├─ Auth Flow  (optional)
│   ├─ SplashSignup        – benefit highlights
│   ├─ EmailPassword       / OAuthButtons
│   └─ AccountSuccess      – "Fly Alone unlocked!" confetti
│
└─ Supervised Stack  (requires account)
    ├─ Child‑Solo Mode  « Mode Conte »
    │   ├─ MicLaunch          (black screen + pulse mic)
    │   ├─ StoryWizard (shared, variant="voice")
    │   ├─ StoryGenerating   – "J'imagine ton histoire…" + subtle spinner
    │   ├─ StoryPlayback
    │   │   ├─ PlayPause (big circle)
    │   │   ├─ ProgressRing (time remaining)
    │   │   ├─ ChangeStory
    │   │   └─ StartNew
    │   └─ EndOfStory
    │       ├─ PostStoryPrompt   – Feedback (👍 / 👎 • voice comment)
    │       ├─ QuotaMeter        – shrinking ring / "2 stories left today"
    │       ├─ LimitReachedOverlay  – quota message + friendly mascot
    │       └─ ParentalGate
    │           ├─ Primary: FaceID / TouchID
    │           ├─ Secondary: Device PIN (via iOS/Android API)
    │           ├─ Fallback: Shared secret question (for older devices)
    │           └─ Security: 30s timeout, 3-attempt lockout to prevent shoulder-surfing
    │
    └─ Parent Dashboard
        ├─ HomeStats        – usage + quick‑create CTA (Best‑of chart default)
        │   └─ RequiresParentAuth<AdvancedFilters> (date range • content level) [hidden by chevron]
        ├─ HistoryList      – cloud stories
        │   └─ RequiresParentAuth<StoryDetail>     (prompts + moderation flags)
        ├─ RequiresParentAuth<LimitsControls>   – stories/day • minutes/day • content level
        └─ Settings
            ├─ Account
            ├─ Privacy & Data (GDPR / CNIL)
            └─ Legal / Credits
```

## User Journey Smoke Tests

1. **Guest story → account-upgraded parent**
   - Start in Copilot Mode
   - Complete story creation and playback
   - Respond to account creation banner
   - Verify access to Parent Dashboard features

2. **Child solo offline**
   - Enter Child-Solo Mode
   - Disconnect network
   - Create and play story
   - Verify OfflineQueueMgr captures events
   - Reconnect and confirm sync via SyncManager

3. **Quota hit at bedtime**
   - Use Child-Solo Mode until quota limit reached
   - Verify LimitReachedOverlay appears
   - Attempt ParentalGate access
   - Confirm quota settings in Parent Dashboard

4. **Parent bulk-deletes flagged story**
   - Access Parent Dashboard
   - Navigate to HistoryList
   - Identify and select flagged stories
   - Confirm deletion and verify telemetry events

5. **Network drop during playback**
   - Begin story playback
   - Disconnect network mid-playback
   - Verify NetworkAlert appears
   - Test resume functionality when reconnected

*This exercise often surfaces hidden states and missing components.*

--- 

# Appendix A — SyncManager

*Offline orchestration, deduplication & versioning*

> **Audience**: front‑end, back‑end, QA, Dev‑Ops.
> **Status**: Draftv0.2 —awaiting backend review (ETA2025‑07‑10).

---

## Purpose

Provide a **single façade** that batches and retries *all* client‑originated writes while the device is offline, flaky, or rate‑limited, guaranteeing:

1. **Exactly‑once semantics** on the server
2. **Deterministic conflict resolution** when two devices edit the same logical record
3. **Predictable back‑off behaviour** shared across feature modules

SyncManager frees individual services (Quota, Telemetry, OfflineQueue, Moderation flags) from hand‑rolled retry logic and unifies observability.

## Scope

| Included                                                                                  | Excluded / future                                                                          |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| 🔹 Quota counters<br>🔹 Story JSON metadata<br>🔹 Telemetry events<br>🔹 Moderation flags | 🔸 Audio blob upload (handled by ChunkUploader)<br>🔸 Remote‑config fetch (idempotent GET) |

## Responsibilities

* **Queue** outbound envelopes to disk (IndexedDB) with durable ordering.
* **Flush** envelopes in controlled batches with exponential back‑off + jitter.
* **Dedupe** requests on both client and server via idempotency keys.
* **Invoke conflict handlers** supplied by domain packages.
* **Expose** `syncStatus`, `pendingCount`, `lastError` to UI (*NetworkAlert*).

Non‑responsibilities: encryption at rest (delegated to Service Worker “crypto vault” TBD), feature flag gating, analytics sampling logic.

## Envelope Schema

```ts
interface OutboundEnvelope {
  id: string;          // ULID = time‑sortable idempotency key
  domain: "quota" | "story" | "telemetry" | "moderation";
  payload: unknown;    // JSON‑serialisable
  rev: number;         // monotonically increasing per‑resource revision
  ts_created: number;  // epoch ms (debug only)
  attempts: number;    // retry count for back‑off
}
```

*`id` + `domain` form the server de‑duplication tuple (24h TTL).*
ULID keeps local queue chronologically sortable even after reboot.

## Queue Storage & Durability

* Stored in **IndexedDB** `talemo.sync.queue` object store.
* Write‑ahead log style: append only, delete on ACK.
* Corruption fallback: if IndexedDB throws, clear store & emit `sync_queue_reset` †.

† QA team adds a chaos test that forcibly wipes the store mid‑session.

## Flush Algorithm

```text
onOnline || onTimerTick -> flush()
flush():
  batch = first 50 envelopes ORDER BY ts_created
  POST /sync/batch batch
  switch (server response):
    ok | dup      -> delete from store
    conflict      -> merged = domain.merge(); save merged (rev++)
    error 429/503 -> backOff *= 2, jitter ±20 %, re‑queue
    error fatal   -> log + drop + emit operational_error
```

Back‑off capped at **120s**. `attempts` resets to0 after any success.

## Versioning & ConflictRules

| Domain    | Client field | Server field | Merge rule                                                                                                           |
| --------- | ------------ | ------------ | -------------------------------------------------------------------------------------------------------------------- |
| Story     | `rev`        | `server_rev` | Keep payload with **highest rev**.<br>If equal but hash diff → mark `conflict:true`, enqueue `story_conflict` event. |
| Quota     | `day_seq`    | same         | Server keeps **MAX(used)** for that YYYY‑MM‑DD.                                                                      |
| Telemetry | `id`         | –            | Fire & forget; server ignores duplicates.                                                                            |

Server rejects any envelope where `rev < server_rev` for mutable resources.

## Back‑off Formula

```
interval  = min( 2s * 2^attempts , 120s )
interval += random(‑0.2 .. +0.2 * interval)
```

Shared across all domains to avoid “thundering herd” after network restore.

## API Contract

`POST /sync/batch` — accepts **1‑100** envelopes.

Response example:

```jsonc
{
  "ok":       ["01HB…"],
  "dup":      ["01HB…"],
  "conflict": ["01HB…"],
  "error":    [{"id":"01HB…","code":503}]
}
```

Headers: `X‑Device‑Id` (UUID), `Authorization` (JWT).
Server guarantees idempotent processing keyed by `id` + `domain` for 24h.

## Observability & Alerting

| Metric            | Target          | Dashboard                |
| ----------------- | --------------- | ------------------------ |
| Sync success rate | ≥98% last7d | Kibana ➜ *SyncHealth*   |
| Avg batch latency | ≤200ms p95    | same                     |
| Conflict ratio    | <0.1%         | same (alert >0.5%)     |
| Queue size > 500  | PagerDuty warn  | OpsGenie + Slack #alerts |

Telemetry events emitted: `sync_batch_sent`, `sync_batch_result`, `sync_queue_reset`.

## Security & Data Protection

1. **Envelope payloads encrypted at rest** – AES‑GCM via WebCrypto (2025‑Q4 stretch).
2. **JWT quota token** includes daily nonce to prevent replay (see QuotaService doc).
3. **CSRF** not applicable — mobile app / PWA uses same‑origin fetch with JWT.

## Open Questions

1. Should story **audio blobs** piggy‑back on envelopes or stay with current S3 presign flow?
2. Is 24h idempotency TTL sufficient for week‑long offline trips?
3. Where to surface `story_conflict` in Parent Dashboard UI?