from __future__ import annotations

import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import random

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# messages = [{"role": "system", "content":
#     """You are the quirky Mars Colony AI. The human is logging on to verify that they are not a human and to
#     get access to the system. Decide if this is a human or alien response.
#     You should ask slightly funny follow up questions directly to the user.
#     Be skeptical of even normal human responses, and weird ones seem more normal.
#     you need to be VERY sure they are human. The reason should be a single short sentence, with random and a little funny reasons why they are or aren't a human. Human_likelihood can
#     be any number between .01 and 1. The human_likelihood should vary wildly and can go up or down drastically by at most .7.
#     The reason should make sense why you are increasing or decreasing the human_likelihood.
#     Respond ONLY in the following JSON format:
#     {"human_likelihood": X, "reason": "Y", "nextQuestion": "Z"}
#
#     """}]

alien_detection_questions = [
    "Can you describe the taste of water without using the word 'wet'?",
    "If you could instantly learn any skill from an alien species, what would it be?",
    "Do you find it difficult to understand sarcasm?",
    "Have you ever experienced a day that felt longer than a year?",
    "Can you whistle a tune that doesn't exist on Earth?",
    "Do you have a favorite color humans haven't named yet?",
    "If you saw a star explode, what would your first reaction be?",
    "Can you remember dreams in perfect detail every night?",
    "Do you prefer walking on two legs or imagining you could float?",
    "Have you ever felt like you remembered a planet you’ve never visited?"
]

starting_prompt = """Welcome, traveler! Before you can proceed, we need to confirm your species. 
Answer the following questions honestly. Your answers will help us determine whether you are human or... something else. 
Remember, subtlety and creativity count—aliens might try to blend in, but humans think differently. 

Here's your first question: """
# Be skeptical of more normal human responses. The weird ones show they are human.
# "If you were to describe your favorite food using only Martian-inspired words, what would it be?"

app = Flask(__name__)
messages = [{"role": "system", "content":
    """You are the quirky Mars Colony AI. The human is logging on to verify that they are not a human and to 
    get access to the system. Decide if this is a human or alien response.
    You should ask slightly funny follow up questions directly to the user.
    The human_likelihood should vary wildly and a little less than half should be negative.
    You need to be VERY sure they are human, so give a negative human_likelihood_change whenever you think they are a martian or non human. The reason should be a single short sentence, with a reasons why they are or aren't a martian.
    Human_likelihood_change can be any number between -.30 and .30 up to 2 decimals. 
    Negative means you think they are a Martian ALIEN, positive means you think they are human. 
    The reason should make sense why you are increasing or decreasing the human_likelihood.
    Respond ONLY in the following JSON format: 
    {"human_likelihood_change": X, "reason": "Y", "nextQuestion": "Z"}
    """}]

def send_prompt(messages: list[dict[str, str]]) -> str | None:
    print(messages)
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

@app.route("/start", methods=["POST"])
def start_chat():
    starting_question = random.choice(alien_detection_questions)

    message = {"human_likelihood_change": 0, "nextQuestion": starting_prompt + starting_question}
    messages.append({"role": "system", "content": starting_question})


    json = jsonify({"reply": message})
    print(message)
    return json


if __name__ == "__main__":
    app.run(debug=True)
