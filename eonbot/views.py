import json
import os
import markdown
from django.shortcuts import render, redirect
from django.http import HttpResponse
import openai
from django.utils.safestring import mark_safe
import eonchatapp
from eonchatapp import settings
import pandas as pd
from django.templatetags.static import static
import html
import re
from googleapiclient.discovery import build
from openai import OpenAI

# Define the path to the file containing the API key
google_api_key_file = '/home/eon/VSCodeProjects/eonchatapp/googlesecret_key.txt'

# Read the API key from the file
with open(google_api_key_file, 'r') as f:
    google_api_key = f.read().strip()

# Set up the Custom Search Engine ID as an environment variable
search_engine_id = os.environ['SEARCH_ENGINE_ID'] = 'b608d92f156b5480e'


openai_api_key_file = "/home/eon/VSCodeProjects/eonchatapp/openaisecret_key.txt"
# Read the API key from the file
with open(openai_api_key_file, 'r') as f:
    openai_api_key = f.read().strip()

client = OpenAI(api_key=openai_api_key)

# Variable to store the conversation history
conversation_history = []


# Function to get images based on a query using Google Custom Search API
def get_images(query):
    num_results = 3
    service = build("customsearch", "v1", developerKey=google_api_key)
    res = service.cse().list(q=query, cx=search_engine_id, searchType='image', safe='medium', num=num_results).execute()
    image_links = [item['link'] for item in res['items']]
    return image_links

# Function to define the tool for image search
def define_tool():
    tool = {
        "type": "function",
        "function": {
            "name": "get_images",
            "description": "Get images based on a query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for images",
                    }
                },
                "required": ["query"],
            },
        },
    }
    return tool

# Function to run the conversation with image search functionality
def run_conversation(tool, question):
    try:
        messages = [{"role": "user", "content": question}]
        tools = [tool]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            available_functions = {
                "get_images": get_images,
            }
            messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    query=function_args.get("query"),
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(function_response),
                    }
                )

            second_response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages,
            )
            if(second_response):
                response = second_response.choices[0].message.content
                conversation_history.append(response)
                conversation_length = len(conversation_history)
            return response
    except Exception as e:
        print(f"Error: {e}")


def get_custom_chatgpt_response(question):
    global conversation_history
    if(question):
       
        # Get the previous question and response from the conversation history
        prev_question = conversation_history[-2] if len(conversation_history) >= 2 else ""
        prev_response = conversation_history[-1] if len(conversation_history) >= 1 else ""
        # print(prev_question+" : "+prev_response+"\n"+"***")

        # Append the current question to the conversation history
        conversation_history.append(question)

        # Make a Completion
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "Respond to user question as concisely as possible"},
                {"role": "assistant", "content": "answer to user questions"},
                {"role": "user", "content": question}
            ],
            temperature=0.5,
            max_tokens=1500,
            top_p=0,
            frequency_penalty=1,
            presence_penalty=0
        )
        print(response)
        # Check if response exists and has 'choices' list
        if response:
            response_content = response.choices[0].message.content
            response = response_content.strip() if response_content else 'Sorry, I could not answer your question. Please try again later or ask a different question.'
        else:
            response = 'Sorry, Something went wrong cannot process your request at the moment. Please try again later.'

        # Append the current question and AI response to the conversation history
        conversation_history.append(response)
        conversation_length = len(conversation_history)
        # print(conversation_history)
        return response, conversation_length
    else:
        quest=question
        res="Please ask a question to generate a response"
        conversation_history.append(quest)
        conversation_history.append(res)
        conversation_length = len(conversation_history)
        return res, conversation_length

def get_chatgpt_response(question):
    global conversation_history
    # API implementation
    
    # Get the previous question and response from the conversation history
    prev_question = conversation_history[-2] if len(conversation_history) >= 2 else ""
    prev_response = conversation_history[-1] if len(conversation_history) >= 1 else ""
    # print(prev_question+" : "+prev_response+"\n"+"***")
    # Construct the prompt using previous question and response
    prompt = f"{prev_question}\n{prev_response}"
    # print(prompt)
    prompt_data = "Answer as consisely and relevantly as possible"
    # Append the current question to the conversation history
    conversation_history.append(question)
    response = client.Completion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": prompt_data},
            {"role": "assistant", "content": prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.5,
        max_tokens=500,
        top_p=0,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Check if response exists and has 'choices' list
    if response and 'choices' in response and response['choices']:
        response_content = response['choices'][0]['message']['content']
        response = response_content.strip() if response_content else 'Sorry, I could not answer your question. Please try again later or ask a different question.'
    else:
        response = 'Sorry, Something went wrong cannot process your request at the moment. Please try again later.'

    # Append the current question and AI response to the conversation history
    conversation_history.append(response)
    conversation_length = len(conversation_history)
    # print(conversation_history)

    return response, conversation_length

def response_view(request):
    response = request.session.get('response', '')  # Retrieve the response from the session
    print('='*100)
    print("\nResponse:\n",response,"\n")
    print('='*100)

    def convert_to_markdown(plain_text):
    # Function to replace YouTube links with embeds
        def replace_youtube_links(match):
            video_id = match.group(2)
            return f'\n<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>\n<br><br>'

        # Regular expression to find YouTube video links
        youtube_link_pattern = r'\[([^]]+)\]\(https:\/\/www\.youtube\.com\/watch\?v=([^\)]+)\)'

        # Replace YouTube video links with embeds
        markdown_text = re.sub(youtube_link_pattern, replace_youtube_links, plain_text)

        # Convert plain text to Markdown
        markdown_text = markdown.markdown(markdown_text)

        print("\n",'='*100,"\n")
        print("Raw Markdown:\n",markdown_text)
        print("\n",'='*100,"\n")
        markdown_text=fix_markdown_format(markdown_text)
        return markdown_text
    
    def fix_markdown_format(markdown_text):
        # Remove extra spaces around links
        markdown_text = re.sub(r'\]\s+\(', '](', markdown_text)

        print("\n",'='*100,"\n")
        print("Filtered Markdown:\n",markdown_text)
        print("\n",'='*100,"\n")

        return markdown_text


    markdown_output = convert_to_markdown(response)
    html_page = f"<html><body>{markdown_output}</body></html>"
    #print(html_page)
    return render(request, "response_view.html", {"response": html_page})

def home(request):
    # Check for form submission
    if request.method == "POST":
        question = request.POST.get('question')
        # Get the value of the toggle switch
        print("Form data:", request.POST)

        toggle_switch = request.POST.get('toggle_switch_checked')
        if toggle_switch == 'on':
            response, conversation_length = get_custom_chatgpt_response(question)
            image_response = run_conversation(define_tool(), question)

        else :
            response, conversation_length = get_chatgpt_response(question)

        #Store the response in the session
        request.session['response'] = response
        print("\nResponse ","="*10,"\n",response)
        print("\nImage response ","="*10,"\n",image_response)
       
        # Combine text and image responses
        response = f"{response}\n\nImages:\n{image_response}"
        print("\nResponse ","="*10,"\n",response)

        # Convert Markdown to HTML
        html_response = markdown.markdown(response)
        html_response = f"<html><body>{html_response}</body></html>"
      
        return render(request, "home.html", {'response': html_response, 'conversation_history': conversation_history})

    return render(request, "home.html", {})

