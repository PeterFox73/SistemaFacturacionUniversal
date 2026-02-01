'''
This script shows how to connect to the Google Gemini API and list the available models.

Instructions:
1. Make sure you have the google-generativeai library installed:
   pip install google-generativeai

2. Get your API key from Google AI Studio: https://aistudio.google.com/app/apikey

3. Replace "YOUR_API_KEY" in this script with your actual key.
'''
import google.generativeai as genai
import os

# --- IMPORTANT ---
# Replace "YOUR_API_KEY" with your actual Gemini API key.
# For better security, consider using environment variables or a secrets management tool.
api_key = "AIzaSyC60alduYilL0CE4yVxjKz5EJSIZBAanB8"

genai.configure(api_key=api_key)

print("Successfully connected to the Gemini API.")
print("Available models:")

for model in genai.list_models():
  # This example lists models that support the "generateContent" method.
  if 'generateContent' in model.supported_generation_methods:
    print(f"- {model.name}")
