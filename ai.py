import openai
from dotenv import load_dotenv
load_dotenv()
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
def getAiRespose(context, mt=1000, t=1, f=0):
    """
    Generate a chat response using the OpenAI ChatCompletion API.

    Args:
        context (str): The conversation context to generate a response for.
        mt (int, optional): The maximum number of tokens allowed in the response. Defaults to 1000.
        t (float, optional): The temperature parameter for response generation. Defaults to 1.
        f (float, optional): The frequency penalty parameter for response generation. Defaults to 0.

    Returns:
        str: The generated chat response.
    """
    # create a chat completion using the OpenAI ChatCompletion API
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": context}],
        max_tokens=mt,
        temperature=t,
        frequency_penalty=f
    )

    # return the content of the first choice in the chat completion response
    return chat_completion.choices[0].message.content
