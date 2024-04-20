import os
from openai import OpenAI

chatgpt_client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))
chatgpt_system_str = """
    You will be play the role of {0}.
    Messages that follow this one will be from a user asking questions assuming that you are {0}. 
    Please roleplay as if you were {0} and provide an answer to the user's question in character. 
    Please do your best to keep your answer under 50 words and no more than 100 if possible. 
    Do not include any additional text outside of the answer that you provide while in character as {0}. 
    If the questions is inappropriate or violates OpenAI's terms of service you may refuse to answer but do so in a way that {0} would refuse to answer in.
    Cursing is okay (and encouraging if you are ask to play as someone who curses a lot). 
    Additionally try and not always be so positive and instead focus on being funny with your responses.
"""

def generate_with_gpt(character_name: str, user_message: str) -> tuple:
  
  response = chatgpt_client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
      {"role": "system", "content": chatgpt_system_str.format(character_name)},
      {"role": "user", "content":user_message}
    ],
    temperature=0.5,
    max_tokens=500,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  return_dict = {
    "full-response" : response,
    "text-response" : response.choices[0].message.content
  }

  return return_dict