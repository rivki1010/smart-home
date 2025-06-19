import requests
import json

# ==============================================================================
#           !!! החלף את שלושת הערכים הבאים בפרטים שלך !!!
# ==============================================================================

# 1. החלף בכתובת המלאה של Home Assistant שלך
HA_URL = "http://homeassistant.local:8123" 

# 2. החלף ב-Access Token הארוך שיצרת ושמרת
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmMzZlMzQwNTFjODk0MDgxOTExN2Q2ZjQwMDUzZjg1MCIsImlhdCI6MTc1MDE5NTUzOCwiZXhwIjoyMDY1NTU1NTM4fQ.rlLsq0XZPIjK03V2jSBGj75Zrba09Yi6yuTdFQEVa94"

# 3. החלף במזהה הישות (Entity ID) המדויק של המתג שיצרת
ENTITY_ID_TO_TOGGLE = "input_boolean.tvrt_mshrd" 

# ==============================================================================
#                       סוף אזור ההגדרות האישיות
# ==============================================================================


# הכנת הנתונים לשליחה לפי הפורמט של ה-API
# ----------------------------------------------------

# הכתובת המדויקת של ה-API להפעלת שירותים
api_url = f"{HA_URL}/api/services/input_boolean/toggle"

# ה"כותרות" של הבקשה. כאן אנחנו מציגים את ה"תעודה המזהה" שלנו (הטוקן)
headers = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

# ה"גוף" של הבקשה. כאן אנחנו אומרים על איזה מכשיר אנחנו רוצים לפעול
data = {
    "entity_id": ENTITY_ID_TO_TOGGLE
}


# שליחת הבקשה
# ----------------
print(f">>> מתחבר ל-Home Assistant בכתובת: {HA_URL}")
print(f">>> שולח פקודת 'toggle' לישות: {ENTITY_ID_TO_TOGGLE}")

try:
    # כאן מתבצעת הפנייה בפועל לשרת של Home Assistant
    response = requests.post(api_url, headers=headers, data=json.dumps(data))

    # בדיקה אם הפעולה הצליחה
    if response.status_code == 200:
        print("\n>>> הצלחה! הפקודה נשלחה בהצלחה ל-Home Assistant.")
        print(">>> בדוק בממשק של Home Assistant אם המתג שינה את מצבו.")
    else:
        print(f"\nXXX שגיאה! Home Assistant החזיר קוד שגיאה: {response.status_code}")
        print(f"XXX תוכן התגובה: {response.text}")

except requests.exceptions.ConnectionError as e:
    print(f"\nXXX שגיאת חיבור חמורה!")
    print("XXX לא הצלחתי להתחבר לכתובת שציינת. ודא שהיא נכונה וש-Home Assistant פועל.")
    print(f"XXX פרטי השגיאה: {e}")

except Exception as e:
    print(f"\nXXX אירעה שגיאה לא צפויה: {e}")