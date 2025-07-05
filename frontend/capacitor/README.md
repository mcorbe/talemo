# CapacitorJS Native App Wrappers

This directory contains the configuration for wrapping the Talemo PWA into native applications for iOS and Android using CapacitorJS.

## Overview

CapacitorJS is a cross-platform native runtime that makes it easy to build web apps that run natively on iOS, Android, and the web. It provides a consistent, web-focused set of APIs that enable an app to stay as close to web standards as possible while accessing the full native capabilities of each platform.

## Setup Instructions

### Prerequisites

- Node.js 14+ and npm
- For Android:
  - Android Studio
  - Android SDK
  - Java Development Kit (JDK) 11+
- For iOS:
  - Xcode 13+
  - CocoaPods
  - macOS

### Installation

1. Navigate to the capacitor directory:
   ```
   cd frontend/capacitor
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Initialize Capacitor:
   ```
   npm run init
   ```

4. Add platforms:
   ```
   npm run add-android
   npm run add-ios
   ```

### Development Workflow

1. Make changes to the PWA in the Django project
2. Sync changes to native projects:
   ```
   npm run sync
   ```

3. Open native projects in their respective IDEs:
   ```
   npm run open-android
   npm run open-ios
   ```

4. Build native apps:
   ```
   npm run build-android
   npm run build-ios
   ```

## Native Plugins

The following native plugins have been configured:

### Core Plugins

- **SplashScreen**: Displays a splash screen during app launch
- **PushNotifications**: Enables push notifications on native platforms

### Additional Plugins

To add more plugins, install them using npm and update the capacitor.config.json file:

```bash
npm install @capacitor/plugin-name
npx cap sync
```

## Platform-Specific Configurations

### Android

Android-specific configurations are defined in the `android` section of capacitor.config.json. Additional configurations can be made in the generated Android project after running `npm run add-android`.

Key files for customization:
- `android/app/src/main/AndroidManifest.xml`: App permissions and configurations
- `android/app/src/main/res/values/strings.xml`: App name and other strings
- `android/app/build.gradle`: App dependencies and build configurations

### iOS

iOS-specific configurations are defined in the `ios` section of capacitor.config.json. Additional configurations can be made in the generated iOS project after running `npm run add-ios`.

Key files for customization:
- `ios/App/App/Info.plist`: App permissions and configurations
- `ios/App/App/AppDelegate.swift`: App initialization code
- `ios/App/Podfile`: iOS dependencies

## App Store Submissions

### Google Play Store

1. Generate a signed APK or App Bundle:
   - Open the project in Android Studio
   - Build > Generate Signed Bundle/APK
   - Follow the wizard to create a signing key and generate the release build

2. Prepare store listing:
   - App name: Talemo
   - Short description: Family Audio Stories
   - Full description: Discover, listen to, and co-create short audio stories for families
   - Screenshots from various devices
   - Feature graphic and icon

3. Complete the content rating questionnaire

4. Set up pricing and distribution

### Apple App Store

1. Create an app record in App Store Connect

2. Prepare the app for submission:
   - Open the project in Xcode
   - Update signing and capabilities
   - Set the correct bundle identifier and version
   - Archive the app (Product > Archive)

3. Prepare store listing:
   - App name: Talemo
   - Subtitle: Family Audio Stories
   - Description: Discover, listen to, and co-create short audio stories for families
   - Screenshots from various devices
   - App icon

4. Complete the App Review Information section

5. Submit for review

## Troubleshooting

### Common Issues

1. **Capacitor sync fails**:
   - Ensure the webDir path in capacitor.config.json is correct
   - Check that the static directory contains the PWA files

2. **Android build fails**:
   - Check Android SDK and JDK versions
   - Ensure all required Android SDK components are installed

3. **iOS build fails**:
   - Ensure Xcode command-line tools are installed
   - Check that CocoaPods is properly installed
   - Run `pod install` in the ios/App directory

## Resources

- [Capacitor Documentation](https://capacitorjs.com/docs)
- [Android Developer Documentation](https://developer.android.com/docs)
- [iOS Developer Documentation](https://developer.apple.com/documentation/)