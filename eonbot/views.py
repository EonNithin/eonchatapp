import json
import os
from django.shortcuts import render
from django.http import HttpResponse
import openai
import eonchatapp
from eonchatapp import settings
from eonchatapp.settings import OPENAI_API_KEY
import pandas as pd
from django.templatetags.static import static

# CSV file data importing and processing
csv_file_path = os.path.join(eonchatapp.settings.STATIC_ROOT, 'CBSE Syllabus class9&10.csv')
# static('csv_files/CBSE-Syllabus.csv')  # Update with the actual CSV file name

df = pd.read_csv(csv_file_path)
# Extract relevant information from the CSV data
# Handle missing values
df = df.stack().reset_index(drop=True).to_frame()
relevant_info = df.dropna() # Drop rows with missing values

# Convert the extracted information to a string
syllabus_keywords = relevant_info_str = ','.join(df.values.flatten())

# Variable to store the conversation history
conversation_history = []

def is_syllabus_related_question(question):
    question_lower = question.lower()
    for keyword in syllabus_keywords:
        if keyword in question_lower:
            return True
    return False

def get_chatgpt_response(question):
    global conversation_history

    if is_syllabus_related_question(question):
        # API implementation
        # create openai instance
        openai.Model.list()
        # Set the API key -- Get OpenAI api key from environment variables path(eonchatapp-m3) done in settings.py file.
        openai.api_key = OPENAI_API_KEY
        #print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")

        # Append the current question to the conversation history
        conversation_history.append(question)

        # Construct the prompt using conversation history
        prompt = "\n".join(conversation_history)

        # send relevant info as prompt to openai completion
        prompt = 'please provide information about '+relevant_info_str

        # Make a Completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.5,
            max_tokens=500,
            top_p=0,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_content = response['choices'][0]['message'][ 'content'] if response and 'choices' in response else 'Sorry, Something went wrong cannot process your request at the moment. Please try again later.'
        response = response_content.strip() if response_content else 'Sorry, I could not answer your question. Please try again later or ask a different question.'

        # Append the current question and AI response to the conversation history
        conversation_history.append(response)
        conversation_length = len(conversation_history)
        #print(conversation_history)
        return response, conversation_length

    else:
        quest=question
        res="Please ask a question related to the class syllabus."
        conversation_history.append(quest)
        conversation_history.append(res)
        conversation_length = len(conversation_history)
        return res, conversation_length

def home(request):
    # Check for form submission
    if request.method == "POST":
        question = request.POST.get('question')
        response = get_chatgpt_response(question)

        return render(request, "home.html", {"question": question, "response": response, "conversation_history":conversation_history })

    return render(request, "home.html", {})

