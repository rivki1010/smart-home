#!/bin/bash

# 1. הגדרת סביבת המקור והיעד
SOURCE_DIR="/tmp/8ddb32529188e1c" # נתיב זמני של Oryx
DEPLOYMENT_TARGET="/home/site/wwwroot"

# 2. הרצת תהליך הבנייה הסטנדרטי של Oryx
/bin/oryx build $SOURCE_DIR -o $DEPLOYMENT_TARGET --platform python --platform-version 3.12

# 3. התקנת FFMPEG
echo "--- Installing FFMPEG ---"
apt-get update
apt-get install -y ffmpeg

echo "--- Deployment finished ---"