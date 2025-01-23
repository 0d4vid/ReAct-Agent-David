# Define the calculator tool

from sympy import sympify
def calculator(expression):
    try:
        result = sympify(expression)
        return result
    except Exception as e:
        return f"Error in calculation: {e}"

calculator("1*2*3*4*5")

# Define the translation tool

from googletrans import Translator

def translator(text, dest_lang):
    translator = Translator()
    try:
        result = translator.translate(text, dest=dest_lang)
        return result.text
    except Exception as e:
        return f"Error in translation: {e}"


import re

def extract_action_and_input(text):
  action = re.search(r"Action: (.*)", text)
  action_input = re.search(r"Action Input: (.*)", text)
  return action.group(1).strip() if action else None, action_input.group(1).strip() if action else None

extract_action_and_input("""
Thought: To calculate the square root of 144, I can use the math library in Python or a calculator.

Action: Calculator
Action Input: sqrt(144)
""")


from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=('api-key-here'),
)
user_prompt = "Translate 'Hello' to Spanish"


chat_history = [
    {
      "role": "system",
      "content": """
      You have access to the following tools:
      Calculator: Use this when you want to do math. Use SymPy expressions, eg: 2 + 2
      Translator: Use this when you want to translate text. Provide the text and the destination language code, eg: "Hello", "es"

      Use the following format:

      Question: the input question you must answer
      Thought: you should always think about what to do
      Action: the action to take, should be one of [Calculator, Translator]
      Action Input: the input to the action
      Observation: the result of the action
      ... (the Thought/Action/Observation can repeat any number of times)
      Thought: I now know the final answer!
      Final Answer: the answer to the original input question
      """
    },
    {
      "role": "user",
      "content": f"Question: {user_prompt}"
    }
  ]


import re

while True:
  completion = client.chat.completions.create(
    model="meta-llama/llama-3.2-90b-vision-instruct:free",
    messages=chat_history,
    stop=["Observation:"]
  )
  response_text = completion.choices[0].message.content
  action, action_input = extract_action_and_input(response_text)
  print(response_text)
  # We want to see if the LLM took an action
  if action == "Calculator":
    action_result = calculator(action_input)
    print(f"Observation: {action_result}")
    chat_history.extend([
      { "role": "assistant", "content": response_text },
      { "role": "user", "content": f"Observation: {action_result}" }
    ])
  elif action == "Translator":
    # Extract text and destination language from action_input
    match = re.match(r'"(.*?)", "(.*?)"', action_input)
    if match:
        text, dest_lang = match.groups()
        action_result = translator(text, dest_lang)
        print(f"Observation: {action_result}")
        chat_history.extend([
          { "role": "assistant", "content": response_text },
          { "role": "user", "content": f"Observation: {action_result}" }
        ])
    else:
        action_result = "Error: Invalid input format for Translator."
        print(f"Observation: {action_result}")
        chat_history.extend([
          { "role": "assistant", "content": response_text },
          { "role": "user", "content": f"Observation: {action_result}" }
        ])
  else:
    break

print(response_text)


calculator("sqrt(144)")

chat_history

chat_history.extend([
    { "role": "assistant", "content": response_text },
    { "role": "user", "content": "Observation: The knife did not work! A tree has fallen down between you and the present." }
])

chat_history

completion = client.chat.completions.create(
  model="meta-llama/llama-3.2-90b-vision-instruct:free",
  messages=chat_history
)
response_text = completion.choices[0].message.content

response_text