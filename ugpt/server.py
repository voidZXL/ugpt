import os
import openai
from chat import start_chat
openai.organization = "org-Ulj26Q3PQn242QpDdwlHFga2"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.proxy = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}


if __name__ == '__main__':
    start_chat()
