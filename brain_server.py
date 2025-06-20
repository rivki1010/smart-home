from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello from Azure!"

@app.route("/api/call")
def handle_call_test():
    # מחזירים תשובה פשוטה שימות המשיח יבינו
    return "read=t-shart-ha-api-עובד=,hangup"

if __name__ == "__main__":
    # שינוי חשוב: Azure מספקת את הפורט במשתנה סביבה
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)