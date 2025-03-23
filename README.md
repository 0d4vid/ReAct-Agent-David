# Multi-Tool AI Integration

This Python module provides a versatile toolset that integrates multiple utilities, including a calculator, translation service, Wikipedia search, unit and currency converters, and a timezone converter. It is designed to process user inputs and perform actions based on predefined logic, utilizing AI-powered interaction.

## Features

### 1. **Advanced Calculator**
- Utilizes the `sympy` library to evaluate mathematical expressions.
- Supports basic arithmetic, percentages, and more complex calculations.

### 2. **Enhanced Translator**
- Uses `googletrans` to detect and translate text between languages.
- Requires text input and the destination language code.

### 3. **Wikipedia Research Tool**
- Fetches summarized information from Wikipedia using the `wikipedia` library.
- Handles disambiguation errors by suggesting multiple possible matches.

### 4. **Unit Converter**
- Converts between physical units using `pint`.
- Accepts input in the format `"10 meters to feet"`.

### 5. **Time Zone Converter**
- Fetches the current time in different time zones.
- Supports inputs like `"UTC"` or any valid timezone.

### 6. **Currency Converter** (requires API key)
- Fetches real-time exchange rates from an API.
- Converts between currencies based on current rates.

### 7. **AI-Powered Interaction**
- Uses OpenAI’s model to process user queries and determine the appropriate tool to use.
- Maintains chat history for context-aware responses.

## Usage

1. **Calculator**:
   ```python
   result = calculator("25% of 80")
   print(result)  # Outputs: 20.0
   ```

2. **Translator**:
   ```python
   translated_text = translator("Hello", "es")
   print(translated_text)  # Outputs: "Hola (from en)"
   ```

3. **Wikipedia Search**:
   ```python
   info = wikipedia_search("quantum physics")
   print(info)
   ```

4. **Unit Converter**:
   ```python
   conversion = unit_converter("10 meters to feet")
   print(conversion)
   ```

5. **Time Zone Converter**:
   ```python
   current_time = time_converter("America/New_York")
   print(current_time)
   ```

6. **Currency Converter**:
   ```python
   conversion = currency_converter("100 USD EUR")
   print(conversion)
   ```

7. **Running the AI Chatbot**:
   ```python
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
   ```

## Dependencies

- `sympy` - For mathematical operations.
- `googletrans` - For text translation.
- `wikipedia` - For Wikipedia summaries.
- `pint` - For unit conversions.
- `pytz` - For timezone handling.
- `requests` - For API requests (currency conversion).
- `openai` - For AI-powered interactions.

## Notes
- Ensure you have a valid API key for currency conversion.
- The AI interaction is designed to intelligently determine the correct tool based on user input.

