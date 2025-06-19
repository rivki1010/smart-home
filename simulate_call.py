import requests
import os
import http.server
import socketserver
import threading
import time

# --- הגדרות ---
BRAIN_SERVER_URL = "http://127.0.0.1:5001/api/call"
AUDIO_FILE_PATH = "test_audio.wav"
SIMULATOR_PORT = 8080 # פורט שבו נגיש את קובץ האודיו

# --- קוד שמריץ שרת קבצים קטן ברקע ---
class FileServerThread(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.httpd = None
        self.daemon = True # אפשר לסגור את התוכנית גם אם השרשור עדיין רץ

    def run(self):
        Handler = http.server.SimpleHTTPRequestHandler
        try:
            with socketserver.TCPServer(("", self.port), Handler) as self.httpd:
                print(f">>> שרת קבצים זמני רץ ברקע בפורט {self.port}")
                self.httpd.serve_forever()
        except Exception as e:
            print(f"XXX שרת קבצים זמני נכשל: {e}")

    def stop(self):
        if self.httpd:
            print(">>> מכבה את שרת הקבצים הזמני...")
            self.httpd.shutdown()
            self.httpd.server_close()

# --- התהליך הראשי ---
if __name__ == "__main__":
    if not os.path.exists(AUDIO_FILE_PATH):
        print(f"XXX שגיאה: קובץ '{AUDIO_FILE_PATH}' לא נמצא!")
        exit()

    # 1. הפעלת שרת הקבצים ברקע
    server_thread = FileServerThread(SIMULATOR_PORT)
    server_thread.start()
    time.sleep(1) # נותנים לשרת שנייה לעלות

    # 2. בניית הקישור לקובץ האודיו המקומי שלנו
    # ימות המשיח ישלחו כתובת IP, אבל בבדיקה מקומית 127.0.0.1 מספיק
    recording_url = f"http://127.0.0.1:{SIMULATOR_PORT}/{AUDIO_FILE_PATH}"
    print(f">>> מדמה שיחה עם קישור לקובץ: {recording_url}")

    # 3. שליחת הבקשה לשרת המוח שלנו
    print(f"\n>>> שולח בקשה לשרת המוח...")
    params = {'ApiRecordFile': recording_url}

    try:
        response = requests.post(BRAIN_SERVER_URL, data=params)
        print(f">>> שרת המוח ענה (סטטוס {response.status_code}):")
        print(response.text)
    except Exception as e:
        print(f"XXX שגיאה בפנייה לשרת המוח: {e}")
    finally:
        # 4. כיבוי שרת הקבצים
        server_thread.stop()