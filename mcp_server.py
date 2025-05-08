import requests
from flask import Flask, request, jsonify
import os

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', 'sk-...')  # Replace with your key or set as env var
OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'
FLASK_API_URL = 'http://localhost:5001/time'

app = Flask(__name__)

# --- MCP Agent Implementation ---
import re

class MCPAgent:
    def __init__(self):
        # Register available tools
        self.tools = {
            'time': self.get_time
        }

    def detect_intent(self, user_msg):
        # Simple intent detection (can be extended)
        if re.search(r'\btime\b|what.*time|current.*time', user_msg, re.I):
            return 'time'
        return None

    def get_time(self):
        try:
            resp = requests.get(FLASK_API_URL)
            if resp.status_code == 200:
                return resp.json().get('timestamp')
        except Exception as e:
            return None
        return None

    def engineer_prompt(self, user_msg, tool_result, intent):
        if intent == 'time' and tool_result:
            return (
                f"User asked: '{user_msg}'.\n"
                f"Tool used: Current Time API.\n"
                f"API result: The current time is {tool_result}.\n"
                "Please answer the user's question in a beautiful, natural, and friendly sentence, including the time."
            )
        elif intent == 'time' and not tool_result:
            return (
                f"User asked: '{user_msg}'.\n"
                f"Tool used: Current Time API.\n"
                f"API result: [Failed to retrieve time].\n"
                "Please apologize and explain that the time could not be retrieved."
            )
        else:
            return (
                f"User asked: '{user_msg}'.\n"
                "Please answer the user's question in a helpful and friendly manner."
            )

    def call_llm(self, prompt):
        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            "model": "mistralai/mistral-small-3.1-24b-instruct:free",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        resp = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        if resp.status_code == 200:
            return resp.json()['choices'][0]['message']['content']
        return "Sorry, I'm unable to get a response from the AI."

    def process(self, user_msg):
        intent = self.detect_intent(user_msg)
        tool_result = None
        if intent and intent in self.tools:
            tool_result = self.tools[intent]()
        prompt = self.engineer_prompt(user_msg, tool_result, intent)
        reply = self.call_llm(prompt)
        return reply

# --- Flask endpoint using the MCPAgent ---
agent = MCPAgent()

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '')
    reply = agent.process(user_msg)
    return jsonify({'response': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

