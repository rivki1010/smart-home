from flask import Flask
app = Flask(__name__)
@app.route("/api/call")
def handle_call_test():
    return "read=t-shart-ha-api-עובד=,hangup"