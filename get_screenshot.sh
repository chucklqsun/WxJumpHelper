adb shell screencap -p | perl -pe 's/\x0D\x0A/\x0A/g' > screenshot.png
