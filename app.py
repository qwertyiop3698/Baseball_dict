import json
import os

import requests
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

with open("./players_data.json", "r", encoding="UTF-8") as f:
    player_db = json.load(f)


def load_env_value(key, env_path=".env"):
    if key in os.environ:
        return os.environ[key].strip().strip('"').strip("'")

    try:
        with open(env_path, "r", encoding="UTF-8") as env_file:
            for line in env_file:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue

                name, value = line.split("=", 1)
                if name.strip() == key:
                    return value.strip().strip('"').strip("'")
    except FileNotFoundError:
        return ""

    return ""


API_KEY = load_env_value("API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"


def get_all_player_names():
    return {
        player["name"]
        for group in ("pitchers", "batters")
        for player in player_db.get(group, [])
        if player.get("name")
    }


PLAYER_NAMES = get_all_player_names()


def is_player_question(user_input):
    return any(name in user_input for name in PLAYER_NAMES)


def get_term_answer(user_input):
    if not API_KEY:
        raise RuntimeError("API_KEY is not configured. Please set API_KEY in the .env file.")

    if is_player_question(user_input):
        return "메인 화면에서는 야구용어만 질문할 수 있습니다. 선수 비교는 왼쪽 하단의 선수 비교 분석 버튼을 눌러 이용해주세요."

    prompt = (
        "너는 야구용어 백과사전이야. 사용자가 묻는 야구 규칙, 기록 지표, 전술, 포지션, "
        "경기 상황 용어만 한국어로 쉽고 정확하게 설명해줘. "
        "초심자들에게 너무 어려운 용어가 섞이면 안 되니까 야구를 처음 접하는 중,고등학생한테 말하듯이 설명해."
        "특정 선수 평가나 선수 비교 요청이면 답하지 말고 선수 비교 화면을 이용하라고 안내해. "
        "답변은 HTML 조각으로 작성하고 코드블록은 쓰지 마.\n\n"
        f"질문: {user_input}"
    )
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(
        GEMINI_URL,
        params={"key": API_KEY},
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )

    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError("Gemini API returned a non-JSON response.") from exc

    if response.status_code != 200:
        message = result.get("error", {}).get("message", "Unknown Gemini API error.")
        raise RuntimeError(message)

    try:
        answer = result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError("Gemini API response did not include an answer.") from exc

    return answer.replace("```html", "").replace("```", "").strip()


def handle_ask_request():
    if request.method == "GET":
        user_input = request.args.get("question", "").strip()
    else:
        data = request.get_json(silent=True) or request.form or {}
        user_input = data.get("question", "").strip()

    if not user_input:
        return jsonify({"answer": "질문할 야구용어를 입력해주세요."}), 400

    try:
        return jsonify({"answer": get_term_answer(user_input)})
    except Exception as e:
        return jsonify({"answer": f"오류 발생: {str(e)}"}), 500


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return handle_ask_request()

    if request.args.get("question"):
        return handle_ask_request()

    return render_template("dict.html")


@app.route("/compare")
def compare():
    return render_template("compare.html", players=player_db)


@app.route("/players")
def players():
    return jsonify(player_db)


@app.route("/ask", methods=["GET", "POST"])
@app.route("/ask/", methods=["GET", "POST"])
def ask():
    return handle_ask_request()


if __name__ == "__main__":
    print("야구용어 백과사전 서버 실행 중")
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
