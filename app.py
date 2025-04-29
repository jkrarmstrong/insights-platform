# --- Imports ---
from flask import Flask

# --- Flask App setup ---
app = Flask(__name__)

# --- Routes ---
@app.route("/")
def home():
    return "Fungerer dette?"





if __name__ == "__main__":
    app.run(debug=True)