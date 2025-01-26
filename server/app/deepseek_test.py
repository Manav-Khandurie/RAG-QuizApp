from langchain_openai.chat_models.base import BaseChatOpenAI

# Initialize the BaseChatOpenAI instance
m = BaseChatOpenAI(
    model='deepseek-chat',  # Correct model name
    openai_api_key='',  # Replace with your actual API key
    openai_api_base='https://api.deepseek.com',  # Correct API base URL
    max_tokens=1024  # Correctly assign max_tokens
)

# Invoke the model with a prompt
response = m.invoke("Hi!")

# Print the response content
print(response.content)