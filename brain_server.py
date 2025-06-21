from flask import Flask
import os

app = Flask(__name__)

@app.route("/api/call")
def handle_call_test():
    print(">>> Request received at /api/call endpoint!", flush=True)
    return "read=t-shart-ha-api-oved=,hangup"

@app.route("/")
def hello_world():
    print(">>> Request received at / (root) endpoint!", flush=True)
    return "Hello, the brain server is running!"

if __name__ == "__main__":
    # Azure מספק את הפורט במשתנה סביבה, עם ברירת מחדל ל-8000
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)