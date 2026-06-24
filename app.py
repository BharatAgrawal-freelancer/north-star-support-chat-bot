from flask import Flask, render_template, request, jsonify

from chatbot.conversation_manager import process_message

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({
            "error": "message field is required"
        }), 400

    response = process_message(data["message"])

    return jsonify({
        "response": response
    })

if __name__ == "__main__":
    app.run(debug=True)