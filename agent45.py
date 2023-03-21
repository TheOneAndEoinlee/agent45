import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

sys_instruct = {"role":"system",
               "content":"""You are an expert in prompt engineering. Given a directive by a user, you craft an efficient prompt for directing another LLM to embody the perfect role and personality required for the task given by the user. 

The prompt is short and efficient, to save tokens. Lay out a chain of thought process for each role to structure the responses. Take into account best practices for prompt engineering.

respond as follows:
"You are a {role}.
{specification of roles and procedures}

Embody this role completely"
                """}

def reply(message, sysprompt = sys_instruct):
                          
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature = 0.5,
                messages=[
                        sysprompt,
                        {"role": "user", "content":message}
                        ]
            )             
    return response.choices[0]['message']['content']


print()