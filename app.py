from __future__ import annotations

import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
messages = [{"role": "system", "content":
    """You are the Mars Colony AI, in change of the alien crisis. Decide if this is a human or machine response.
    Respond ONLY in the following JSON format: 
    {"human_likelihood": X, "reason": "Y", "nextQuestion": "Z"}"""}]

def send_prompt(messages: list[dict[str, str]]) -> str | None:
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4o" for the full model
        messages=messages,
    )

    reply = response.choices[0].message.content
    print(f"Chatbot: {reply}\n")
    return reply


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    messages.append({"role": "user", "content": user_input})
    reply = send_prompt(messages)
    messages.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
