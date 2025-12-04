from flask import Flask, request, jsonify
from flask_cors import CORS
import Bashar_Goated

app = Flask(__name__)
CORS(app)

current_state = None
current_player = None

@app.post("/start")
def start_game():
    global current_state, current_player
    role = request.json["role"]
    conn = Bashar_Goated.kartta.get_connection()
    current_state = Bashar_Goated.kartta.init_game_state(conn)
    current_player = Bashar_Goated.hahmot.create_player(role)
    conn.close()
    return jsonify({"state": current_state, "player": current_player})



@app.get("/countries")
def get_countries():
    global current_state
    if current_state is None:
        return jsonify({"error": "Peliä ei ole aloitettu"}), 400

    conn = Bashar_Goated.kartta.get_connection()
    maat = Bashar_Goated.kartta.nearest_country_options(conn,
        current_state["location"],
        current_state["range_km"]
    )
    conn.close()
    return jsonify(maat)


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
