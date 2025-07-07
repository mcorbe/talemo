# Talemo – MVP Wireframe

Information Architecture 

```aiignore
🏠 Root Shell
├─ Global Components
│   ├─ ModeBanner      (mode status + switch CTA)
│   ├─ HelpDrawer      (tour • FAQ • contact)
│   ├─ AuthRouter      (guarded routes + RoleContext)
│   └─ NetworkAlert    (offline / retry toast)
│
├─ Copilot Mode  (no login)
│   ├─ HomeCopilot       – “Start Story” CTA
│   ├─ WizardCopilot (global)
│   │   ├─ Step1  Topic
│   │   ├─ Step2  Hero (2 suggestions + free answer)
│   │   ├─ Step3  Place (2 suggestions + free answer)
│   │   └─ Step4  Tool  (2 suggestions + free answer)
│   ├─ GeneratingScreen   – “J’imagine ton histoire…” + subtle spinner
│   ├─ CloudPlayback
│   │   ├─ PlayPause (big circle)
│   │   ├─ ProgressRing (time remaining)
│   │   ├─ ChangeStory
│   │   └─ StartNew
│   └─ EndOfStory        – **FeedbackOnly**
│       ├─ 👍 / 👎 rating buttons
│       ├─ “Dis‑le nous !” voice note capture (optional)
│       └─ Banner invite to create account (unobtrusive)
│
├─ Auth Flow  (optional)
│   ├─ SplashSignup        – benefit highlights
│   ├─ EmailPassword       /  OAuthButtons
│   └─ AccountSuccess      – “Fly Alone unlocked!” confetti
│
└─ Supervised Stack  (requires account)
    ├─ Child‑Solo Mode  « Mode Conte »
    │   ├─ MicLaunch          (black screen + pulse mic)
    │   ├─ WizardSolo (voice‑only, dark UI)
    │   │   ├─ Step1  Topic
    │   │   ├─ Step2  Hero (2 suggestions + free answer)
    │   │   ├─ Step3  Place (2 suggestions + free answer)
    │   │   └─ Step4  Tool  (2 suggestions + free answer)
    │   ├─ GeneratingScreen   – “J’imagine ton histoire…” + subtle spinner
    │   ├─ CloudPlayback
    │   │   ├─ PlayPause (big circle)
    │   │   ├─ ProgressRing (time remaining)
    │   │   ├─ ChangeStory
    │   │   └─ StartNew
    │   └─ EndOfStory
    │       ├─ PostStoryPrompt   – Feedback (👍 / 👎 • voice comment)
    │       ├─ LimitReachedOverlay  – quota message + friendly mascot
    │       └─ ParentalGateExit     – long‑press corner + FaceID/PIN
    │
    └─ Parent Dashboard
        ├─ HomeStats        – usage + quick‑create CTA
        ├─ HistoryList      – cloud stories
        │   └─ StoryDetail     (prompts + moderation flags)
        ├─ LimitsControls   – stories/day • minutes/day • content level
        └─ Settings
            ├─ Account
            ├─ Privacy & Data (GDPR / CNIL)
            └─ Legal / Credits
```
