# Talemo – MVP Wireframe

Information Architecture 

```aiignore
🏠 Root Shell
├─ Global Components
│   ├─ ErrorBoundary     (wraps Wizard & Playback; mascot fallback)
│   ├─ OfflineQueueMgr   (persist jobs, retry on reconnection)
│   ├─ ModeBanner        (mode status + switch CTA)
│   ├─ HelpDrawer        (tour • FAQ • contact)
│   ├─ AuthRouter        (guarded routes + RoleContext)
│   ├─ ModerationService (check prompt & story pre‑TTS)
│   └─ NetworkAlert      (offline / retry toast + "Process when back online")
│
├─ Resources
│   └─ i18nPrompts.json  (wizard voice strings, easy locale add‑ons)
│
├─ Copilot Mode  (no login)
│   ├─ HomeCopilot       – “Start Story” CTA + quota ring
│   ├─ StoryWizard (global)
│   │   ├─ Step1  Topic
│   │   ├─ Step2  Hero  (2 suggestions + free answer)
│   │   ├─ Step3  Place (2 suggestions + free answer)
│   │   └─ Step4  Tool  (2 suggestions + free answer)
│   ├─ StoryGenerating   – “J’imagine ton histoire…” + subtle spinner
│   ├─ StoryPlayback
│   │   ├─ PlayPause (big circle)
│   │   ├─ ProgressRing (time remaining)
│   │   ├─ ChangeStory
│   │   └─ StartNew
│   └─ EndOfStory        – FeedbackOnly
│       ├─ 👍 / 👎 rating buttons
│       ├─ “Dis‑le nous !” voice note capture (optional)
│       └─ Banner invite to create account (unobtrusive)
│
├─ Auth Flow  (optional)
│   ├─ SplashSignup        – benefit highlights
│   ├─ EmailPassword       / OAuthButtons
│   └─ AccountSuccess      – “Fly Alone unlocked!” confetti
│
└─ Supervised Stack  (requires account)
    ├─ Child‑Solo Mode  « Mode Conte »
    │   ├─ MicLaunch          (black screen + pulse mic)
    │   ├─ StoryWizard (voice‑only, dark UI)
    │   │   ├─ Step1  Topic
    │   │   ├─ Step2  Hero  (2 suggestions + free answer)
    │   │   ├─ Step3  Place (2 suggestions + free answer)
    │   │   └─ Step4  Tool  (2 suggestions + free answer)
    │   ├─ StoryGenerating   – “J’imagine ton histoire…” + subtle spinner
    │   ├─ StoryPlayback
    │   │   ├─ PlayPause (big circle)
    │   │   ├─ ProgressRing (time remaining)
    │   │   ├─ ChangeStory
    │   │   └─ StartNew
    │   └─ EndOfStory
    │       ├─ PostStoryPrompt   – Feedback (👍 / 👎 • voice comment)
    │       ├─ QuotaMeter        – shrinking ring / “2 stories left today”
    │       ├─ LimitReachedOverlay  – quota message + friendly mascot
    │       └─ ParentalGateExit     – long‑press corner + FaceID/PIN
    │
    └─ Parent Dashboard
        ├─ HomeStats        – usage + quick‑create CTA (Best‑of chart default)
        │   └─ AdvancedFilters (date range • content level) [hidden by chevron]
        ├─ HistoryList      – cloud stories
        │   └─ StoryDetail     (prompts + moderation flags)
        ├─ LimitsControls   – stories/day • minutes/day • content level
        └─ Settings
            ├─ Account
            ├─ Privacy & Data (GDPR / CNIL)
            └─ Legal / Credits

```
