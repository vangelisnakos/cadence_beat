[app]

# (str) Title of your application
title = CadenceBeat

# (str) Package name
package.name = cadenceapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.vangelis

# (str) Source code where the main.py lives
source.dir = src

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,wav
source.include_patterns = main.py, packages/*, data/*

# (str) Application versioning
version = 0.1

# (list) Application requirements
p4a.branch = master
requirements = python3==3.10, kivy

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (str) Custom text/icon colors if used in your app
# color = 0.8,0.65,0.1,1
# text_color = 0.1,0.1,0.1,1

# (str) Presplash & icon paths (optional)
# presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/images/icon.png


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1


[android]

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
