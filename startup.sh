#!/bin/bash
#!בדיקה 
# שלב 1: ניסיון להתקין את FFMPEG
echo "--- Attempting to install FFMPEG ---"
apt-get update -y && apt-get install -y ffmpeg

# שלב 2: בדיקה קריטית אם ההתקנה הצליחה
if ! [ -x "$(command -v ffmpeg)" ]; then
  echo '--- FATAL ERROR: FFMPEG installation failed. Exiting. ---' >&2
  exit 1
fi

# שלב 3: רק אם ההתקנה הצליחה, הפעל את השרת
echo "--- FFMPEG found. Starting Gunicorn... ---"
gunicorn --bind=0.0.0.0:8000 "brain_server:app"