import os
import markdown
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import eonchatapp
from eonchatapp import settings
import pandas as pd
from django.templatetags.static import static
import re
import openai
from openai import OpenAI
import time

# Retrieve the OpenAI API key from the environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Check if the API key is available
if not openai_api_key:
    raise ValueError("OpenAI API key is not set. Please set it in your environment variables.")

# Initialize the OpenAI client with the API key
# API key set inside basch file
client = OpenAI()


def upload_file():
    file = client.files.create(
    file=open("/content/X MATHS NCERT TEXTBOOK 2023-24 EDITION.pdf", "rb"),
    purpose='assistants'
    )

    file_id=file.id
    file_name=file.filename
    print(file_id,"="*3,file_name)
    return file_id, file_name


def retrieve_uploaded_files():

    files_dict = {}
    files_list = client.files.list()
    for file in files_list:
        files_dict[file.id] = file.filename

    print("File Information Dictionary:", files_dict)



def createAssistant():
    assistant = client.beta.assistants.create(
    instructions="""
    You are an educational assistant for an Edutech platform. 
    You can assist teachers, students, and management with various educational queries.
    you can perform below tasks:
    For teachers:
    - Provide lesson plans for specific classes.
    - Suggest teaching strategies for a particular subject.
    - Help with grading and assessment methods.
    For students:
    - Offer assistance with homework or specific subjects.
    - Provide explanations for challenging concepts.
    - Recommend study resources and learning strategies.
    For management:
    - Generate reports on student performance.
    - Assist in scheduling and managing classes.
    - Provide insights into educational trends and improvements.
    Remember to provide detailed and context-specific responses. 
    If the user asks for a lesson plan, include relevant details like the subject, class, and any specific requirements. 
    If the question is about a challenging concept, explain it in a way that is easy for the user to understand.
    Feel free to ask for clarification if needed, and always prioritize providing helpful and accurate information to enhance the educational experience.
    """,
    name="chatbot test",
    tools=[{"type": "code_interpreter"},{"type": "retrieval"}],
    model="gpt-3.5-turbo-1106",
    file_ids=[file.id]
    )

    assistant_id=assistant.id
    file_id=file.id
    print(assistant.id, "="*3, file.id)
    return assistant_id, file_id


thread_id=""

def get_assistant_response(question):

    assistant_id = "asst_ZB8ScuNwWCsMybVQ7Ao6zjhg"
    file_id = "file-zPCEr1BM0Y3Oy6sTyLHAmu0s" #file that assistant is having

    # Retirieving existing assistant
    assistant = client.beta.assistants.retrieve("asst_ZB8ScuNwWCsMybVQ7Ao6zjhg")

    if thread_id == "":
        # Creating empty thread
        thread = client.beta.threads.create(
            # file_ids=[file.id] === this file ids we can use if user is uploading some files from frontend for that session or thread
        )
        curr_thread = thread
        curr_thread_id = curr_thread.id
    else:
        curr_thread = client.beta.threads.retrieve(curr_thread.id)

    # Add a message to thread
    message = client.beta.threads.messages.create(
    thread_id=curr_thread.id,
    role="user",
    content=question, # user question
    )

    # Run thread
    run = client.beta.threads.runs.create(
    thread_id=curr_thread.id,
    assistant_id=assistant_id, #assistant.id
    instructions="Please address User as Learner."
    )

    start_time = time.time()

    # Poll the run status until it's completed, failed, or 40 seconds have passed
    while run.status not in ["completed", "failed"]:
        time.sleep(10)  # Adjust the sleep duration as needed
        elapsed_time = time.time() - start_time
        print(f"Current run status: {run.status}, Elapsed time: {elapsed_time} seconds")

        if elapsed_time >= 100:
            response = "There is heavy traffic. Please try again later."
            return response

        run = client.beta.threads.runs.retrieve(thread_id=curr_thread.id, run_id=run.id)

    # Check if run status is completed and retrieve messages
    if run.status == "completed":
        messages = client.beta.threads.messages.list(
            thread_id=curr_thread.id,
            order="asc"
        )
        response = ""
        for msg in messages:
            if msg.content[0].type == "text":
                if msg.role == "user":
                    msg.role = "User"
                elif msg.role == "assistant":
                    msg.role = "Maths Teacher"
                response += f"{msg.role}: {msg.content[0].text.value}\n"
            elif msg.content[0].type == "image":
                response += f"{msg.role}: [Image]\n"
            # Add more conditions for other content types as needed

        print("Response :",response)
        return response
    else:
        response = f"Assistant run failed with status: {run.status}. Please try after sometime."

    return response


def response_view(request):
    response = request.session.get('response', '')  # Retrieve the response from the session
    print('='*100)
    print("\nResponse:\n",response,"\n")
    print('='*100)

    return render(request, "response_view.html", {"response": response})


def home(request):
    # Check for form submission
    if request.method == "POST":
        question = request.POST.get('question')

        # Get the value of the toggle switch
        print("Form data:", request.POST)

        toggle_switch = request.POST.get('toggle_switch_checked')
        if toggle_switch == 'on':
            response = get_assistant_response(question)
        else :
            response = get_assistant_response(question)

        #Store the response in the session
        request.session['response'] = response

        return redirect('response_view')

    return render(request, "home.html", {})

