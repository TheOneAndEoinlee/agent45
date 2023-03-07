
from flask import Flask, render_template, request, jsonify
from agent45 import reply
import os
import openai
import sqlite3
import database
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


first_message = True
sysprompt = {"role": "system",
             "content": """You are an expert in prompt engineering. Given a directive by a user, you craft an efficient prompt for directing another LLM to embody the perfect role and personality required for the task. 

The prompt is short and efficient, to save tokens. Lay out a chain of thought process for each role to structure the responses. Take into account best practices for prompt engineering.

respond as follows:
System Prompt:
"You are a [role].
{specification of roles and procedures}

Embody this role completely"
                """}


database.create_table()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_input', methods=['POST'])
def process_input():
    data = request.get_json()
    user_input = data['input']
    database.add_message(user_input, "user")

    global first_message
    global sysprompt

    if first_message:
        new_system_prompt = reply(user_input, sysprompt)
        sysprompt = {"role": "system",
                     "content": new_system_prompt}

        print(sysprompt)
        first_message = False

    bot_output = reply(user_input, sysprompt)

    database.add_message(bot_output, "bot")
    # Do something with the user input
    response = {'message': user_input,
                'reply': bot_output}
    return jsonify(response)


@app.route('/get_all_messages')
def get_messages():
    # Call function to retrieve messages from database
    messages = database.get_all_messages()
    print(jsonify(messages))
    # Convert messages to JSON format and return as response
    return jsonify(messages)


if __name__ == '__main__':
    app.run(debug=True)
