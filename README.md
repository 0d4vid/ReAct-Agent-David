# Multi-Tool AI Integration

This Python module provides a versatile toolset that integrates a calculator, a translation service, and an AI interaction framework. It is designed to process user inputs and perform actions based on predefined logic, utilizing both mathematical and language translation capabilities.

## Features

- **Calculator**: Utilizes the SymPy library to evaluate mathematical expressions. It can handle complex calculations and return results or error messages if the input is invalid.

- **Translator**: Leverages the `googletrans` library to translate text between languages. It requires the text to be translated and the destination language code as inputs.

- **AI Interaction**: Connects to the OpenAI API to process user prompts and generate responses. It uses a chat history to maintain context and determine actions based on the AI's output.

## Usage

1. **Calculator**: Input a mathematical expression as a string to the `calculator` function to receive the evaluated result.

2. **Translator**: Provide the text and destination language code to the `translator` function to get the translated text.

3. **AI Interaction**: The module uses a loop to interact with the AI model, processing user prompts and executing actions like calculations or translations based on the AI's suggestions.

## Dependencies

- `sympy`: For symbolic mathematics.
- `googletrans`: For language translation.
- `openai`: For AI model interaction.

## Example

```python
# Calculate the factorial of 5
result = calculator("1*2*3*4*5")
print(result)

# Translate "Hello" to Spanish
translated_text = translator("Hello", "es")
print(translated_text)
