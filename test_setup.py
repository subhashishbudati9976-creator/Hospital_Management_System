from config import OPENAI_API_KEY, MODEL_NAME
from src.agent import agent


print("API key configured:", bool(OPENAI_API_KEY))
print("Model:", MODEL_NAME)
print("Agent created:", agent is not None)
print("Setup test passed.")
