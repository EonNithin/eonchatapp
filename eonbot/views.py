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

'''
def get_video_url(selected_topic):
    # Implement a function to get the video URL based on the selected topic
    video_urls = {
        'Boiling Point of Water - Class 9 Chemistry': 'https://drive.google.com/uc?id=1Lhjkiw-IyAjCYeX_5Eg-HNEZlJepI-tG',
        'Law of Conservation of Mass - Class 9 Chemistry': 'https://drive.google.com/uc?id=1kw8B88Tmsx4YC2t3RXEJzT34N1A9L3mg',
        'Melting Point of Ice - Class 9 Chemistry': 'https://drive.google.com/uc?id=1MJKeZmJu3iGDyuKRPho-3Teq7QZjyhgC',
        'Mixtures_and_Compounds- Class 9 Chemistry': 'https://drive.google.com/uc?id=1njCIyq4Z561ezBMeSuMJ4YnMDuwrGQWU',
        'Separation_of_Components_of_a_Mixture- Class 9 Chemistry': 'https://drive.google.com/uc?id=1GXaLd1I88Fzui9XTC-Kyr3AinEVDJXTh',
        'True_solutions_suspensions_colloids- Class 9 Chemistry': 'https://drive.google.com/uc?id=1YGrJVgapEpNqClszOewsrpeOT8VTS3WJ',
        'Types_of_chemical_reactions- Class 9 Chemistry': 'https://drive.google.com/uc?id=1CBDG_RTZknyfnBoBRdsiyG0X_4GXyyVs',
        'Archemedis_principle- Class 9 Physics' : 'https://drive.google.com/uc?id=1YvKqjE-CGraFqC6u_vAXgyrU7aiqQD5k',
        'Density_of_metal- Class 9 Physics' : 'https://drive.google.com/uc?id=1C3i-nQ3nI-B-mZoOr-DxkRyw--1Z08S-',
        'Characteristics_of_convex_lens- Class 10 Physics' : 'https://drive.google.com/uc?id=1uRagsxZXAX1mM9mLw7kzYu-IHv5Ek3bY',
        'Focal_length_of_a_concave_mirror- Class 10 Physics' : 'https://drive.google.com/uc?id=1eRVD6r8DOBsv-CGSoyNcpv0YyQLhjbDb',
        'Focal_length_of_a_convex_lens- Class 10 Physics' : 'https://drive.google.com/uc?id=1H-c_UzErgba9vw3qRq2yjkEXZmPga3xr',
        'Ohms_law- Class 10 Physics' : 'https://drive.google.com/uc?id=1L0joHxMoakX8lFt_qJeOjRWcmvSElTIC',
        'Refraction_through_a_glass_prism- Class 10 Physics' : 'https://drive.google.com/uc?id=1Ut-xtBPtUvbAviGnkVSE0_ihYy1ZE1kW',
        'Refraction_through_a_glass_slab- Class 10 Physics' : 'https://drive.google.com/uc?id=1f84OioUQBUHPHaSYqWBiqe0N2Uzpt9wz',
        'Resistors_series_parallel- Class 10 Physics' : 'https://drive.google.com/uc?id=1kYjHyiCHK21sw9RPMil4xOhEgdq4zXJA',
        # Add more mappings as needed
    }
    return video_urls.get(selected_topic, '')

def generate_drive_videos_embed_code(selected_topic,video_url):
    # Generating HTML code for embedding Google Drive videos in an iframe
    video_name = selected_topic
    video_url = video_url
    embed_code = "<html><body>"
    embed_code += f"<h3>Lab Activity on {video_name}</h3>"
    embed_code += f"<video width='700' height='480' controls>\n"
    embed_code += f"  <source src='{video_url}' type='video/mp4'>\n"
    embed_code += f"  Your browser does not support the video tag.\n"
    embed_code += f"</video><br>"
    embed_code += "</body></html>"
    return embed_code
'''

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

def get_file_content(file_ids):
    pdf_filenames = []
    for file_id in file_ids:
        # Generate a unique filename for the image
        pdf_filename = f"{file_id}.pdf"
        pdf_filenames.append(pdf_filename)

        pdf_data = client.files.content(file_id)
        pdf_data_bytes = pdf_data.read()

        pdf_files_directory = os.path.join(eonchatapp.settings.MEDIA_ROOT,"pdf files")
        print("PDF files diretory:",pdf_files_directory)

        # Create the 'pdf files' subdirectory if it doesn't exist
        os.makedirs(pdf_files_directory, exist_ok=True)

        # Build the full path to the file within the 'images' subdirectory
        pdf_file_path = os.path.join(pdf_files_directory, pdf_filename)
        print("PDF file path:",pdf_file_path)

        with open(pdf_file_path, "wb") as file:
            file.write(pdf_data_bytes)

    print("PDF file names are:",pdf_filenames)
    return pdf_filenames

def get_youtube_video(question):
    # Get YouTube videos based on the question
    youtube_api_key = 'AIzaSyBWWs5-b4ybIfCzm46eXfp0nkDtHqulspk'  # Replace with your actual YouTube API key
    youtube_question = " ".join(re.findall(r'\b\w+\b', question))  # Remove special characters
    max_results = 1
    youtube = build("youtube", "v3", developerKey=youtube_api_key)

    # Search for videos
    search_response = youtube.search().list(
        q=youtube_question,
        part="id,snippet",
        maxResults=max_results,
        relevanceLanguage="en"  # Set the language to English
    ).execute()

    # Extract video links
    video_links = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            video_id = search_result["id"]["videoId"]
            #video_title = search_result["snippet"]["title"]
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            video_links.append(video_link)

    return video_links
    
def display_video_links(video_links):
    for i, video_link in enumerate(video_links, start=1):
        print(f"{i}. {video_link}")
        embed_code = generate_embed_code(video_links)
    return embed_code

def generate_embed_code(video_links):
# Generating HTML code for embedding videos in an iframe
    embed_code = "<html><body>\n<h3>Reference Video :</h3>\n"

    for i, video_link in enumerate(video_links, start=1):
        # Extract video ID from the link
        video_id = video_link.split("v=")[1]
        # Create the YouTube embed link
        embed_link = f"https://www.youtube.com/embed/{video_id}"
        # Add video title before the iframe
        #embed_code += f"<h3>{i}. {video_link.title}</h3>\n"
        embed_code += f"<iframe width='640' height='360' src='{embed_link}' frameborder='0' allowfullscreen></iframe>\n"
    embed_code += "</body></html>"
    print("I am inside generate_embed_code:",embed_code)

    return embed_code

def get_assistant_response(question):
    global thread_id, assistant_id, assistant_file_ids
    
    # Retrieving existing thread or creating a new one
    if thread_id is None:
        # Delete files with names starting with "file-" in the specified paths
        pdf_files_directory = os.path.join(eonchatapp.settings.MEDIA_ROOT, "pdf files")
        image_files_directory = os.path.join(eonchatapp.settings.MEDIA_ROOT, "images")

        for filename in os.listdir(pdf_files_directory):
            if filename.startswith("file-"):
                file_path = os.path.join(pdf_files_directory, filename)
                os.remove(file_path)

        for filename in os.listdir(image_files_directory):
            if filename.startswith("file-"):
                file_path = os.path.join(image_files_directory, filename)
                os.remove(file_path)

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

    # Poll the run status until it's completed, failed, or few seconds have passed
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
        file_ids = []
        for msg in messages:
            
            if msg.content[0].type == "text":
                print("hi, Iam inside if msg.content[0].type == text")
                if msg.role == "user":
                    msg.role = "YOU"
                    response += "<hr>" + "\n"
                elif msg.role == "assistant":
                    msg.role = "EON"
                '''
                Here add code for text message extraction ( {msg.content[0].text.value} ).
                then extract keywords from whole text message.
                send that keywords as input for extracting top 1 youtube video.
                '''
                if msg.role == "YOU":
                    response += f"{msg.role}: {msg.content[0].text.value} \n"
                elif msg.role == "EON":
                    response += f"{msg.role}: {msg.content[0].text.value} \n"
                # Code to extract all file ids 
                file_ids = msg.file_ids
                if file_ids:
                    print("Iam inside if type == text and trying to retrieve file ids :\n")
                    print("file_ids are :\n",file_ids)
                    pdf_filenames = get_file_content(file_ids)
                    
                    for pdf_filename in pdf_filenames:
                        # Construct the image URL using MEDIA_URL and the image filename
                        pdf_file_url = f"{settings.MEDIA_URL}/pdf files/{pdf_filename}"
                        print("final pdf path url is :\n",pdf_file_url)
                        response += f'<div>{msg.role}:\n<a href="{pdf_file_url}" download > Click Here To Download PDF File:{pdf_filename} </a></div>\n'
                    
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
                response += f"{msg.role}: {msg.content[1].text.value} \n"

        return response
    else:
        response = f"Assistant run failed with status: {run.status}. Please try after sometime."
    print(response)
    return response

def response_view(request):
    #retrieve required vaues from session
    #selected_topic = request.session.get('selected_topic','')
    #selected_lab_topic = request.session.get('selected_lab_topic','')
    response = request.session.get('response', '')  # Retrieve the response from the session

    # video_embedings = request.session.get('video_embedings', [])  # Retrieve video references from the session
    # Remove square brackets and double quotes
    # video_embedings = video_embedings[0].strip('[]"')
    # print("Iam in response view, video embedings are:",video_embedings)
    print('='*100)
    print("\nResponse:\n",response,"\n")
    print('='*100)

    # Convert Markdown to HTML
    html_response = markdown.markdown(response)
    # Concatenate your additional HTML code with the response HTML and video references HTML
    #full_html_response = f"{html_response}{video_embedings}"
    # Mark the HTML content as safe
    safe_html_response = mark_safe(html_response)
    print(safe_html_response)
    # Pass the safe HTML content to the template
    return render(request, "response_view.html", {"response": safe_html_response})

def home(request):
    
    # Check for form submission
    if request.method == "POST":
        question = request.POST.get('question')

        '''
        selectedTopic = request.POST.get('selectedTopic', '')
        print("Selected Topic is:",selectedTopic)
        
        selected_lab_topic = request.POST.get('selectedLabActivity', '')
        
        # Initialize an empty string to store video embed code
        video_embedings = ""

        # Get the video URL and embed code only when a topic is selected
        if selected_lab_topic !='':
            print("selected lab topic is:\n",selected_lab_topic)
            video_url = get_video_url(selected_lab_topic)  # Implement a function to get the video URL based on the selected topic
            print("videourl:\n",video_url)
            video_embedings = generate_drive_videos_embed_code(selected_lab_topic,video_url)
            print("Iam in home page, video embedings are:",video_embedings)
        '''

        # Get the value of the toggle switch
        print("Form data:", request.POST)

        # Initialize an empty list to store uploaded file paths
        uploaded_file_paths = []
        # Get the uploaded files
        uploaded_files = request.FILES.getlist('attachment')
        print("uploaded files:\n",uploaded_files)

        toggle_switch = request.POST.get('toggle_switch_checked')
        if toggle_switch == 'on':
            response = get_assistant_response(question)
            video_references = get_youtube_video(question)
            embed_videos = display_video_links(video_references)
        else :
            response = get_assistant_response(question)

        #Store the response in the session
        request.session['question'] = question
        request.session['response'] = response
        request.session['embed_videos'] = embed_videos
        request.session['uploaded_files'] = [uploaded_file.name for uploaded_file in uploaded_files]
        '''
        request.session['selected_topic'] = selectedTopic
        request.session['selected_lab_topic'] = selected_lab_topic
        request.session['video_embedings'] = [video_embedings]
        '''
        return redirect('response_view')

    return render(request, "home.html", {})

# Run project : python3 manage.py runserver SERVER-IP:PORT
# SERVER-IP and PORT are optional parameters. 127.0.0.1:8000 will be used by default if you don’t specify any of them. 
# If you plan to remotely access the server, you should use the IP address 0.0.0.0, or the actual server IP address.