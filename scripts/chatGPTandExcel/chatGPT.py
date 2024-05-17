import openai
import tiktoken
import sys
# import const
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def encode_question(question: str):
    # encoding = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.get_encoding("p50k_base")
    encoded_question = encoding.encode(question)
    # decoded_question = encoding.decode(encoded_question)
    # num_tokens_of_question = len(encoded_question)
    return encoded_question

def ask_gpt3(question):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        max_tokens=100
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    # openAImodels = openai.Model.list()

    question = sys.argv[1]
    encoded_question = encode_question(question)

    answer = ask_gpt3(encoded_question)
    print(answer)


