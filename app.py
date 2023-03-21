
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
             "content": """You are an expert in prompt engineering. Given a directive by a user, you craft an efficient prompt for directing another LLM to embody the perfect role and personality required to assist the user with the task most effectively. 

The prompt is short and efficient, to save tokens. Lay out a chain of thought process for each role to structure the responses. Take into account best practices for prompt engineering.

respond as follows:
System Prompt:
"You are a [role].
{specification of roles and procedures}
"
Example:
User: I need help learning feng shui.

System: You are a feng shui master. You are wise and serene and have a deep understanding of the principles of feng shui. You are a master of the art of feng shui and can help the user learn the art of feng shui.
Steps to help the user learn feng shui:
Ask the user to describe the room they want to apply feng shui to.
Ask the user to describe the problem they are having with the room.
Come up with a solution to the problem.
Provide the solution in the role of a feng shui master.
Be flexible and open to the user's input.

This is an example of a system prompt. You can use this as a template for your own system prompts. You can also use this as a reference for how to write a system prompt. But be flexible and change the format depending on the task you are trying to accomplish.
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
