# Talemo – MVP Wireframe

Information Architecture 

```aiignore
🏠 Root Shell
├─ Global Components
│   ├─ ErrorBoundary     (component bugs → mascot fallback)
│   ├─ OperationalErrors (TTS fails, moderation blocked, network down → contextual toast/voice prompt)
│   ├─ OfflineQueueMgr   (persist jobs, retry on reconnection)
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
├─ Accessibility Checklist
│   ├─ Voice equivalents for every ring / progress indicator
│   ├─ Text alternatives for icons ("Play", "Pause")
│   ├─ Focus order predictable when keyboard or switch-access is used
│   └─ Colour-blind-safe palette for quota rings
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
    │       └─ ParentalGateExit     – long‑press corner + FaceID/PIN
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