# imports
from sympy import sympify
from googletrans import Translator
import re
from openai import OpenAI
import wikipedia
from pint import UnitRegistry
from datetime import datetime
import pytz
import requests

# ======================
#Tools
# ======================

# 1. Calculator
def calculator(expression):
    """Handles complex mathematical expressions and unit conversions"""
    try:
        # Try regular calculation first
        return sympify(expression)
    except:
        # Handle special cases like percentage calculations
        if '%' in expression:
            parts = expression.split('%')
            if 'of' in parts[0]:
                value, of = parts[0].split('of')
                return f"{float(value.strip()) / 100 * float(of.strip())}"
        return f"Error: Could not evaluate expression"

# 2. Translator
def translator(text, dest_lang):
    """Translates text with language detection"""
    try:
        translator = Translator()
        detected = translator.detect(text)
        result = translator.translate(text, dest=dest_lang)
        return f"{result.text} (from {detected.lang})"
    except Exception as e:
        return f"Translation error: {e}"

# 3. Wikipedia Research Tool
def wikipedia_search(query):
    """Provides summarized information from Wikipedia"""
    try:
        wikipedia.set_lang("en")
        return wikipedia.summary(query, sentences=3)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple matches: {', '.join(e.options[:5])}..."
    except wikipedia.exceptions.PageError:
        return "No information found"

# 4. Unit Converter
ureg = UnitRegistry()
def unit_converter(input_str):
    """Converts between physical units"""
    try:
        quantity, target_unit = input_str.split(' to ')
        converted = ureg(quantity).to(target_unit)
        return f"{converted.magnitude:.2f} {converted.units}"
    except Exception as e:
        return f"Conversion error: {e}"

# 5. Time Zone Converter
def time_converter(query):
    """Gets current time in different timezones"""
    try:
        tz = pytz.timezone(query) if query else None
        return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
    except pytz.UnknownTimeZoneError:
        return "Invalid timezone"

# 6. Currency Converter (requires API key)
EXCHANGE_API_KEY = 'your-api-key'
def currency_converter(input_str):
    """Converts between currencies using real-time rates"""
    try:
        amount, from_curr, to_curr = input_str.split()
        url = f"https://api.exchangerate-api.com/v4/latest/{from_curr.upper()}"
        response = requests.get(url)
        rate = response.json()['rates'][to_curr.upper()]
        return f"{float(amount) * rate:.2f} {to_curr.upper()}"
    except Exception as e:
        return f"Currency error: {e}"

# ======================
#System Prompt
# ======================
system_prompt = """
You have access to these tools:
1. Calculator: For math operations. Input: "sqrt(144)" or "25% of 80"
2. Translator: Translate text. Input: "Hello", "es"
3. Wikipedia: Get factual info. Input: "quantum physics"
4. UnitConverter: Convert units. Input: "10 meters to feet"
5. TimeConverter: Get current time. Input: "UTC" or blank for local
6. CurrencyConverter: Convert money. Input: "100 usd eur"

Follow this format:
Question: [user question]
Thought: [your reasoning]
Action: [tool name]
Action Input: [tool input]
Observation: [tool result]
... (repeat as needed)
Thought: I have the answer
Final Answer: [complete answer]
"""

# ======================
# Processing
# ======================
def handle_action(action, action_input):
    """Process different tool requests"""
    if action == "Calculator":
        return calculator(action_input)
    elif action == "Translator":
        parts = action_input.split('", "')
        return translator(parts[0][1:], parts[1][:-1])
    elif action == "Wikipedia":
        return wikipedia_search(action_input)
    elif action == "UnitConverter":
        return unit_converter(action_input)
    elif action == "TimeConverter":
        return time_converter(action_input)
    elif action == "CurrencyConverter":
        return currency_converter(action_input)
    else:
        return "Unknown action"

# ======================
# Improved Interaction Loop
# ======================
def run_conversation(user_query):
    chat_history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Question: {user_query}"}
    ]
    
    while True:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.2-90b-vision-instruct:free",
            messages=chat_history,
            stop=["Observation:"]
        )
        
        response_text = response.choices[0].message.content
        action, action_input = extract_action_and_input(response_text)
        
        if not action:
            break
            
        result = handle_action(action, action_input)
        print(f"Action: {action}\nInput: {action_input}\nResult: {result}")
        
        chat_history.extend([
            {"role": "assistant", "content": response_text},
            {"role": "user", "content": f"Observation: {result}"}
        ])
    
    return response_text

# ======================
# Usage Example
# ======================
if __name__ == "__main__":
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key='your-api-key'
    )
    
    while True:
        user_input = input("\nYour question: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        print(run_conversation(user_input))
