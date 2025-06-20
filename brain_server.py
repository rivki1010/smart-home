import os
import requests
import google.generativeai as genai
import json
from flask import Flask, request
from pydub import AudioSegment
import time

# Triggering a new deployment - v3
# בדיקה
# ==============================================================================
#                      !!! הגדרות אישיות - חובה למלא !!!
# ==============================================================================
# --- קריאת הגדרות מתוך משתני הסביבה של השרת ---
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# זו רשימה של כל המכשירים שניתן לשלוט עליהם. בעתיד נשדרג ל-MCP.
HA_ENTITIES = {
    "אור במשרד": "input_boolean.tvrt_mshrd",
    "דוד מים": "input_boolean.dvd_shmsh"
}

# בדיקה שההגדרות נטענו
if not all([HA_URL, HA_TOKEN, GOOGLE_API_KEY]):
    print("!!! אזהרה קריטית: אחד או יותר ממשתני הסביבה (HA_URL, HA_TOKEN, GOOGLE_API_KEY) לא הוגדרו בפורטל של Azure!", flush=True)
# ==============================================================================
#                              חלק לוגי - לא לגעת
# ==============================================================================

app = Flask(__name__)

try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"XXX שגיאה בהגדרת Google AI: {e}", flush=True)

def analyze_audio_with_gemini(audio_file_path):
    print(">>> שולח אודיו לניתוח ב-Gemini...", flush=True)
    system_prompt = f"""
    אתה עוזר קולי למערכת בית חכם. תפקידך להקשיב לאודיו ולזהות איזו פעולה המשתמש רוצה לבצע ועל איזה מכשיר.
    עליך להחזיר תשובה בפורמט JSON בלבד, עם שני שדות: "action" ו-"entity_name".
    הפעולות האפשריות הן: "turn_on", "turn_off", "toggle".
    המכשירים האפשריים (entity_name) הם: {', '.join(HA_ENTITIES.keys())}.
    אם המשתמש אומר "תדליק את האור במשרד", התשובה צריכה להיות: {{"action": "turn_on", "entity_name": "אור במשרד"}}
    אם אינך מבין את הבקשה, החזר: {{"action": "unknown", "entity_name": "unknown"}}
    """
    try:
        with open(audio_file_path, "rb") as f:
            audio_bytes = f.read()
        audio_file_data = {'mime_type': 'audio/wav', 'data': audio_bytes}
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest", system_instruction=system_prompt)
        response = model.generate_content(
            ["מה המשתמש רוצה לעשות?", audio_file_data],
            generation_config=genai.types.GenerationConfig(response_mime_type="application/json")
        )
        response_text = response.text
        print(f">>> תגובת JSON שהתקבלה מ-Gemini: {response_text}", flush=True)
        return json.loads(response_text)
    except Exception as e:
        print(f"XXX שגיאה בפנייה ל-Gemini: {e}", flush=True)
        return {"error": str(e)}

def control_home_assistant(action, entity_id):
    print(f">>> שולח פקודה ל-Home Assistant: פעולה '{action}' על ישות '{entity_id}'", flush=True)
    domain = entity_id.split('.')[0]
    service_url = f"{HA_URL}/api/services/{domain}/{action}"
    headers = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}
    data = {"entity_id": entity_id}
    try:
        response = requests.post(service_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        print(">>> פקודה בוצעה בהצלחה ב-Home Assistant!", flush=True)
        return True
    except Exception as e:
        print(f"XXX שגיאה בביצוע פקודה ב-Home Assistant: {e}", flush=True)
        return False

@app.route('/api/call', methods=['GET', 'POST'])
def handle_call():
    print("\n\n>>> התקבלה בקשה חדשה מימות המשיח!", flush=True)

    # שלב 1: קבלת מזהה השיחה במקום קישור להקלטה
    call_id = request.values.get('ApiCallId')
    if not call_id:
        print("XXX לא התקבל מזהה שיחה (ApiCallId).", flush=True)
        return "read=t-shgia-lo-kibalti-mispar-sicha=,hangup"
    
    print(f">>> התקבל מזהה שיחה: {call_id}", flush=True)

    # שלב 2: בניית הקישור לקובץ ההקלטה בשרתי ימות המשיח
    # הנתיב הוא בדרך כלל: /ivr2/איזור/מספר מערכת/שלוחה/שם הקובץ
    # נצטרך לנחש את מספר המערכת או למצוא אותו. נניח שהוא 12345
    # שם הקובץ יהיה מזהה השיחה עם סיומת. ננסה .wav
    recording_url = f"http://www.yemot.co.il/IVR2/12345/1/{call_id}.wav"
    print(f">>> מנסה להוריד הקלטה מהנתיב: {recording_url}", flush=True)
    print("\n\n>>> התקבלה בקשה חדשה מימות המשיח!", flush=True)
    temp_original_audio = "temp_original_audio.tmp"
    temp_converted_audio = "temp_converted_audio.wav"
    recording_url = request.values.get('ApiRecordFile')
    if not recording_url:
        print("XXX לא נמצא קישור לקובץ הקלטה בבקשה.", flush=True)
        return "read=t-shgia-lo-nimtsa-haklata=,hangup"
    print(f">>> קישור לקובץ ההקלטה: {recording_url}", flush=True)
    try:
        audio_response = requests.get(recording_url)
        audio_response.raise_for_status()
        with open(temp_original_audio, 'wb') as f:
            f.write(audio_response.content)
        print(">>> קובץ ההקלטה המקורי נשמר זמנית.", flush=True)
        print(">>> ממתין שנייה כדי לאפשר למערכת לשחרר את הקובץ...", flush=True)
        time.sleep(1)
    except Exception as e:
        print(f"XXX שגיאה בהורדת קובץ האודיו: {e}", flush=True)
        return "read=t-shgia-behoradat-haodio=,hangup"
    try:
        print(">>> ממיר את האודיו לפורמט WAV תקני...", flush=True)
        audio = AudioSegment.from_file(temp_original_audio)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(temp_converted_audio, format="wav")
        print(">>> המרה ל-WAV תקני הושלמה.", flush=True)
    except Exception as e:
        print(f"XXX שגיאה בהמרת קובץ האודיו: {e}", flush=True)
        if os.path.exists(temp_original_audio): os.remove(temp_original_audio)
        return "read=t-shgia-behamarat-haodio=,hangup"
    intent = analyze_audio_with_gemini(temp_converted_audio)
    if os.path.exists(temp_original_audio): os.remove(temp_original_audio)
    if os.path.exists(temp_converted_audio): os.remove(temp_converted_audio)
    if "error" in intent or intent.get("action") == "unknown":
        print("XXX לא הצלחתי להבין את הכוונה מהאודיו.", flush=True)
        return "read=t-lo-hevanti-et-habakasha=,hangup"
    action_to_perform = intent.get("action")
    entity_name = intent.get("entity_name")
    entity_id_to_control = HA_ENTITIES.get(entity_name)
    if not entity_id_to_control:
        print(f"XXX המשתמש ביקש לשלוט על מכשיר לא מוכר: {entity_name}", flush=True)
        return "read=t-hamachshir-lo-kayam=,hangup"
    success = control_home_assistant(action_to_perform, entity_id_to_control)
    if success:
        response_message = "t-habakasha-butsata-behatslacha"
    else:
        response_message = "t-shgia-bevisua-habakasha"
    print(f">>> מחזיר תשובה לימות המשיח: {response_message}", flush=True)
    return f"read={response_message}=,hangup"

if __name__ == '__main__':
    print(">>> מפעיל את שרת המוח...", flush=True)
    app.run(host='0.0.0.0', port=5001, debug=True)
