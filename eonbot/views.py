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
import time
from django.conf import settings

# Retrieve the OpenAI API key from the environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Check if the API key is available
if not openai_api_key:
    raise ValueError("OpenAI API key is not set. Please set it in your environment variables.")

# Initialize the OpenAI client with the API key
# API key set inside basch file
client = OpenAI()

'''
asst_ZB8ScuNwWCsMybVQ7Ao6zjhg === ['file-qdVl4pmqpcJXHpZjEGgyQ5zD', 'file-kpasq1hQ8fCDDDuQUPvkvqV4', 'file-iRsXYA4MDzxIgURI7dqYWueu', 'file-NFruvcolPoPvxASsD5wcgTlr', 'file-Z9aYtYYzB26Jzr3myoeznxa3', 'file-O4HyAHeBTbnYpmB2oSHxSx0n', 'file-SoGo3TxBFR25fX2yk6KwC9pr']

'''

assistant_id = "asst_ZB8ScuNwWCsMybVQ7Ao6zjhg"
assistant_file_ids = "['file-qdVl4pmqpcJXHpZjEGgyQ5zD', 'file-kpasq1hQ8fCDDDuQUPvkvqV4', 'file-iRsXYA4MDzxIgURI7dqYWueu', 'file-NFruvcolPoPvxASsD5wcgTlr', 'file-Z9aYtYYzB26Jzr3myoeznxa3', 'file-O4HyAHeBTbnYpmB2oSHxSx0n', 'file-SoGo3TxBFR25fX2yk6KwC9pr']"  # file that assistant is having
thread_id = None  # Use None instead of an empty string

def get_imageFileContent(image_file_id):
    image_file = openai.files.content(image_file_id)

    # Generate a unique filename for the image
    image_filename = f"{image_file_id}.png"

    # Build the path to the 'images' subdirectory
    # MEDIA_ROOT = os.path.join(BASE_DIR, 'images')
    images_directory = os.path.join(eonchatapp.settings.MEDIA_ROOT,"images")
    print("Images_diretory:",images_directory)

    # Create the 'images' subdirectory if it doesn't exist
    os.makedirs(images_directory, exist_ok=True)

    # Build the full path to the file within the 'images' subdirectory
    image_file_path = os.path.join(images_directory, image_filename)
    print("image file path:",image_file_path)

    # Write the image content to the file
    with open(image_file_path, "wb") as f:
        f.write(image_file.content)


    return image_filename


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
                print("hi, Iam inside if msg.content[0].type == text")
                if msg.role == "user":
                    msg.role = "YOU"
                    response += "<hr>" + "\n"
                elif msg.role == "assistant":
                    msg.role = "EON"

                response += f"{msg.role}: {msg.content[0].text.value} \n"
            
            elif msg.content[0].type == "image_file":
                # Handle images
                print("hi, Iam inside elif msg.content[0].type == image_file")
                if msg.role == "user":
                    msg.role = "YOU"
                    response += "<hr>" + "\n"
                elif msg.role == "assistant":
                    msg.role = "EON"

                image_file_id = msg.content[0].image_file.file_id
                image_filename = get_imageFileContent(image_file_id)
            
                # Construct the image URL using MEDIA_URL and the image filename
                image_url = f"{settings.MEDIA_URL}/images/{image_filename}"
                print("final image url is :\n",image_url)

                response += f'{msg.role}:\n<div style=""><img src="{image_url}" alt="Image file" style="max-width:40%; max-height:40%;"></div>\n'
            
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