import openai

# Set your OpenAI API key
openai.api_key = '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'

client = OpenAI()

my_assistant = openai.Assistant.create(
    instructions="You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
    name="Math Tutor",
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo",
)
print(my_assistant)
