[app]

# (str) Title of your application
title = Cadence Beat

# (str) Package name
package.name = CadenceBeat

# (str) Package domain (needed for android/ios packaging)
package.domain = org.vangelis

# (str) Source code where the main.py lives
source.dir = src
source.include_dirs = src/packages, src/data

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,wav,kv
source.include_patterns = main.py, packages/**, data/**

android.add_assets = src/data

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
p4a.branch = master
requirements = python3,kivy==2.3.1,filetype

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (str) Custom text/icon colors if used in your app
# color = 0.8,0.65,0.1,1
# text_color = 0.1,0.1,0.1,1

# (str) Presplash & icon paths (optional)
presplash.filename = src/data/images/icon.png
icon.filename = src/data/images/icon.png


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1


[android]

android.services = audio
android.service_files = src/service_audio:service_audio

# (int) Target Android API
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (str) Paths to your system SDK/NDK
android.ndk_path = /home/vangelis/.buildozer/android/platform/android-ndk-r25b
android.sdk_path = /home/vangelis/Android/Sdk

# (str) Path to sdkmanager (fix for WSL)
android.sdkmanager_path = /home/vangelis/Android/Sdk/cmdline-tools/latest/bin/sdkmanager
android.cmdline_tools_path = /home/vangelis/Android/Sdk/cmdline-tools/latest

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Copy library instead of making libpymodules.so
android.copy_libs = 1

# (bool) Enable Android auto backup feature (API >=23)
android.allow_backup = True

# Build
# source buildozer-venv/bin/activate
# buildozer android debug

# Get Android logs
# Tap 7 times on build number
# Turn on USB debugging
# Open terminal at cadence_beat
# ./adb logcat -s python
