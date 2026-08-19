from openai import OpenAI
from app.core.config import API_KEY,BASE_URL,MODEL
from app.core.logger import logger
from app.core.exception import BusinessException

client=OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

def chat_with_ai(messages):

    

    
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
        
    
    

    return response.choices[0].message.content

def chat_stream_ai(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True
    )

    for chunk in response:
        content=chunk.choices[0].delta.content
        if content:
            yield content