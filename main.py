import os
from openai import OpenAI
from dotenv import load_dotenv

# Load your API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat():
    print("🤖 Chatbot ready! Type 'exit' to quit.\n")
    messages = [{"role": "system", "content": "You are a helpful and friendly AI assistant."}]

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4o" for the full model
            messages=messages,
        )

        reply = response.choices[0].message.content
        print(f"Chatbot: {reply}\n")
        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    chat()
