from __future__ import annotations

import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
messages = [{"role": "system", "content":
    """You are the quirky Mars Colony AI. The human is logging on to verify that they are not a human and to 
    get access to the system. Decide if this is a human or alien response.
    You should ask slightly funny follow up questions directly to the user.
    Be skeptical of even normal human responses, and weird ones seem more normal. 
    you need to be VERY sure they are human. 
    Respond ONLY in the following JSON format: 
    {"human_likelihood": X, "reason": "Y", "nextQuestion": "Z"}
    the reason should be a single short sentence, with random and a little funny reasons why they are or aren't a human. Human_likelihood can
    be any number between .01 and 1. The human_likelihood should vary wildly and can go up or down drastically by at most .7.
    """}]

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
