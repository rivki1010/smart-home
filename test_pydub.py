from pydub import AudioSegment
import os

# מגדירים את הנתיבים, בדיוק כמו בסקריפט הראשי
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe   = r"C:\ffmpeg\bin\ffprobe.exe"

# שמות הקבצים
source_file = "test_audio.wav"
output_file = "test_output.wav"

print(">>> מתחיל את בדיקת האבחון של pydub...")

# 1. בודקים שקובץ המקור קיים
if not os.path.exists(source_file):
    print(f"XXX שגיאה: קובץ המקור '{source_file}' לא נמצא.")
    print("XXX אנא ודא שיש לך קובץ 'test_audio.wav' בתיקייה זו.")
else:
    try:
        # 2. מנסים לטעון ולהמיר את הקובץ
        print(f">>> טוען את הקובץ '{source_file}'...")
        audio = AudioSegment.from_file(source_file)
        
        print(">>> ממיר את הקובץ (משנה ערוצים וקצב דגימה)...")
        audio = audio.set_channels(1).set_frame_rate(16000)
        
        print(f">>> מייצא את התוצאה לקובץ '{output_file}'...")
        audio.export(output_file, format="wav")
        
        print("\n>>> הצלחה! קובץ האודיו הומר בהצלחה.")
        print(f">>> קובץ חדש בשם '{output_file}' אמור להופיע עכשיו בתיקייה.")
        
    except Exception as e:
        print(f"\nXXX כישלון! הבדיקה נכשלה עם שגיאה.")
        print("XXX פרטי השגיאה:")
        # נשתמש ב-repr(e) כדי לקבל את כל פרטי השגיאה
        print(repr(e))