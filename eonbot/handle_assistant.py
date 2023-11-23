#!pip install openai==0.28.0
#!pip install --upgrade openai
#!pip show openai

# Create OpenAI obj named client

from openai import OpenAI

client = OpenAI()

# uplaod files

file = client.files.create(
  file=open("/content/X MATHS NCERT TEXTBOOK 2023-24 EDITION.pdf", "rb"),
  purpose='assistants'
)
print(file.id)

# list out existing files

files_list = client.files.list()
print(files_list)
for file in files_list:
    print(file.id, "="*3, file.filename)

# Create a new Assistant

assistant = client.beta.assistants.create(
    instructions="""
    You are an educational assistant for an Edutech platform.
    You can assist teachers, students, and management with various educational queries.
    """,
    name="Maths Tutor",
    tools=[{"type": "code_interpreter"},{"type": "retrieval"}],
    model="gpt-3.5-turbo-1106",
    file_ids=[file.id]
)

print(assistant.id, "="*3, file.id)

# Retrieve available Assistant
assistant_id = "asst_ZB8ScuNwWCsMybVQ7Ao6zjhg"
file_id = "file-zPCEr1BM0Y3Oy6sTyLHAmu0s"  # file that assistant is having

assistant = client.beta.assistants.retrieve("asst_ZB8ScuNwWCsMybVQ7Ao6zjhg")
# print(assistant)
print(assistant.id, "="*3, assistant.file_ids)

# Update existing assistant

# This is the assistant I am using in VS Code
assistant_id="asst_ZB8ScuNwWCsMybVQ7Ao6zjhg"
assistant = client.beta.assistants.update(
  assistant_id=assistant_id,
  instructions="""You are an educational assistant for an Edutech platform.
    You can assist teachers, students, and management with various educational queries based on user questions.""",
  name="Maths teacher",
  tools=[{"type": "code_interpreter"},{"type": "retrieval"}],
  model="gpt-3.5-turbo-1106",
  file_ids=["file-zPCEr1BM0Y3Oy6sTyLHAmu0s"],
)

# list out Assistants created

my_assistants_list = client.beta.assistants.list(
    order = "desc",
    limit = "20"
)

for assistant in my_assistants_list:
    print(assistant.id, "\\"*3, assistant.name,"\\"*3, assistant.model)

# Delete an Assistant

response = client.beta.assistants.delete("give ur assistant id here")
print(response)

# Create Empty Thread

thread = client.beta.threads.create(
    # file_ids=[file.id] === this file ids we can use if user is uploading some files from frontend for that session or thread
)
print(thread)

# Add a user message to the thread. Here we give user question.

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="Explain abour linear equations and quadratic equations.", # user question
)
print(message)

# Retrieve message and .....

# Retrieve the message object
message = client.beta.threads.messages.retrieve(
  thread_id=thread.id,
  message_id=message.id
)

# Extract the message content
message_content = message.content[0].text
annotations = message_content.annotations
citations = []

# Iterate over the annotations and add footnotes
for index, annotation in enumerate(annotations):
    # Replace the text with a footnote
    message_content.value = message_content.value.replace(annotation.text, f' [{index}]')

    # Gather citations based on annotation attributes
    if (file_citation := getattr(annotation, 'file_citation', None)):
        cited_file = client.files.retrieve(file_citation.file_id)
        citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
    elif (file_path := getattr(annotation, 'file_path', None)):
        cited_file = client.files.retrieve(file_path.file_id)
        citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
        # Note: File download functionality not implemented above for brevity

# Add footnotes to the end of the message before displaying to user
message_content.value += '\n' + '\n'.join(citations)

print(message_content)

# Run the Assistant to get response

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id="asst_aSKkiJT9ZeyobxvTMTbqx6VH", #assistant.id
  instructions="Please address User as User."
)
print(run.id)

# Retrieve Run Status

run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)
print(run.id,run.status)

# (Optional) List out run steps

run_steps = client.beta.threads.runs.steps.list(
    thread_id=thread.id,
    run_id=run.id
)
for run in run_steps:
  print(run.id, run.status, run.assistant_id)

# once run status is completed retrieve messages bcoz messages stores whole communication

messages = client.beta.threads.messages.list(
    thread_id=thread.id,
    order="asc"
)
for msg in messages:
  print(msg.role, ":", msg.content[0].text.value)
  print("="*80)

# Delete thread to clear all messages. Then we need to go back to creating thread, adding message, run thread, check status and retrieve messages.

from openai.resources.beta.threads.messages.messages import Messages

# Get the list of messages
messages = client.beta.threads.messages.list(thread.id)

# Delete each message in the thread
for message in messages:
    client.beta.threads.delete(thread_id=thread.id)

print(f"All messages in thread {thread_id} have been deleted.")


#retrieve and Delete assistants

my_assistants_list = client.beta.assistants.list(
    order = "desc",
    limit = "20"
)

for assistant in my_assistants_list:
    print(assistant.id, "\\"*3, assistant.name,"\\"*3, assistant.model)
for assistant in my_assistants_list:
  if(assistant.name == "Math Teacher"):
    response = client.beta.assistants.delete(assistant.id)
    print(response)


import time

assistant_id = "asst_ZB8ScuNwWCsMybVQ7Ao6zjhg"
file_id = "file-zPCEr1BM0Y3Oy6sTyLHAmu0s"

# User question
question = input("enter your question: \n")

# Retirieving existing assistant
assistant = client.beta.assistants.retrieve("asst_ZB8ScuNwWCsMybVQ7Ao6zjhg")

# Creating empty thread
thread = client.beta.threads.create(
    # file_ids=[file.id] === this file ids we can use if user is uploading some files from frontend for that session or thread
)
#thread_id=thread.id

# Add a message to thread
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content=question, # user question
)

# Run thread
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant_id, #assistant.id
  instructions="Please address User as Learner."
)

# Poll the run status until it's completed
while run.status != "completed":
    time.sleep(5)  # Adjust the sleep duration as needed
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    #run_status=run.status
    print(f"Current run status: {run.status}")

# Check if run status is completed and retrieve messages
if run.status == "completed":
    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
        order="asc"
    )

    for msg in messages:
        print(msg.role, ":", msg.content[0].text.value)

