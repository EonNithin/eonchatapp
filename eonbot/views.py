import os
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
import markdown


# Retrieve the OpenAI API key from the environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Check if the API key is available
if not openai_api_key:
    raise ValueError("OpenAI API key is not set. Please set it in your environment variables.")

# Initialize the OpenAI client with the API key
# API key set inside basch file
client = OpenAI()
import time
import time

assistant_id = "asst_ZB8ScuNwWCsMybVQ7Ao6zjhg"
file_id = "file-zPCEr1BM0Y3Oy6sTyLHAmu0s"  # file that assistant is having
thread_id = None  # Use None instead of an empty string

def get_assistant_response(question):
    global thread_id, assistant_id, file_id

    # Retrieving existing thread or creating a new one
    if thread_id is None:
        print("Creating new thread")
        # Creating empty thread
        thread = client.beta.threads.create()
        curr_thread = thread
        thread_id = curr_thread.id  # Update thread_id with the new thread ID
    else:
        print("Retrieving existing thread")
        # Retrieve existing thread
        curr_thread = client.beta.threads.retrieve(thread_id)

    # Add a message to thread
    message = client.beta.threads.messages.create(
        thread_id=curr_thread.id,
        role="user",
        content=question,  # user question
    )

    # Run thread
    run = client.beta.threads.runs.create(
        thread_id=curr_thread.id,
        assistant_id=assistant_id,
        instructions="Please address User as Pal."
    )

    start_time = time.time()

    # Poll the run status until it's completed, failed, or 40 seconds have passed
    while run.status not in ["completed", "failed"]:
        time.sleep(10)
        elapsed_time = time.time() - start_time
        print(f"Current run status: {run.status}, Elapsed time: {elapsed_time} seconds")
        run = client.beta.threads.runs.retrieve(thread_id=curr_thread.id, run_id=run.id)

    # Check if run status is completed and retrieve messages
    if run.status == "completed":
        # Update the global thread_id with the current thread ID
        thread_id = curr_thread.id

        messages = client.beta.threads.messages.list(
            thread_id=curr_thread.id,
            order="asc"
        )
        print("\n",messages,"\n")
        response = ""
        for msg in messages:
            if msg.content[0].type == "text":
                if msg.role == "user":
                    msg.role = "YOU"
                    response += "<hr>" + "\n"
                elif msg.role == "assistant":
                    msg.role = "EON"

                response += f"{msg.role}: {msg.content[0].text.value} \n"

            elif msg.content[0].type == "image":
                # Handle images
                image_url = msg.content[0].image.url
                response += f"{msg.role}: <img src='{image_url}' alt='Image'>\n"
        return response
    else:
        response = f"Assistant run failed with status: {run.status}. Please try after sometime."
    print(response)
    return response


def response_view(request):
    response = request.session.get('response', '')  # Retrieve the response from the session
    print('='*100)
    print("\nResponse:\n",response,"\n")
    print('='*100)
    # Convert Markdown to HTML
    html_response = markdown.markdown(response)
    # Mark the HTML content as safe
    safe_html_response = mark_safe(html_response)
    print(safe_html_response)
    # Pass the safe HTML content to the template
    return render(request, "response_view.html", {"response": safe_html_response})


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

# Run project : python3 manage.py runserver SERVER-IP:PORT
# SERVER-IP and PORT are optional parameters. 127.0.0.1:8000 will be used by default if you don’t specify any of them. 
# If you plan to remotely access the server, you should use the IP address 0.0.0.0, or the actual server IP address.