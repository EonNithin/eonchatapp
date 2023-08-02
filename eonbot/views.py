# import json
import os
from django.shortcuts import render
# from django.http import HttpResponse
import openai
import eonchatapp
from eonchatapp import settings
from eonchatapp.settings import OPENAI_API_KEY
import pandas as pd
# from django.templatetags.static import static

# CSV file data importing and processing
csv_file_path = os.path.join(eonchatapp.settings.STATIC_ROOT, 'CBSE Syllabus class9&10.csv')
# static('csv_files/CBSE-Syllabus.csv')  # Update with the actual CSV file name

df = pd.read_csv(csv_file_path)
# Extract relevant information from the CSV data
# Handle missing values
df = df.stack().reset_index(drop=True).to_frame()
relevant_info = df.dropna()  # Drop rows with missing values

# Convert the extracted information to a string
relevant_info_str = ','.join(df.values.flatten())

syllabus_keywords = ["Hi", "what", "hello", "ok", "class"]

# Variable to store the conversation history
conversation_history = []


def is_syllabus_related_question(question):
    question_lower = question.lower()
    for keyword in syllabus_keywords:
        if keyword.lower() in question_lower:
            return True
    return False


def get_custom_chatgpt_response(question):
    global conversation_history

    if is_syllabus_related_question(question):
        # API implementation
        # create openai instance
        openai.Model.list()
        # Set the API key -- Get OpenAI api key from environment variables path(eonchatapp-m3) done in settings.py file.
        openai.api_key = OPENAI_API_KEY
        # print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")

        # Append the current question to the conversation history
        conversation_history.append(question)

        # Construct the prompt using conversation history
        prompt = "\n".join(conversation_history)

        # send relevant info as prompt to openai completion
        prompt = 'please provide information about ' + relevant_info_str

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
        response_content = response['choices'][0]['message']['content'] if response and 'choices' in response else 'Sorry, Something went wrong cannot process your request at the moment. Please try again later.'
        response = response_content.strip() if response_content else 'Sorry, I could not answer your question. Please try again later or ask a different question.'

        # Append the current question and AI response to the conversation history
        conversation_history.append(response)
        conversation_length = len(conversation_history)
        # print(conversation_history)
        return response, conversation_length

    else:
        quest = question
        res = "Please ask a question related to the class syllabus."
        conversation_history.append(quest)
        conversation_history.append(res)
        conversation_length = len(conversation_history)
        return res, conversation_length


def get_chatgpt_response(question, use_csv_response=True):
    global conversation_history

    # API implementation for OpenAI GPT-3.5 Turbo response
    # create openai instance
    openai.Model.list()
    # Set the API key -- Get OpenAI api key from environment variables path (eonchatapp-m3) done in settings.py file.
    openai.api_key = OPENAI_API_KEY

    # Append the current question to the conversation history
    conversation_history.append(question)

    # Construct the prompt using conversation history
    prompt = "\n".join(conversation_history)

    # Make a Completion using the OpenAI ChatGPT API
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

    response_content = response['choices'][0]['message']['content'] if response and 'choices' in response else 'Sorry, Something went wrong. Cannot process your request at the moment. Please try again later.'
    response = response_content.strip() if response_content else 'Sorry, I could not answer your question. Please try again later or ask a different question.'

    # Append the current question and AI response to the conversation history
    conversation_history.append(response)
    conversation_length = len(conversation_history)

    return response, conversation_length


"""def home(request):
    global conversation_history
    
    # Check for form submission
    if request.method == "POST":
        question = request.POST.get('question')

        # Get the value of the form_switch checkbox from the form data
        toggle_switch_on = request.POST.get('form_switch') == 'on'
        toggle_switch_off = request.POST.get('form_switch') == 'off'
        # Pass the user's choice to the get_chatgpt_response function
        if toggle_switch_on:
            response, conversation_length = get_custom_chatgpt_response(question)
        elif toggle_switch_off:
            response, conversation_length = get_chatgpt_response(question, use_csv_response=True)
        else:
            response, conversation_length = get_chatgpt_response(question, use_csv_response=False)

        return render(request, "home.html",
                      {"question": question, "response": response, "conversation_history": conversation_history})

    return render(request, "home.html", {})"""


# ... (your imports and other functions)

def home(request):
    global conversation_history

    # Check for form submission
    if request.method == "POST":
        question = request.POST.get('question')

        # Get the value of the form_switch checkbox from the form data
        toggle_switch_on = request.POST.get('form_switch') == 'on'
        toggle_switch_off = request.POST.get('form_switch') == 'off'

        # Clear the conversation history when the toggle switch is off
        if toggle_switch_off:
            conversation_history = []

        # Decide whether to use CSV response or not based on the toggle switch state
        use_csv_response = toggle_switch_on

        # Pass the user's choice to the appropriate function
        if toggle_switch_off:
            response, conversation_length = get_chatgpt_response(question, use_csv_response=use_csv_response)
        else:
            response, conversation_length = get_custom_chatgpt_response(question)

        return render(request, "home.html", {"question": question, "response": response, "conversation_history": conversation_history})

    return render(request, "home.html", {})
