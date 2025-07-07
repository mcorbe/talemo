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