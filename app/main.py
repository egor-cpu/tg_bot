from flask import Flask, render_template
from database import db

app = Flask(__name__, template_folder='.')

@app.route("/")
def main_menu():
    return render_template('menu.html')

@app.route("/game")
def game():
    return render_template('game.html')

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route("/submit_score", methods=["POST"])
def submit_score():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        score = data.get("score")
        is_correct = data.get("is_correct", True)

        if user_id is None or score is None:
            return jsonify({"status": "error", "message": "Missing 'user_id' or 'score'"}), 400

        db.update_stats(user_id, is_correct, score)
        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        ssl_context=('cert.pem', 'key.pem'),
        debug=True
    )
