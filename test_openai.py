from openai import OpenAI

from config import OPENAI_API_KEY, MODEL_NAME


client = OpenAI(api_key=OPENAI_API_KEY)

response = client.responses.create(
    model=MODEL_NAME,
    input="Reply with exactly: OpenAI API connection successful."
)

print(response.output_text)
