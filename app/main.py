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

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'), debug=True)