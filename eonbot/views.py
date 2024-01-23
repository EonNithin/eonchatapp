import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from httpx import request
import eonchatapp
from eonchatapp import settings
from django.templatetags.static import static
import re
import openai
from openai import OpenAI
import time
import markdown
from django.conf import settings
import base64

# Retrieve the OpenAI API key from the environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Check if the API key is available
if not openai_api_key:
   raise ValueError("OpenAI API key is not set. Please set it in your environment variables.")

# Initialize the OpenAI client with the API key
# API key set inside basch file
client = OpenAI()

# Define the assistant IDs and file IDs
assistant_id = "asst_ZB8ScuNwWCsMybVQ7Ao6zjhg"
lab_activity_assistant_id = "asst_UyQkSAAsiq08WT38AqW5EMze"
general_assistant_id = "asst_ww4lJCBRUSVB4ziCRhuYopGF"

# Use None instead of an empty string
thread_id_asst_jhg = None  
thread_id_asst_Mze = None
thread_id_asst_pGF = None

lab_activity_keywords = ['lab', 'activity', 'reference', 'video', 'reference link', 'activities', 'experiment', 'laboratory', 'practical']

# Function to encode image data to Base64
def encode_image_data_to_base64(image_data_bytes):
    encoded_image = base64.b64encode(image_data_bytes).decode("utf-8")
    return f"data:image/png;base64,{encoded_image}"


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


def clear_old_files():
    pdf_files_directory = os.path.join(settings.MEDIA_ROOT, "pdf files")
    image_files_directory = os.path.join(settings.MEDIA_ROOT, "images")

    for filename in os.listdir(pdf_files_directory):
        if filename.startswith("file-"):
            file_path = os.path.join(pdf_files_directory, filename)
            os.remove(file_path)

    for filename in os.listdir(image_files_directory):
        if filename.startswith("file-"):
            file_path = os.path.join(image_files_directory, filename)
            os.remove(file_path)


def handle_thread(thread_id, assistant_id, question):
    thread_id = thread_id
    assistant_id = assistant_id
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question
    )

    if any(keyword in question.lower() for keyword in lab_activity_keywords):
        instructions = """
        Objective: Provide users with immediate access to reference links for lab activities, alongside a general explanation and steps to perform each activity, solely based on the provided "Lab Activity.html" file.

        Streamlined User Query Response Protocol:

        Reference Link Provision:

        For every lab activity inquiry, promptly provide the YouTube reference link from the "Lab Activity.html" file without any additional prompts or information from the user.
        Lab Activity Guidance:

        Include a general explanation of the lab activity, focusing on standard procedures that are commonly associated with the type of activity mentioned (e.g., "Density of metal" might involve measuring mass and volume, calculating density).
        Autonomous Resource Reference:

        The assistant should autonomously refer to the uploaded "Lab Activity.html" file when providing reference links and should not request further information from the user for this purpose.
        Engage with Follow-Up:

        After supplying the reference link and a general explanation, encourage the user to explore the video for specific details and invite further queries related to lab activities or other topics.
        Maintain User Privacy:

        Continue to ensure the user's privacy and security by not requesting or disclosing personal information.
        """
    else:    
        instructions = """
        Instructions for Eon AI Assistant - Edutech Platform Support
        Objective: Your primary role is to assist users, mainly students and teachers, by providing specific, accurate information from our educational resources. Your responses should be concise and directly relevant to the users' queries.

        Resources at Your Disposal:

        Gr 10 Month wise syllabus 2022- '23.pdf: Details the month-wise syllabus for all subjects for Grade 10. Refer to this for syllabus-related queries.

        Grade 10 Science Worksheet.docx: This document includes a collection of questions covering various topics in Grade 10 Science. These can be used for creating quizzes and assignments, aiding teachers in assessing student understanding and providing practice for students.

        Grade 10 Mathematics Worksheet.docx: Contains a diverse set of questions for Grade 10 Mathematics topics. This resource is ideal for generating quizzes and assignments, helping teachers to evaluate student progress and offer students valuable practice opportunities.

        Grade 10 Social Science Worksheet.docx: Offers a range of questions on different topics in Grade 10 Social Science. These questions are useful for constructing quizzes and assignments, serving as a tool for teachers to gauge learning and for students to reinforce their knowledge.

        10 MATHS TEXTBOOK.pdf: The textbook for Grade 10 Mathematics. Use for specific content-related queries in Mathematics.

        10 Science Textbook.pdf: The Science textbook for Grade 10. Refer to this for content-specific queries in Science.

        10 Social Science Textbook.pdf: The Social Science textbook for Grade 10. Use this for content-specific queries in Social Science.

        Interacting with Users:

        Prompting for Clarification: If a user's question is vague or lacks specific details, politely ask for clarification to provide the most accurate and helpful response.

        Directing to Resources: When applicable, guide users to the specific section or page number of the relevant resource.

        Updating on Availability: If the information requested is not available in the provided resources, inform the user accordingly and, if possible, suggest alternative ways to find the information.

        Maintaining Engagement: Keep your responses engaging and encouraging, especially when interacting with younger students, to foster a positive learning environment.

        Note: Always prioritize user privacy and safety in your interactions. Do not solicit or disclose personal information.
        """
    
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=instructions
    )

    start_time = time.time()
    while run.status not in ["completed", "failed"]:
        time.sleep(10)
        elapsed_time = time.time() - start_time
        print(f"Current run status: {run.status}, Elapsed time: {elapsed_time} seconds")
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

    if run.status == "completed":
        # Process and return messages
        # Update the global thread_id with the current thread ID

        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            order="asc"
        )
        print("\n",messages,"\n")

        return process_messages(messages)
    else:
        return f"Assistant run failed with status: {run.status}. Please try after sometime."


def process_messages(messages):
    response = ""
    keywords_image = ["image","diagram","picture"]
    file_ids = []
    for msg in messages:
        
        if msg.content[0].type == "text":
            print("hi, Iam inside if msg.content[0].type == text")
            if msg.role == "user":
                msg.role = "YOU"
                response += "<hr>" + "\n"
            elif msg.role == "assistant":
                msg.role = "EON"

            if msg.role == "YOU":
                response += f'<div class="question-div" style="color: Red;"><strong>{msg.role}: {msg.content[0].text.value}</strong> </div>\n\n'
                curr_question = msg.content[0].text.value
            elif msg.role == "EON":
                response += f'{msg.role}: {msg.content[0].text.value} \n'
            
            # Code to extract all file ids
            
            file_ids = msg.file_ids
            try:
                if file_ids and "pdf" in curr_question.lower():
                    print("Iam inside if type == text and trying to retrieve file ids :\n")
                    print("file_ids are :\n",file_ids)
                    pdf_filenames = get_file_content(file_ids)
                    
                    for pdf_filename in pdf_filenames:
                        # Construct the pdf URL using MEDIA_URL and the pdf filename
                        pdf_file_url = f"{settings.MEDIA_URL}/pdf files/{pdf_filename}"
                        print("final pdf path url is :\n",pdf_file_url)
                        response += f'<div>{msg.role}:\n<a href="{pdf_file_url}" download > Click Here To Download PDF File:{pdf_filename} </a></div>\n'
            except Exception as e:
                    print(f"An error occurred: {e}")

        # Check msg.content type and check if any of the words in the question are in keywords_image
        elif msg.content[0].type == "image_file" and any(keyword in curr_question.lower() for keyword in keywords_image):
            # Handle images
            print("hi, Iam inside elif msg.content[0].type == image_file")
            if msg.role == "user":
                msg.role = "YOU"
                response += "<hr>" + "\n"
            elif msg.role == "assistant":
                msg.role = "EON"

            try: 
                image_file_id = msg.content[0].image_file.file_id

                # Fetching the image data
                image_data = client.files.content(image_file_id)
                image_data_bytes = image_data.read()

                # Encoding the image data to Base64
                base64_encoded_image = encode_image_data_to_base64(image_data_bytes)

                # Constructing the HTML content with the Base64 encoded image
                response += f'<div style=""><img src="{base64_encoded_image}" alt="Image file" style="max-width:40%; max-height:40%;"></div>'
                response += f'<div class="imageTextResponse-div" style="color:#797D7F;">{msg.role}: {msg.content[1].text.value} </div>\n'
            except Exception as e:
                print(f"An error occurred: {e}")

    return response


def get_assistant_response(question, request):
    global assistant_id, lab_activity_assistant_id

    # Retrieve thread IDs from the session
    thread_id_asst_jhg = request.session.get('thread_id_asst_jhg')
    thread_id_asst_Mze = request.session.get('thread_id_asst_jhg') 

    print("\nthread_id_asst_jhg:",thread_id_asst_jhg,"\n")
    print("\nthread_id_asst_Mze:", thread_id_asst_Mze,"\n")

    if any(keyword in question.lower() for keyword in lab_activity_keywords):
        assistant_id_to_use = lab_activity_assistant_id
        thread_id = thread_id_asst_Mze
    else:
        assistant_id_to_use = assistant_id
        thread_id = thread_id_asst_jhg

    if thread_id is None:
        clear_old_files()
        thread = client.beta.threads.create()
        thread_id = thread.id

        # Save the new thread ID in session
        if any(keyword in question.lower() for keyword in lab_activity_keywords):
            request.session['thread_id_asst_Mze'] = thread_id
        else:
            request.session['thread_id_asst_jhg'] = thread_id

    return handle_thread(thread_id, assistant_id_to_use, question)


def get_general_assistant_response(question, request):
    global general_assistant_id

    # Retrieve thread IDs from the session
    thread_id_asst_pGF = request.session.get('thread_id_asst_pGF')
    
    print("thread_id_asst_pGF:",thread_id_asst_pGF,"\n")

    if(question):
        assistant_id_to_use = general_assistant_id
        thread_id = thread_id_asst_pGF
    else:
        return "No question was provided. Please ask a question."
    
    if thread_id is None:
        clear_old_files()
        thread = client.beta.threads.create()
        thread_id = thread.id

    # Save the new thread ID in session
    request.session['thread_id_asst_pGF'] = thread_id

    thread_id = thread_id
    assistant_id = assistant_id_to_use
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question
    )

    instructions = """
    You are a helpful assistant, Answer to user questions as concisely and relevantly as possible.
    Note: Always prioritize user privacy and safety in your interactions. Do not solicit or disclose personal information.
    """
    
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=instructions
    )

    start_time = time.time()
    while run.status not in ["completed", "failed"]:
        time.sleep(10)
        elapsed_time = time.time() - start_time
        print(f"Current run status: {run.status}, Elapsed time: {elapsed_time} seconds")
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

    if run.status == "completed":
        # Process and return messages
        # Update the global thread_id with the current thread ID

        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            order="asc"
        )
        print("\n",messages,"\n")

        return process_messages(messages)
    else:
        return f"Assistant run failed with status: {run.status}. Please try after sometime."


def response_view(request):
    
    response = request.session.get('response', '')  # Retrieve the response from the session
    toggle_switch_value = request.session.get('toggle_switch')

    print("\nToggle Switch State captured in response view page:", toggle_switch_value, "\n")

    # Convert Markdown to HTML
    html_response = markdown.markdown(response)

    # Updated YouTube link pattern to exclude trailing characters like ')'
    youtube_link_pattern = r'[.,()]*<a href="https://www.youtube.com/embed/([^"]+?)">([^<]+)</a>[.,()]*|https://www.youtube.com/embed/([^"\s]+?)\b'

    embed_code = '\n<div style="margin-top: 20px; margin-bottom: 20px;"><iframe width="720" height="420" src="https://www.youtube.com/embed/{}" frameborder="0" allowfullscreen></iframe></div>\n'

    def replace_youtube_links(match):   
        # Check if the first or second capturing group is not None
        if match.group(1) is not None:
            video_id = match.group(1)
        else:
            video_id = match.group(3)

        return embed_code.format(video_id)

    # Check if the YouTube link pattern is found in the HTML response
    if re.search(youtube_link_pattern, html_response):
        html_response = re.sub(youtube_link_pattern, replace_youtube_links, html_response)
    
    # Regular expression pattern to find sandbox links
    sandbox_link_pattern = r'\(sandbox:/mnt/data/[^)]+\)' or r'download.+?\[.*?\]\(sandbox:/mnt/data/[^)]+\)'
    if re.search(sandbox_link_pattern, html_response):
        html_response = re.sub(sandbox_link_pattern," ", html_response)

    # Mark the HTML content as safe
    safe_html_response = mark_safe(html_response)
    print(safe_html_response)

    # Pass the safe HTML content to the template
    return render(request, "response_view.html", {"response": safe_html_response , "toggle_switch_value": toggle_switch_value})


def home(request):
    if request.method == 'GET':
        # Clearing all session data to simulate a restart
        request.session.flush()
        global thread_id_asst_jhg, thread_id_asst_Mze

        # Reset thread IDs when loading the home page
        if request.path == "/":  # '/' is your home page URL
            thread_id_asst_jhg = None
            thread_id_asst_Mze = None

    # Check for form submission
    elif request.method == "POST":
        
        flag_file_path = os.path.join(settings.BASE_DIR, 'server_restart_flag.txt')

        # Check if the server restarted
        server_restarted = False
        if os.path.exists(flag_file_path):
            with open(flag_file_path, 'r') as f:
                server_restarted = f.read().strip() == '1'

        if server_restarted:
            # Clear session and reset threads
            request.session.flush()
            #global thread_id_asst_jhg, thread_id_asst_Mze
            thread_id_asst_jhg = None
            thread_id_asst_Mze = None

            # Reset the flag
            with open(flag_file_path, 'w') as f:
                f.write('0')
        
        # Retrieve question submitted from form
        question = request.POST.get('question')

        # Get the value of the toggle switch
        toggle_switch = request.POST.get('toggle_switch_checked')
        print("\nToggle_Switch value captured from home page:", toggle_switch,"\n")
        
        # check form data being submitted.
        print("\nForm data:", request.POST, "\n")

        if toggle_switch == 'on':
            response = get_assistant_response(question, request)
        else :
            response = get_general_assistant_response(question, request)

        #Store the response in the session
        request.session['toggle_switch'] = toggle_switch
        request.session['response'] = response

        return redirect('response_view')

    return render(request, "home.html", {})

