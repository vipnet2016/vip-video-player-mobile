[app]

# Application name
title = VIP多线路播放器
package.name = videoplayer
package.domain = com.example

# Source code
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Version
version = 1.0
requirements = python3,kivy

# Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Orientation; possible values: all, landscape, portrait or sensor
orientation = portrait

# Icons and splash
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/splash.png

# Build options
android.archs = arm64-v8a
android.minapi = 21
android.api = 30

# Services (if needed)
# services = NAME:ENTRY_POINT_SPEC

# AndroidX disabled to avoid gradle issues
android.enable_androidx = False
android.enable_jar_warning = False
android.accept_sdk_license = True
# Use ant instead of gradle
# android.gradle_enabled = False  # May not be supported in this version
android.gradle_dependencies_enabled = False

[buildozer]

# Log level (2=verbose, 1=info, 0=warning)
log_level = 2

# Directory to build in
# build_dir = /tmp/buildozer

# Directory to copy built apk to
# bin_dir = ./bin

# Whether to delete the build and/or bin dir before building
# clean_build = True
# clean_bin = True

# Whether to clean the python-install inside the build when restarting
# clean_python_install = True

# Whether to install the package on the device when deploying
# install_only = True

# Whether to connect to a remote device via adb
# remote_conn = myhost:22

# Whether to enable backups
# backup = True

# Target platform
target = android

# Whether to use the private copy of python
# private_storage = True

# Extra environment variables to set
# extra_env_vars = MYVAR=value

# Extra paths to set in PATH
# extra_paths = /opt/bin

# Extra scripts to run before build
# prebuild_scripts = script1.sh, script2.sh

# Extra scripts to run after build
# postbuild_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution build
# postbuild_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK build
# postbuild_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution cleaning
# postclean_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK cleaning
# postclean_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution deploy
# postdeploy_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK deploy
# postdeploy_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution run
# postrun_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK run
# postrun_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution serve
# postserve_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK serve
# postserve_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution update
# postupdate_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK update
# postupdate_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution uninstall
# postuninstall_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK uninstall
# postuninstall_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution install
# postinstall_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK install
# postinstall_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution debug
# postdebug_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK debug
# postdebug_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution release
# postrelease_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK release
# postrelease_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution logcat
# postlogcat_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK logcat
# postlogcat_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution clean
# postclean_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK clean
# postclean_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution build
# postbuild_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK build
# postbuild_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution deploy
# postdeploy_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK deploy
# postdeploy_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution run
# postrun_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK run
# postrun_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution serve
# postserve_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK serve
# postserve_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution update
# postupdate_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK update
# postupdate_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution uninstall
# postuninstall_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK uninstall
# postuninstall_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution install
# postinstall_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK install
# postinstall_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution debug
# postdebug_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK debug
# postdebug_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution release
# postrelease_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK release
# postrelease_apk_scripts = script1.sh, script2.sh

# Extra scripts to run after distribution logcat
# postlogcat_dist_scripts = script1.sh, script2.sh

# Extra scripts to run after APK logcat
# postlogcat_apk_scripts = script1.sh, script2.sh